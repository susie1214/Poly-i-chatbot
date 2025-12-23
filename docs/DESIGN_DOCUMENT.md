# Poly-i 설계 문서 ✨

안녕하세요! 분당폴리텍(융합기술교육원) 상담을 돕는  챗봇 Poly-i의 설계 문서예요.   🧑‍💻💙

---

## 1. 서론 (Introduction) 🧩

### 1.1 개발 배경 및 필요성
- 학교 홈페이지 및 행정부서에 모집요강/지원자격/훈련수당 문의가 반복 발생 🌀
- 기존 FAQ는 정형화된 질문만 대응 가능하고, 복합 질문 처리에 한계가 있음
- 그래서 LLM + RAG 기반의 지능형 상담 시스템이 필요함 ✨

### 1.2 프로젝트 목표
- 공식 문서 기반의 신뢰도 높은 응답 제공 📚
- 24시간 비대면 상담 구현 ⏰
- 반복 업무 자동화로 행정 효율 개선 🚀

---

## 2. 시스템 아키텍처 (System Architecture) 🏗️

### 2.1 기술 스택 (Technology Stack)
- 🤖 LLM: Meta-Llama-3.1-8B-Instruct (GGUF Q4_K_M)
- 🔎 RAG: FAISS Vector Search
- 🧠 Embedding: intfloat/multilingual-e5-large-instruct
- 🐍 Backend: Flask (Python)
- 🌐 API Gateway: Node.js
- 🎨 Frontend: React (Vite)
- 📦 Infra: Docker / docker-compose
- 🧭 Routing: LangGraph

### 2.2 구조도
```
┌──────────────┐
│ User UI      │
│ (Web / CLI)  │
└──────┬───────┘
       │ Query
       ▼
┌──────────────┐
│ Query Parser │
│ - 정규화     │
│ - 불용어 제거│
└──────┬───────┘
       │
       ▼
┌────────────────────────┐
│ Retrieval Layer         │
│  ┌────────────┐ ┌──────┐│
│  │ Keyword    │ │Vector││
│  │ Search     │ │Search││
│  └─────┬──────┘ └──┬───┘│
└────────┴────────────┴──┘
       │
       ▼
┌───────────────────────┐
│ Context Builder        │
│ - 관련 문서 필터링     │
│ - 중복/노이즈 제거     │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Response Generator     │
│ - 요약 중심 응답       │
│ - 규칙 기반 포맷       │
└──────────┬────────────┘
           │
           ▼
┌────────────┐
│ Answer     │
│ (Text)     │
└────────────┘
```

### 2.3 LangGraph 라우팅 🔁
- ✅ 키워드 응답 우선
- 💬 일반 질문 → LLM 직접 답변
- 🏫 학교 문의 → RAG 검색 + LLM 답변
- 🧯 RAG 실패 시 LLM 폴백

---

## 3. 핵심 구현 (Implementation Details) 🛠️

### 3.1 하이브리드 응답 엔진 (llm_service.py)
- 🧩 Keyword Matching: 학과/취업/인사 등 즉답
- 🤖 LLM Answer: 일반 질문 생성 응답
- 📚 RAG Answer: 학교 문의 문서 기반 응답

### 3.2 문서 파싱 & OCR (rag_service.py)
- 🔍 Primary: Chandra OCR
- 📄 Fallback: pypdf
- ⚙️ 환경변수 제어  
  - `CHANDRA_PDF_ENABLED=true|false`  
  - `CHANDRA_METHOD=hf|vllm`
- 💾 FAISS 인덱스 캐시 저장/재사용

### 3.3 공지사항 크롤러 (kopo_crawler_rag.py)
- 🕵️‍♀️ 학교 공지사항 자동 수집
- 📁 `kopo_notices_cache.txt`로 캐싱 후 RAG 포함

### 3.4 프론트 UX (Frontend)
- 💬 ChatContainer: 반응형 채팅 + 자동 인사 + 추천 질문
- 👩‍🏫 ProfessorIntro: 교수 소개 + 한/영 라벨

---

## 4. 시범 운영 및 검증 (Pilot & Validation) ✅

### 4.1 로드맵
1) 내부 테스트로 RAG 정확도/환각 검증  
2) 행정 문의 시나리오 기반 품질 고도화  
3) 홈페이지 iframe 연동 및 외부 배포

### 4.2 기대 효과
- 🧾 반복 문의 자동화
- 🌙 24시간 상담 제공
- 📊 질의 로그 기반 데이터 자산화

---

## 5. 결론 및 향후 과제 (Conclusion) 🌱

Poly-i는 교육 행정에 특화된 LLM + RAG 시스템으로,  
LLM의 환각 문제를 줄이고 최신 정보를 반영할 수 있도록 설계되었습니다. ✨  
  
향후에는 LMS 연동, 개인화 상담, 학과별 특화 봇으로 확장할 예정입니다. 🚀
