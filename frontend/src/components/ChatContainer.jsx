import React, { useState, useEffect, useRef } from 'react';
import { FiSend, FiMic, FiArrowLeft } from 'react-icons/fi';
import useChatStore from '@/store/chatStore';
import ChatMessage from './ChatMessage';
import ChatHeader from './ChatHeader';
import ProfessorInfo from './ProfessorInfo';

const PROMPTS = {
  ko: {
    welcome: "안녕하세요! 저는 Poly-i입니다.",
    subtitle: "분당폴리텍 교육과정에 대해 궁금한 점을 물어봐주세요!",
    phone: "☎️ 031-696-8803",
    placeholder: "메시지를 입력하세요...",
    error: "죄송합니다. 오류가 발생했습니다.",
    systemPrompt: `당신은 분당폴리텍 교육과정을 안내하는 친절한 챗봇 Poly-i입니다.`
  },
  en: {
    welcome: "Hello! I'm Poly-i.",
    subtitle: "Ask me about Bundang Polytechnic's programs!",
    phone: "☎️ 031-696-8803",
    placeholder: "Type a message...",
    error: "Sorry, an error occurred.",
    systemPrompt: `You are Poly-i, a friendly chatbot for Bundang Polytechnic education programs.`
  }
};

export default function ChatContainer() {
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [currentView, setCurrentView] = useState('chat');
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

  const handleQuestionClick = async (question) => {
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: question,
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

  return (
    <div className="flex flex-col h-full bg-white">
      {currentView === 'professors' ? (
        <ProfessorInfo 
          onBack={() => setCurrentView('chat')}
          language={language}
        />
      ) : (
        <>
          {/* 헤더 + 언어 선택 */}
          <div className="flex items-center justify-between border-b border-gray-200 p-3">
            <ChatHeader />
            <div className="flex gap-2">
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
                <p className="text-gray-500 mt-2 text-sm mb-2">{PROMPTS[language].subtitle}</p>
                
                {/* 전화번호 */}
                <a
                  href="tel:031-696-8803"
                  className="text-blue-600 hover:underline text-sm mb-4 flex items-center justify-center gap-1"
                >
                  {PROMPTS[language].phone}
                </a>
                
                {/* 안내 메뉴 */}
                <div className="w-full max-w-sm bg-white rounded-lg shadow-md p-4 text-left space-y-2">
                  {language === 'ko' ? (
                    <>
                      <p className="text-sm font-bold text-poly-blue mb-3">📋 궁금한 것을 선택하세요:</p>
                      <button 
                        onClick={() => {
                          addMessage({
                            id: Date.now(),
                            type: 'user',
                            text: '주차 정보 알려줘',
                            timestamp: new Date().toISOString(),
                          });
                          handleQuestionClick('주차 정보 알려줘');
                        }}
                        className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 rounded text-sm transition"
                      >
                        🚗 주차 정보 알려줘
                      </button>
                      <button 
                        onClick={() => {
                          addMessage({
                            id: Date.now(),
                            type: 'user',
                            text: '식사 정보 알려줘',
                            timestamp: new Date().toISOString(),
                          });
                          handleQuestionClick('식사 정보 알려줘');
                        }}
                        className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 rounded text-sm transition"
                      >
                        🍽️ 식사 정보 알려줘
                      </button>
                      <button 
                        onClick={() => {
                          addMessage({
                            id: Date.now(),
                            type: 'user',
                            text: '수당 정보 알려줘',
                            timestamp: new Date().toISOString(),
                          });
                          handleQuestionClick('수당 정보 알려줘');
                        }}
                        className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 rounded text-sm transition"
                      >
                        💰 수당 정보 알려줘
                      </button>
                      <button 
                        onClick={() => setCurrentView('professors')}
                        className="w-full text-left p-3 bg-green-50 hover:bg-green-100 rounded text-sm transition"
                      >
                        👨‍🏫 교수진 정보
                      </button>
                      <button 
                        onClick={() => window.open('https://docs.google.com/forms/d/e/1FAIpQLSdsViAfnWSNeug8kLYRprui3k4cRVRtVjY5SKeERIK2D9Y9Hg/viewform?pli=1', '_blank')}
                        className="w-full text-left p-3 bg-orange-50 hover:bg-orange-100 rounded text-sm transition"
                      >
                        📢 입시설명회 바로연결
                      </button>
                    </>
                  ) : (
                    <>
                      <p className="text-sm font-bold text-poly-blue mb-3">📋 What would you like to know?</p>
                      <button 
                        onClick={() => {
                          addMessage({
                            id: Date.now(),
                            type: 'user',
                            text: 'Tell me about parking',
                            timestamp: new Date().toISOString(),
                          });
                          handleQuestionClick('Tell me about parking');
                        }}
                        className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 rounded text-sm transition"
                      >
                        🚗 Parking Information
                      </button>
                      <button 
                        onClick={() => {
                          addMessage({
                            id: Date.now(),
                            type: 'user',
                            text: 'Tell me about lunch',
                            timestamp: new Date().toISOString(),
                          });
                          handleQuestionClick('Tell me about lunch');
                        }}
                        className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 rounded text-sm transition"
                      >
                        🍽️ Lunch Information
                      </button>
                      <button 
                        onClick={() => {
                          addMessage({
                            id: Date.now(),
                            type: 'user',
                            text: 'Tell me about allowance',
                            timestamp: new Date().toISOString(),
                          });
                          handleQuestionClick('Tell me about allowance');
                        }}
                        className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 rounded text-sm transition"
                      >
                        💰 Allowance Information
                      </button>
                      <button 
                        onClick={() => setCurrentView('professors')}
                        className="w-full text-left p-3 bg-green-50 hover:bg-green-100 rounded text-sm transition"
                      >
                        👨‍🏫 Faculty
                      </button>
                      <button 
                        onClick={() => window.open('https://docs.google.com/forms/d/e/1FAIpQLSdsViAfnWSNeug8kLYRprui3k4cRVRtVjY5SKeERIK2D9Y9Hg/viewform?pli=1', '_blank')}
                        className="w-full text-left p-3 bg-orange-50 hover:bg-orange-100 rounded text-sm transition"
                      >
                        📢 Admission Talk
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
                onClick={() => setCurrentView('chat')}
                className="p-2 rounded-full hover:bg-gray-200 text-gray-600 transition"
              >
                <FiArrowLeft className="w-5 h-5" />
              </button>
              
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
        </>
      )}
    </div>
  );
}
