from langchain_huggingface import HuggingFaceEmbeddings

print("Loading model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

print("Model loaded.")

vector = embeddings.embed_query("What is Artificial Intelligence?")

print("Vector Length:", len(vector))
print("First 10 values:", vector[:10])