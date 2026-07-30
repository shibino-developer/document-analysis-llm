"""
rebuilder.py

Knowledge Base Rebuilder

Responsibilities
----------------
- Reload all saved documents
- Rebuild FAISS index
- Update metadata
"""

from pathlib import Path
from datetime import datetime

from utils.loader import DocumentLoader
from utils.cleaner import TextCleaner
from utils.splitter import DocumentSplitter
from utils.vectorstore import VectorStoreService
from utils.metadata import MetadataManager


class KnowledgeBaseRebuilder:

    DOCUMENTS_FOLDER = Path("database/documents")

    def rebuild(self):
        """
        Rebuild the entire knowledge base.
        """

        loader = DocumentLoader()
        cleaner = TextCleaner()
        splitter = DocumentSplitter()

        documents = []

        filenames = []
        file_types = []

        # ---------------------------------------------
        # Load every saved document
        # ---------------------------------------------

        for file_path in sorted(
            self.DOCUMENTS_FOLDER.iterdir()
        ):

            if not file_path.is_file():
                continue

            docs = loader.load_file(file_path)

            documents.extend(docs)

            filenames.append(file_path.name)

            file_types.append(
                file_path.suffix.replace(".", "").upper()
            )

        # ---------------------------------------------
        # Clean
        # ---------------------------------------------

        documents = cleaner.clean(documents)

        # ---------------------------------------------
        # Split
        # ---------------------------------------------

        chunks = splitter.split(documents)

        # ---------------------------------------------
        # Create new FAISS
        # ---------------------------------------------

        vector_store = VectorStoreService()

        if chunks:

            vector_store.create_vector_store(chunks)

            vector_store.save_vector_store()

            vectors = vector_store.vector_count()

        else:

            vector_store.delete_vector_store()

            vectors = 0

        # ---------------------------------------------
        # Save metadata
        # ---------------------------------------------

        metadata = MetadataManager()

        metadata.save(
            {
                "filenames": filenames,
                "file_types": file_types,
                "documents": len(filenames),
                "chunks": len(chunks),
                "vectors": vectors,
                "embedding_model":
                    "sentence-transformers/all-MiniLM-L6-v2",
                "llm": "Gemini Flash",
                "uploaded_at":
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
            }
        )