# 📡 Poly-i Chatbot

공공·기관 환경을 염두에 둔 **문서 기반 질의응답 시스템**입니다.  
과도한 생성 중심 접근을 지양하고, **검색·근거·일관성**을 중심으로 설계되었습니다.

----

## 🔍 Overview
- 내부 문서(PDF / Text) 기반 질의응답
- 키워드 검색 + 벡터 검색을 결합한 혼합 검색 구조
- 불필요한 장문 생성 없이 핵심 정보만 제공
- 로컬 실행 기준 설계 (교육·연구·프로토타입 환경 적합)

----

## ✨ Key Features
- 📄 문서 업로드 및 자동 인덱싱
- 🔎 질의 시 관련 문서 우선 검색
- 🧠 문서 맥락 기반 요약 응답
- 📌 응답 근거를 문서 단위로 추적 가능
- ♻ 동일 질의에 대해 일관된 결과 제공

----
<img width="500" height="922" alt="image" src="https://github.com/user-attachments/assets/1c26a355-4d20-4733-a6ce-d8cd377c2269" />

## 🏗 System Architecture
```
┌──────────────┐
│ User UI │
│ (Web / CLI) │
└──────┬───────┘
│ Query
▼
┌──────────────┐
│ Query Parser │
│ - 정규화 │
│ - 불용어 제거│
└──────┬───────┘
│
▼
┌────────────────────────┐
│ Retrieval Layer │
│ │
│ ┌────────────┐ ┌──────┐│
│ │ Keyword │ │Vector││
│ │ Search │ │Search││
│ └─────┬──────┘ └──┬───┘│
└────────┴────────────┴──┘
│
▼
┌───────────────────────┐
│ Context Builder │
│ - 관련 문서 필터링 │
│ - 중복/노이즈 제거 │
└──────────┬────────────┘
│
▼
┌───────────────────────┐
│ Response Generator │
│ - 요약 중심 응답 │
│ - 규칙 기반 포맷 │
└──────────┬────────────┘
│
▼
┌────────────┐
│ Answer │
│ (Text) │
└────────────┘
```
----

## 🧱 Tech Stack
- **Language**: Python
- **Backend**: FastAPI
- **Retrieval**: Vector Search (FAISS / Qdrant), Keyword Search
- **NLP**: Sentence Embedding, Lightweight LLM
- **Data**: PDF, Plain Text

----

## 📁 Project Structure
```
Poly-i-chatbot/
├── app.py # Application entry point
├── api/ # API endpoints
├── core/
│ ├── parser.py # Query preprocessing
│ ├── retriever.py # Document retrieval logic
│ └── responder.py # Response generation
├── data/ # Source documents
├── vector_db/ # Vector index storage
├── requirements.txt
└── README.md
```

----

## ⚙ How It Works
1. 문서를 벡터화하여 인덱스 생성
2. 사용자 질의를 전처리
3. 키워드 검색 + 벡터 검색으로 관련 문서 추출
4. 핵심 정보만 선별하여 응답 구성
5. 동일 입력에 대해 재현 가능한 결과 제공

----

## 🚀 Execution
```bash
pip install -r requirements.txt
python app.py
🎯 Use Cases

🏛 기관·학교 내부 FAQ 시스템

🎓 RAG 구조 학습용 예제

📚 문서 기반 정보 검색 서비스

🧪 생성형 모델 도입 전 구조 검증

⚠ Notes

생성 다양성보다 정확성·근거·일관성을 우선

실서비스 이전 단계의 구조 검증 목적

외부 API, 다중 문서 타입 확장 가능

👤 Author

Jin-kyung Cho

GitHub: https://github.com/susie1214

