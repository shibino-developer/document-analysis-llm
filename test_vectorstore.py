"""
test_vectorstore.py

Tests the complete pipeline:

PDF
    ↓
Loader
    ↓
Cleaner
    ↓
Splitter
    ↓
Embeddings
    ↓
FAISS Vector Store
    ↓
Similarity Search
"""

from utils.loader import DocumentLoader
from utils.cleaner import TextCleaner
from utils.splitter import DocumentSplitter
from utils.vectorstore import VectorStoreService


def main():

    print("=" * 80)
    print("STEP 1 : Loading Document")
    print("=" * 80)

    loader = DocumentLoader()

    with open("AI.pdf", "rb") as file:
        documents = loader.load(file)

    print(f"Loaded Documents : {len(documents)}")

    print("\nMetadata")

    for doc in documents:
        print(doc.metadata)

    print("\n" + "=" * 80)
    print("STEP 2 : Cleaning Text")
    print("=" * 80)

    cleaner = TextCleaner()

    cleaned_documents = cleaner.clean(documents)

    print("Cleaning Completed.")

    print("\n" + "=" * 80)
    print("STEP 3 : Splitting into Chunks")
    print("=" * 80)

    splitter = DocumentSplitter()

    chunks = splitter.split(cleaned_documents)

    print(f"Total Chunks : {len(chunks)}")

    print("\nGenerated Chunks\n")

    for i, chunk in enumerate(chunks, start=1):

        print("=" * 50)
        print(f"Chunk {i}")
        print("=" * 50)

        print(f"Characters : {len(chunk.page_content)}")

        print("\nMetadata")

        print(chunk.metadata)

        print("\nPreview")

        preview = chunk.page_content[:300]

        print(preview)

        print("\n")

    print("=" * 80)
    print("STEP 4 : Creating FAISS Vector Store")
    print("=" * 80)

    vector_store = VectorStoreService()

    vector_store.create_vector_store(chunks)

    vector_store.save_vector_store()

    print("\nVector Store Created Successfully")

    print(f"Vectors Stored : {vector_store.vector_count()}")

    print("\n" + "=" * 80)
    print("STEP 5 : Semantic Search")
    print("=" * 80)

    query = "What is Artificial Intelligence?"

    print(f"Query : {query}")

    results = vector_store.similarity_search(
        query=query,
        k=2,
    )

    print(f"\nRetrieved Results : {len(results)}")

    for i, result in enumerate(results, start=1):

        print("\n" + "=" * 60)
        print(f"Result {i}")
        print("=" * 60)

        print("Metadata")

        print(result.metadata)

        print("\nCharacters")

        print(len(result.page_content))

        print("\nContent")

        print(result.page_content)

    print("\n" + "=" * 80)
    print("Pipeline Executed Successfully")
    print("=" * 80)


if __name__ == "__main__":
    main()