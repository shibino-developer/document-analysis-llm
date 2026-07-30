from utils.loader import DocumentLoader

loader = DocumentLoader()

documents = loader.load_file("database/documents/AI.pdf")

print(f"Loaded {len(documents)} document(s)\n")

for doc in documents:
    print(doc.metadata)