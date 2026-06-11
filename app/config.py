from pydantic_settings import BaseSettings

class Settings(BaseSettings):
        OPENAI_API_KEY: str = ""
        OLLAMA_HOST: str = "http://127.0.0.1:11434"
        OLLAMA_MODEL: str = "qwen2.5:3b"
        OLLAMA_TIMEOUT: int = 120
        CHROMA_DIR: str = "data/indexes/chroma"
        FAISS_DIR: str = "data/indexes/faiss_index"
        BM25_PATH: str ="data/indexes/bm25_index.pkl"
        CHUNK_SIZE: int = 800
        CHUNK_OVERLAP: int = 100

        class Config:
                env_file = ".env"

#settings = Settings()

