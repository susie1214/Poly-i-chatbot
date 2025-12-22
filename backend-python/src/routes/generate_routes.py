from flask import Blueprint, request, jsonify
import logging
import time
from datetime import datetime
from src.services.llm_service import generate_response, get_keyword_response
from src.services.rag_service import generate_rag_response, is_rag_initialized

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

        if not prompt:
            return jsonify({'error': 'prompt is required'}), 400

        # 요청 로깅
        start_time = time.time()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("\n" + "="*60)
        print(f"📥 새로운 요청 수신 [{timestamp}]")
        print(f"   사용자: {user_id}")
        print(f"   질문: {prompt}")
        print(f"   언어: {language}")
        print("="*60)

        # RAG 초기화 확인
        rag_initialized = is_rag_initialized()
        logger.info(f"RAG initialized: {rag_initialized}")

        # 먼저 키워드 기반 응답 확인 (빠른 응답 보장)
        keyword_resp = get_keyword_response(prompt, language)
        if keyword_resp:
            elapsed = time.time() - start_time
            print(f"\n✅ 키워드 매칭 성공 (소스: keyword)")
            print(f"⏱️  처리 시간: {elapsed:.2f}초")
            print(f"📤 응답: {keyword_resp['response'][:100]}...")
            print("="*60 + "\n")
            keyword_resp['user_id'] = user_id
            return jsonify(keyword_resp), 200

        # RAG 기반 응답 생성
        if rag_initialized:
            print(f"\n🔍 RAG 검색 시작...")
            response = generate_rag_response(
                query=prompt,
                language=language,
                k=3  # 검색 문서 개수: 5 → 3개로 감소
            )
            # 문서 정보 추가
            response['user_id'] = user_id
            response['tokens_used'] = response.get('tokens_used', 0)

            # 응답 로깅
            elapsed = time.time() - start_time
            print(f"\n✅ RAG 응답 생성 완료")
            print(f"   소스: {response.get('source', 'unknown')}")
            print(f"   토큰: {response.get('tokens_used', 0)}")
            print(f"   문서 수: {len(response.get('documents', []))}")
            print(f"⏱️  처리 시간: {elapsed:.2f}초")
            print(f"📤 응답 내용:")
            print("-"*60)
            print(response.get('response', '')[:500])
            if len(response.get('response', '')) > 500:
                print("... (이하 생략)")
            print("="*60 + "\n")

            return jsonify(response), 200
        else:
            # RAG 미초기화 시 기존 LLM 사용
            print(f"\n⚠️ RAG 미초기화 - Fallback LLM 사용")
            logger.info("Using fallback LLM response")
            response = generate_response(
                prompt=prompt,
                user_id=user_id,
                max_tokens=max_tokens,
                temperature=temperature,
                language=language
            )

            elapsed = time.time() - start_time
            print(f"\n✅ LLM 응답 생성 완료")
            print(f"⏱️  처리 시간: {elapsed:.2f}초")
            print(f"📤 응답: {response.get('response', '')[:200]}...")
            print("="*60 + "\n")

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
