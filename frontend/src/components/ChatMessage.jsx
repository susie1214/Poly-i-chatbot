import React from 'react';

// 간단한 마크다운 포맷팅
const formatMessage = (text) => {
  return text
    .split('\n')
    .map((line, idx) => {
      // 헤더 포맷
      if (line.startsWith('## ')) {
        return <h3 key={idx} className="font-bold text-sm mt-2 text-gray-800">{line.slice(3)}</h3>;
      }
      if (line.startsWith('**') && line.endsWith('**')) {
        return <strong key={idx}>{line.slice(2, -2)}</strong>;
      }
      // 리스트 포맷
      if (line.startsWith('- ')) {
        return <div key={idx} className="ml-3 text-sm">• {line.slice(2)}</div>;
      }
      if (line.startsWith('1. ') || line.startsWith('2. ') || line.startsWith('3. ')) {
        return <div key={idx} className="ml-3 text-sm">{line}</div>;
      }
      return <div key={idx} className="text-sm">{line || ' '}</div>;
    });
};

// 위치 정보 기반 지도 임베드
const LocationMap = ({ keyword }) => {
  // 카카오맵 좌표 (분당폴리텍 관련 위치들)
  const locations = {
    '주차': { name: '분당폴리텍 주변 주차장', lat: 37.1799, lng: 127.1047 },
    '식사': { name: '분당폴리텍 구내식당', lat: 37.1799, lng: 127.1047 },
    '위치': { name: '분당폴리텍융합기술교육원', lat: 37.1799, lng: 127.1047 },
    '수당': null, // 수당은 위치 정보 없음
  };

  const location = locations[keyword];
  if (!location) return null;

  // Google Maps 임베드 URL (간단한 방법)
  const googleMapsUrl = `https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3169.4848!2d${location.lng}!3d${location.lat}!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x357b64e65f0e0001%3A0x${Math.random().toString(36).substr(2, 9)}!2s${location.name}!5e0!3m2!1sko!2skr!4v1670000000000`;
  
  // 카카오맵 임베드 (더 간단한 방법)
  const kakaoMapUrl = `https://map.kakao.com/link/map/${location.name},${location.lat},${location.lng}`;

  return (
    <div className="mt-3 rounded-lg overflow-hidden border border-gray-300 bg-gray-100">
      <a
        href={kakaoMapUrl}
        target="_blank"
        rel="noopener noreferrer"
        className="block p-3 text-center bg-blue-500 hover:bg-blue-600 text-white font-semibold text-sm transition"
      >
        🗺️ 카카오맵에서 보기 ({location.name})
      </a>
    </div>
  );
};

export default function ChatMessage({ message }) {
  const isUser = message.type === 'user';

  // 키워드 기반 위치 표시 (주차, 식사, 위치)
  const showMap = !isUser && (
    message.text.includes('주차장') || 
    message.text.includes('구내식당') || 
    message.text.includes('분당폴리텍')
  );

  const mapKeyword = message.text.includes('주차장') ? '주차' : 
                     message.text.includes('식사') || message.text.includes('구내식당') ? '식사' : 
                     message.text.includes('위치') ? '위치' : null;

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className="w-full max-w-xs">
        <div
          className={`max-w-xs px-4 py-2 rounded-2xl ${
            isUser
              ? 'bg-poly-blue text-white rounded-br-none'
              : 'bg-gray-200 text-gray-900 rounded-bl-none'
          }`}
        >
          <div className={`break-words leading-relaxed ${isUser ? '' : ''}`}>
            {isUser ? message.text : formatMessage(message.text)}
          </div>
          <span className={`text-xs mt-1 block ${isUser ? 'text-blue-100' : 'text-gray-500'}`}>
            {new Date(message.timestamp).toLocaleTimeString('ko-KR', {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </span>
        </div>
        
        {/* 위치 정보가 있을 경우 지도 표시 */}
        {showMap && mapKeyword && (
          <div className="mt-2 max-w-xs">
            <LocationMap keyword={mapKeyword} />
          </div>
        )}
      </div>
    </div>
  );
}
