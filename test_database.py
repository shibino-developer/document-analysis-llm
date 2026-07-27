from utils.vectorstore import VectorStoreService

vs = VectorStoreService()

print("Database Exists:", vs.vector_store_exists())