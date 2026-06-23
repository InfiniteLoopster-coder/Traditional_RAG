from src.config import EMBEDDING_MODEL, EMBEDDING_PROVIDER
from src.vector_store import get_embedding_model


def main():
    print("Embedding Provider:", EMBEDDING_PROVIDER)
    print("Embedding Model:", EMBEDDING_MODEL)

    embedding_model = get_embedding_model()

    sample_text = "Retrieval augmented generation helps LLMs answer using external documents."

    vector = embedding_model.embed_query(sample_text)

    print("Embedding generated successfully.")
    print("Vector dimension:", len(vector))
    print("Vector preview:", vector[:5])


if __name__ == "__main__":
    main()