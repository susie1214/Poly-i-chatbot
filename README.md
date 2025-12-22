# Poly-i Chatbot

Bundang Polytechnic (융합기술교육원) RAG 기반 안내 챗봇입니다.  
PDF/정적 문서 + 크롤링 공지사항을 검색해 답변합니다.

## 현재 흐름
1) 문서 로딩: `static_manual_ko.txt` + PDF + (선택) 공지사항 캐시  
2) 텍스트 정제/청킹 → 임베딩 생성 → FAISS 인덱스 구성  
3) 키워드 응답 우선 → RAG 검색 → LLM 답변  

## 주요 구성
- Frontend: `frontend/` (Vite + React)
- Backend (Python): `backend-python/` (Flask)
- LLM: `backend-python/models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf`
- Embedding: `intfloat/multilingual-e5-large-instruct`
- RAG: FAISS + 텍스트 청킹

## PDF 추출
1) Chandra OCR (우선)  
2) 실패 시 pypdf 폴백  

환경변수:
- `CHANDRA_PDF_ENABLED=true|false`
- `CHANDRA_METHOD=hf|vllm`

## 실행
```bash
cd backend-python
pip install -r requirements.txt
python app.py
```

```bash
cd frontend
npm install
npm run dev
```

## 공지사항 크롤러 (선택)
```bash
python -m src.services.kopo_crawler_rag
```
실행 후 `kopo_notices_cache.txt`가 생성되며 RAG에 자동 포함됩니다.

