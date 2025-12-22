"""

RAG (Retrieval Augmented Generation) 서비스

- PDF -> 텍스트 추출/클리닝/청킹/중복제거

- 임베딩 생성 + (옵션) PCA 차원 축소 + FAISS 검색

"""



import logging
import os
import re
from pathlib import Path

from typing import List, Dict, Any, Optional, Tuple



try:
    import faiss
    _FAISS_AVAILABLE = True
except Exception:
    faiss = None
    _FAISS_AVAILABLE = False
import numpy as np

try:
    from pypdf import PdfReader
except Exception:
    PdfReader = None

try:
    from chandra.input import load_file as chandra_load_file
    from chandra.model import InferenceManager
    from chandra.model.schema import BatchInputItem
    _CHANDRA_AVAILABLE = True
except Exception:
    chandra_load_file = None
    InferenceManager = None
    BatchInputItem = None
    _CHANDRA_AVAILABLE = False


from src.services.embedding_service import clean_text, chunk_text, deduplicate
from langchain_core.prompts import PromptTemplate


logger = logging.getLogger(__name__)

_chandra_manager = None
_chandra_manager_method = None


def _get_chandra_manager(method: str):
    global _chandra_manager, _chandra_manager_method
    if _chandra_manager is None or _chandra_manager_method != method:
        _chandra_manager = InferenceManager(method=method)
        _chandra_manager_method = method
    return _chandra_manager


def _extract_pdf_text_chandra(pdf_path: Path, method: str) -> List[str]:
    if not _CHANDRA_AVAILABLE:
        return []
    try:
        images = chandra_load_file(str(pdf_path), {})
        if not images:
            return []
        manager = _get_chandra_manager(method)
        batch = [BatchInputItem(image=img, prompt_type="ocr_layout") for img in images]
        results = manager.generate(
            batch,
            include_images=False,
            include_headers_footers=False,
        )
        page_texts = []
        for result in results:
            text = (result.markdown or "").strip()
            if text:
                page_texts.append(text)
        return page_texts
    except Exception as e:
        logger.warning(f"Chandra OCR failed for {pdf_path}: {e}")
        return []


def _load_text_file(filename: str, fallback: str = "") -> str:
    text_path = Path(__file__).with_name(filename)
    try:
        if text_path.exists():
            return text_path.read_text(encoding="utf-8")
    except Exception as e:
        logger.warning(f"Failed to read {filename}: {e}")
    return fallback



def _get_embedding_model():
    try:
        from src.models.model_manager import get_embedding_model

        return get_embedding_model()
    except Exception as e:
        logger.warning(f"Embedding model unavailable: {e}")
        return None


def _get_llm_model():
    try:
        from src.models.model_manager import get_llm_model

        return get_llm_model()
    except Exception as e:
        logger.warning(f"LLM model unavailable: {e}")
        return None


def _simple_hash_embeddings(texts: List[str], dim: int = 512) -> np.ndarray:
    mat = np.zeros((len(texts), dim), dtype=np.float32)
    for i, text in enumerate(texts):
        for token in re.findall(r"\\S+", text.lower()):
            idx = hash(token) % dim
            mat[i, idx] += 1.0
    return mat


def _clean_context_ko(text: str) -> str:
    if not text:
        return ""
    cleaned = re.sub(r"[^0-9A-Za-z\u3131-\u318E\uAC00-\uD7A3\s.,;:!?()\-/·%]", " ", text)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


# RAG 상태

_rag_system = {
    "index": None,
    "embeddings_norm": None,
    "metadatas": [],
    "chunks": [],
    "pca": None,
    "initialized": False,
    "dimension": None,
    "original_dimension": None,
    "use_faiss": False,
}




STATIC_TEXT = ""
_static_text_path = Path(__file__).with_name("static_manual_ko.txt")
_notice_cache_path = Path(__file__).with_name("kopo_notices_cache.txt")
if _static_text_path.exists():
    STATIC_TEXT = _static_text_path.read_text(encoding="utf-8")
if _notice_cache_path.exists():
    notice_text = _notice_cache_path.read_text(encoding="utf-8")
    STATIC_TEXT = f"{STATIC_TEXT}\n\n{notice_text}".strip()
if not STATIC_TEXT:
    STATIC_TEXT = "Static manual not available."

def create_rag_prompt(language: str = "ko") -> PromptTemplate:
    """RAG prompt."""
    if language == "ko":
        template = _load_text_file(
            "rag_prompt_ko.txt",
            fallback="""당신은 분당융합기술교육원의 공식 AI 상담원입니다.
**반드시 한국어로만** 답변하세요.
제공된 문맥 정보만을 사용해 정확하고 간결하게 답하세요.
정보가 없으면 "해당 내용은 현재 자료에 없습니다. 교학처(031-696-8803)로 문의해 주세요."라고 안내하세요.

[문맥]
{context}

질문: {question}
답변(한국어): """,
        )
    else:
        template = """Context from Bundang Polytechnic documents:

{context}

Answer in English only, concisely, based only on the context. If unknown, suggest contacting the admin office (031-696-8803).

Question: {question}
Answer:"""

    return PromptTemplate(template=template, input_variables=["context", "question"])


def generate_rag_response(query: str, language: str = "ko", k: int = 5) -> Dict[str, Any]:
    """RAG response."""
    docs = retrieve_documents(query, k=k)
    if not docs:
        not_found_ko = _load_text_file(
            "rag_not_found_ko.txt",
            fallback="No matching documents found. Please contact the admin office (031-696-8803).",
        )
        return {
            "response": not_found_ko if language == "ko" else "No documents found.",
            "source": "none",
            "language": language,
        }

    context = "\n\n".join([d["content"] for d in docs])
    if language == "ko":
        context = _clean_context_ko(context)
    prompt = create_rag_prompt(language)
    formatted = prompt.format(context=context, question=query)

    model = _get_llm_model()
    if not model:
        return {
            "response": context[:1000] + "...",
            "source": "rag_document",
            "documents": docs,
            "language": language,
        }

    # 응답 속도 개선: max_tokens를 256으로 제한 (512 → 256)
    output = model(
        formatted,
        max_tokens=256,  # 응답 속도 2배 향상
        temperature=0.3,
        top_p=0.9,
        repeat_penalty=1.1,
        echo=False,
    )

    response_text = output["choices"][0]["text"].strip()
    tokens_used = output.get("usage", {}).get("completion_tokens", 0)

    return {
        "response": response_text,
        "source": "rag_llm",
        "documents": docs,
        "language": language,
        "tokens_used": tokens_used,
    }


def _load_pdfs(pdf_paths: Optional[List[Path]] = None, include_static: bool = True) -> Tuple[List[str], List[Dict[str, Any]]]:

    """PDF들을 페이지 단위로 읽어 텍스트와 메타데이터 반환. 필요 시 STATIC_TEXT도 포함."""
    texts: List[str] = []
    metas: List[Dict[str, Any]] = []

    def split_static_text(text: str) -> List[Tuple[str, str]]:
        lines = text.strip().splitlines()
        sections: List[Tuple[str, str]] = []
        current_title = "static_manual"
        current_lines: List[str] = []
        for line in lines:
            stripped = line.strip()
            if stripped and (stripped.startswith("#") or re.match(r"^\\d+#", stripped)):
                if current_lines:
                    sections.append((current_title, "\n".join(current_lines).strip()))
                    current_lines = []
                current_title = stripped
            current_lines.append(line)
        if current_lines:
            sections.append((current_title, "\n".join(current_lines).strip()))
        return sections

    targets: List[Path] = []

    if pdf_paths:
        print(f"  📌 사용자 지정 PDF 경로: {len(pdf_paths)}개")
        targets = pdf_paths

    else:
        print(f"  🔍 자동 PDF 검색 중...")
        root_dir = Path(__file__).parent.parent.parent.parent  # repo root
        print(f"     검색 경로: {root_dir}")

        candidates = list(root_dir.glob("*.pdf")) + list((root_dir / "backend-python").glob("*.pdf"))
        print(f"  📁 발견된 PDF 파일: {len(candidates)}개")

        targets = [p for p in candidates if p.exists()]
        if targets:
            for pdf in targets:
                print(f"     - {pdf.name}")



    if not targets or (PdfReader is None and not _CHANDRA_AVAILABLE):
        if PdfReader is None and targets and not _CHANDRA_AVAILABLE:
            print(f"  ⚠️ pypdf/chandra 사용 불가 - PDF 추출 건너뜀")
            logger.warning("No PDF reader available; skipping PDF extraction.")
        if include_static:
            print(f"  📝 Static manual 로드 중...")
            sections = split_static_text(STATIC_TEXT)
            print(f"  ✅ Static manual {len(sections)}개 섹션 로드 완료")
            for i, (title, section_text) in enumerate(sections, start=1):
                texts.append(section_text)
                metas.append(
                    {
                        "file": "static_manual",
                        "path": "static_manual",
                        "page": i,
                        "section": title,
                    }
                )
        return texts, metas

    if not targets:
        print(f"  ⚠️ PDF 파일을 찾을 수 없습니다")
        logger.warning("No PDF files found.")
        return texts, metas


    print(f"  📖 PDF 파일 읽는 중...")
    pdf_page_count = 0
    for pdf_path in targets:

        try:
            chandra_enabled = os.getenv("CHANDRA_PDF_ENABLED", "false").lower() in (
                "1",
                "true",
                "yes",
            )
            chandra_method = os.getenv("CHANDRA_METHOD", "hf")
            chandra_texts = []
            if chandra_enabled and _CHANDRA_AVAILABLE:
                print(f"     - {pdf_path.name}: Chandra OCR 시도 중...")
                chandra_texts = _extract_pdf_text_chandra(pdf_path, chandra_method)
                if chandra_texts:
                    print(f"     - {pdf_path.name}: Chandra OCR {len(chandra_texts)}페이지 추출")
                    for page_idx, page_text in enumerate(chandra_texts):
                        page_text = page_text.replace("\x00", " ").strip()
                        if not page_text:
                            continue
                        texts.append(page_text)
                        pdf_page_count += 1
                        metas.append(
                            {
                                "file": pdf_path.name,
                                "path": str(pdf_path),
                                "page": page_idx + 1,
                                "source": "chandra",
                            }
                        )
                    continue

            if PdfReader is None:
                print(f"     - {pdf_path.name}: pypdf 사용 불가, PDF 추출 건너뜀")
                continue
            reader = PdfReader(str(pdf_path))
            num_pages = len(reader.pages)
            print(f"     - {pdf_path.name}: {num_pages}페이지")

            for page_idx, page in enumerate(reader.pages):

                try:

                    raw = page.extract_text() or ""

                except Exception:

                    raw = ""

                raw = raw.replace("\x00", " ").strip()

                if not raw:

                    continue

                texts.append(raw)
                pdf_page_count += 1

                metas.append(

                    {

                        "file": pdf_path.name,

                        "path": str(pdf_path),

                        "page": page_idx + 1,

                    }

                )

        except Exception as e:
            print(f"  ❌ PDF 읽기 실패 ({pdf_path.name}): {e}")
            logger.error(f"Failed to read {pdf_path}: {e}")

            continue

    print(f"  ✅ PDF에서 {pdf_page_count}개 페이지 추출 완료")



    # 추가 스태틱 텍스트 삽입
    if include_static:
        print(f"  📝 Static manual 추가 중...")
        sections = split_static_text(STATIC_TEXT)
        print(f"  ✅ Static manual {len(sections)}개 섹션 추가 완료")
        for i, (title, section_text) in enumerate(sections, start=1):
            texts.append(section_text)
            metas.append(
                {
                    "file": "static_manual",
                    "path": "static_manual",
                    "page": i,
                    "section": title,
                }
            )

    print(f"  📊 총 {len(texts)}개 문서 준비 완료")
    return texts, metas





def _build_embeddings(

    texts: List[str],

    metas: List[Dict[str, Any]],

    chunk_size: int = 800,

    chunk_overlap: int = 120,

    target_dim: Optional[int] = 256,

) -> Tuple[np.ndarray, List[str], List[Dict[str, Any]], Optional[Any]]:

    """

    텍스트 -> 청크 -> 임베딩 -> (PCA) -> 정규화 벡터

    """

    print(f"  🔧 임베딩 모델 로드 중...")
    embedding_model = _get_embedding_model()
    if embedding_model:
        print(f"  ✅ 임베딩 모델 로드 성공")
    else:
        print(f"  ⚠️ 임베딩 모델 없음 - 해시 임베딩 사용")

    all_chunks: List[str] = []

    all_meta: List[Dict[str, Any]] = []


    print(f"  ✂️ 텍스트 청킹 중 (chunk_size={chunk_size}, overlap={chunk_overlap})...")
    for idx, text in enumerate(texts):

        cleaned = clean_text(text)

        chunks = chunk_text(cleaned, max_len=chunk_size, overlap=chunk_overlap)

        chunks = deduplicate(chunks)

        for chunk in chunks:

            all_chunks.append(chunk)

            meta_copy = dict(metas[idx]) if idx < len(metas) else {}

            meta_copy["source_index"] = idx

            meta_copy["text_length"] = len(chunk)

            all_meta.append(meta_copy)

    print(f"  ✅ 청킹 완료: {len(all_chunks)}개 청크 생성")



    if not all_chunks:
        print(f"  ⚠️ 청크가 없습니다")
        return np.empty((0, 0)), [], [], None


    print(f"  🧮 임베딩 생성 중 ({len(all_chunks)}개 청크)...")
    if embedding_model:
        emb_matrix = embedding_model.encode(
            all_chunks, convert_to_numpy=True, show_progress_bar=False
        )
        # sentence-transformers returns ndarray; HF wrapper returns list of arrays
        if isinstance(emb_matrix, list):
            emb_matrix = np.vstack(emb_matrix)
        print(f"  ✅ 임베딩 생성 완료 (shape: {emb_matrix.shape})")
    else:
        emb_matrix = _simple_hash_embeddings(all_chunks, dim=512)
        print(f"  ✅ 해시 임베딩 생성 완료 (shape: {emb_matrix.shape})")


    pca = None

    if target_dim and target_dim > 0:

        n_samples, n_features = emb_matrix.shape
        print(f"  📐 PCA 차원 축소 검토 중 (현재: {n_features}D → 목표: {target_dim}D)...")

        # 샘플 수가 충분할 때만 PCA 적용. 부족하면 원본 차원(예: 1024)을 유지.

        if n_samples > target_dim and target_dim < n_features:

            try:
                from sklearn.decomposition import PCA

                effective_dim = min(target_dim, n_samples - 1)
                if effective_dim > 1:
                    pca = PCA(n_components=effective_dim, random_state=42)
                    emb_matrix = pca.fit_transform(emb_matrix)
                    print(f"  ✅ PCA 적용 완료 ({n_features}D → {emb_matrix.shape[1]}D)")
            except Exception as e:
                print(f"  ⚠️ PCA 적용 실패: {e}")
                pca = None
        else:
            print(f"  ⚠️ PCA 조건 불충족 (샘플: {n_samples}, 차원: {n_features})")


    # 정규화 (내적 기반 검색)
    print(f"  🔄 벡터 정규화 중...")
    norms = np.linalg.norm(emb_matrix, axis=1, keepdims=True) + 1e-10

    emb_norm = emb_matrix / norms
    print(f"  ✅ 정규화 완료")



    return emb_norm.astype("float32"), all_chunks, all_meta, pca





def initialize_rag_system(pdf_paths: Optional[List[str]] = None, target_dim: int = 256) -> bool:
    """PDF를 읽어 벡터 인덱스를 구성."""
    try:
        print("  📄 PDF 문서 로딩 중...")
        paths = [Path(p) for p in pdf_paths] if pdf_paths else None
        texts, metas = _load_pdfs(paths, include_static=True)

        if not texts:
            print("  ⚠️ PDF에서 텍스트를 추출하지 못했습니다.")
            if STATIC_TEXT:
                print("  📝 Static manual로 폴백합니다.")
                texts = [STATIC_TEXT]
                metas = [{"file": "static_manual", "path": "static_manual", "page": 1}]
            else:
                logger.warning("No texts extracted from PDFs.")
                print("  ❌ RAG 시스템 초기화 실패: 문서 없음")
                return False
        else:
            print(f"  ✅ {len(texts)}개 문서 로드 완료")

        print("  🔢 임베딩 생성 중...")
        emb_norm, chunks, metadatas, pca = _build_embeddings(
            texts, metas, chunk_size=800, chunk_overlap=120, target_dim=target_dim
        )

        if emb_norm.size == 0:
            logger.warning("No embeddings built.")
            print("  ❌ 임베딩 생성 실패")
            return False

        print(f"  ✅ {len(chunks)}개 청크 생성 완료")

        dim = emb_norm.shape[1]
        index = None
        if _FAISS_AVAILABLE:
            print(f"  🔍 FAISS 인덱스 구축 중 (차원: {dim})...")
            index = faiss.IndexFlatIP(dim)
            index.add(emb_norm)
            print(f"  ✅ FAISS 인덱스 구축 완료")
        else:
            print(f"  ⚠️ FAISS 사용 불가 - numpy 검색 사용 (차원: {dim})")

        _rag_system["index"] = index
        _rag_system["embeddings_norm"] = emb_norm
        _rag_system["metadatas"] = metadatas
        _rag_system["chunks"] = chunks
        _rag_system["pca"] = pca
        _rag_system["dimension"] = dim
        _rag_system["original_dimension"] = (
            pca.n_features_ if pca is not None else dim
        )
        _rag_system["initialized"] = True
        _rag_system["use_faiss"] = _FAISS_AVAILABLE

        logger.info(f"RAG initialized: chunks={len(chunks)}, dim={dim}")
        print(f"  📊 RAG 시스템 통계:")
        print(f"     - 총 청크: {len(chunks)}")
        print(f"     - 차원: {dim}")
        print(f"     - FAISS: {'사용' if _FAISS_AVAILABLE else '미사용'}")
        return True

    except Exception as e:
        logger.error(f"RAG initialization error: {e}", exc_info=True)
        print(f"  ❌ RAG 초기화 오류: {e}")
        import traceback
        traceback.print_exc()
        return False





def retrieve_documents(query: str, k: int = 5) -> List[Dict[str, Any]]:
    """쿼리로 상위 k개 문서 반환."""
    if not _rag_system["initialized"]:
        print(f"  ⚠️ RAG 미초기화 - 문서 검색 불가")
        logger.warning("RAG system not initialized, cannot retrieve documents")
        return []

    print(f"  🔎 문서 검색: '{query}' (상위 {k}개)")



    embedding_model = _get_embedding_model()
    if not embedding_model:
        # Fallback to hash embeddings when no model is available.
        embedding_model = None


    try:

        if embedding_model:
            q_emb = embedding_model.encode([query], convert_to_numpy=True)
            if isinstance(q_emb, list):
                q_emb = np.array(q_emb[0])
            else:
                q_emb = q_emb[0]
        else:
            q_emb = _simple_hash_embeddings([query], dim=_rag_system["dimension"] or 512)[0]
        if _rag_system["pca"] is not None:

            q_emb = _rag_system["pca"].transform(q_emb.reshape(1, -1))[0]

        q_emb = q_emb / (np.linalg.norm(q_emb) + 1e-10)



        index = _rag_system["index"]
        emb_norm = _rag_system["embeddings_norm"]
        if _rag_system["use_faiss"] and index is not None:
            scores, idxs = index.search(np.array([q_emb], dtype="float32"), k)
            score_list = scores[0]
            idx_list = idxs[0]
        else:
            if emb_norm is None or len(emb_norm) == 0:
                return []
            scores_all = emb_norm @ q_emb
            k = min(k, scores_all.shape[0])
            idx_list = np.argsort(-scores_all)[:k]
            score_list = scores_all[idx_list]

        results = []
        for score, idx in zip(score_list, idx_list):
            if idx < 0 or idx >= len(_rag_system["chunks"]):
                continue
            results.append(

                {

                    "content": _rag_system["chunks"][idx],

                    "metadata": _rag_system["metadatas"][idx],

                    "score": float(score),

                }

            )

        return results

    except Exception as e:

        logger.error(f"Document retrieval error: {e}")

        return []





def is_rag_initialized() -> bool:

    return _rag_system["initialized"]





def get_vector_store():

    return _rag_system["index"]

