import os

from src.services.rag_service import initialize_rag_system


def main():
    os.environ.setdefault("RAG_CACHE_MODE", "refresh")
    ok = initialize_rag_system()
    if not ok:
        raise SystemExit("RAG cache build failed")
    print("RAG cache build complete.")


if __name__ == "__main__":
    main()
