from utils.rag import RAGService


def main():

    print("=" * 80)
    print("STREAMING RAG TEST")
    print("=" * 80)

    rag = RAGService()

    question = "What is Machine Learning?"

    stream, sources = rag.stream_answer(
        question=question,
        chat_history=[],
        top_k=5,
    )

    print("\nANSWER\n")
    print("-" * 80)

    for chunk in stream:

        print(chunk, end="", flush=True)

    print("\n")
    print("=" * 80)

    print("RETRIEVED SOURCES")
    print("=" * 80)

    for i, document in enumerate(
        sources,
        start=1,
    ):

        print(f"\nSource {i}")

        print(document.metadata)

        print(
            document.page_content[:300]
        )

        print("-" * 80)


if __name__ == "__main__":
    main()