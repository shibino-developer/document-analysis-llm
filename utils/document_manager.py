"""
document_manager.py

Document Manager

Responsibilities
----------------
- Delete saved documents
- Rebuild Knowledge Base
"""

from pathlib import Path

from utils.rebuilder import KnowledgeBaseRebuilder


class DocumentManager:

    DOCUMENTS_FOLDER = Path("database/documents")

    def delete_document(
        self,
        filename: str,
    ):
        """
        Delete one document and rebuild
        the knowledge base.
        """

        file_path = self.DOCUMENTS_FOLDER / filename

        if not file_path.exists():
            raise FileNotFoundError(filename)

        file_path.unlink()

        rebuilder = KnowledgeBaseRebuilder()

        rebuilder.rebuild()