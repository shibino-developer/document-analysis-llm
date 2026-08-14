from utils.vectorstore import VectorStoreService
from utils.retrieval.reranker import CrossEncoderReranker


def main():

    print("=" * 70)
    print("TESTING CROSS ENCODER")
    print("=" * 70)

    vector_store = VectorStoreService()

    vector_store.load_vector_store()

    results = vector_store.similarity_search(
        "What is Machine Learning?",
        k=5,
    )

    reranker = CrossEncoderReranker()

    ranked = reranker.rerank_with_scores(
        query="What is Machine Learning?",
        documents=results,
        top_k=5,
    )

    print()
    print("=" * 70)
    print("RANKED RESULTS")
    print("=" * 70)

    for index, (score, document) in enumerate(
        ranked,
        start=1,
    ):

        print()
        print(f"Rank {index}")
        print("-" * 70)

        print(
            f"Cross Encoder Score: {float(score):.4f}"
        )

        print(
            f"Source: "
            f"{document.metadata.get('source', 'Unknown')}"
        )

        print(
            f"Page: "
            f"{document.metadata.get('page', '-')}"
        )

        print()

        print(
            document.page_content[:300]
        )

        print("-" * 70)


if __name__ == "__main__":
    main()