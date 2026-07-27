from utils.vectorstore import VectorStoreService

vs = VectorStoreService()

vs.delete_vector_store()

print("Deleted!")

print(vs.vector_store_exists())