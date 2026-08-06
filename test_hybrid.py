from utils.loader import DocumentLoader
from utils.cleaner import TextCleaner
from utils.splitter import DocumentSplitter
from utils.vectorstore import VectorStoreService

from utils.retrieval.bm25 import BM25RetrieverService
from utils.retrieval.hybrid import HybridRetriever

loader = DocumentLoader()

documents = loader.load_file(
    "database/documents/AI.pdf"
)

documents = TextCleaner().clean(documents)

chunks = DocumentSplitter().split(documents)

# Build BM25
bm25 = BM25RetrieverService()
bm25.build(chunks)
bm25.save()

# Build FAISS
vector_store = VectorStoreService()
vector_store.create_vector_store(chunks)

# Hybrid
hybrid = HybridRetriever(
    vector_store,
    bm25,
)

results = hybrid.search(
    "Artificial Intelligence"
)

print()

print(f"Retrieved: {len(results)}")

for doc in results:

    print(doc.metadata)

    print(doc.page_content[:150])

    print("-" * 50)