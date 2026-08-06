"""
bm25.py

BM25 Retrieval Service

Responsibilities
----------------
- Build BM25 index
- Save BM25 index
- Load BM25 index
- Perform keyword search
"""

from pathlib import Path
from typing import List
import pickle

from rank_bm25 import BM25Okapi
from langchain_core.documents import Document


class BM25RetrieverService:
    """
    BM25 keyword retrieval.
    """

    DEFAULT_INDEX_PATH = (
        "database/knowledge_base/bm25.pkl"
    )

    def __init__(
        self,
        index_path: str = DEFAULT_INDEX_PATH,
    ):

        self.index_path = Path(index_path)

        self.documents: List[Document] = []

        self.tokenized_documents = []

        self.bm25 = None

    # ---------------------------------------------------------
    # Build
    # ---------------------------------------------------------

    def build(
        self,
        documents: List[Document],
    ):
        """
        Build BM25 index.
        """

        self.documents = documents

        self.tokenized_documents = [

            document.page_content.lower().split()

            for document in documents

        ]

        self.bm25 = BM25Okapi(
            self.tokenized_documents
        )

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    def save(self):
        """
        Save BM25 index.
        """

        self.index_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        print(f"Saving BM25 to: {self.index_path}")

        with open(
            self.index_path,
            "wb",
        ) as file:

            pickle.dump(

                {
                    "documents": self.documents,
                    "tokenized_documents":
                        self.tokenized_documents,
                    "bm25": self.bm25,
                },

                file,

            )
            print("BM25 save complete.")

    # ---------------------------------------------------------
    # Load
    # ---------------------------------------------------------

    def load(self):
        """
        Load BM25 index.
        """

        if not self.index_path.exists():

            raise FileNotFoundError(
                "BM25 index not found."
            )

        with open(
            self.index_path,
            "rb",
        ) as file:

            data = pickle.load(file)

        self.documents = data["documents"]

        self.tokenized_documents = (
            data["tokenized_documents"]
        )

        self.bm25 = data["bm25"]

    # ---------------------------------------------------------
    # Exists
    # ---------------------------------------------------------

    def exists(self) -> bool:

        return self.index_path.exists()

    # ---------------------------------------------------------
    # Delete
    # ---------------------------------------------------------

    def delete(self):

        if self.index_path.exists():

            self.index_path.unlink()

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    def search(
        self,
        query: str,
        k: int = 5,
    ) -> List[Document]:

        if self.bm25 is None:

            raise ValueError(
                "BM25 index has not been built."
            )

        query_tokens = query.lower().split()

        scores = self.bm25.get_scores(
            query_tokens
        )

        ranked = sorted(
            zip(scores, self.documents),
            reverse=True,
            key=lambda item: item[0],
        )

        return [

            document

            for score, document in ranked[:k]

        ]

    # ---------------------------------------------------------
    # Search With Scores
    # ---------------------------------------------------------

    def search_with_scores(
        self,
        query: str,
        k: int = 5,
    ):

        if self.bm25 is None:

            raise ValueError(
                "BM25 index has not been built."
            )

        query_tokens = query.lower().split()

        scores = self.bm25.get_scores(
            query_tokens
        )

        ranked = sorted(
            zip(scores, self.documents),
            reverse=True,
            key=lambda item: item[0],
        )

        return ranked[:k]