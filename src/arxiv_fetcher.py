import arxiv
from langchain_core.documents import Document


def fetch_arxiv_papers(query: str, max_docs: int = 10) -> list[Document]:
    """
    Fetch latest arXiv papers using the arxiv Python package directly.

    This returns LangChain Document objects containing paper metadata
    and summary text. Full PDF extraction can be added in the next step.
    """

    client = arxiv.Client()

    search = arxiv.Search(
        query=query,
        max_results=max_docs,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    documents: list[Document] = []

    for result in client.results(search):
        metadata = {
            "arxiv_id": result.entry_id.split("/")[-1],
            "title": result.title,
            "authors": [author.name for author in result.authors],
            "summary": result.summary,
            "published": str(result.published),
            "updated": str(result.updated),
            "pdf_url": result.pdf_url,
            "entry_id": result.entry_id,
            "categories": result.categories,
            "source": result.entry_id,
        }

        page_content = f"""
Title: {result.title}

Authors: {", ".join(author.name for author in result.authors)}

Published: {result.published}

Updated: {result.updated}

Categories: {", ".join(result.categories)}

Summary:
{result.summary}

PDF URL:
{result.pdf_url}
"""

        documents.append(
            Document(
                page_content=page_content.strip(),
                metadata=metadata,
            )
        )

    return documents