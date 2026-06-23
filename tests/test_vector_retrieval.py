from src.vector_store import get_vector_store


def main():
    vector_store = get_vector_store()

    query = "What are recent research trends in large language models and agents?"

    results = vector_store.similarity_search(
        query=query,
        k=3,
    )

    print("Query:", query)
    print("Results:", len(results))

    for index, doc in enumerate(results, start=1):
        print("\n" + "=" * 100)
        print(f"Result {index}")
        print("-" * 100)
        print("Title:", doc.metadata.get("title"))
        print("arXiv ID:", doc.metadata.get("arxiv_id"))
        print("Published:", doc.metadata.get("published"))
        print("PDF:", doc.metadata.get("pdf_url"))
        print("\nContent Preview:")
        print(doc.page_content[:700])


if __name__ == "__main__":
    main()
