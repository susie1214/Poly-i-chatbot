import logging
from src.models.model_manager import get_llm_model

logger = logging.getLogger(__name__)

# 키워드 기반 응답 (모델이 로드되지 않았을 때 사용)
KEYWORD_RESPONSES = {
    'ko': {
        '주차': {
            'title': '🚗 주차장 안내',
            'content': """## 분당폴리텍융합기술교육원 주차 안내

### 주변 주차장 옵션
1. **분당구청 주차장**
   - 1시간 무료, 초과 시 30분당 400원
   - 평일 8시~19시 운영

2. **서현역 환승공영주차장**
   - 30분 400원, 1시간 1,000원
   - 24시간 운영

3. **호텔스카이파크 센트럴서울판교**
   - 평일 4,900원, 휴일 4,400원
   - 월 정기권 17만원

4. **황새울공원 주차장**
   - 새벽 5시 도착 시 주차 가능
   - 주소: 경기 성남시 분당구 황새울로 287

**분당폴리텍 위치**: 경기 성남시 분당구 서현동
**가장 가까운 주차**: 분당구청 주차장 (1시간 무료)"""
        },
        '식사': {
            'title': '🍽️ 식사 정보',
            'content': """## 분당폴리텍융합기술교육원 식사 안내

### 학내 구내식당
- **분당우체국 구내식당**: 6,500원
- **분당세무서**: 6,500원
- **AK 구내식당**: 6,000원

### 근처 음식점
- 일반 밥집: 약 12,000원 (점심)
- 편의점: 3,000~5,000원

### 학교 시설
- 1층: 도시락 섭취 공간 운영
- 냉장고, 전자렌지, 정수기 제공

**점심시간**: 12:00~13:00 (±30분 조정 가능)"""
        },
        '수당': {
            'title': '💰 훈련수당 및 교통비 안내',
            'content': """## 국민취업지원제도 지원금

### 훈련수당
- **일반**: 1일 3,300원 (월 6만6천원 한도)
- **취약계층**: 1일 1만원 (월 20만원 한도)

### 교통비
- **지원액**: 1일 2,500원 (월 5만원 한도)

### 지급 조건
- 출석률 80% 이상 (월 단위)
- 지급 시기: 다음달 중순경
- 계좌: 개인 예금 통장으로 입금

### 지원 대상
- 만 39세 이하
- 2년제 대학 이상 졸업(예정)자
- 4년제 대학 2년 이상 수료자
- 동일/유사 계열 2년 이상 실무 종사자"""
        },
        '위치': {
            'title': '📍 분당폴리텍융합기술교육원 위치',
            'content': """## 분당폴리텍융합기술교육원 안내

### 정확한 위치
- **주소**: 경기 성남시 분당구 서현동
- **전화**: 031-696-8803
- **대중교통**: 서현역 인근

### 건물 안내
- **2층**: 도서관, 행정실
- **1층**: 강의실, 도시락 섭취 공간
- **편의시설**: 냉장고, 전자렌지, 정수기

### 교통 안내
- 서현역 2번 출구 도보 15분
- 주변 주차장: 분당구청, 서현역 환승 주차장"""
        },
    },
    'en': {
        'parking': {
            'title': '🚗 Parking Guide',
            'content': """## Bundang Polytechnic Parking Information

### Nearby Parking Options
1. **Bundang District Office Parking**
   - 1 hour free, 400 won per 30 min after
   - Weekdays 8 AM - 7 PM

2. **Seohyeon Station Transfer Parking**
   - 400 won per 30 min, 1,000 won per hour
   - Open 24 hours

3. **Hotel Skypark Central Seoul Pangyo**
   - 4,900 won (weekday), 4,400 won (weekend)
   - Monthly pass: 170,000 won

4. **Hwangsaeul Park Parking**
   - Arrive at 5 AM for guaranteed spot
   - Address: 287, Hwangsaeul-ro, Bundang-gu

**Location**: Seohyeon-dong, Bundang-gu, Seongnam-si, Gyeonggi-do"""
        },
        'lunch': {
            'title': '🍽️ Dining Information',
            'content': """## Bundang Polytechnic Dining Options

### On-Campus Cafeterias
- Bundang Post Office: 6,500 won
- Tax Office: 6,500 won
- AK Cafeteria: 6,000 won

### Nearby Restaurants
- General restaurants: ~12,000 won (lunch)
- Convenience stores: 3,000-5,000 won

### School Facilities
- Floor 1: Lunch area available
- Amenities: Refrigerator, microwave, water purifier

**Lunch Time**: 12:00 PM - 1:00 PM (±30 min flexible)"""
        },
        'allowance': {
            'title': '💰 Training Allowance Information',
            'content': """## National Employment Support Program Benefits

### Training Allowance
- **General**: 3,300 won/day (Max 66,000 won/month)
- **Low-income**: 10,000 won/day (Max 200,000 won/month)

### Transportation
- **Allowance**: 2,500 won/day (Max 50,000 won/month)

### Payment Terms
- Requirement: 80% or higher monthly attendance
- Payment: Mid-next month to personal account
- Unit: Monthly

### Eligibility
- Age 39 or under
- 2-year university graduate or expected
- 4-year university with 2+ years coursework
- 2+ years practical experience in related field"""
        },
    }
}

def get_keyword_response(prompt: str, language: str = 'ko') -> dict:
    """키워드 기반 응답 검색"""
    prompt_lower = prompt.lower()
    responses = KEYWORD_RESPONSES.get(language, KEYWORD_RESPONSES['ko'])
    
    # 한국어 키워드 매핑
    if language == 'ko':
        keyword_map = {
            '주차': '주차',
            '식사': '식사',
            '수당': '수당',
            '위치': '위치',
            '점심': '식사',
            '밥': '식사',
            '주소': '위치',
            '가는길': '위치',
            '교통': '위치',
            '훈련수당': '수당',
            '교통비': '수당',
            'allowance': '수당',
        }
        
        for keyword, response_key in keyword_map.items():
            if keyword in prompt_lower:
                if response_key in responses:
                    return {
                        'response': responses[response_key]['content'],
                        'tokens_used': 0,
                        'model': 'KEYWORD_MATCHER',
                        'language': language,
                        'source': 'keyword'
                    }
    else:
        # 영어 키워드 매핑
        keyword_map = {
            'parking': 'parking',
            'lunch': 'lunch',
            'dining': 'lunch',
            'restaurant': 'lunch',
            'allowance': 'allowance',
            'food': 'lunch',
            'location': 'parking',
            'address': 'parking',
        }
        
        for keyword, response_key in keyword_map.items():
            if keyword in prompt_lower:
                if response_key in responses:
                    return {
                        'response': responses[response_key]['content'],
                        'tokens_used': 0,
                        'model': 'KEYWORD_MATCHER',
                        'language': language,
                        'source': 'keyword'
                    }
    
    return None

def generate_response(prompt: str, user_id: str = "default", max_tokens: int = 256, temperature: float = 0.7, language: str = "ko"):
    """
    SOLAR-7B 모델로 텍스트 생성 (한국어/영어 지원)
    
    Args:
        prompt: 입력 프롬프트
        user_id: 사용자 ID
        max_tokens: 최대 토큰 수
        temperature: 생성 온도 (0.0 ~ 1.0)
        language: 언어 ('ko' 또는 'en')
    
    Returns:
        dict: 생성된 응답과 메타데이터
    """
    
    try:
        # 1. 먼저 키워드 기반 응답 확인
        keyword_response = get_keyword_response(prompt, language)
        if keyword_response:
            return keyword_response
        
        # 2. LLM 모델로 응답 생성
        model = get_llm_model()
        
        if not model:
            # 모델이 로드되지 않은 경우 기본 응답 반환
            logger.warning("LLM model not loaded, using fallback response")
            fallback_msg = "죄송합니다. 모델 로드 중입니다. 다시 시도해주세요." if language == "ko" else "Sorry, model is loading. Please try again."
            return {
                'response': fallback_msg,
                'tokens_used': 0,
                'model': 'SOLAR-7B',
                'user_id': user_id,
                'language': language,
                'error': 'model_not_loaded'
            }
        
        # 언어에 따른 시스템 프롬프트
        if language == "ko":
            system_prompt = """당신은 분당폴리텍 교육과정을 안내하는 친절한 챗봇 Poly-i입니다.

## 📍 분당폴리텍 프로그램 정보

### 💼 국민취업지원제도 (O)
- **훈련수당**: 1일 3,300원 (월 6만6천원 한도)
- **취약계층 훈련수당**: 1일 1만원 (월 20만원 한도)
- **교통비**: 1일 2,500원 (월 5만원 한도)
- **지급조건**: 단위기간 1개월 동안 출석률 80% 이상
- **지급시기**: 다음달 중순경 개인계좌로 입금

### 👤 지원자격
다음 중 하나에 해당해야 함:
1. **만 39세 이하**인 자
2. **2년제 대학 이상 졸업 (예정)자**
3. **4년제 대학 2년 이상 수료자**
4. **이와 동등 수준의 학력** (학점은행제 등)
5. **동일 및 유사 계열 2년 이상 실무 종사자**

### 🎯 교육 특징
- ✅ **조기취업 가능** - 교육 중에 취업하면 조기 수료 가능
- ❌ **기숙사 미운영** - 통학 또는 자체 숙소 필요
- 📚 **교재 및 강사료 제공** - 교수님이 제공

### 🏢 시설 안내
- **2층**: 도서관 + 행정실
- **1층**: 도시락 섭취 공간 (구내 식당 없음)
- **편의시설**: 냉장고, 전자렌지, 정수기

### ⏰ 시간표 및 방학
- **수업 시작 시간**: 오전 9시
- **점심시간**: 12:00~13:00 (±30분 조정 가능)
- **출석 확인**: 교수님이 직접 체크
- **방학기간**: 연 2회 (상세일정은 교육과정별로 상이)

## 🚗 주차장 안내

### 분당구청 주차장
- **1시간**: 무료
- **1시간 초과**: 30분당 400원
- **3시간**: 3,100원
- **운영시간**: 평일 8시~19시
- **주말**: 무료 (오전 만차 가능)

### 서현역 환승공영주차장
- **30분**: 400원
- **1시간**: 1,000원
- **1시간 초과**: 1시간 기준 1,200원씩 추가

### 호텔스카이파크 센트럴서울판교
- **주만사 할인권**: 평일 4,900원, 휴일 4,400원
- **월 정기권**: 17만원 (주만사 15% 할인 시 약 14.5만원)
- **위치**: 경기 성남시 분당구 서현동 261-1

### 황새울공원 주차장
- **주소**: 경기 성남시 분당구 황새울로 287
- **팁**: 새벽 5시에 도착하면 주차 가능

## 🍽️ 점심 식사 정보

### 학내 구내식당
- **분당우체국 구내식당**: 6,500원
- **분당세무서**: 6,500원
- **AK 구내식당**: 6,000원

### 근처 음식점
- **일반 밥집**: 약 12,000원 (점심 기준)

### 학교 내 편의시설
- 1층에서 도시락 섭취 가능
- 냉장고, 전자렌지, 정수기 제공

## 대답 방식
- 사용자의 질문에 정확하고 친절하게 답변
- 마크다운 형식으로 정보를 정리
- 구체적인 금액과 조건을 명시
- 모르는 정보는 행정실 문의 안내"""
            prefix = "사용자: "
            suffix = "\n답변:"
        else:
            system_prompt = """You are Poly-i, a friendly chatbot for Bundang Polytechnic education programs.

## 📍 Bundang Polytechnic Program Information

### 💼 National Employment Support Program (YES)
- **Training Allowance**: 3,300 won/day (Max 66,000 won/month)
- **Low-income Allowance**: 10,000 won/day (Max 200,000 won/month)
- **Transportation**: 2,500 won/day (Max 50,000 won/month)
- **Requirement**: 80% or higher monthly attendance
- **Payment**: Mid-next month to personal account

### 👤 Eligibility Requirements
One of the following:
1. **Age 39 or under**
2. **2-year university graduate or expected graduate**
3. **4-year university with 2+ years of coursework**
4. **Equivalent education level** (Credit Bank System, etc.)
5. **2+ years of practical experience in related field**

### 🎯 Program Features
- ✅ **Early Employment Possible** - Can graduate early if employed
- ❌ **No Dormitory** - Commute or self-arranged housing
- 📚 **Materials & Instruction Provided**

### 🏢 Facilities
- **Floor 2**: Library + Administration Office
- **Floor 1**: Lunch Area (No cafeteria)
- **Amenities**: Refrigerator, Microwave, Water purifier

### ⏰ Schedule & Holidays
- **Class Start**: 9:00 AM
- **Lunch Time**: 12:00~13:00 (±30 min flexible)
- **Attendance**: Instructor verification
- **Breaks**: 2 breaks per year (varies by program)

## 🚗 Parking Information

### Bundang District Office Parking
- **1 hour**: Free
- **Over 1 hour**: 400 won per 30 min
- **3 hours**: 3,100 won
- **Weekdays**: 8 AM - 7 PM
- **Weekends**: Free (May be full in the morning)

### Seohyeon Station Transfer Parking
- **30 min**: 400 won
- **1 hour**: 1,000 won
- **Over 1 hour**: 1,200 won per hour

### Hotel Skypark Central Seoul Pangyo
- **Discount Ticket**: 4,900 won (weekday), 4,400 won (weekend)
- **Monthly Pass**: 170,000 won (15% discount with Jumansa)
- **Location**: 261-1, Seohyeon-dong, Bundang-gu, Seongnam-si, Gyeonggi-do

### Hwangsaeul Park Parking
- **Address**: 287, Hwangsaeul-ro, Bundang-gu, Seongnam-si
- **Tip**: Arrive at 5 AM for guaranteed parking

## 🍽️ Lunch Options

### On-Campus Dining
- **Bundang Post Office Cafeteria**: 6,500 won
- **Tax Office**: 6,500 won
- **AK Cafeteria**: 6,000 won

### Nearby Restaurants
- **Local Restaurants**: About 12,000 won (lunch)

### School Facilities
- Lunch area available on 1st floor
- Refrigerator, microwave, water purifier provided

## Response Style
- Accurate and helpful answers
- Use markdown format
- Specify exact amounts and conditions
- Refer to administration office for unknown details"""
            prefix = "User: "
            suffix = "\nResponse:"
        
        full_prompt = f"{system_prompt}\n\n{prefix}{prompt}{suffix}"
        
        # 모델 실행
        output = model(
            full_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=0.95,
            top_k=50,
            repeat_penalty=1.1,
            echo=False
        )
        
        response_text = output['choices'][0]['text'].strip()
        tokens_used = output['usage']['completion_tokens']
        
        return {
            'response': response_text,
            'tokens_used': tokens_used,
            'model': 'SOLAR-7B',
            'user_id': user_id,
            'language': language
        }
        
    except Exception as e:
        logger.error(f"LLM Generation Error: {str(e)}")
        error_msg = f"오류가 발생했습니다: {str(e)}" if language == "ko" else f"Error occurred: {str(e)}"
        return {
            'response': error_msg,
            'tokens_used': 0,
            'model': 'SOLAR-7B',
            'user_id': user_id,
            'language': language,
            'error': str(e)
        }

def create_system_prompt(intent: str = "general"):
    """
    의도별 시스템 프롬프트 생성
    
    Args:
        intent: 사용자 의도 (general, inquiry, complaint, feedback 등)
    
    Returns:
        str: 시스템 프롬프트
    """
    
    prompts = {
        "general": """당신은 Poly-i라는 친절한 상담 챗봇입니다.
- 사용자의 질문에 정확하고 도움이 되는 답변을 제공하세요.
- 명확하고 간결한 언어를 사용하세요.
- 모르는 것은 솔직하게 인정하세요.""",
        
        "inquiry": """당신은 제품/서비스 문의를 담당하는 상담원입니다.
- 사용자의 질문에 구체적인 정보를 제공하세요.
- 필요하면 추가 정보 수집을 위해 명확한 질문을 하세요.
- 친절하고 전문적인 태도를 유지하세요.""",
        
        "complaint": """당신은 민원 처리 담당자입니다.
- 사용자의 불만을 공감하는 태도로 경청하세요.
- 문제를 이해하려고 노력하세요.
- 해결 방안을 적극적으로 제시하세요.
- 상황에 따라 인간 담당자로의 전환을 제안하세요.""",
        
        "feedback": """당신은 피드백을 수집하는 담당자입니다.
- 사용자의 의견을 개방적으로 받아들이세요.
- 명확한 피드백을 수집하세요.
- 감사의 마음을 표현하세요.""",
    }
    
    return prompts.get(intent, prompts["general"])
