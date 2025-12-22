from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import flask.cli
from dotenv import load_dotenv
from src.routes.generate_routes import generate_bp
from src.routes.embed_routes import embed_bp
from src.models.model_manager import initialize_models
from src.services.rag_service import initialize_rag_system
import json

# 환경변수 로드
load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False  # 한글 깨짐 방지

# 콘솔 배너 출력 시 Windows 핸들 오류를 피하기 위해 배너 비활성화 및 컬러 출력 끔
flask.cli.show_server_banner = lambda *args, **kwargs: None
os.environ.setdefault("CLICOLOR", "0")
os.environ.setdefault("NO_COLOR", "1")
os.environ.setdefault("COLORAMA_DISABLE", "1")
os.environ.setdefault("TERM", "dumb")

# 모델 초기화
print("🔄 Loading LLM Model...")
initialize_models()

# RAG 시스템 초기화
print("🔄 Initializing RAG system...")
rag_initialized = initialize_rag_system()
if rag_initialized:
    print("✅ RAG system initialized successfully")
else:
    print("⚠️ RAG system initialization failed, using fallback LLM")

# Blueprint 등록
app.register_blueprint(generate_bp, url_prefix='/generate')
app.register_blueprint(embed_bp, url_prefix='/embed')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'OK',
        'service': 'Poly-i Python LLM Server',
        'timestamp': __import__('datetime').datetime.now().isoformat(),
        'rag_initialized': rag_initialized
    })

@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        'model': 'Meta-Llama-3.1-8B-Instruct',
        'quantization': 'GGUF (Q4_K_M)',
        'embedding_model': os.getenv('EMBEDDING_MODEL_NAME', 'Qwen/Qwen3-Embedding-0.6B'),
        'rag_system': 'Enabled' if rag_initialized else 'Disabled',
        'max_tokens': 512,
        'device': 'cuda' if __import__('torch').cuda.is_available() else 'cpu'
    })

if __name__ == '__main__':
    port = int(os.getenv('PYTHON_PORT', 5001))
    print(f"🚀 Starting Python LLM Server on port {port}")
    # Windows 콘솔 핸들 오류를 피하기 위해 reloader/디버거 비활성화
    app.run(
        debug=False,
        use_reloader=False,
        port=port,
        host='0.0.0.0'
    )
