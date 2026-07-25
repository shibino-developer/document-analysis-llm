from utils.loader import DocumentLoader
from utils.cleaner import TextCleaner
from utils.splitter import DocumentSplitter
from utils.embeddings import EmbeddingService

loader = DocumentLoader()

with open("AI.pdf", "rb") as file:
    documents = loader.load(file)

cleaner = TextCleaner()
documents = cleaner.clean(documents)

splitter = DocumentSplitter()
chunks = splitter.split(documents)

embedding_service = EmbeddingService()

vectors = embedding_service.embed_langchain_documents(chunks)

print("=" * 60)

print(f"Total Chunks      : {len(chunks)}")
print(f"Total Vectors     : {len(vectors)}")
print(f"Vector Dimension  : {len(vectors[0])}")

print("\nFirst Chunk Metadata")
print("-" * 30)
print(chunks[0].metadata)

print("\nFirst Chunk Preview")
print("-" * 30)
print(repr(chunks[0].page_content[:200]))

print("\nFirst 10 Values of First Vector")
print("-" * 30)
print(vectors[0][:10])

print("=" * 60)