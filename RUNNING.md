# RUNNING

이 문서는 로컬에서 프로젝트를 실행하는 방법과 Docker Compose로 실행하는 방법을 정리합니다.

요약
- 개발: 각 서비스(`backend-python`, `backend-node`, `frontend`)를 별도 터미널에서 실행
- 도커: `docker compose up --build`로 전체 스택을 컨테이너로 실행

1) 로컬(개발) 실행 요약

- `backend-python` (LLM 서버)
  1. `cd backend-python`
  2. `python -m venv venv`
  3. `.\venv\Scripts\Activate` (Windows PowerShell)
  4. `pip install -r requirements.txt` (또는 실패 시 개별 설치)
  5. 모델 파일을 `backend-python/models/`에 넣고 `backend-python/.env`에 `MODEL_PATH` 설정
  6. `python app.py`

- `backend-node` (API)
  1. `cd backend-node`
  2. `npm install`
  3. `.env`에 `PYTHON_LLM_URL=http://host.docker.internal:5001` 또는 `http://localhost:5001`
  4. `npm run dev` 또는 `npm start`

- `frontend` (Vite)
  1. `cd frontend`
  2. `npm install`
  3. `npm run dev`
  4. 브라우저 열기: `http://localhost:3001`

2) Docker Compose (권장: 다른 사람에게 배포/공유할 때)

- 전제: Docker 및 Docker Compose(또는 Docker Desktop)가 설치되어 있어야 합니다.
- 모델 파일은 크기 때문에 컨테이너에 포함하지 않습니다. 로컬에서 모델 파일을 가진 폴더를 컨테이너의 `/app/models`에 마운트해야 합니다.

예시 실행 (루트에서):

```powershell
# 빌드 및 백그라운드 실행
docker compose up --build -d

# 로그 확인
docker compose logs -f

# 중지
docker compose down
```

3) 배포/공유 팁
- 가장 쉬운 방법: GitHub 저장소 링크(https://github.com/susie1214/Poly-i-chatbot)와 이 `RUNNING.md`를 제공하고, 모델 다운로드 링크 및 `backend-python/.env` 예시를 함께 전달하세요.
- 더 편리하게: `docker compose` 이미지를 빌드해서 제공하거나, `docker save`로 이미지를 공유할 수 있습니다(모델은 별도).
- 기업용/대규모 배포: 모델 라이선스와 리소스(메모리, GPU)를 확인하세요.

4) 문제 해결
- `pip install` 또는 `llama-cpp-python` 설치 문제 발생 시: 빌드 툴(Windows: Visual Studio Build Tools, 또는 Linux: build-essential, cmake 등)을 설치하세요.
- 도커 실행 실패 시: Docker가 설치되어 있고 권한(Windows의 경우 WSL2 백엔드 설정)이 올바른지 확인하세요.

문의주시면 `docker-compose.yml` 수정(모델 경로, 포트)이나 Docker Desktop 설정을 도와드리겠습니다.

---
자세한 실행 파일은 `docker-compose.yml` 및 각 서비스 `Dockerfile`을 참조하세요.
