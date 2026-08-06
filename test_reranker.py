from utils.loader import DocumentLoader
from utils.cleaner import TextCleaner
from utils.splitter import DocumentSplitter
from utils.vectorstore import VectorStoreService

from utils.retrieval.bm25 import BM25RetrieverService
from utils.retrieval.hybrid import HybridRetriever
from utils.retrieval.reranker import CrossEncoderReranker

loader = DocumentLoader()

documents = loader.load_file(
    "database/documents/AI.pdf"
)

documents = TextCleaner().clean(
    documents
)

chunks = DocumentSplitter().split(
    documents
)

# BM25

bm25 = BM25RetrieverService()

bm25.build(chunks)
bm25.save()

# FAISS

vector_store = VectorStoreService()

vector_store.create_vector_store(
    chunks
)

# Hybrid

hybrid = HybridRetriever(
    vector_store,
    bm25,
)

results = hybrid.search(
    "What is Artificial Intelligence?",
    k=10,
)

print()

print("Before reranking")

print(len(results))

# Cross Encoder

reranker = CrossEncoderReranker()

results = reranker.rerank(
    "What is Artificial Intelligence?",
    results,
)

print()

print("After reranking")

print(len(results))

print()

for document in results:

    print(document.metadata)

    print(document.page_content[:250])

    print("-" * 80)