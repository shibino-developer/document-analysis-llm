from utils.loader import DocumentLoader
from utils.cleaner import TextCleaner
from utils.splitter import DocumentSplitter
from utils.retrieval.bm25 import BM25RetrieverService

loader = DocumentLoader()

documents = loader.load_file(
    "database/documents/AI.pdf"
)

cleaner = TextCleaner()
documents = cleaner.clean(documents)

splitter = DocumentSplitter()
chunks = splitter.split(documents)

bm25 = BM25RetrieverService()

bm25.build(chunks)
bm25.save()

results = bm25.search(
    "Artificial Intelligence"
)

print()

print(f"Results: {len(results)}")

print()

for doc in results:

    print(doc.metadata)

    print(doc.page_content[:200])

    print("-" * 50)