import logging
import re
from typing import List, Dict, Any, Optional

import numpy as np
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity

from src.models.model_manager import get_embedding_model

logger = logging.getLogger(__name__)


def clean_text(text: str) -> str:
    """특수기호/중복 공백 제거 등 기본 클리닝."""
    if not text:
        return ""
    cleaned = re.sub(r"[^0-9A-Za-z\u3131-\u318E\uAC00-\uD7A3\s.,;:!?()\-/·%]", " ", text)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def chunk_text(text: str, max_len: int = 600, overlap: int = 80) -> List[str]:
    """문단 단위로 나눈 뒤 max_len 기준 슬라이딩 오버랩."""
    if not text:
        return []
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks: List[str] = []
    for para in paragraphs:
        tokens = para.split()
        start = 0
        while start < len(tokens):
            end = min(len(tokens), start + max_len)
            chunk = " ".join(tokens[start:end]).strip()
            if chunk:
                chunks.append(chunk)
            if end == len(tokens):
                break
            start = max(0, end - overlap)
    return chunks


def deduplicate(chunks: List[str]) -> List[str]:
    seen = set()
    uniq: List[str] = []
    for c in chunks:
        if c not in seen:
            seen.add(c)
            uniq.append(c)
    return uniq


def reduce_dimension(embeddings: np.ndarray, target_dim: int = 256) -> np.ndarray:
    """차원 축소 (PCA). 샘플 수가 적으면 스킵."""
    if embeddings.shape[1] <= target_dim:
        return embeddings
    # n_components는 min(n_samples, n_features, target_dim)보다 작아야 함
    n_samples, n_features = embeddings.shape
    max_components = min(n_samples, n_features)
    if target_dim >= max_components:
        return embeddings
    pca = PCA(n_components=target_dim, random_state=42)
    return pca.fit_transform(embeddings)


def generate_embeddings(
    texts: List[str],
    do_clean: bool = True,
    do_chunk: bool = True,
    max_len: int = 600,
    overlap: int = 80,
    reduce_dim: Optional[int] = 256,
) -> Dict[str, Any]:
    """여러 텍스트 -> 임베딩 + 옵션 클리닝/차원축소/중복제거."""
    model = get_embedding_model()
    if not model:
        raise Exception("Embedding model not loaded")

    all_chunks: List[str] = []
    chunk_meta: List[Dict[str, Any]] = []

    for idx, raw in enumerate(texts):
        txt = clean_text(raw) if do_clean else raw
        chunks = chunk_text(txt, max_len=max_len, overlap=overlap) if do_chunk else [txt]
        chunks = deduplicate(chunks)
        for c in chunks:
            all_chunks.append(c)
            chunk_meta.append({"source_index": idx, "text_length": len(c)})

    if not all_chunks:
        return {
            "embeddings": [],
            "dimension": 0,
            "model": "all-MiniLM-L6-v2",
            "chunks": [],
            "metadata": [],
        }

    embedding_matrix = model.encode(all_chunks, convert_to_numpy=True, show_progress_bar=False)

    if reduce_dim and reduce_dim > 0:
        embedding_matrix = reduce_dimension(embedding_matrix, target_dim=reduce_dim)
    dim = embedding_matrix.shape[1]

    model_name = getattr(model, "model_id", None) or getattr(model, "name", None) or "unknown"

    return {
        "embeddings": embedding_matrix.tolist(),
        "dimension": dim,
        "model": model_name,
        "chunks": all_chunks,
        "metadata": chunk_meta,
    }


def similarity_search(query_embedding: list, embeddings_db: list, top_k: int = 5):
    """코사인 유사도로 상위 문서 검색."""
    query_vec = np.array(query_embedding).reshape(1, -1)
    db_vecs = np.array(embeddings_db)

    similarities = cosine_similarity(query_vec, db_vecs)[0]
    top_indices = np.argsort(similarities)[::-1][:top_k]

    return [
        {
            "index": int(idx),
            "similarity": float(similarities[idx])
        }
        for idx in top_indices
    ]
