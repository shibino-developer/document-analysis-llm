"""
knowledge_base.py

Knowledge Base Management Service

Responsibilities
----------------
- Rebuild FAISS index
- Rebuild BM25 index
- Update metadata
- Delete individual documents
- Clear entire knowledge base
"""

from datetime import datetime

from utils.cleaner import TextCleaner
from utils.splitter import DocumentSplitter
from utils.vectorstore import VectorStoreService
from utils.metadata import MetadataManager
from utils.document_storage import DocumentStorage
from utils.retrieval.bm25 import BM25RetrieverService


class KnowledgeBaseManager:
    """
    Manages the complete document knowledge base.
    """

    def __init__(self):

        # -----------------------------------------------------
        # Services
        # -----------------------------------------------------

        self.storage = DocumentStorage()

        self.metadata_manager = MetadataManager()

        self.cleaner = TextCleaner()

        self.splitter = DocumentSplitter()

    # =========================================================
    # REBUILD KNOWLEDGE BASE
    # =========================================================

    def rebuild(self):
        """
        Rebuild FAISS and BM25 from all documents
        currently stored in database/documents.
        """

        # -----------------------------------------------------
        # Load stored documents
        # -----------------------------------------------------

        documents = (
            self.storage.load_all_documents()
        )

        # -----------------------------------------------------
        # No documents
        # -----------------------------------------------------

        if not documents:

            metadata = {
                "filenames": [],
                "file_types": [],
                "documents": 0,
                "chunks": 0,
                "vectors": 0,
                "embedding_model":
                    "sentence-transformers/"
                    "all-MiniLM-L6-v2",
                "llm": "Gemini Flash",
                "uploaded_at":
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
            }

            self.metadata_manager.save(
                metadata
            )

            return metadata

        # -----------------------------------------------------
        # Clean documents
        # -----------------------------------------------------

        documents = self.cleaner.clean(
            documents
        )

        # -----------------------------------------------------
        # Split documents
        # -----------------------------------------------------

        chunks = self.splitter.split(
            documents
        )

        # -----------------------------------------------------
        # Rebuild FAISS
        # -----------------------------------------------------

        vector_store = VectorStoreService()

        vector_store.create_vector_store(
            chunks
        )

        vector_store.save_vector_store()

        # -----------------------------------------------------
        # Rebuild BM25
        # -----------------------------------------------------

        bm25 = BM25RetrieverService()

        bm25.build(
            chunks
        )

        bm25.save()

        # -----------------------------------------------------
        # Files
        # -----------------------------------------------------

        filenames = (
            self.storage.list_documents()
        )

        file_types = [
            filename
            .split(".")[-1]
            .upper()
            for filename in filenames
        ]

        # -----------------------------------------------------
        # Metadata
        # -----------------------------------------------------

        metadata = {

            "filenames": filenames,

            "file_types": file_types,

            "documents": len(
                filenames
            ),

            "chunks": len(
                chunks
            ),

            "vectors":
                vector_store.vector_count(),

            "embedding_model":
                "sentence-transformers/"
                "all-MiniLM-L6-v2",

            "llm":
                "Gemini Flash",

            "uploaded_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
        }

        self.metadata_manager.save(
            metadata
        )

        return metadata

    # =========================================================
    # DELETE DOCUMENT
    # =========================================================

    def delete_document(
        self,
        filename,
    ):
        """
        Delete one document and rebuild
        the complete knowledge base.
        """

        # -----------------------------------------------------
        # Check document
        # -----------------------------------------------------

        if not self.storage.exists(
            filename
        ):

            raise FileNotFoundError(
                f"Document not found: {filename}"
            )

        # -----------------------------------------------------
        # Delete physical document
        # -----------------------------------------------------

        self.storage.delete(
            filename
        )

        # -----------------------------------------------------
        # Rebuild indexes
        # -----------------------------------------------------

        return self.rebuild()

    # =========================================================
    # CLEAR KNOWLEDGE BASE
    # =========================================================

    def clear(self):
        """
        Delete every stored document and
        rebuild an empty knowledge base.
        """

        # -----------------------------------------------------
        # Delete documents
        # -----------------------------------------------------

        self.storage.clear()

        # -----------------------------------------------------
        # Rebuild empty indexes
        # -----------------------------------------------------

        return self.rebuild()