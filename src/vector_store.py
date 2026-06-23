from uuid import NAMESPACE_URL, uuid5

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings

from src.config import (
    CHROMA_COLLECTION,
    CHROMA_DIR,
    EMBEDDING_MODEL,
    EMBEDDING_PROVIDER,
    OPENAI_API_KEY,
)


def get_embedding_model():
    """
    Initialize embedding model based on EMBEDDING_PROVIDER.

    Supported providers:
    - local: HuggingFace sentence-transformers model
    - openai: OpenAI embedding model
    """

    if EMBEDDING_PROVIDER == "local":
        return HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    if EMBEDDING_PROVIDER == "openai":
        if not OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is missing. Add it to .env or use EMBEDDING_PROVIDER=local."
            )

        return OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            api_key=OPENAI_API_KEY,
        )

    raise ValueError(
        f"Unsupported EMBEDDING_PROVIDER='{EMBEDDING_PROVIDER}'. "
        "Use 'local' or 'openai'."
    )


def get_vector_store() -> Chroma:
    """
    Initialize Chroma vector store with the selected embedding model.
    """

    embedding_model = get_embedding_model()

    return Chroma(
        collection_name=CHROMA_COLLECTION,
        embedding_function=embedding_model,
        persist_directory=CHROMA_DIR,
    )


def create_chunk_id(document: Document) -> str:
    """
    Create deterministic chunk ID to reduce duplicate storage across daily runs.
    """

    arxiv_id = document.metadata.get("arxiv_id", "")
    chunk_index = str(document.metadata.get("chunk_index", ""))
    content_preview = document.page_content[:300]

    unique_text = f"{arxiv_id}|{chunk_index}|{content_preview}"

    return str(uuid5(NAMESPACE_URL, unique_text))


def store_chunks(chunks: list[Document]) -> int:
    """
    Store chunks into Chroma vector database.
    """

    if not chunks:
        return 0

    vector_store = get_vector_store()

    ids = [create_chunk_id(chunk) for chunk in chunks]

    vector_store.add_documents(
        documents=chunks,
        ids=ids,
    )

    return len(chunks)