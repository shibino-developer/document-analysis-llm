from utils.document_storage import DocumentStorage

storage = DocumentStorage()

documents = storage.load_all_documents()

print("=" * 60)
print("DOCUMENTS LOADED:", len(documents))
print("=" * 60)

for i, doc in enumerate(documents, start=1):
    print(f"\nDocument {i}")
    print(doc.metadata)
    print(doc.page_content[:200])