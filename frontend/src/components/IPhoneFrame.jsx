import React from 'react';

export default function IPhoneFrame({ children }) {
  return (
    <div className="relative w-full max-w-md">
      {/* 아이폰 외형 */}
      <div className="bg-black rounded-[3rem] shadow-2xl overflow-hidden border-8 border-gray-900" 
           style={{
             aspectRatio: '9/19.5',
             boxShadow: '0 20px 60px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.2)'
           }}>
        
        {/* 콘텐츠 영역 */}
        <div className="w-full h-full bg-white overflow-hidden flex flex-col">
          {children}
        </div>
      </div>

      {/* 스피커 */}
      <div className="absolute top-1 left-1/3 right-1/3 h-1 bg-gray-900 rounded-full mx-auto"></div>
      
      {/* 홈 버튼 시뮬레이션 */}
      <div className="absolute bottom-2 left-1/2 transform -translate-x-1/2 w-20 h-1 bg-gray-900 rounded-full"></div>
    </div>
  );
}
