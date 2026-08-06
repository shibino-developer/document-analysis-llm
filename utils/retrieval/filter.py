"""
filter.py

Metadata Filtering

Responsibilities
----------------
- Filter retrieved documents
- Filter by filename
- Filter by page
- Filter by file type
"""

from typing import List

from langchain_core.documents import Document


class MetadataFilter:

    """
    Filters documents using metadata.
    """

    @staticmethod
    def filter(
        documents: List[Document],
        filename: str = None,
        page: int = None,
        file_type: str = None,
    ) -> List[Document]:

        results = documents

        if filename:

            results = [
                doc
                for doc in results
                if doc.metadata.get("source") == filename
            ]

        if page is not None:

            results = [
                doc
                for doc in results
                if doc.metadata.get("page") == page
            ]

        if file_type:

            results = [
                doc
                for doc in results
                if doc.metadata.get("file_type") == file_type.lower()
            ]

        return results