from utils.metadata import MetadataManager

manager = MetadataManager()

manager.save(
    {
        "documents": [
            "AI.pdf",
            "ML.pdf"
        ],
        "chunks": 20,
        "vectors": 20
    }
)

print(manager.load())