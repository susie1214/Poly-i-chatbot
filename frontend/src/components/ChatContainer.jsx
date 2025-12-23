import React, { useEffect, useRef, useState } from 'react';
import { FiMic, FiSend } from 'react-icons/fi';
import useChatStore from '@/store/chatStore';
import ChatMessage from './ChatMessage';
import WaveBanner from './WaveBanner';
import ProfessorIntro from './ProfessorIntro';

const PROMPTS = {
  ko: {
    welcome: '안녕하세요, Poly-i 입니다!',
    subtitle: '분당폴리텍(융합기술교육원) 학과/취업/생활 정보를 물어보세요.',
    phone: '☎ 031-696-8803',
    placeholder: '메시지를 입력하세요...',
    error: '죄송합니다, 오류가 발생했습니다.',
    closing: {
      title: '마무리 인사',
      lines: [
        '"성공은 준비와 기회가 만나는 지점에 있다." — 보비 언저 (Bobby Unser)',
        '"우리가 하는 일은 바다에 떨어진 한 방울이지만, 그 한 방울이 없으면 바다는 그만큼 줄어요." — 마더 테레사 (Mother Teresa)',
        '"작은 시작이 위대한 결과를 만든다." — 크리스토퍼 리브 (Christopher Reeve)',
        '분당폴리텍융합기술교육원은 여러분의 도전을 멈추지 않게 하는 든든한 엔진이에요.',
        '취업률 91.7%의 전설은 작은 실천과 포기하지 않는 마음에서 시작됐습니다.',
        '오늘 만든 챗봇이 청년 구직자에게는 희망의 길잡이, 신중년 교육생에게는 인생 2막의 개막 신호탄이 되길 응원합니다.',
        '준비가 되셨나요? 이제 세상에 여러분의 결과물을 보여줄 시간이에요!',
      ],
      highlight: '91.7%',
    },
  },
  en: {
    welcome: "Hello! I'm Poly-i.",
    subtitle: "Ask me about Bundang Polytechnic's programs and campus info.",
    phone: '☎ 031-696-8803',
    placeholder: 'Type a message...',
    error: 'Sorry, an error occurred.',
    closing: {
      title: 'Closing Note',
      lines: [
        '"Success is where preparation and opportunity meet." — Bobby Unser',
        '"What we do is a drop in the ocean. But without it, the ocean would be less." — Mother Teresa',
        '"Starting small is the only way to do great things." — Christopher Reeve',
        'Bundang Polytechnic is the engine that keeps your challenge moving forward. The 91.7% employment legend begins with meticulous technical effort and a never-give-up mindset.',
        'May this chatbot guide young job seekers to hope and help mature learners open a brilliant second act.',
        'Are you ready? It is time to show your results to the world!',
      ],
      highlight: '91.7%',
    },
  },
};

export default function ChatContainer() {
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [view, setView] = useState('home');
  const [showClosing, setShowClosing] = useState(false);
  const messagesEndRef = useRef(null);
  const recognitionRef = useRef(null);
  const closingTimerRef = useRef(null);
  const greetingTimerRef = useRef(null);
  const greetedRef = useRef(false);

  const { messages, addMessage, language } = useChatStore();

  // STT 설정
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = language === 'ko' ? 'ko-KR' : 'en-US';

      recognitionRef.current.onresult = (event) => {
        const transcript = Array.from(event.results)
          .map((result) => result[0].transcript)
          .join('');
        setInputValue(transcript);
        setIsListening(false);
      };

      recognitionRef.current.onerror = () => setIsListening(false);
      recognitionRef.current.onend = () => setIsListening(false);
    }
  }, [language]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (messages.length > 0 && view !== 'chat') {
      setView('chat');
    }
    if (messages.length === 0 && view === 'chat') {
      setView('home');
    }
  }, [messages.length, view]);

  useEffect(() => {
    if (greetingTimerRef.current) {
      clearTimeout(greetingTimerRef.current);
      greetingTimerRef.current = null;
    }

    if (messages.length === 0 && view === 'home') {
      greetedRef.current = false;
      greetingTimerRef.current = setTimeout(() => {
        if (messages.length === 0 && view === 'home' && !greetedRef.current) {
          greetedRef.current = true;
          addMessage({
            id: Date.now(),
            type: 'assistant',
            text: '안녕하세요 Poly-i 입니다. 무엇을 도와드릴까요 ?',
            timestamp: new Date().toISOString(),
          });
        }
      }, 8000);
    }

    return () => {
      if (greetingTimerRef.current) {
        clearTimeout(greetingTimerRef.current);
        greetingTimerRef.current = null;
      }
    };
  }, [messages.length, view, addMessage]);

  useEffect(() => {
    if (closingTimerRef.current) {
      clearTimeout(closingTimerRef.current);
      closingTimerRef.current = null;
    }

    if (messages.length === 0 || isLoading) {
      setShowClosing(false);
      return undefined;
    }

    setShowClosing(false);
    closingTimerRef.current = setTimeout(() => {
      setShowClosing(true);
    }, 10_000);

    return () => {
      if (closingTimerRef.current) {
        clearTimeout(closingTimerRef.current);
        closingTimerRef.current = null;
      }
    };
  }, [messages, isLoading]);

  const sendToBackend = async (text, source = 'text') => {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 200_000); // 60초 timeout

    try {
      const response = await fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: text,
          language: language,
          user_id: 'web-user',
          source: source,
        }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP ${response.status}`);
      }

      const data = await response.json();
      return data.response || data.reply || PROMPTS[language].error;
    } catch (error) {
      clearTimeout(timeoutId);
      if (error.name === 'AbortError') {
        throw new Error('요청 시간이 초과되었습니다. 다시 시도해주세요.');
      }
      throw error;
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    setView('chat');
    addMessage({
      id: Date.now(),
      type: 'user',
      text: inputValue,
      timestamp: new Date().toISOString(),
    });

    setInputValue('');
    setIsLoading(true);

    try {
      const replyText = await sendToBackend(inputValue);
      addMessage({
        id: Date.now() + 1,
        type: 'assistant',
        text: replyText,
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

  const handleQuestionClick = async (question) => {
    setView('chat');

    // 사용자 질문 메시지 추가
    addMessage({
      id: Date.now(),
      type: 'user',
      text: question,
      timestamp: new Date().toISOString(),
    });

    setInputValue('');
    setIsLoading(true);

    try {
      const replyText = await sendToBackend(question, 'button');
      addMessage({
        id: Date.now() + 1,
        type: 'assistant',
        text: replyText,
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

  const handleHomeClick = () => {
    setView('home');
    setShowClosing(false);
  };

  return (
    <div className="flex flex-col h-full bg-white">
      <WaveBanner onHomeClick={handleHomeClick} />

      <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50">
        {view === 'professors' ? (
          <ProfessorIntro onBack={() => setView('home')} />
        ) : messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center overflow-y-auto">
            <div className="text-5xl mb-3">🏫</div>
            <h2 className="text-xl font-bold text-gray-800">{PROMPTS[language].welcome}</h2>
            <p className="text-gray-500 mt-2 text-sm mb-2">{PROMPTS[language].subtitle}</p>

            <a
              href="tel:031-696-8803"
              className="text-blue-600 hover:underline text-sm mb-4 flex items-center justify-center gap-1"
            >
              {PROMPTS[language].phone}
            </a>

            <div className="w-full max-w-sm bg-white rounded-lg shadow-md p-4 text-left space-y-2">
              {language === 'ko' ? (
                <>
                  <p className="text-sm font-bold text-poly-blue mb-3">알고 싶은 내용을 선택하세요</p>
                  <button
                    onClick={() => handleQuestionClick('학과소개')}
                    className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 rounded text-sm transition"
                  >
                    🏫 학과소개
                  </button>
                  <button
                    onClick={() => handleQuestionClick('취업현황 알려줘')}
                    className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 rounded text-sm transition"
                  >
                    👨‍💼 취업현황
                  </button>
                  <button
                    onClick={() => handleQuestionClick('식당/주차장 안내')}
                    className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 rounded text-sm transition"
                  >
                    🍽️ 식당/주차장
                  </button>
                  <button
                    onClick={() => handleQuestionClick('서류/입학정보 알려줘')}
                    className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 rounded text-sm transition"
                  >
                    📚 서류/입학정보
                  </button>
                  <button
                    type="button"
                    onClick={() => setView('professors')}
                    className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 rounded text-sm transition"
                  >
                    🧑‍🏫 교수님 소개
                  </button>
                </>
              ) : (
                <>
                  <p className="text-sm font-bold text-poly-blue mb-3">What would you like to know?</p>
                  <button
                    onClick={() => handleQuestionClick('Department overview')}
                    className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 rounded text-sm transition"
                  >
                    🏫 Departments
                  </button>
                  <button
                    onClick={() => handleQuestionClick('Show me employment stats')}
                    className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 rounded text-sm transition"
                  >
                    👨‍💼 Employment
                  </button>
                  <button
                    onClick={() => handleQuestionClick('Cafeteria and parking info')}
                    className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 rounded text-sm transition"
                  >
                    🍽️ Dining/Parking
                  </button>
                  <button
                    onClick={() => handleQuestionClick('Documents or course info')}
                    className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 rounded text-sm transition"
                  >
                    📚 Docs/Courses
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
                <div className="bg-gray-200 text-gray-900 rounded-2xl rounded-bl-none px-4 py-2">
                  <div className="text-sm">...</div>
                </div>
              </div>
            )}
            {messages.length > 0 && showClosing && (
              <div className="flex justify-start">
                <div className="w-full max-w-xs">
                  <div className="max-w-xs px-4 py-3 rounded-2xl rounded-bl-none border border-sky-100 bg-gradient-to-br from-sky-50 via-white to-amber-50 text-gray-800 shadow-sm">
                    <div className="text-sm leading-relaxed space-y-2">
                      <div className="font-semibold text-sky-700">{PROMPTS[language].closing.title}</div>
                      {PROMPTS[language].closing.lines.map((line, idx) => {
                        const highlight = PROMPTS[language].closing.highlight;
                        if (highlight && line.includes(highlight)) {
                          const [before, after] = line.split(highlight);
                          return (
                            <div key={idx}>
                              {before}
                              <strong>{highlight}</strong>
                              {after}
                            </div>
                          );
                        }
                        return <div key={idx}>{line}</div>;
                      })}
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      <form onSubmit={handleSendMessage} className="border-t border-gray-200 bg-white p-3">
        <div className="flex gap-2 items-end">
          <button
            type="button"
            onClick={handleMicClick}
            className={`p-2 rounded-full transition ${
              isListening ? 'bg-red-500 text-white' : 'hover:bg-poly-blue-light text-poly-blue'
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
            className="flex items-center gap-1.5 px-4 py-2 bg-poly-blue hover:bg-poly-blue-dark text-white rounded-full disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            <FiSend className="w-5 h-5" />
            <span className="text-sm font-semibold">전송</span>
          </button>
        </div>
      </form>
    </div>
  );
}
