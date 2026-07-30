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
import os
import shutil

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from utils.embeddings import EmbeddingService


class VectorStoreService:
    """
    Handles FAISS vector database operations.
    """

    DEFAULT_INDEX_PATH = "database/knowledge_base/faiss_index"

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
    # Add Documents
    # ---------------------------------------------------------

    def add_documents(
        self,
        documents: List[Document]
    ):
        """
        Add new documents to the existing vector store.
        """

        if self.vectorstore is None:
            raise ValueError(
                "Vector store is not loaded."
            )

        self.vectorstore.add_documents(
            documents
            )
    # Save
    # ---------------------------------------------------------

    def save_vector_store(
        self,
        folder_path: str = DEFAULT_INDEX_PATH,
    ):
        """
        Save the FAISS vector store to disk.
        """

        if self.vectorstore is None:
            raise ValueError(
                "Vector store has not been created."
            )

        os.makedirs(folder_path, exist_ok=True)
        self.vectorstore.save_local(folder_path)


    # ---------------------------------------------------------
    # Load
    # ---------------------------------------------------------

    def load_vector_store(
        self,
        folder_path: str = DEFAULT_INDEX_PATH,
    ):
        """
        Load existing FAISS vector store.
        """

        if not os.path.exists(folder_path):
            raise FileNotFoundError(
            "No saved vector store found."
        )

        self.vectorstore = FAISS.load_local(folder_path,self.embedding_model,allow_dangerous_deserialization=True)

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

    def delete_vector_store(
        self,
        folder_path: str = DEFAULT_INDEX_PATH,
    ):
       """Delete the saved vector store."""
       if os.path.exists(folder_path):
           shutil.rmtree(folder_path)

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

        return (self.index_path.exists() and any(self.index_path.iterdir()))

    def vector_store_exists(
        self,
        folder_path: str = DEFAULT_INDEX_PATH,
    ):
        """Check whether a saved vector store exists."""

        return (os.path.exists(folder_path) and len(os.listdir(folder_path)) > 0)
    
        # ---------------------------------------------------------
    # Storage Size
    # ---------------------------------------------------------

    def storage_size(self) -> int:
        """
        Return the size of the saved FAISS index in bytes.
        """

        if not self.index_path.exists():
            return 0

        total_size = 0

        for file in self.index_path.rglob("*"):
            if file.is_file():
                total_size += file.stat().st_size

        return total_size