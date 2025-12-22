export const professors = [
  {
    id: 1,
    name: '박길식',
    title: '교수',
    isChair: false,
    phone: '031-696-8854',
    email: 'gilsikpark@kopo.ac.kr',
    mainSubjects: ['백엔드프로그래밍', '프로젝트실습'],
    education: '동국대학교 컴퓨터공학과 인공지능 공학박사',
    career: [
      '(주)사람을위한AI 대표',
      '건국대학교/경희대학교/국민대학교 대학원 인공지능전공 겸임교수',
      '광운대학교 전자공학과 연구초빙교수',
      '연세대학교 공학대학원 객원교수'
    ],
    achievements: [
      '2024 이기적 ADsP 데이터분석 준전문가 기본서(영진닷컴)',
      'Android Studio를 활용한 안드로이드 프로그래밍(한빛아카데미)',
      '지존 미니족보 정보처리기사 필기(영진닷컴)',
      '국내 특허등록 4건',
      '인공지능 관련 국내외 논문 다수 게재',
      '기계학습 모델 기반 환자 맞춤형 항생제 처방 기술 개발 등 다수 국가 R&D 연구과제 수행'
    ],
    researchFields: ['머신러닝', '딥러닝', 'NLP', '강화학습', '생성형AI'],
    review: '꼼꼼하고 미래 지향적이며 학생들의 논문도 봐주시고 학생들 이름을 잘 기억하시는 AI 특화 교수님입니다.',
    en: {
      title: 'Professor',
      mainSubjects: ['Backend Programming', 'Project Practice'],
      education: 'Ph.D. in AI, Computer Engineering, Dongguk University',
      career: [
        'CEO, AI for Humans Co., Ltd.',
        'Adjunct Professor, AI major (Konkuk/Kyung Hee/Kookmin Graduate Schools)',
        'Research Visiting Professor, Kwangwoon University (Dept. of Electronic Engineering)',
        'Visiting Professor, Yonsei University Graduate School of Engineering'
      ],
      achievements: [
        '2024 ADsP Data Analysis Study Guide (Youngjin.com)',
        'Android Programming with Android Studio (Hanbit Academy)',
        'Information Processing Engineer Prep Notes (Youngjin.com)',
        '4 domestic patents',
        'Numerous AI-related domestic and international papers',
        'Led multiple national R&D projects on ML-based personalized antibiotic prescription'
      ],
      researchFields: ['Machine Learning', 'Deep Learning', 'NLP', 'Reinforcement Learning', 'Generative AI'],
      review: 'Known for thorough, forward-looking guidance and strong support for student research.'
    }
  },
  {
    id: 2,
    name: '조영준',
    title: '교수',
    isChair: false,
    phone: '031-696-8853',
    email: 'samcho2017@kopo.ac.kr',
    mainSubjects: ['프로그래밍심화', 'AI비전프로그래밍'],
    education: '한국기술교육대학교 전자공학과 학사, 석사, 박사',
    career: [
      '㈜이화트론 기술연구소(DVR 하드웨어 개발)',
      '㈜카티스 기술연구소 (RFID 및 보안 시스템 하드웨어 개발)',
      '에이케이시스템 대표',
      '하드웨어/펌웨어 설계 및 개발 경력 15년'
    ],
    achievements: [
      'AVR, 8051, Arduino, 영상처리, 파이썬 관련 저서 8권 집필',
      '국내 실용신안 3건',
      '한국장애인고용공단 청각장애인용 보조공학장치 다수 개발',
      '서울메트로 전동차 관련 국산화 개발 프로젝트 다수 참여',
      '무대장치용 AIoT 조명 제어 시스템, 연출용 화염제어 시스템 다수 개발'
    ],
    researchFields: ['제약회사용 HPLC 제어 장치 개발', '스마트공장용 가공장비 실시간 모니터링 시스템 개발', 'AIoT 시스템, 스마트 공장'],
    review: '상담을 매우 잘해주시며 밥도 잘사주시고 자상하신 분입니다. 학생들을 멘탈적으로 잘 관리해주시는 C++, OpenCV 주로 가르치시는 교수님입니다.',
    en: {
      title: 'Professor',
      mainSubjects: ['Advanced Programming', 'AI Vision Programming'],
      education: 'B.S./M.S./Ph.D. in Electronic Engineering, KOREATECH',
      career: [
        'R&D, Ihwa Tron (DVR hardware development)',
        'R&D, Katis (RFID and security systems hardware)',
        'CEO, AK System',
        '15 years of hardware/firmware design and development'
      ],
      achievements: [
        'Authored 8 books on AVR, 8051, Arduino, image processing, Python',
        '3 domestic utility models',
        'Developed assistive devices for the hearing-impaired (Korea Employment Agency for the Disabled)',
        'Participated in multiple Seoul Metro rolling stock localization projects',
        'Developed AIoT lighting control and stage effects control systems'
      ],
      researchFields: [
        'HPLC control devices for pharma companies',
        'Smart factory processing equipment monitoring',
        'AIoT systems, smart factories'
      ],
      review: 'Friendly and supportive mentor; strong in C++ and OpenCV, with great student care.'
    }
  },
  {
    id: 3,
    name: '김남호',
    title: '교수',
    isChair: false,
    phone: '031-696-8851',
    email: 'namo@kopo.ac.kr',
    mainSubjects: ['엣지프로그래밍', 'AIoT프로젝트'],
    education: '고려대학교 전자공학과 학사, 석사 / 한경대학교 전기전자제어공학과 박사',
    career: [
      '현대전자 멀티미디어 연구소(DTV 셋탑박스HW 개발)',
      '펜타마이크로 중앙연구소(DVR SW 개발)',
      '팬택앤큐리텔 UMTS 연구소(유럽향단말기 SW 개발)',
      '엠진중앙연구소(저장장치 칩, 백터그래픽칩 SW 개발)',
      '총 경력 24년'
    ],
    achievements: [
      '국내 특허등록 3건',
      '영상처리 및 머신러닝관련 국내외 논문 9건 게재',
      '도플러 레이더 센서를 사용한 인공지능 기반 낙상 인식 시스템에 관한 연구 등 다수 국가 R&D연구과제 수행'
    ],
    researchFields: ['리눅스', '안드로이드', '디바이스 드라이버', 'AIoT SW', '신호처리', '영상처리 및 머신비전'],
    review: '교수님이 하라는 것만 잘해도 좋으시고 수업 결석하면 안되지만, 교수님 성격이 매우 좋으신 분입니다.',
    en: {
      title: 'Professor',
      mainSubjects: ['Edge Programming', 'AIoT Project'],
      education: 'B.S./M.S. in Electronic Engineering (Korea Univ.) / Ph.D. in Electrical & Control Engineering (Hankyong Univ.)',
      career: [
        'Hyundai Electronics Multimedia Lab (DTV set-top HW)',
        'Pentamicro R&D Center (DVR software)',
        'Pantech & Curitel UMTS Lab (EU handset SW)',
        'Mjin R&D Center (storage chip, vector graphics chip SW)',
        '24 years of experience'
      ],
      achievements: [
        '3 domestic patents',
        '9 papers in image processing and ML',
        'Multiple national R&D projects including AI fall detection using Doppler radar'
      ],
      researchFields: [
        'Linux', 'Android', 'Device Drivers', 'AIoT Software',
        'Signal Processing', 'Image Processing and Machine Vision'
      ],
      review: 'Clear guidance and a kind personality; attendance matters, but mentorship is excellent.'
    }
  },
  {
    id: 4,
    name: '이승원',
    title: '교수(AI응용소프트웨어학과장)',
    isChair: true,
    phone: '031-696-8852',
    email: 'lsw@kopo.ac.kr',
    mainSubjects: ['JAVA프로그래밍', 'AI데이터분석'],
    education: '한양대학교 정보시스템학과 공학박사',
    career: [
      '경민대학교 컴퓨터소프트웨어과 조교수',
      '가천대학교 컴퓨터공학과 연구교수',
      '제주대학교 SW융합교육원 학술연구교수',
      '웹/앱 연구 개발 경력 3년'
    ],
    achievements: [
      'AI 기반 비대면 문진 및 환자 상태 자동 분류를 위한 스마트 사이니지 기술개발',
      '사이버공격에 따른 원전 사보타주 정량적 리스크 평가모델 개발 등 다수 국가 R&D 연구과제 수행',
      'SCI(E)/SCOPUS 3편, KCI 2편, 국내/외 Conference 다수 게재'
    ],
    researchFields: ['인공지능', '정보보안', '블록체인'],
    review: '학과장님이시고 JAVA를 메인으로 가르치셔주시며 학생들과 챗을 좋아하시고 스마트하고 편하신 분입니다.',
    en: {
      title: 'Professor (Chair, AI Application Software Dept.)',
      mainSubjects: ['Java Programming', 'AI Data Analysis'],
      education: 'Ph.D. in Information Systems, Hanyang University',
      career: [
        'Assistant Professor, Kyungmin University (Computer Software)',
        'Research Professor, Gachon University (Computer Engineering)',
        'Research Professor, Jeju University SW Convergence Center',
        '3 years of web/app R&D'
      ],
      achievements: [
        'AI-based smart signage for automated health screening',
        'Risk assessment model for cyber attacks on nuclear facilities',
        'SCI(E)/SCOPUS 3 papers, KCI 2 papers, multiple conferences'
      ],
      researchFields: ['AI', 'Information Security', 'Blockchain'],
      review: 'Approachable chair who teaches Java and creates a friendly class atmosphere.'
    }
  },
  // AI금융소프트웨어학과 교수진
  {
    id: 5,
    name: '윤창호',
    title: '교수(AI금융소프트웨어학과장)',
    isChair: true,
    phone: '031-696-8829',
    email: 'zep25dr@kopo.ac.kr',
    mainSubjects: ['인공지능', '웹프로그래밍', '모바일프로그래밍'],
    education: '서울시립대학교 전자전기컴퓨터공학과 공학박사',
    career: [
      '(주)UGLSoft 대표 (\'09.04~\'23.05)',
      'ISO/IEC JTC1/SC22(프로그래밍언어 표준화) GD 위원 (\'13.10~현재)',
      '대한민국 국가표준위원회 시스템 소프트웨어 위원 (\'16.07~현재)',
      'iamroot.org(리눅스 커널 커뮤니티) 대표 (\'19.02~현재)',
      '서울시립대학교 도시과학빅데이터AI연구원 슈퍼컴퓨터 관리자 (\'22.07~\'23.10)'
    ],
    achievements: [
      '[논문] 스마트시티를 위한 스트림 리즈닝 등 다수 발표',
      '[특허] 스트림리즈닝 시스템 등 13건 등록',
      '[표준] ISO/IEC 23360-1-1:2021 Linux Standard Base(LSB) 등 10건'
    ],
    researchFields: ['인공지능', 'Distributed AI', 'Intelligent Systems', 'GPU 컴퓨팅'],
    review: '프로그래밍 분야의 국제 표준화 활동을 리드하는 전문가 교수님입니다.',
    en: {
      title: 'Professor (Chair, AI Finance Software Dept.)',
      mainSubjects: ['Artificial Intelligence', 'Web Programming', 'Mobile Programming'],
      education: 'Ph.D. in Electrical/Electronic/Computer Engineering, University of Seoul',
      career: [
        'CEO, UGLSoft (2009.04~2023.05)',
        'ISO/IEC JTC1/SC22 GD member (2013.10~present)',
        'National Standards Committee, System Software (2016.07~present)',
        'Founder, iamroot.org (Linux kernel community)',
        'Supercomputer admin, UOS Big Data AI Institute (2022.07~2023.10)'
      ],
      achievements: [
        'Papers on stream reasoning for smart cities',
        '13 patents including stream reasoning systems',
        '10 standards including ISO/IEC 23360-1-1:2021 (LSB)'
      ],
      researchFields: ['AI', 'Distributed AI', 'Intelligent Systems', 'GPU Computing'],
      review: 'Leads international standardization efforts in programming and systems software.'
    }
  },
  {
    id: 6,
    name: '김규석',
    title: '교수',
    isChair: false,
    phone: '031-696-8832',
    email: 'kyuseokkim@kopo.ac.kr',
    mainSubjects: ['데이터분석프로그래밍', '기본프로그래밍'],
    education: '한국항공대학교 정보통신공학 학사 / 아주대학교 정보통신공학 석사 / 서울대학교 도시계획학 박사',
    career: [
      '한국폴리텍대학 AI금융소프트웨어과 교수 (\'20.02~현재)',
      'LG유플러스 책임 - 홈미디어 서비스 R&D (\'19.07~\'20.02)',
      'LG전자 선임연구원 - 근거리 무선통신 R&D (\'11.01~\'19.06)',
      '대학 및 기업체 빅데이터, 인공지능 이론 및 실습 강의'
    ],
    achievements: [
      '[저서] 부동산 트렌드 2026/2025, 나 개발자로 100명 취업시켰다, 나도 하는 파이썬 데이터 분석, 난생 처음 데이터 분석 with 파이썬 등',
      '[특허] Big Data, Speech Recognition, Short-Range Wireless Communication 등 ICT 분야 해외 특허 5건, 국내 특허 22건 출원/등록',
      '[논문] AI-based Big Data Analysis, Context-awareness 등 국내 저널 30여편, 학술발표 10여건 등'
    ],
    researchFields: ['Big Data Analysis on Social Science Topics', 'AI-based Analytics Model SNS'],
    review: '빅데이터와 AI 분석에 매우 능숙한 교수님으로 실무 경험이 풍부합니다.',
    en: {
      title: 'Professor',
      mainSubjects: ['Data Analysis Programming', 'Fundamentals of Programming'],
      education: 'B.S. ICT, Korea Aerospace Univ. / M.S. ICT, Ajou Univ. / Ph.D. Urban Planning, Seoul National Univ.',
      career: [
        'Professor, AI Finance Software, Korea Polytechnics (2020~present)',
        'LG U+ Lead Engineer, Home Media R&D (2019~2020)',
        'LG Electronics Senior Researcher, Short-Range Wireless R&D (2011~2019)',
        'Lectures on big data and AI for universities and companies'
      ],
      achievements: [
        'Books on real estate trends and Python data analysis',
        '5 international patents, 22 domestic patents in ICT',
        '30+ journal papers and 10+ conference presentations'
      ],
      researchFields: ['Big Data Analysis in Social Science', 'AI-based SNS Analytics'],
      review: 'Strong in big data and AI analytics with rich industry experience.'
    }
  },
  {
    id: 7,
    name: '홍필두',
    title: '교수',
    isChair: false,
    phone: '031-696-8831',
    email: 'iamhpd@kopo.ac.kr',
    mainSubjects: ['인공지능 시스템 설계', '대규모 기업업무 프로그래밍'],
    education: '서울시립대 분산처리 시스템 공학박사',
    career: [
      '정보처리 기술사',
      '정보시스템 수석감리원',
      '메리츠금융 그룹 IT개발팀장',
      '서울시립대/세종사이버대 겸임교수 출강',
      'ISO/IEC SC22,24(리눅스.프로그래밍분과) 국제표준화기구 국내대표위원(GD)',
      '국방부표준화위원(DITA), NCS자문위원',
      '20년 이상 실무 경험'
    ],
    achievements: [
      '[논문] SCI(E) 4편, 그 외 논문 다수',
      '[특허] 프로그래밍 특허 4건',
      '[학회활동] 인터넷정보학회/정보통신학회/실천공학교육학회 등 상임이사 및 학술지편집위원장 역임'
    ],
    researchFields: ['AI모델학습', 'LLM', '웹 클라이언트/서버 및 정보시스템', '프로젝트 관리'],
    review: '20년 이상의 실무 경험으로 현장 중심의 교육을 제공하는 교수님입니다.',
    en: {
      title: 'Professor',
      mainSubjects: ['AI System Design', 'Enterprise Programming'],
      education: 'Ph.D. in Distributed Processing Systems, University of Seoul',
      career: [
        'Professional Engineer (Information Processing)',
        'Senior IS Auditor',
        'IT Development Team Lead, Meritz Financial Group',
        'Adjunct Professor, UOS/Sejong Cyber University',
        'ISO/IEC SC22/24 national representative (GD)',
        'Defense Standardization Committee (DITA), NCS Advisor',
        '20+ years of field experience'
      ],
      achievements: [
        '4 SCI(E) papers and numerous publications',
        '4 programming-related patents',
        'Executive roles in multiple academic societies'
      ],
      researchFields: [
        'AI Model Training', 'LLM', 'Web Client/Server & IS',
        'Project Management'
      ],
      review: 'Provides field-oriented education backed by 20+ years of experience.'
    }
  },
  // 생명의료시스템학과 교수진
  {
    id: 8,
    name: '이광호',
    title: '교수(생명의료시스템학과장)',
    isChair: true,
    phone: '031-696-8842',
    email: 'khlee17@kopo.ac.kr',
    mainSubjects: ['분자생물학', '의생명공정실무', '유전자조작실무'],
    education: '고려대학교 농화학과 학사 / 고려대학교 대학원 분자생물학 석사 / KAIST 생명화학공학 박사 / 서울대학교 경영대학원 CJ-MBA course 수료',
    career: [
      'CJ제일제당 BIO연구소 GreenBio1센터장',
      '총 경력 20년'
    ],
    achievements: [
      'L-라이신 생산방법 외 해외 특허등록 44건',
      'Molecular Systems Biology 외 해외논문 8편',
      '학술발표 12건'
    ],
    researchFields: ['미생물 대사공학(아미노산 및 핵산 생산균주 개발)', '발효공정 연구'],
    review: '현장 경험이 풍부하고 설명이 친절해 수업 이해가 잘 된다는 평이 많습니다. 핵심을 정리해 주셔서 실습 방향을 잡기 쉽다는 의견도 있습니다.',
    en: {
      title: 'Professor (Chair, Biomedical Systems Dept.)',
      mainSubjects: ['Molecular Biology', 'Bioprocess Practice', 'Genetic Engineering Practice'],
      education: 'B.S. Agricultural Chemistry, Korea Univ. / M.S. Molecular Biology, Korea Univ. / Ph.D. Chemical & Biological Engineering, KAIST / CJ-MBA, SNU',
      career: [
        'Head of GreenBio1 Center, CJ CheilJedang BIO Research Institute',
        '20 years of industry experience'
      ],
      achievements: [
        '44 international patents including L-lysine production',
        '8 international papers including Molecular Systems Biology',
        '12 academic presentations'
      ],
      researchFields: ['Microbial metabolic engineering', 'Fermentation process research'],
      review: 'Rich field experience and clear explanations help students grasp lab work effectively.'
    }
  },
  {
    id: 9,
    name: '김준석',
    title: '교수(교학처장)',
    isChair: false,
    phone: '031-696-8841',
    email: 'junskim@kopo.ac.kr',
    mainSubjects: ['HPLC밸리데이션', '의약품분석'],
    education: '미국 조지아주립대 분석화학 박사',
    career: [
      '삼성전자반도체 책임연구원',
      '한국과학기술연구원 박사후연구원',
      '오송첨단의료산업진흥재단 선임연구원',
      '총 경력 15년'
    ],
    achievements: ['Nature Methods 외 다수'],
    researchFields: ['HPLC를 이용한 의약품 분석연구', '바이오의약품 특성분석'],
    review: '실무 사례를 잘 풀어줘서 이해가 쉽고, 질문에 꼼꼼히 답해주신다는 평가가 있습니다. 자료 정리도 탄탄해서 시험 대비에 도움이 된다는 반응이 많습니다.',
    en: {
      title: 'Professor (Academic Affairs Director)',
      mainSubjects: ['HPLC Validation', 'Pharmaceutical Analysis'],
      education: 'Ph.D. in Analytical Chemistry, Georgia State University (USA)',
      career: [
        'Principal Researcher, Samsung Semiconductor',
        'Postdoctoral Researcher, KIST',
        'Senior Researcher, Osong Medical Innovation Foundation',
        '15 years of experience'
      ],
      achievements: ['Numerous publications including Nature Methods'],
      researchFields: ['HPLC-based drug analysis', 'Biopharmaceutical characterization'],
      review: 'Clear explanations with real-world cases and attentive feedback on questions.'
    }
  },
  {
    id: 10,
    name: '안정미',
    title: '교수',
    isChair: false,
    phone: '031-696-8843',
    email: 'ahnj@kopo.ac.kr',
    mainSubjects: ['세포배양실무', '세포생물학'],
    education: 'KAIST 생물공학 석사 / 텍사스주립의대(UTHSCSA) 암생물학 박사',
    career: [
      '텍사스주립대(UTSA) 박사후연구원',
      '텍사스주립의대(UTHSCSA IBT) 연구/강의 조교',
      '서울대학병원 임상의학연구소 연구원'
    ],
    achievements: [],
    researchFields: [
      '동물세포배양',
      '동물세포주 개발',
      '암생물학',
      '줄기세포 배양/분화',
      '쥐발생학',
      '동물세포의 약물반응',
      '유전자 발현 조절 연구'
    ],
    review: '차분하고 세심하게 지도해 주셔서 실습 이해도가 높아진다는 의견이 많습니다. 피드백이 빠르고 정확해서 공부 방향을 잡기 좋다는 말이 있습니다.',
    en: {
      title: 'Professor',
      mainSubjects: ['Cell Culture Practice', 'Cell Biology'],
      education: 'M.S. in Bioengineering, KAIST / Ph.D. in Cancer Biology, UTHSCSA',
      career: [
        'Postdoctoral Researcher, UTSA',
        'Research/Teaching Assistant, UTHSCSA IBT',
        'Researcher, Seoul National University Hospital'
      ],
      achievements: [],
      researchFields: [
        'Animal cell culture', 'Cell line development', 'Cancer biology',
        'Stem cell culture/differentiation', 'Embryology',
        'Drug response in animal cells', 'Gene expression regulation'
      ],
      review: 'Calm and attentive guidance improves practical understanding with precise feedback.'
    }
  },
  {
    id: 11,
    name: '권영삼',
    title: '외래교수',
    isChair: false,
    phone: '',
    email: 'gs20181653@kopo.ac.kr',
    mainSubjects: ['프로젝트실습(GMP교육)'],
    education: '중앙대학교 약학대학 약학과 학사',
    career: [
      '(현) (주)제테마 품질총괄임원',
      '(전) (주)휴메딕스 품질팀장',
      '(전) (주)한독 품질보증팀장, 품질관리팀장, 생산팀장'
    ],
    achievements: [],
    researchFields: [],
    review: '',
    en: {
      title: 'Adjunct Professor',
      mainSubjects: ['Project Practice (GMP Training)'],
      education: 'B.S. in Pharmacy, Chung-Ang University',
      career: [
        'SVP, Quality Division, Jetema Co., Ltd. (current)',
        'Former QA/QC team lead roles at Humedix and Handok'
      ],
      achievements: [],
      researchFields: [],
      review: ''
    }
  },
  {
    id: 12,
    name: '김세연',
    title: '외래교수',
    isChair: false,
    phone: '',
    email: 'gs20160388@kopo.ac.kr',
    mainSubjects: ['생화학', '프로젝트실습'],
    education: '이화여자대학교 과학교육학과(생물전공) 이학사 / 이화여자대학교 대학원 생물학 석사 / 일리노이주립대(UIUC) 미생물학 박사',
    career: [
      'CJ제일제당 BIO연구소 연구원'
    ],
    achievements: [],
    researchFields: ['L-라이신 생산균주 개발', '유전자 돌연변이를 이용한 단백질 구조와 기능에 관한 연구'],
    review: '',
    en: {
      title: 'Adjunct Professor',
      mainSubjects: ['Biochemistry', 'Project Practice'],
      education: 'B.S. Science Education (Biology), Ewha Womans Univ. / M.S. Biology, Ewha / Ph.D. Microbiology, UIUC',
      career: ['Researcher, CJ CheilJedang BIO Research Institute'],
      achievements: [],
      researchFields: ['L-lysine strain development', 'Protein structure via genetic mutation'],
      review: ''
    }
  },
  {
    id: 13,
    name: '정하종',
    title: '외래교수',
    isChair: false,
    phone: '',
    email: 'gs20181655@kopo.ac.kr',
    mainSubjects: ['프로젝트실습(GMP교육)'],
    education: '경희대학교 유전공학 학사',
    career: [
      '(현) (주)제테마 공장장',
      '(전) 대웅제약 나보타 cGMP 획득',
      '(전) 대웅제약 바이오의약품(EGF, hGH, EPO, BMP2)품목 허가',
      '(전) K-BIO 임상신약 생산센터 구축'
    ],
    achievements: [],
    researchFields: [],
    review: '',
    en: {
      title: 'Adjunct Professor',
      mainSubjects: ['Project Practice (GMP Training)'],
      education: 'B.S. in Genetic Engineering, Kyung Hee University',
      career: [
        'Plant Manager, Jetema Co., Ltd. (current)',
        'Led cGMP acquisition for DaeWoong Bio (Nabota)',
        'Handled approvals for biopharmaceuticals (EGF, hGH, EPO, BMP2)',
        'Built K-BIO clinical drug production center'
      ],
      achievements: [],
      researchFields: [],
      review: ''
    }
  }
];
