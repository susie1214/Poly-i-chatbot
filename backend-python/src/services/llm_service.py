import logging
import re
from typing import Optional, Dict, Any

from src.models.model_manager import get_llm_model

logger = logging.getLogger(__name__)

KEYWORD_RESPONSES: Dict[str, Dict[str, Dict[str, str]]] = {
    "ko": {
        "주차": {
            "title": "주차 정보 안내",
            "content": """## 분당폴리텍 주변 주차 안내
1. 분당구청 주차장(가장 가깝고 저렴)
   - 1시간 무료, 이후 30분당 400원 부과
   - 평일 08:00~19:00 운영
2. 서현역 환승공영주차장
   - 30분 400원, 1시간 1,000원
   - 24시간 운영
3. 황새울공원 주차장
   - 무료 이용 가능(공간 협소)
교내 주차타워는 학과사무실 또는 행정실에 문의해 주세요.
주차장 검색: https://map.kakao.com/?q=%EB%B6%84%EB%8B%B9%ED%8F%B4%EB%A6%AC%ED%85%8D%20%EC%A3%BC%EC%B0%A8%EC%9E%A5"""
        },
        "식당": {
            "title": "식당 안내",
            "content": """## 분당폴리텍 식당 정보 안내
### 교내 시설
- 1층 카페테리아: 도시락 식사 공간(냉장고/전자레인지/정수기/식수대)
### 주변 식당
- 분당우체국/분당세무서/AK플라자 구내식당 등
MAP_EMBED:https://maps.google.com/maps?q=%EC%84%9C%ED%98%84%EC%97%AD%20%EB%A7%9B%EC%A7%91&output=embed
맛집 참고 링크: https://blog.naver.com/hahaha067/224088892518"""
        },
        "식사": {
            "title": "식당 안내",
            "content": """## 분당폴리텍 식당 정보 안내
### 교내 시설
- 1층 카페테리아: 도시락 식사 공간(냉장고/전자레인지/정수기/식수대)
### 주변 식당
- 분당우체국/분당세무서/AK플라자 구내식당 등
MAP_EMBED:https://maps.google.com/maps?q=%EC%84%9C%ED%98%84%EC%97%AD%20%EB%A7%9B%EC%A7%91&output=embed
맛집 참고 링크: https://blog.naver.com/hahaha067/224088892518"""
        },
        "식당주차": {
            "title": "식당/주차장 안내",
            "content": """## 분당폴리텍 식당/주차장 안내
### 식당(교내/주변)
- 1층 카페테리아: 도시락 식사 공간(냉장고/전자레인지/정수기/식수대)
- 주변 식당: 분당우체국/분당세무서/AK플라자 구내식당 등
MAP_EMBED:https://maps.google.com/maps?q=%EC%84%9C%ED%98%84%EC%97%AD%20%EB%A7%9B%EC%A7%91&output=embed
맛집 참고 링크: https://blog.naver.com/hahaha067/224088892518

### 주변 주차장
- 분당구청 주차장: 1시간 무료, 이후 30분당 400원
- 서현역 환승공영주차장: 30분 400원, 1시간 1,000원
- 황새울공원 주차장: 무료(공간 협소)
MAP_EMBED:https://maps.google.com/maps?q=%EB%B6%84%EB%8B%B9%EC%9C%B5%ED%95%A9%EA%B8%B0%EC%88%A0%EA%B5%90%EC%9C%A1%EC%9B%90%20%EC%A3%BC%EC%B0%A8%EC%9E%A5&output=embed
주차장 검색: https://map.kakao.com/?q=%EB%B6%84%EB%8B%B9%ED%8F%B4%EB%A6%AC%ED%85%8D%20%EC%A3%BC%EC%B0%A8%EC%9E%A5"""
        },
        "학과소개": {
            "title": "학과 소개",
            "content": """## 분당융합기술교육원 학과 소개
### 하이테크과정
1. 인공지능소프트웨어과(구 AI금융소프트웨어과)
2. 생명의료시스템과
3. AI응용소프트웨어과

### 신중년 특화과정(집중)
1. AI코딩어시스턴스직종
2. AIoT코딩기초직종
3. 정보시스템감리기초직종

각 과정의 세부 커리큘럼과 모집 요강은 공식 자료를 기준으로 확인해 주세요.
궁금한 점은 교학처(031-696-8803)로 문의해 주세요."""
        },
        "신중년특화안내": {
            "title": "신중년 특화과정(집중) 안내",
            "content": """신중년 특화과정(집중) 학과 안내 해드리겠습니다.
1. AI코딩어시스턴스직종
2. AIoT코딩기초직종
3. 정보시스템감리기초직종
이렇게 구분됩니다."""
        },
        "취업현황": {
            "title": "취업 현황 안내",
            "content": """## 취업 현황 안내
최근 5년(2019-2023) 기준 취업률은 **91.7%**입니다.

### AI금융소프트웨어과 (2024~2016)
- 뱅크웨어글로벌(주)
- ㈜유클릭
- ㈜매커스
- ㈜큐드
- ㈜만들다소프트
- ㈜희남

### AI응용소프트웨어과 (2024~2017)
- (주)인스케이프
- 주식회사퀸타매트릭스
- 하이온넷(주)
- ㈜라온피플
- ㈜APSystems

### 생명의료시스템과 (2024~2016)
- 이지솔루텍
- 에스티젠바이오
- 기초과학연구원

학과별 취업 사례와 상세 통계는 공식 자료를 기준으로 확인해 주세요.
필요한 경우 교학처(031-696-8803)로 문의해 주세요."""
        },
        "입학": {
            "title": "입학/서류 안내",
            "content": """## 입학/서류 안내
- 입학원서 및 자기소개서
- 개인정보 동의서
- 졸업(예정)증명서 등 학력 증빙 서류
세부 제출서류와 자격요건은 모집요강에 따라 달라질 수 있습니다.
정확한 안내는 교학처(031-696-8803)로 문의해 주세요."""
        },
        "교수소개": {
            "title": "교수님 소개 안내",
            "content": """## 교수님 소개
상단 메뉴의 교수님 소개에서 학과별 교수님 정보를 확인할 수 있습니다.
추가 문의는 교학처(031-696-8803)로 연락해 주세요."""
        },
        "인사": {
            "title": "인사",
            "content": "안녕하세요, Poly-i 입니다. 궁금한 점이 있으면 물어보세요."
        },
        "훈련장려금": {
            "title": "훈련장려금 안내",
            "content": """## 훈련장려금 안내
혜택: 교육훈련비 전액 국비지원, 출석률 80% 이상 시 훈련장려금 지급
- 훈련장려금 상세: 일반 1일 3,300원(월 6.6만 한도), 취약계층 1일 10,000원(월 20만 한도), 교통비 1일 2,500원(월 5만 한도)"""
        },
        "비전공자취업현황": {
            "title": "비전공자 취업 현황 안내",
            "content": """## 비전공자 취업 현황 안내
### AI금융소프트웨어과 (2016~2024)
- 2024 행정학과 (비공학/비전공) → ㈜큐드
- 2024 조리외식경영 (비공학/비전공) → ㈜만들다소프트
- 2024 관광경영학과 (비공학/비전공) → ㈜매커스
- 2023 영어학과 (비공학/비전공) → ㈜유클릭
- 2022 불어불문학 (비공학/비전공) → ㈜유클릭
- 2021 연극영화학 (비공학/비전공) → 뱅크웨어글로벌(주)
- 2016 신학 (비공학/비전공) → ㈜희남

### AI응용소프트웨어과 (주요 비전공 사례)
- 2024 경제세무학과 (비공학/비전공) → (주)인스케이프
- 2024 간호학과 (비공학/비전공) → 주식회사퀸타매트릭스
- 2024 체육학과 (비공학/비전공) → 하이온넷(주)
- 2017 국어교육 (비공학/비전공) → ㈜라온피플
- 2017 일본어일본학 (비공학/비전공) → ㈜APSystems

### 생명의료시스템과 (주요 사례)
- 2024 화공신소재 (공학/전공) → 이지솔루텍
- 2024 응용화학 (공학/전공) → 에스티젠바이오
- 2016 제지공학 (공학/전공) → 기초과학연구원"""
        },
        "기업연계": {
            "title": "기업 연계 안내",
            "content": """## 기업 연계 안내
2025학년도 모집요강과 학과별 취업현황(2024~2016) 데이터를 바탕으로, 강력한 기업 연계 시스템을 갖추고 있습니다.
단순한 소개를 넘어 기업 맞춤형 프로젝트와 산학 연계를 통해 실제 취업으로 이어지도록 지원합니다.

### 기업 연계 프로젝트
- 수도권 중견·강소기업과 사전 취업 협약 체결
- 기업 요구 기술을 배우는 맞춤형 프로젝트 과정 운영

### 채용 연계형 공동 개발
- 학생·교수·기업이 함께 참여하는 공동 기술 개발
- 실제 채용으로 연계되는 구조

### 실제 사례
뱅크웨어글로벌, 유클릭, 제니스앤컴퍼니, 삼성바이오로직스 등 협약 기업 또는 동문 기업으로 취업 사례가 있습니다."""
        },
        "비전공자비율": {
            "title": "비전공자 비율 안내",
            "content": """## 비전공자 비율 안내
비전공자의 비율이 상당히 높으며, 인문·사회·예체능 계열 등 다양한 전공자가 참여하고 있습니다.
IT 관련 학과의 경우 과반수 이상이 비전공자인 기수도 많습니다.

### 다양한 전공 분포
2024학년도 취업 현황을 보면 행정학, 조리외식경영, 관광경영, 사회복지학, 국어국문학, 영어영문학, 간호학, 체육학, 패션 전공 등
매우 다양한 비전공자들이 입학하여 교육을 받았습니다.

### 지원 체계
모집 요강에 인문계·비전공자 지원 체계가 명시되어 있으며, 비전공자를 위한 기초 단기 과정을 운영해
전공 탐색 기회와 학습 적응력을 높여줍니다."""
        },
        "비전공자취업가능": {
            "title": "비전공자 취업 가능 여부",
            "content": """## 비전공자도 취업 가능해요
네, 충분히 가능합니다. 실제 데이터를 보면 비전공자들이 교육 수료 후 IT 및 소프트웨어 개발자로 성공적으로 취업하고 있습니다.

### 취업 성공 사례(2024 기준)
- 행정학과 → IT 기업 ㈜큐드, ㈜코어인프라
- 조리외식경영 → 소프트웨어 기업 ㈜만들다소프트
- 간호학과 → 바이오/IT 기업 주식회사퀸타매트릭스
- 체육학과 → 공공기관 전산/체육 분야 진출
- 어문계열(영어, 국어국문 등) → 메리티움(주), ㈜아이플랜비즈 등 IT 기업

### 교육 과정
비전공자 수준에 맞춘 기초 과정(프로그래밍 언어 기초 등)부터 시작해 심화·특화 과정으로 이어지는
단계별 커리큘럼이 있어 개발자로 성장할 수 있습니다."""
        },
        "인공지능소프트웨어과": {
            "title": "인공지능소프트웨어과 안내",
            "content": """인공지능(AI) 기술을 소프트웨어에 접목시키는 실무형 AI 소프트웨어 엔지니어를 양성하는 곳입니다.

한국폴리텍대학 분당융합기술교육원의 인공지능소프트웨어과(구 AI금융소프트웨어과)는
비전공자도 기초부터 심화까지 체계적으로 배워 IT 개발자로 취업할 수 있도록 돕는 국비지원 과정입니다.

## 주요 교육 내용
- 프로그래밍 언어: Java, Python, C언어 등 개발 필수 언어
- 소프트웨어 개발: Web/App 풀스택 개발, 정보시스템 구축 및 운영
- AI 및 빅데이터: 딥러닝, 머신러닝, 빅데이터 분석 및 시각화
- 클라우드 및 인프라: 리눅스, 클라우드 컴퓨팅 환경 구축

## 이런 분들에게 추천해요
- 비전공자이지만 개발자로 커리어를 전환하고 싶은 분
- AI 기술을 활용한 서비스를 만들고 싶은 분
- 10개월 집중 교육으로 포트폴리오와 자격증을 준비하고 싶은 분

## 취업 분야
- AI 응용 소프트웨어 개발자
- 웹/앱 개발자
- 빅데이터 분석 및 플랫폼 엔지니어
- 핀테크 및 금융 IT 전문가

## 지원 혜택
- 교육비, 교재비, 실습비 전액 무료
- 매월 훈련수당 및 교통비 지급
- 수료 후 우수 기업 취업 알선 및 사후 관리"""
        },
        "인공지능소프트웨어학과설명": {
            "title": "인공지능소프트웨어학과 설명",
            "content": """## 인공지능소프트웨어학과 특징
1. 빅데이터 분석, AI 응용, 정보시스템 구축·운영, 데이터베이스 설계 등 소프트웨어 개발자 양성을 목표로 합니다.
2. 10~20년 이상 현장 경험이 풍부한 전임 교수진이 지도합니다.
3. 최신 워크스테이션 구축 등 최신 교육 환경을 제공합니다.
4. 우수 기업과의 산학협력(MOU) 체결 및 추가 진행 중입니다.
5. 정원 20명 내외 소수정예 클래스로 운영됩니다.
6. 교육비 전액 정부지원(+교통비, 중식비, 교육수당 지급)."""
        },
        "위치": {
            "title": "위치 안내",
            "content": """한국폴리텍대학 분당융합기술교육원
길찾기
전화
031-696-8800
주소
황새울로329번길 5 한국폴리텍대학 융합기술교육원
지번
서현동 272-6"""
        },
        "교육비": {
            "title": "교육비 안내",
            "content": """## 교육비 안내
교육비는 전액 무료(국비 지원)입니다. 매월 훈련수당을 받으면서 다닐 수 있습니다.

### 전액 국비 지원
- 교육훈련비, 실습비, 교재비 전액 지원
- 원서 접수비 및 면접 전형료도 무료

### 훈련장려금(출석률 80% 이상)
- 일반 훈련생: 월 최대 11만 6천 원
- 취약계층: 월 최대 25만 원"""
        },
    },
    "en": {
        "parking": {
            "title": "Parking Information",
            "content": """## Parking
- Bundang District Office Parking: 1 hour free, 400 KRW / 30 min
- Seohyeon Station Transfer Parking: 1,000 KRW / hour, open 24/7
Map: https://map.kakao.com/?q=Bundang+Polytechnic+Parking"""
        },
        "lunch": {
            "title": "Dining Information",
            "content": """## Dining
- 1F Cafeteria: space for packed lunches (microwave/water available)
- Nearby dining options around Seohyeon Station
Map: https://map.kakao.com/?q=Seohyeon+Station+Food"""
        },
        "greeting": {
            "title": "Greeting",
            "content": "Hello, I'm Poly-i. How can I help you?"
        },
        "location": {
            "title": "Location",
            "content": """Bundang Polytechnic College (융합기술교육원)
Phone
031-696-8800
Address
5 Hwangsaeul-ro 329beon-gil, Bundang-gu, Seongnam-si
Lot number
272-6, Seohyeon-dong"""
        },
        "departments": {
            "title": "Departments",
            "content": """## Hi-Tech Programs
1. AI Software (formerly AI Finance Software)
2. Biomedical Systems
3. AI Application Software

## Senior Programs (Intensive)
1. AI Coding Assistance
2. AIoT Coding Basics
3. IT Audit Basics"""
        },
        "employment": {
            "title": "Employment Overview",
            "content": """Recent 5-year employment rate (2019-2023): 91.7%.
Department employment examples are available on request."""
        },
        "tuition": {
            "title": "Tuition",
            "content": "Tuition is fully government-funded. You may also receive monthly training allowances."
        }
    },
}

KO_KEYWORD_MAP = {
    "비전공자 취업현황": "비전공자취업현황",
    "비전공 취업현황": "비전공자취업현황",
    "비전공자 취업": "비전공자취업현황",
    "비전공 취업": "비전공자취업현황",
    "비전공자": "비전공자취업현황",
    "비전공": "비전공자취업현황",
    "안녕": "인사",
    "안녕하세요": "인사",
    "반가워": "인사",
    "기업연계": "기업연계",
    "기업 연계": "기업연계",
    "기업연계해주니": "기업연계",
    "기업 연계해주니": "기업연계",
    "연계": "기업연계",
    "비전공자 비율": "비전공자비율",
    "비전공 비율": "비전공자비율",
    "비전공자 비율 어떻게": "비전공자비율",
    "비전공자 비율 어떻게 돼": "비전공자비율",
    "비전공자도 취업 가능": "비전공자취업가능",
    "비전공자 취업 가능": "비전공자취업가능",
    "비전공자도 취업": "비전공자취업가능",
    "비전공 취업 가능": "비전공자취업가능",
    "교육비": "교육비",
    "교육비가 얼마": "교육비",
    "교육비 얼마": "교육비",
    "인공지능소프트웨어과": "인공지능소프트웨어과",
    "인공지능 소프트웨어과": "인공지능소프트웨어과",
    "AI소프트웨어과": "인공지능소프트웨어과",
    "AI 소프트웨어과": "인공지능소프트웨어과",
    "인공지능소프트웨어과가 뭐": "인공지능소프트웨어과",
    "인공지능소프트웨어과가 뭐 가르치는": "인공지능소프트웨어과",
    "인공지능소프트웨어학과": "인공지능소프트웨어학과설명",
    "인공지능소프트웨어학과 설명": "인공지능소프트웨어학과설명",
    "식당/주차장": "식당주차",
    "주차/식당": "식당주차",
    "주차": "주차",
    "주차 안내": "주차",
    "식사": "식사",
    "식당": "식사",
    "점심": "식사",
    "학과소개": "학과소개",
    "학과 소개": "학과소개",
    "학과": "학과소개",
    "취업현황": "취업현황",
    "취업 현황": "취업현황",
    "취업률": "취업현황",
    "훈련장려금": "훈련장려금",
    "훈련수당": "훈련장려금",
    "교통비": "훈련장려금",
    "위치": "위치",
    "오시는 길": "위치",
    "주소": "위치",
    "하이테크": "학과소개",
    "하이테크과정": "학과소개",
    "교수": "교수소개",
    "교수님": "교수소개",
    "교수님 소개": "교수소개",
    "서류": "입학",
    "입학": "입학",
    "입학정보": "입학",
    "서류/입학정보": "입학",
    "신중년 특화과정": "신중년특화안내",
    "신중년특화과정": "신중년특화안내",
    "신중년 특화": "신중년특화안내",
    "신중년": "신중년특화안내",
}

EN_KEYWORD_MAP = {
    "hello": "greeting",
    "hi": "greeting",
    "hey": "greeting",
    "parking": "parking",
    "car": "parking",
    "lunch": "lunch",
    "food": "lunch",
    "dining": "lunch",
    "allowance": "tuition",
    "support": "tuition",
    "transport": "tuition",
    "tuition": "tuition",
    "fee": "tuition",
    "location": "location",
    "address": "location",
    "department": "departments",
    "departments": "departments",
    "employment": "employment",
}


def get_keyword_response(prompt: str, language: str = "ko") -> Optional[Dict[str, Any]]:
    """간단 키워드 매칭 응답."""
    prompt_lower = prompt.lower()
    prompt_clean = re.sub(r"[^0-9A-Za-z\u3131-\u318E\uAC00-\uD7A3\s]", "", prompt_lower).strip()
    responses = KEYWORD_RESPONSES.get(language, KEYWORD_RESPONSES["ko"])

    if language == "ko":
        keyword_map = KO_KEYWORD_MAP
    else:
        keyword_map = EN_KEYWORD_MAP

    if language == "ko" and prompt_clean in {"안녕", "안녕하세요", "반가워"}:
        resp = responses.get("인사")
        if resp:
            return {
                "response": resp["content"],
                "tokens_used": 0,
                "model": "KEYWORD_MATCHER",
                "language": language,
                "source": "keyword",
                "title": resp.get("title", ""),
            }

    if language != "ko" and prompt_clean in {"hello", "hi", "hey"}:
        resp = responses.get("greeting")
        if resp:
            return {
                "response": resp["content"],
                "tokens_used": 0,
                "model": "KEYWORD_MATCHER",
                "language": language,
                "source": "keyword",
                "title": resp.get("title", ""),
            }

    for keyword, response_key in keyword_map.items():
        if (keyword in prompt_lower or keyword in prompt_clean) and response_key in responses:
            resp = responses[response_key]
            return {
                "response": resp["content"],
                "tokens_used": 0,
                "model": "KEYWORD_MATCHER",
                "language": language,
                "source": "keyword",
                "title": resp.get("title", ""),
            }
    return None


def _build_system_prompt(language: str) -> str:
    if language == "ko":
        return (
            "당신은 분당융합기술교육원의 AI 상담원입니다. 제공된 자료를 바탕으로 답변하세요. "
            "모르는 내용은 지어내지 말고, 필요한 경우 교학처(031-696-8803)로 문의하도록 안내하세요. "
            "숫자/조건/기간은 명확히 쓰고, 간결한 Markdown 형식을 사용하세요."
        )
    return (
        "You are an AI counselor for a university career center. Answer using the provided data only. "
        "Do not fabricate; if unsure, advise contacting the admin office (031-696-8803). "
        "Use Markdown and keep answers concise with clear numbers."
    )


def generate_response(
    prompt: str,
    user_id: str = "default",
    max_tokens: int = 256,
    temperature: float = 0.7,
    language: str = "ko",
) -> Dict[str, Any]:
    """LLM 기반 응답 (키워드 우선, 없으면 LLM)."""
    try:
        keyword_resp = get_keyword_response(prompt, language)
        if keyword_resp:
            keyword_resp["user_id"] = user_id
            return keyword_resp

        model = get_llm_model()
        if not model:
            msg = "모델 로딩 중입니다. 잠시 후 다시 시도해 주세요." if language == "ko" else "Model is loading. Please try again."
            return {
                "response": msg,
                "tokens_used": 0,
                "model": "LLM",
                "user_id": user_id,
                "language": language,
                "error": "model_not_loaded",
            }

        system_prompt = _build_system_prompt(language)
        prefix = "사용자: " if language == "ko" else "User: "
        suffix = "\n답변:" if language == "ko" else "\nResponse:"
        full_prompt = f"{system_prompt}\n\n{prefix}{prompt}{suffix}"

        output = model(
            full_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=0.95,
            top_k=50,
            repeat_penalty=1.1,
            echo=False,
        )

        response_text = output["choices"][0]["text"].strip()
        tokens_used = output.get("usage", {}).get("completion_tokens", 0)

        return {
            "response": response_text,
            "tokens_used": tokens_used,
            "model": "LLM",
            "user_id": user_id,
            "language": language,
            "source": "llm",
        }

    except Exception as e:
        logger.error(f"LLM Generation Error: {e}")
        error_msg = f"오류가 발생했습니다: {e}" if language == "ko" else f"Error occurred: {e}"
        return {
            "response": error_msg,
            "tokens_used": 0,
            "model": "LLM",
            "user_id": user_id,
            "language": language,
            "error": str(e),
        }


def create_system_prompt(intent: str = "general") -> str:
    prompts = {
        "general": "질문에 간단하고 명확하게 답변하세요.",
        "inquiry": "문의 응답: 필요한 정보와 근거, 연락처(031-696-8803)를 안내하세요.",
        "complaint": "민원 응답: 공감하고 해결 절차와 담당 부서를 안내하세요.",
        "feedback": "피드백 수집: 개선 의견을 경청하고 기록하세요.",
    }
    return prompts.get(intent, prompts["general"])
