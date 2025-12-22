from flask import Blueprint, request, jsonify
import logging
from src.services.embedding_service import generate_embeddings

embed_bp = Blueprint('embed', __name__)
logger = logging.getLogger(__name__)


@embed_bp.route('/', methods=['POST'])
def embed():
    """
    임베딩 생성 API

    Request 예시:
    {
        "text": "단일 텍스트" 또는 "texts": ["문서1", "문서2"],
        "clean": true,
        "chunk": true,
        "max_len": 600,
        "overlap": 80,
        "reduce_dim": 256
    }
    """
    try:
        data = request.get_json(force=True)
        # 'text' 또는 'texts' 둘 다 지원
        texts = data.get('texts') or data.get('text') or []
        if isinstance(texts, str):
            texts = [texts]

        if not texts:
            return jsonify({'error': 'text or texts is required'}), 400

        result = generate_embeddings(
            texts=texts,
            do_clean=data.get('clean', True),
            do_chunk=data.get('chunk', True),
            max_len=int(data.get('max_len', 600)),
            overlap=int(data.get('overlap', 80)),
            reduce_dim=data.get('reduce_dim', 256),
        )

        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Embedding Error: {e}")
        return jsonify({'error': str(e)}), 500
