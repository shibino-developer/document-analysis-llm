from utils.document_storage import DocumentStorage
from utils.retrieval.filter import MetadataFilter

storage = DocumentStorage()

documents = storage.load_all_documents()

print("=" * 60)
print("ALL DOCUMENTS")
print("=" * 60)

for doc in documents:
    print(doc.metadata)

print("\n")

# ----------------------------------------------------
# Test 1: Filter by filename
# ----------------------------------------------------

filtered = MetadataFilter.filter(
    documents,
    filename="AI.pdf",
)

print("=" * 60)
print("FILTER: AI.pdf")
print("=" * 60)

for doc in filtered:
    print(doc.metadata)

print("Total:", len(filtered))

print("\n")

# ----------------------------------------------------
# Test 2: Filter by page
# ----------------------------------------------------

filtered = MetadataFilter.filter(
    documents,
    page=2,
)

print("=" * 60)
print("FILTER: Page 2")
print("=" * 60)

for doc in filtered:
    print(doc.metadata)

print("Total:", len(filtered))

print("\n")

# ----------------------------------------------------
# Test 3: Filter by file type
# ----------------------------------------------------

filtered = MetadataFilter.filter(
    documents,
    file_type="pdf",
)

print("=" * 60)
print("FILTER: PDF")
print("=" * 60)

for doc in filtered:
    print(doc.metadata)

print("Total:", len(filtered))