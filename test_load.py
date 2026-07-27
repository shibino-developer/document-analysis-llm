from utils.vectorstore import VectorStoreService

vs = VectorStoreService()

vs.load_vector_store()

print("Vector Store Loaded Successfully!")

print("Vectors:", vs.vector_count())