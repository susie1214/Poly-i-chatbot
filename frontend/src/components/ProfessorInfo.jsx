import React from 'react';
import { FiPhone, FiMail, FiArrowLeft } from 'react-icons/fi';
import { professors } from '@/data/professors';

export default function ProfessorInfo({ onBack, language }) {
  return (
    <div className="flex flex-col h-full bg-white">
      {/* 헤더 */}
      <div className="border-b border-gray-200 p-4 flex items-center gap-2">
        <button
          onClick={onBack}
          className="p-2 hover:bg-gray-100 rounded-full transition"
        >
          <FiArrowLeft className="w-5 h-5" />
        </button>
        <h1 className="text-lg font-bold text-poly-blue">
          {language === 'ko' ? 'AI응용소프트웨어학과 교수진' : 'Faculty'}
        </h1>
      </div>

      {/* 교수진 리스트 */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {professors.map((prof) => (
          <div key={prof.id} className="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition p-4">
            {/* 이름 및 직위 */}
            <div className="flex items-start justify-between mb-3">
              <div>
                <h2 className="text-lg font-bold text-gray-900">{prof.name}</h2>
                <p className="text-sm text-poly-blue font-medium">{prof.title}</p>
              </div>
              {prof.isChair && (
                <span className="px-2 py-1 bg-poly-blue text-white text-xs rounded font-semibold">
                  {language === 'ko' ? '학과장' : 'Chair'}
                </span>
              )}
            </div>

            {/* 연락처 정보 */}
            <div className="space-y-2 mb-3 text-sm">
              <a
                href={`tel:${prof.phone}`}
                className="flex items-center gap-2 text-blue-600 hover:underline"
              >
                <FiPhone className="w-4 h-4" />
                {prof.phone}
              </a>
              <a
                href={`mailto:${prof.email}`}
                className="flex items-center gap-2 text-blue-600 hover:underline break-all"
              >
                <FiMail className="w-4 h-4" />
                {prof.email}
              </a>
            </div>

            {/* 주요 과목 */}
            <div className="mb-3 pb-3 border-b border-gray-200">
              <p className="text-xs font-semibold text-gray-600 mb-1">
                {language === 'ko' ? '주요 과목' : 'Main Subjects'}
              </p>
              <div className="flex flex-wrap gap-1">
                {prof.mainSubjects.map((subject, idx) => (
                  <span key={idx} className="px-2 py-1 bg-blue-50 text-xs text-blue-700 rounded">
                    {subject}
                  </span>
                ))}
              </div>
            </div>

            {/* 학력 */}
            <div className="mb-3">
              <p className="text-xs font-semibold text-gray-600 mb-1">
                {language === 'ko' ? '학력' : 'Education'}
              </p>
              <p className="text-sm text-gray-700">{prof.education}</p>
            </div>

            {/* 경력 */}
            <div className="mb-3">
              <p className="text-xs font-semibold text-gray-600 mb-1">
                {language === 'ko' ? '주요 경력' : 'Career'}
              </p>
              <ul className="text-sm text-gray-700 space-y-1">
                {prof.career.map((item, idx) => (
                  <li key={idx} className="flex gap-2">
                    <span className="text-poly-blue">•</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* 주요 성과 */}
            <div className="mb-3">
              <p className="text-xs font-semibold text-gray-600 mb-1">
                {language === 'ko' ? '주요 성과' : 'Achievements'}
              </p>
              <ul className="text-sm text-gray-700 space-y-1">
                {prof.achievements.map((item, idx) => (
                  <li key={idx} className="flex gap-2">
                    <span className="text-poly-blue">•</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* 연구 분야 */}
            <div className="mb-3">
              <p className="text-xs font-semibold text-gray-600 mb-1">
                {language === 'ko' ? '연구 분야' : 'Research Fields'}
              </p>
              <div className="flex flex-wrap gap-1">
                {prof.researchFields.map((field, idx) => (
                  <span key={idx} className="px-2 py-1 bg-green-50 text-xs text-green-700 rounded">
                    {field}
                  </span>
                ))}
              </div>
            </div>

            {/* 학생 평가 */}
            <div className="p-3 bg-yellow-50 border border-yellow-200 rounded">
              <p className="text-xs font-semibold text-yellow-800 mb-1">
                {language === 'ko' ? '💬 학생 평가' : '💬 Student Review'}
              </p>
              <p className="text-sm text-yellow-900">{prof.review}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
