import React, { useState, useEffect, useRef } from 'react';
import { FiSend, FiMic } from 'react-icons/fi';
import useChatStore from '@/store/chatStore';
import ChatMessage from './ChatMessage';
import ChatHeader from './ChatHeader';

const PROMPTS = {
  ko: {
    welcome: "안녕하세요! 저는 **Poly-i**입니다.",
    subtitle: "분당폴리텍 교육과정에 대해 궁금한 점을 물어봐주세요!",
    placeholder: "메시지를 입력하세요...",
    error: "죄송합니다. 오류가 발생했습니다.",
    systemPrompt: `당신은 분당폴리텍 교육과정을 안내하는 친절한 챗봇 Poly-i입니다.

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
- 모르는 정보는 행정실 문의 안내`
  },
  en: {
    welcome: "Hello! I'm **Poly-i**.",
    subtitle: "Ask me about Bundang Polytechnic's programs!",
    placeholder: "Type a message...",
    error: "Sorry, an error occurred.",
    systemPrompt: `You are Poly-i, a friendly chatbot for Bundang Polytechnic education programs.

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
- Refer to administration office for unknown details`
  }
};

export default function ChatContainer() {
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const messagesEndRef = useRef(null);
  const recognitionRef = useRef(null);
  
  const { messages, addMessage, language, setLanguage } = useChatStore();

  // STT 초기화
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = language === 'ko' ? 'ko-KR' : 'en-US';
      
      recognitionRef.current.onresult = (event) => {
        const transcript = Array.from(event.results)
          .map(result => result[0].transcript)
          .join('');
        setInputValue(transcript);
        setIsListening(false);
      };

      recognitionRef.current.onerror = () => {
        setIsListening(false);
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
      };
    }
  }, [language]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputValue.trim()) return;

    // 사용자 메시지 추가
    addMessage({
      id: Date.now(),
      type: 'user',
      text: inputValue,
      timestamp: new Date().toISOString(),
    });

    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: inputValue,
          language: language 
        }),
      });

      const data = await response.json();
      
      addMessage({
        id: Date.now() + 1,
        type: 'assistant',
        text: data.reply,
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      console.error('Chat error:', error);
      addMessage({
        id: Date.now() + 1,
        type: 'assistant',
        text: PROMPTS[language].error,
        timestamp: new Date().toISOString(),
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleMicClick = () => {
    if (!recognitionRef.current) {
      alert('STT not supported in your browser');
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      recognitionRef.current.start();
      setIsListening(true);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white">
      {/* 헤더 + 언어 선택 */}
      <div className="flex items-center justify-between">
        <ChatHeader />
        <div className="pr-4 flex gap-2">
          <button
            onClick={() => setLanguage('ko')}
            className={`px-3 py-1 rounded text-sm ${
              language === 'ko'
                ? 'bg-poly-blue text-white'
                : 'bg-gray-200 text-gray-700'
            }`}
          >
            한글
          </button>
          <button
            onClick={() => setLanguage('en')}
            className={`px-3 py-1 rounded text-sm ${
              language === 'en'
                ? 'bg-poly-blue text-white'
                : 'bg-gray-200 text-gray-700'
            }`}
          >
            ENG
          </button>
        </div>
      </div>

      {/* 메시지 영역 */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center overflow-y-auto">
            <div className="text-5xl mb-3">💬</div>
            <h2 className="text-xl font-bold text-gray-800">{PROMPTS[language].welcome}</h2>
            <p className="text-gray-500 mt-2 text-sm mb-6">{PROMPTS[language].subtitle}</p>
            
            {/* 안내 메뉴 */}
            <div className="w-full max-w-sm bg-white rounded-lg shadow-md p-4 text-left space-y-2">
              {language === 'ko' ? (
                <>
                  <p className="text-sm font-bold text-poly-blue mb-3">📋 궁금한 것을 선택하세요:</p>
                  <button className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 rounded text-sm transition">
                    💼 국민취업지원제도 / 훈련수당, 교통비 지급
                  </button>
                  <button className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 rounded text-sm transition">
                    👤 지원자격 (연령, 학력, 경력)
                  </button>
                  <button className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 rounded text-sm transition">
                    🚀 조기취업 / 기숙사 / 교재
                  </button>
                  <button className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 rounded text-sm transition">
                    🍽️ 점심시간 / 방학기간
                  </button>
                </>
              ) : (
                <>
                  <p className="text-sm font-bold text-poly-blue mb-3">📋 What would you like to know?</p>
                  <button className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 rounded text-sm transition">
                    💼 National Employment Support / Allowance
                  </button>
                  <button className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 rounded text-sm transition">
                    👤 Eligibility Requirements
                  </button>
                  <button className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 rounded text-sm transition">
                    🚀 Early Employment / Facilities
                  </button>
                  <button className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 rounded text-sm transition">
                    🍽️ Lunch Time / Holidays
                  </button>
                </>
              )}
            </div>
          </div>
        ) : (
          <>
            {messages.map((msg) => (
              <ChatMessage key={msg.id} message={msg} />
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-poly-blue text-white rounded-2xl rounded-bl-none px-4 py-2">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-white rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* 입력 영역 */}
      <form onSubmit={handleSendMessage} className="border-t border-gray-200 bg-white p-3">
        <div className="flex gap-2 items-end">
          <button
            type="button"
            onClick={handleMicClick}
            className={`p-2 rounded-full transition ${
              isListening
                ? 'bg-red-500 text-white'
                : 'hover:bg-poly-blue-light text-poly-blue'
            }`}
          >
            <FiMic className="w-5 h-5" />
          </button>

          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder={PROMPTS[language].placeholder}
            className="flex-1 border border-gray-300 rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-poly-blue focus:border-transparent text-sm"
          />

          <button
            type="submit"
            disabled={!inputValue.trim() || isLoading}
            className="p-2 bg-poly-blue hover:bg-poly-blue-dark text-white rounded-full disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            <FiSend className="w-5 h-5" />
          </button>
        </div>
      </form>
    </div>
  );
}
