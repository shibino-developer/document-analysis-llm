"""
embeddings.py

Provides a reusable embedding service for the Document Analysis
using LLMs project.

This module loads a HuggingFace Sentence Transformer model
and exposes helper methods for generating embeddings.
"""

from typing import List

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingService:
    """
    Embedding Service

    Responsibilities
    ----------------
    - Load embedding model
    - Generate query embeddings
    - Generate text embeddings
    - Extract text from LangChain Documents
    - Return embedding model for FAISS
    """

    DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        device: str = "cpu",
        normalize_embeddings: bool = True,
    ):
        """
        Initialize embedding model.

        Parameters
        ----------
        model_name : str
            HuggingFace model name

        device : str
            cpu or cuda

        normalize_embeddings : bool
            Normalize vectors for cosine similarity
        """

        self.model_name = model_name
        self.device = device
        self.normalize_embeddings = normalize_embeddings

        print(f"\nLoading embedding model: {self.model_name}")

        self.embedding_model = HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs={
                "device": self.device
            },
            encode_kwargs={
                "normalize_embeddings": self.normalize_embeddings
            }
        )

        print("Embedding model loaded successfully.\n")

    # ---------------------------------------------------------
    # Model
    # ---------------------------------------------------------

    def get_embedding_model(self):
        """
        Returns LangChain embedding model.

        Returns
        -------
        HuggingFaceEmbeddings
        """

        return self.embedding_model

    # ---------------------------------------------------------
    # Query Embedding
    # ---------------------------------------------------------

    def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a query.

        Parameters
        ----------
        query : str

        Returns
        -------
        List[float]
        """

        return self.embedding_model.embed_query(query)

    # ---------------------------------------------------------
    # Multiple Text Embeddings
    # ---------------------------------------------------------

    def embed_documents(
        self,
        texts: List[str]
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Parameters
        ----------
        texts : List[str]

        Returns
        -------
        List[List[float]]
        """

        return self.embedding_model.embed_documents(texts)

    # ---------------------------------------------------------
    # LangChain Documents
    # ---------------------------------------------------------

    def embed_langchain_documents(
        self,
        documents: List[Document]
    ) -> List[List[float]]:
        """
        Generate embeddings from LangChain Documents.

        Parameters
        ----------
        documents : List[Document]

        Returns
        -------
        List[List[float]]
        """

        texts = [
            document.page_content
            for document in documents
        ]

        return self.embed_documents(texts)

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    @staticmethod
    def extract_text(
        documents: List[Document]
    ) -> List[str]:
        """
        Extract text from LangChain Documents.

        Parameters
        ----------
        documents : List[Document]

        Returns
        -------
        List[str]
        """

        return [
            document.page_content
            for document in documents
        ]

    @staticmethod
    def document_count(
        documents: List[Document]
    ) -> int:
        """
        Returns number of documents.
        """

        return len(documents)

    @staticmethod
    def vector_dimension(
        vector: List[float]
    ) -> int:
        """
        Returns embedding vector dimension.
        """

        return len(vector)