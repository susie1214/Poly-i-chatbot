# -*- coding: utf-8 -*-
"""
한국폴리텍대학 분당융합기술교육원(https://www.kopo.ac.kr/ctc/index.do)
공지사항 크롤러 + RAG 인덱스 구축 스크립트.
- 공지사항 목록/본문 크롤링
- 한글 깨짐 방지(NFKC) 정규화
- 청크 분할
- multilingual-e5-large-instruct 기반 임베딩 인덱스
- CLI 질의 검색 (LLM 없이 사용 가능)

실행:
    python -m src.services.kopo_crawler_rag
또는
    python src/services/kopo_crawler_rag.py
"""
import os
import re
import unicodedata
from dataclasses import dataclass
from typing import List, Dict, Optional, Set
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(__file__)
NOTICE_CACHE_PATH = os.path.join(BASE_DIR, "kopo_notices_cache.txt")


# =========================
# 1) 데이터 구조
# =========================
@dataclass
class NoticeDocument:
    """공지사항 1건을 표현."""
    title: str
    date: str
    url: str
    content: str


# =========================
# 2) 텍스트 정규화 / 불용어
# =========================
KOR_STOPWORDS = {
    "및", "및의", "등", "또는", "그리고", "그러나",
    "하지만", "관련", "대상", "기준", "통해",
}
ENG_STOPWORDS = {
    "the", "a", "an", "and", "or", "to", "for", "in", "on", "at",
}


def normalize_text(text: str) -> str:
    """한글 깨짐 방지용 정규화 + 노이즈/중복 라인 제거."""
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\u00ad", "").replace("\u200b", "")
    # 하이픈 줄바꿈 복원
    text = re.sub(r"-\s*\n\s*", "", text)
    text = text.replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)
    lines = [ln.strip() for ln in text.split("\n")]
    result = []
    seen: Set[str] = set()
    for ln in lines:
        if not ln:
            continue
        # 장식선 / 구분선 제거
        if re.fullmatch(r"[-=·~\s]+", ln):
            continue
        if ln in seen:
            continue
        seen.add(ln)
        result.append(ln)
    text = "\n".join(result)
    # 제어문자 제거
    text = "".join(
        ch for ch in text if unicodedata.category(ch)[0] != "C"
    )
    return text.strip()


def build_keyword_text(text: str) -> str:
    """불용어 제거 버전 텍스트 (BM25 등 보조 인덱스용)."""
    tokens = re.findall(r"[가-힣A-Za-z0-9]+", text)
    filtered = []
    for t in tokens:
        low = t.lower()
        if low in ENG_STOPWORDS or low in KOR_STOPWORDS:
            continue
        filtered.append(t)
    return " ".join(filtered)


# =========================
# 3) 크롤러
# =========================
class KopoCrawler:
    """
    분당융합기술교육원 홈페이지 크롤러.
    - KOPO NEWS 영역의 공지사항 목록 수집
    - 각 공지 상세 페이지 본문 수집
    """
    BASE_URL = "https://www.kopo.ac.kr"
    INDEX_PATH = "/ctc/index.do"
    UA = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )

    def __init__(self, timeout: int = 10):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.UA})
        self.timeout = timeout

    def fetch(self, url: str) -> Optional[str]:
        try:
            resp = self.session.get(url, timeout=self.timeout)
            resp.raise_for_status()
            resp.encoding = resp.apparent_encoding or "utf-8"
            return resp.text
        except Exception as e:
            print(f"[ERROR] fetch failed: {url} ({e})")
            return None

    def fetch_main_page(self) -> Optional[BeautifulSoup]:
        url = urljoin(self.BASE_URL, self.INDEX_PATH)
        html = self.fetch(url)
        if not html:
            return None
        return BeautifulSoup(html, "html.parser")

    def parse_notices_from_index(
        self, soup: BeautifulSoup, limit: int = 10
    ) -> List[Dict]:
        """
        메인 페이지의 KOPO NEWS → 공지사항 목록을 파싱.
        return:
            [{ "title": ..., "date": ..., "url": ... }, ...]
        """
        results = []
        # "공지사항"이라는 텍스트를 가진 제목(h3/h2 등) 찾기
        header = soup.find(
            lambda tag: tag.name in ("h2", "h3", "h4")
            and tag.get_text(strip=True).startswith("공지사항")
        )
        if not header:
            print("[WARN] 공지사항 헤더를 찾지 못했습니다.")
            return results
        # 공지사항 리스트는 보통 바로 뒤의 <ul> 또는 <div> 안에 존재
        container = header.find_next(lambda tag: tag.name in ("ul", "ol", "div"))
        if not container:
            print("[WARN] 공지사항 컨테이너를 찾지 못했습니다.")
            return results
        links = container.find_all("a", href=True)
        for a in links[:limit]:
            title = a.get_text(" ", strip=True)
            href = a["href"]
            url = urljoin(self.BASE_URL, href)
            # 날짜는 보통 a 주변 span 또는 li 안에 있음
            date = ""
            parent_li = a.find_parent("li")
            if parent_li:
                # YYYY.MM.DD 패턴 검색
                m = re.search(r"\d{4}\.\d{2}\.\d{2}", parent_li.get_text())
                if m:
                    date = m.group(0)
            results.append(
                {
                    "title": normalize_text(title),
                    "date": date,
                    "url": url,
                }
            )
        return results

    def parse_notice_detail(self, url: str) -> str:
        """
        공지 상세 페이지에서 본문 텍스트 추출.
        캠퍼스 게시판 구조가 바뀌어도 동작하도록 다소 넉넉하게 작성.
        """
        html = self.fetch(url)
        if not html:
            return ""
        soup = BeautifulSoup(html, "html.parser")
        # 후보 컨테이너들을 우선순위대로 탐색
        candidates = []
        # id 기반
        for id_name in ["contents", "content", "bo_v_con", "board-container"]:
            c = soup.find(id=id_name)
            if c:
                candidates.append(c)
        # class 기반
        for cls in [
            "board_view",
            "boardView",
            "board-detail",
            "view_con",
            "bd_view",
            "bbs_view",
        ]:
            c = soup.find("div", class_=cls)
            if c:
                candidates.append(c)
        # article 태그
        for tag in soup.find_all("article"):
            candidates.append(tag)
        # fallback: body
        candidates.append(soup.body)
        for c in candidates:
            if not c:
                continue
            text = c.get_text("\n", strip=True)
            text = normalize_text(text)
            # 너무 짧으면 본문이 아닐 가능성이 높음
            if len(text) > 50:
                return text
        return ""

    def crawl_notices(self, limit: int = 20) -> List[NoticeDocument]:
        """
        메인 페이지 → 공지사항 목록 → 상세 페이지까지 크롤링.
        """
        soup = self.fetch_main_page()
        if not soup:
            return []
        meta_list = self.parse_notices_from_index(soup, limit=limit)
        docs: List[NoticeDocument] = []
        for meta in meta_list:
            print(f"[INFO] Fetch notice: {meta['title']} ({meta['url']})")
            content = self.parse_notice_detail(meta["url"])
            if not content:
                continue
            docs.append(
                NoticeDocument(
                    title=meta["title"],
                    date=meta["date"],
                    url=meta["url"],
                    content=content,
                )
            )
        print(f"[INFO] 크롤링 완료: {len(docs)}건")
        return docs


# =========================
# 4) 청크 분할 + 임베딩 인덱스
# =========================
def chunk_text(text: str, max_chars: int = 800, overlap: int = 100) -> List[str]:
    """공지 본문을 RAG용 청크로 분할."""
    paras = re.split(r"\n\s*\n", text)
    paras = [p.strip() for p in paras if p.strip()]
    chunks: List[str] = []
    cur = ""
    for p in paras:
        if len(p) > max_chars:
            s = 0
            while s < len(p):
                e = s + max_chars
                chunks.append(p[s:e])
                s = e - overlap
            continue
        if len(cur) + len(p) + 1 <= max_chars:
            cur = cur + "\n" + p if cur else p
        else:
            chunks.append(cur)
            cur = p
    if cur:
        chunks.append(cur)
    return [c.strip() for c in chunks if len(c) > 30]


class NoticeEmbeddingIndex:
    """
    multilingual-e5-large-instruct 기반 공지사항 RAG 인덱스.
    - query:  "query: {질문}"
    - passage: "passage: {공지 청크}"
    """

    def __init__(self, model_name: str = "intfloat/multilingual-e5-large-instruct", device: str = "cpu"):
        self.model = SentenceTransformer(model_name, device=device)
        self.embeddings: Optional[np.ndarray] = None
        self.metadatas: List[Dict] = []

    def add_notices(self, notices: List[NoticeDocument], max_chars=800, overlap=100):
        texts: List[str] = []
        metas: List[Dict] = []
        for n in notices:
            chunks = chunk_text(n.content, max_chars=max_chars, overlap=overlap)
            for cid, ch in enumerate(chunks):
                texts.append(f"passage: {ch}")
                metas.append(
                    {
                        "title": n.title,
                        "date": n.date,
                        "url": n.url,
                        "chunk_id": cid,
                        "text": ch,
                        "keywords": build_keyword_text(ch),
                    }
                )
        if not texts:
            return
        print(f"[INFO] 임베딩 생성 중... (청크 {len(texts)}개)")
        arr = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True,
        )
        self.embeddings = arr
        self.metadatas = metas
        print("[INFO] 임베딩 인덱스 구축 완료.")

    @staticmethod
    def _cosine_sim(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        a_norm = a / (np.linalg.norm(a, axis=-1, keepdims=True) + 1e-12)
        b_norm = b / (np.linalg.norm(b, axis=-1, keepdims=True) + 1e-12)
        return a_norm @ b_norm.T

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        if self.embeddings is None or len(self.embeddings) == 0:
            return []
        q = self.model.encode([f"query: {query}"], convert_to_numpy=True)
        sims = self._cosine_sim(q, self.embeddings)[0]
        idxs = np.argsort(-sims)[:top_k]
        results: List[Dict] = []
        for i in idxs:
            m = dict(self.metadatas[i])
            m["score"] = float(sims[i])
            results.append(m)
        return results


# =========================
# 5) 단독 실행용 CLI
# =========================
def save_notices_to_cache(notices: List[NoticeDocument]) -> None:
    if not notices:
        return
    blocks = []
    for n in notices:
        block = "\n".join(
            [
                f"#공지사항: {n.title}",
                f"날짜: {n.date}",
                f"URL: {n.url}",
                n.content,
            ]
        )
        blocks.append(block)
    content = "\n\n".join(blocks).strip()
    with open(NOTICE_CACHE_PATH, "w", encoding="utf-8") as f:
        f.write(content + "\n")
    print(f"[INFO] 공지사항 캐시 저장: {NOTICE_CACHE_PATH}")


def build_index() -> NoticeEmbeddingIndex:
    crawler = KopoCrawler()
    notices = crawler.crawl_notices(limit=20)
    save_notices_to_cache(notices)
    index = NoticeEmbeddingIndex(
        model_name="intfloat/multilingual-e5-large-instruct",
        device="cpu",  # GPU 사용 시 "cuda"
    )
    index.add_notices(notices)
    return index


def main():
    index = build_index()
    print("\n[공지사항 RAG 검색 모드]")
    print("질문을 입력하면 관련 공지 내용을 보여줍니다. (엔터만 누르면 종료)\n")
    while True:
        q = input("질문> ").strip()
        if not q:
            break
        results = index.search(q, top_k=5)
        if not results:
            print("  → 검색 결과 없음\n")
            continue
        print(f"\n[Top-{len(results)} 결과]")
        for r in results:
            print("-" * 80)
            print(f"제목: {r['title']}")
            if r.get("date"):
                print(f"날짜: {r['date']}")
            print(f"URL : {r['url']}")
            print(f"청크ID: {r['chunk_id']} | 유사도: {r['score']:.4f}")
            print("\n본문 일부:")
            print(r["text"][:600] + "...\n")
    print("종료.")


if __name__ == "__main__":
    main()
