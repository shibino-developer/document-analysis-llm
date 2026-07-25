"""
vectorstore.py

FAISS Vector Store Service

Responsibilities
----------------
- Create FAISS vector database
- Save vector database
- Load vector database
- Perform similarity search
- Delete vector database
"""

from pathlib import Path
from typing import List

import shutil

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from utils.embeddings import EmbeddingService


class VectorStoreService:
    """
    Handles FAISS vector database operations.
    """

    DEFAULT_INDEX_PATH = "database/faiss_index"

    def __init__(
        self,
        index_path: str = DEFAULT_INDEX_PATH,
    ):

        self.index_path = Path(index_path)

        self.embedding_service = EmbeddingService()

        self.embedding_model = (
            self.embedding_service.get_embedding_model()
        )

        self.vectorstore = None

    # ---------------------------------------------------------
    # Create
    # ---------------------------------------------------------

    def create_vector_store(
        self,
        documents: List[Document]
    ) -> FAISS:
        """
        Create FAISS vector store from documents.
        """

        self.vectorstore = FAISS.from_documents(
            documents=documents,
            embedding=self.embedding_model,
        )

        return self.vectorstore

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    def save_vector_store(self):
        """
        Save FAISS index to disk.
        """

        if self.vectorstore is None:
            raise ValueError(
                "Vector store has not been created."
            )

        self.index_path.mkdir(
            parents=True,
            exist_ok=True
        )

        self.vectorstore.save_local(
            str(self.index_path)
        )

        print(
            f"Vector store saved to {self.index_path}"
        )

    # ---------------------------------------------------------
    # Load
    # ---------------------------------------------------------

    def load_vector_store(self) -> FAISS:
        """
        Load existing FAISS vector store.
        """

        if not self.index_path.exists():
            raise FileNotFoundError(
                "Vector store not found."
            )

        self.vectorstore = FAISS.load_local(
            str(self.index_path),
            self.embedding_model,
            allow_dangerous_deserialization=True,
        )

        return self.vectorstore

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    def similarity_search(
        self,
        query: str,
        k: int = 3,
    ) -> List[Document]:
        """
        Return top-k similar documents.
        """

        if self.vectorstore is None:
            raise ValueError(
                "Vector store is not loaded."
            )

        return self.vectorstore.similarity_search(
            query,
            k=k,
        )

    # ---------------------------------------------------------
    # Search With Scores
    # ---------------------------------------------------------

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 3,
    ):
        """
        Return documents with similarity scores.
        """

        if self.vectorstore is None:
            raise ValueError(
                "Vector store is not loaded."
            )

        return self.vectorstore.similarity_search_with_score(
            query,
            k=k,
        )

    # ---------------------------------------------------------
    # Delete
    # ---------------------------------------------------------

    def delete_vector_store(self):
        """
        Delete saved FAISS index.
        """

        if self.index_path.exists():
            shutil.rmtree(self.index_path)

            print("Vector store deleted.")

    # ---------------------------------------------------------
    # Information
    # ---------------------------------------------------------

    def vector_count(self) -> int:
        """
        Number of vectors in memory.
        """

        if self.vectorstore is None:
            return 0

        return self.vectorstore.index.ntotal

    def exists(self) -> bool:
        """
        Check whether saved index exists.
        """

        return self.index_path.exists()