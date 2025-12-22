"""
LangGraph Agent를 사용한 지능형 챗봇
"""

import logging
from typing import Dict, Any, List, Literal
from enum import Enum

from langgraph.graph import StateGraph
from langgraph.graph import START, END

from typing_extensions import TypedDict

from src.services.rag_service import generate_rag_response, is_rag_initialized
from src.services.llm_service import generate_response, get_keyword_response

logger = logging.getLogger(__name__)

class QueryType(Enum):
    """쿼리 타입 분류"""
    PARKING = "parking"
    DINING = "dining"
    ALLOWANCE = "allowance"
    LOCATION = "location"
    CURRICULUM = "curriculum"
    FACULTY = "faculty"
    DEPARTMENT_INFO = "department_info"
    GENERAL = "general"

class AgentState(TypedDict):
    """Agent 상태"""
    question: str
    language: str
    query_type: QueryType
    response: str
    context: List[Dict[str, Any]]
    source: str
    step: int

class PolyiAgent:
    """Poly-i 지능형 에이전트"""
    
    def __init__(self):
        self.graph = self._build_graph()
        
    def _build_graph(self) -> StateGraph:
        """LangGraph 구성"""
        workflow = StateGraph(AgentState)
        
        # 노드 정의
        workflow.add_node("classify", self._classify_query)
        workflow.add_node("keyword_search", self._keyword_search)
        workflow.add_node("rag_search", self._rag_search)
        workflow.add_node("web_search", self._web_search)
        workflow.add_node("generate_response", self._generate_response)
        
        # 엣지 정의 (라우팅)
        workflow.add_edge(START, "classify")
        workflow.add_conditional_edges(
            "classify",
            self._route_to_search,
            {
                "keyword": "keyword_search",
                "rag": "rag_search",
                "web": "web_search",
            }
        )
        workflow.add_edge("keyword_search", "generate_response")
        workflow.add_edge("rag_search", "generate_response")
        workflow.add_edge("web_search", "generate_response")
        workflow.add_edge("generate_response", END)
        
        return workflow.compile()
    
    def _classify_query(self, state: AgentState) -> AgentState:
        """
        쿼리 분류
        """
        question = state['question'].lower()

        # 한국어 키워드 분류
        if '주차' in question:
            state['query_type'] = QueryType.PARKING
        elif '식사' in question or '식당' in question or '점심' in question:
            state['query_type'] = QueryType.DINING
        elif '훈련장려금' in question or '훈련수당' in question or '교통비' in question:
            state['query_type'] = QueryType.ALLOWANCE
        elif '위치' in question or '주소' in question or '오시는 길' in question:
            state['query_type'] = QueryType.LOCATION
        elif '학과 소개' in question or '학과' in question:
            state['query_type'] = QueryType.DEPARTMENT_INFO
        elif '교육과정' in question or '프로그램' in question or '과정' in question:
            state['query_type'] = QueryType.CURRICULUM
        elif '교수' in question or '강사' in question:
            state['query_type'] = QueryType.FACULTY
        else:
            state['query_type'] = QueryType.GENERAL

        logger.info(f"Query classified as: {state['query_type'].value}")
        return state
    
    def _route_to_search(self, state: AgentState) -> str:
        """
        검색 방법 결정
        """
        if state['query_type'] == QueryType.DEPARTMENT_INFO:
            return "web"
            
        if state['query_type'] in [
            QueryType.PARKING,
            QueryType.DINING,
            QueryType.ALLOWANCE,
            QueryType.LOCATION
        ]:
            return "keyword"
        else:
            return "rag"
    
    def _keyword_search(self, state: AgentState) -> AgentState:
        """
        키워드 기반 검색
        """
        result = get_keyword_response(state['question'], state['language'])
        
        if result:
            state['response'] = result.get('response', '')
            state['source'] = 'keyword'
            state['context'] = []
        else:
            # 키워드 매칭 실패 시 RAG로 폴백
            state = self._rag_search(state)
        
        return state

    def _web_search(self, state: AgentState) -> AgentState:
        """
        웹 검색을 통해 정보 가져오기 (현재는 시뮬레이션)
        """
        question = state['question']
        language = state['language']
        
        logger.info(f"Performing simulated web search for: {question}")
        
        # TODO: 실제 web_fetch tool을 사용하여 동적으로 웹사이트 정보 스크래핑
        # 현재는 기능 시뮬레이션을 위해 미리 정의된 텍스트를 사용합니다.
        scraped_data = """
        분당폴리텍융합기술교육원에는 다음과 같은 학과들이 있습니다:
        - AI융합과: AI 모델링, AI 서비스 개발, AI 플랫폼 구축 및 운영을 위한 교육 제공
        - 생명의료시스템과: 의료기기 소프트웨어, 의료용 앱, 의료 데이터 분석 전문가 양성
        - 로봇융합과: 지능형 로봇 설계, 제작, 제어 및 자동화 시스템 구축 교육
        자세한 정보는 홈페이지(https://www.kopo.ac.kr/ctc/content.do?menu=8209)를 참고하세요.
        """
        
        prompt = f"""
        다음은 웹사이트에서 가져온 정보입니다:
        ---
        {scraped_data}
        ---
        이 정보를 바탕으로 다음 질문에 한국어로 친절하게 답변해주세요: {question}
        """
        
        result = generate_response(prompt, language=language)
        
        state['response'] = result.get('response', '웹에서 정보를 가져오는 데 실패했습니다.')
        state['source'] = 'web_search'
        state['context'] = [{'content': scraped_data, 'source': 'https://www.kopo.ac.kr/ctc/index.do'}]
        
        return state
    
    def _rag_search(self, state: AgentState) -> AgentState:
        """
        RAG 기반 검색
        """
        if not is_rag_initialized():
            logger.warning("RAG system not initialized, falling back to web search.")
            return self._web_search(state)

        result = generate_rag_response(
            state['question'],
            language=state['language'],
            k=5
        )
        state['response'] = result.get('response', '')
        state['source'] = result.get('source', 'rag')
        state['context'] = result.get('documents', [])
        
        return state
    
    def _generate_response(self, state: AgentState) -> AgentState:
        """
        최종 응답 생성 (이미 이전 단계에서 완성됨)
        """
        state['step'] = state.get('step', 0) + 1
        return state
    
    async def invoke(self, question: str, language: str = 'ko') -> Dict[str, Any]:
        """
        에이전트 실행
        
        Args:
            question: 사용자 질문
            language: 언어 ('ko' 또는 'en')
        
        Returns:
            응답 딕셔너리
        """
        initial_state: AgentState = {
            'question': question,
            'language': language,
            'query_type': QueryType.GENERAL,
            'response': '',
            'context': [],
            'source': 'unknown',
            'step': 0
        }
        
        result = self.graph.invoke(initial_state)
        
        return {
            'response': result['response'],
            'source': result['source'],
            'query_type': result['query_type'].value,
            'context': result['context'],
            'language': language
        }

# 전역 에이전트 인스턴스
_agent = None

def initialize_agent():
    """에이전트 초기화"""
    global _agent
    try:
        _agent = PolyiAgent()
        logger.info("✅ Poly-i Agent initialized")
        return True
    except Exception as e:
        logger.error(f"❌ Agent initialization error: {e}")
        return False

def get_agent() -> PolyiAgent:
    """에이전트 인스턴스 반환"""
    global _agent
    if _agent is None:
        initialize_agent()
    return _agent

async def invoke_agent(question: str, language: str = 'ko') -> Dict[str, Any]:
    """
    에이전트 실행 (비동기)
    
    Args:
        question: 사용자 질문
        language: 언어
    
    Returns:
        응답 딕셔너리
    """
    agent = get_agent()
    if agent is None:
        return {
            'response': '에이전트를 초기화할 수 없습니다.' if language == 'ko' else 'Cannot initialize agent.',
            'source': 'error',
            'language': language
        }
    
    return await agent.invoke(question, language)
