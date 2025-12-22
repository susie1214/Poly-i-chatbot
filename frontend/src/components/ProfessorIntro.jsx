import React, { useMemo, useState } from 'react';
import { FiArrowLeft, FiMail, FiPhone } from 'react-icons/fi';
import useChatStore from '@/store/chatStore';
import { professors } from '@/data/professors';

const DEPARTMENTS = [
  {
    key: 'ai-app',
    label: {
      ko: 'AI응용소프트웨어학과',
      en: 'AI Application Software',
    },
    filter: (professor) => professor.id >= 1 && professor.id <= 4,
  },
  {
    key: 'ai-fin',
    label: {
      ko: 'AI금융소프트웨어학과',
      en: 'AI Finance Software',
    },
    filter: (professor) => professor.id >= 5 && professor.id <= 7,
  },
  {
    key: 'bio',
    label: {
      ko: '생명의료시스템학과',
      en: 'Biomedical Systems',
    },
    filter: (professor) => professor.id >= 8,
  },
];

const LABELS = {
  ko: {
    title: '교수님 소개',
    chair: '학과장',
    mainSubjects: '주요 과목',
    education: '학력',
    career: '경력',
    achievements: '주요 성과',
    researchFields: '연구 분야',
    review: '한줄 평가',
  },
  en: {
    title: 'Professor Introductions',
    chair: 'Chair',
    mainSubjects: 'Main Subjects',
    education: 'Education',
    career: 'Career',
    achievements: 'Highlights',
    researchFields: 'Research Fields',
    review: 'Student Note',
  },
};

const Section = ({ title, children }) => (
  <div className="space-y-2">
    <div className="text-xs font-semibold text-gray-700">{title}</div>
    {children}
  </div>
);

const ChipList = ({ items, className = '' }) => (
  <div className={`flex flex-wrap gap-2 ${className}`}>
    {items.map((item, idx) => (
      <span
        key={`${item}-${idx}`}
        className="rounded-full bg-blue-50 px-2.5 py-1 text-xs font-semibold text-blue-700"
      >
        {item}
      </span>
    ))}
  </div>
);

export default function ProfessorIntro({ onBack }) {
  const { language } = useChatStore();
  const labels = LABELS[language] || LABELS.ko;
  const [activeDept, setActiveDept] = useState(DEPARTMENTS[0].key);

  const visibleProfessors = useMemo(() => {
    const department = DEPARTMENTS.find((dept) => dept.key === activeDept);
    return department ? professors.filter(department.filter) : professors;
  }, [activeDept]);

  return (
    <div className="h-full overflow-y-auto bg-gray-50">
      <div className="sticky top-0 z-10 bg-white border-b border-gray-200">
        <div className="flex items-center gap-2 px-4 py-3">
          <button
            type="button"
            onClick={onBack}
            className="p-2 rounded-full hover:bg-gray-100 transition"
            aria-label="Back"
          >
            <FiArrowLeft className="w-5 h-5 text-gray-700" />
          </button>
          <div className="text-base font-bold text-gray-900">{labels.title}</div>
        </div>
        <div className="flex gap-2 overflow-x-auto px-4 pb-3">
          {DEPARTMENTS.map((dept) => (
            <button
              key={dept.key}
              type="button"
              onClick={() => setActiveDept(dept.key)}
              className={`whitespace-nowrap rounded-full px-4 py-1.5 text-xs font-semibold transition ${
                activeDept === dept.key
                  ? 'bg-poly-blue text-white shadow'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {dept.label[language] || dept.label.ko}
            </button>
          ))}
        </div>
      </div>

      <div className="space-y-4 p-4">
        {visibleProfessors.map((professor) => {
          const profile = language === 'en' && professor.en ? professor.en : professor;
          const mainSubjects = Array.isArray(profile.mainSubjects)
            ? profile.mainSubjects
            : [];
          const career = Array.isArray(profile.career) ? profile.career : [];
          const achievements = Array.isArray(profile.achievements)
            ? profile.achievements
            : [];
          const researchFields = Array.isArray(profile.researchFields)
            ? profile.researchFields
            : [];

          return (
            <article
              key={professor.id}
              className="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm space-y-4"
            >
              <div className="flex items-start justify-between gap-3">
                <div>
                  <h3 className="text-lg font-bold text-gray-900">{professor.name}</h3>
                  <p className="text-sm font-semibold text-poly-blue">{profile.title}</p>
                </div>
                {professor.isChair && (
                  <span className="rounded-full bg-blue-100 px-2 py-1 text-xs font-semibold text-blue-700">
                    {labels.chair}
                  </span>
                )}
              </div>

              <div className="space-y-2 text-sm text-gray-700">
                <a
                  className="flex items-center gap-2 text-blue-600 hover:underline"
                  href={`tel:${professor.phone}`}
                >
                  <FiPhone className="h-4 w-4" />
                  {professor.phone}
                </a>
                <a
                  className="flex items-center gap-2 text-blue-600 hover:underline"
                  href={`mailto:${professor.email}`}
                >
                  <FiMail className="h-4 w-4" />
                  {professor.email}
                </a>
              </div>

              {mainSubjects.length > 0 && (
                <Section title={labels.mainSubjects}>
                  <ChipList items={mainSubjects} />
                </Section>
              )}

              {profile.education && (
                <Section title={labels.education}>
                  <p className="text-sm text-gray-700">{profile.education}</p>
                </Section>
              )}

              {career.length > 0 && (
                <Section title={labels.career}>
                  <ul className="list-disc pl-4 text-sm text-gray-700 space-y-1">
                    {career.map((item, idx) => (
                      <li key={`${professor.id}-career-${idx}`}>{item}</li>
                    ))}
                  </ul>
                </Section>
              )}

              {achievements.length > 0 && (
                <Section title={labels.achievements}>
                  <ul className="list-disc pl-4 text-sm text-gray-700 space-y-1">
                    {achievements.map((item, idx) => (
                      <li key={`${professor.id}-achieve-${idx}`}>{item}</li>
                    ))}
                  </ul>
                </Section>
              )}

              {researchFields.length > 0 && (
                <Section title={labels.researchFields}>
                  <ChipList items={researchFields} className="text-xs" />
                </Section>
              )}

              {profile.review && (
                <div className="rounded-xl border border-yellow-200 bg-yellow-50 px-3 py-3 text-sm text-yellow-800">
                  <div className="mb-1 text-xs font-semibold">{labels.review}</div>
                  <p>{profile.review}</p>
                </div>
              )}
            </article>
          );
        })}
      </div>
    </div>
  );
}
