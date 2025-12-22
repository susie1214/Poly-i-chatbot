import os
import torch
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from transformers import AutoModel, AutoTokenizer

_models = {}


def initialize_models():
    """LLM/Embedding 모델 초기화."""
    global _models

    # LLM 로드 (GGUF)
    print("📥 Loading LLM Model...")
    try:
        from llama_cpp import Llama

        backend_root = Path(__file__).parent.parent.parent
        model_filename = 'Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf'
        model_path = os.getenv('LLM_MODEL_PATH')
        if not model_path:
            model_path = backend_root / 'models' / model_filename
        elif not os.path.isabs(model_path):
            model_path = backend_root / model_path
        model_path = str(model_path)

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")

        print(f"  Model path: {model_path}")
        print(f"  Model size: {os.path.getsize(model_path) / (1024**3):.2f} GB")

        _models['llm'] = Llama(
            model_path=model_path,
            n_gpu_layers=-1,  # -1 = 모든 레이어를 GPU에 로드 (40 → -1)
            n_ctx=4096,
            max_tokens=512,
            temperature=0.7,
            top_p=0.95,
            verbose=False,
        )
        print("✅ LLM Model loaded successfully")
        print(f"  GPU Available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"  GPU: {torch.cuda.get_device_name(0)}")
    except Exception as e:
        print(f"❌ Failed to load LLM Model: {e}")
        _models['llm'] = None

    # 임베딩 모델 로드 (기본: Qwen/Qwen3-Embedding-0.6B, GPU float16)
    print("📥 Loading Embedding Model...")
    embedding_name = (
        os.getenv('EMBEDDING_MODEL_NAME')
        or os.getenv('EMBEDDING_MODEL')
        or 'Qwen/Qwen3-Embedding-0.6B'
    )
    embedding_device_pref = os.getenv('EMBEDDING_DEVICE', 'auto')  # auto|cuda|cpu

    class HFEmbeddingModel:
        def __init__(self, model_id: str):
            self.model_id = model_id
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(
                    model_id,
                    local_files_only=False,
                    trust_remote_code=True
                )
            except Exception as e:
                print(f"⚠️ Failed to load tokenizer with trust_remote_code, trying without: {e}")
                self.tokenizer = AutoTokenizer.from_pretrained(
                    model_id,
                    local_files_only=False
                )

            device_map = "cuda" if embedding_device_pref == "cuda" or (embedding_device_pref == "auto" and torch.cuda.is_available()) else "cpu"
            dtype = torch.float16 if device_map == "cuda" else torch.float32

            try:
                self.model = AutoModel.from_pretrained(
                    model_id,
                    torch_dtype=dtype,
                    device_map=device_map,
                    local_files_only=False,
                    trust_remote_code=True,
                )
                self.device = self.model.device
            except Exception as e:
                if "CUDA out of memory" in str(e) or isinstance(e, torch.cuda.OutOfMemoryError):
                    print(f"⚠️ GPU OOM for embedding model; falling back to CPU")
                    self.model = AutoModel.from_pretrained(
                        model_id,
                        torch_dtype=torch.float32,
                        device_map="cpu",
                        local_files_only=False,
                        trust_remote_code=True,
                    )
                    self.device = self.model.device
                else:
                    # trust_remote_code 문제일 수 있음
                    print(f"⚠️ Failed with trust_remote_code, trying without: {e}")
                    self.model = AutoModel.from_pretrained(
                        model_id,
                        torch_dtype=dtype,
                        device_map=device_map,
                        local_files_only=False,
                    )
                    self.device = self.model.device

        def encode(self, texts, convert_to_numpy=True, show_progress_bar=False):
            if isinstance(texts, str):
                texts = [texts]
            vectors = []
            with torch.no_grad():
                for t in texts:
                    inputs = self.tokenizer(t, return_tensors="pt", truncation=True, padding=True)
                    inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
                    outputs = self.model(**inputs)
                    emb = outputs.last_hidden_state.mean(dim=1)  # mean pooling
                    if convert_to_numpy:
                        vectors.append(emb.squeeze(0).cpu().numpy())
                    else:
                        vectors.append(emb.squeeze(0))
            if convert_to_numpy:
                # numpy 배열로 변환하여 반환 (sentence-transformers와 동일한 형식)
                return np.vstack(vectors)
            return torch.stack(vectors)

    try:
        _models['embedding'] = HFEmbeddingModel(embedding_name)
        print(f"✅ Embedding Model loaded: {embedding_name} (device: {_models['embedding'].model.device})")
    except Exception as e:
        print(f"🚧 Failed to load embedding model ({embedding_name}): {e}")
        print("   Falling back to sentence-transformers/all-MiniLM-L6-v2...")
        try:
            _models['embedding'] = SentenceTransformer(
                'sentence-transformers/all-MiniLM-L6-v2',
                cache_folder='./models/embeddings',
                local_files_only=False,
            )
            print("✅ Embedding Model loaded: all-MiniLM-L6-v2")
        except Exception as e2:
            print(f"❌ Embedding model unavailable: {e2}")
            _models['embedding'] = None


def get_llm_model():
    return _models.get('llm')


def get_embedding_model():
    return _models.get('embedding')


def is_gpu_available():
    return torch.cuda.is_available()
