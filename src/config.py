import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

ARXIV_QUERY = os.getenv(
    "ARXIV_QUERY",
    "cat:cs.AI OR cat:cs.CL OR cat:cs.LG",
)

ARXIV_MAX_DOCS = int(os.getenv("ARXIV_MAX_DOCS", "5"))

CHROMA_DIR = os.getenv("CHROMA_DIR", "data/chroma_db")
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "arxiv_ai_papers")

EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "local").lower()
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",
)

LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")