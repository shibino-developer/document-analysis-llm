"""
test_rag.py

Test the complete RAG pipeline.
"""

from utils.rag import RAGService


def main():

    # ---------------------------------------------------------
    # Initialize RAG
    # ---------------------------------------------------------

    rag = RAGService()

    # ---------------------------------------------------------
    # Ask Question
    # ---------------------------------------------------------

    question = "Explain Retrieval Augmented Generation."

    answer, retrieved_chunks = rag.answer(
        question=question,
        chat_history=[],
        top_k=5,
    )

    # ---------------------------------------------------------
    # Display Answer
    # ---------------------------------------------------------

    print("\n" + "=" * 80)
    print("QUESTION")
    print("=" * 80)
    print(question)

    print("\n" + "=" * 80)
    print("ANSWER")
    print("=" * 80)
    print(answer)

    # ---------------------------------------------------------
    # Display Retrieved Chunks
    # ---------------------------------------------------------

    print("\n" + "=" * 80)
    print("RETRIEVED CHUNKS")
    print("=" * 80)

    for i, chunk in enumerate(retrieved_chunks, start=1):

        print(f"\nChunk {i}")

        print("-" * 80)

        print("Metadata:")
        print(chunk.metadata)

        print("\nContent:")
        print(chunk.page_content[:500])

        print("-" * 80)

    print("\nCompressed Context\n")

    for chunk in retrieved_chunks:

        print("-" * 60)

        print(chunk.page_content)

        print()

if __name__ == "__main__":
    main()