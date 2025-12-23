from flask import Blueprint, request, jsonify
import logging
import time
from datetime import datetime
from src.services.llm_service import generate_response, get_keyword_response
from src.services.rag_service import generate_rag_response, is_rag_initialized
try:
    from src.services.langgraph_service import invoke_graph
    LANGGRAPH_AVAILABLE = True
except Exception:
    invoke_graph = None
    LANGGRAPH_AVAILABLE = False

generate_bp = Blueprint('generate', __name__)
logger = logging.getLogger(__name__)

# Agent 모듈은 선택적으로 사용 (오류 발생 시 서버 다운 방지)
AGENT_AVAILABLE = False
try:
    from src.services.agent import invoke_agent, initialize_agent
    if initialize_agent():
        AGENT_AVAILABLE = True
        logger.info("Agent module loaded successfully")
except Exception as e:
    logger.warning(f"⚠️ Agent module not available (will use fallback): {e}")

@generate_bp.route('/', methods=['POST'])
def generate():
    """
    텍스트 생성 엔드포인트 (RAG + Agent 기반)
    
    Request:
    {
        "prompt": "질문 또는 프롬프트",
        "user_id": "사용자ID (선택사항)",
        "max_tokens": 256,
        "temperature": 0.7,
        "language": "ko" 또는 "en"
    }
    
    Response:
    {
        "response": "생성된 응답",
        "tokens_used": 123,
        "model": "LLM",
        "language": "ko",
        "source": "rag_llm" 또는 "keyword" 또는 "llm"
    }
    """
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        user_id = data.get('user_id', 'default')
        max_tokens = data.get('max_tokens', 256)
        temperature = data.get('temperature', 0.7)
        language = data.get('language', 'ko')  # 기본값: 한국어
        source = data.get('source', 'text')

        if not prompt:
            return jsonify({'error': 'prompt is required'}), 400

        # request log (ASCII only)
        start_time = time.time()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("\n" + "=" * 60)
        print(f"[Request] {timestamp}")
        print(f"  user_id: {user_id}")
        print(f"  prompt : {prompt}")
        print(f"  lang   : {language}")
        print("=" * 60)

        # RAG 초기화 확인
        rag_initialized = is_rag_initialized()
        logger.info(f"RAG initialized: {rag_initialized}")

        button_request = source == 'button'
        if button_request:
            response = generate_response(
                prompt=prompt,
                user_id=user_id,
                max_tokens=max_tokens,
                temperature=temperature,
                language=language,
            )
            if response.get('error') == 'model_not_loaded':
                button_request = False

        # LangGraph flow: keyword -> RAG -> LLM fallback
        if not button_request:
            if LANGGRAPH_AVAILABLE and invoke_graph:
                response = invoke_graph(
                    prompt=prompt,
                    language=language,
                    user_id=user_id,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
            else:
                keyword_resp = get_keyword_response(prompt, language)
                if keyword_resp:
                    keyword_resp["user_id"] = user_id
                    response = keyword_resp
                elif rag_initialized:
                    response = generate_rag_response(query=prompt, language=language, k=3)
                    response["user_id"] = user_id
                    response["tokens_used"] = response.get("tokens_used", 0)
                else:
                    response = generate_response(
                        prompt=prompt,
                        user_id=user_id,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        language=language,
                    )

        elapsed = time.time() - start_time
        print("\n[Response] done")
        print(f"  source : {response.get('source', 'unknown')}")
        print(f"  tokens : {response.get('tokens_used', 0)}")
        print(f"  docs   : {len(response.get('documents', []))}")
        print(f"  time   : {elapsed:.2f}s")
        print("  preview:")
        print("-" * 60)
        print(response.get('response', '')[:500])
        if len(response.get('response', '')) > 500:
            print("... (truncated)")
        print("=" * 60 + "\n")
        return jsonify(response), 200        
    except Exception as e:
        # 에러 로깅
        print("\n" + "="*60)
        print(f"❌ 오류 발생!")
        print(f"   에러: {str(e)}")
        print("="*60 + "\n")

        logger.error(f"Generation error: {e}", exc_info=True)
        lang = 'ko'
        try:
            if 'data' in locals() and data:
                lang = data.get('language', 'ko')
        except:
            pass
        return jsonify({
            'error': str(e),
            'language': lang
        }), 500
