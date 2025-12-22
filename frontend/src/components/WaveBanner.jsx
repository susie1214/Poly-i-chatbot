import React from 'react';
import useChatStore from '@/store/chatStore';
import '../styles/wave.css';

const WaveBanner = ({ onHomeClick }) => {
  const { language, setLanguage, clearMessages } = useChatStore();
  const labels = {
    ko: {
      home: '처음으로',
      ko: '한국어',
      en: 'ENG',
    },
    en: {
      home: 'Home',
      ko: 'KOR',
      en: 'ENG',
    },
  }[language] || {
    home: 'Home',
    ko: 'KOR',
    en: 'ENG',
  };

  return (
    <div className="wave-banner">
      <div className="absolute top-3 left-3 z-20">
        <button
          onClick={() => {
            clearMessages();
            if (onHomeClick) {
              onHomeClick();
            }
          }}
          className="px-3 py-1 rounded-full text-xs font-semibold bg-white text-poly-blue shadow-md hover:bg-blue-50 transition"
        >
          {labels.home}
        </button>
      </div>
      <div className="absolute top-3 right-3 z-20 flex gap-2">
        <button
          onClick={() => setLanguage('ko')}
          className={`px-3 py-1 rounded-full text-xs font-semibold transition ${
            language === 'ko'
              ? 'bg-white text-poly-blue shadow-md'
              : 'bg-black bg-opacity-20 text-white'
          }`}
        >
          {labels.ko}
        </button>
        <button
          onClick={() => setLanguage('en')}
          className={`px-3 py-1 rounded-full text-xs font-semibold transition ${
            language === 'en'
              ? 'bg-white text-poly-blue shadow-md'
              : 'bg-black bg-opacity-20 text-white'
          }`}
        >
          {labels.en}
        </button>
      </div>
      <h1>Poly-Chat</h1>
      <div className="wave-container">
        <div className="wave wave1"></div>
        <div className="wave wave2"></div>
      </div>
    </div>
  );
};

export default WaveBanner;
