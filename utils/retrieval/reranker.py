"""
reranker.py

Cross Encoder Re-ranking Service

Responsibilities
----------------
- Re-rank retrieved documents
- Calculate relevance scores
- Remove low-relevance documents
"""

from typing import List, Tuple

from langchain_core.documents import Document
from sentence_transformers import CrossEncoder


class CrossEncoderReranker:
    """
    Cross Encoder Re-ranking.
    """

    MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

    def __init__(self):

        print()
        print("Loading Cross Encoder...")

        self.model = CrossEncoder(
            self.MODEL_NAME
        )

        print("Cross Encoder loaded.")
        print()

    # ---------------------------------------------------------
    # Re-rank
    # ---------------------------------------------------------

    def rerank(
        self,
        query,
        documents,
        top_k=5,
    ):
        """
        Re-rank documents using Cross Encoder.
        """

        if not documents:
            return []

        pairs = [
            (
                query,
                document.page_content,
            )
            for document in documents
        ]

        scores = self.model.predict(
            pairs
        )

        ranked = sorted(
            zip(scores, documents),
            reverse=True,
            key=lambda item: item[0],
        )

        return [
            document
            for score, document in ranked[:top_k]
        ]

    # ---------------------------------------------------------
    # Re-rank With Scores
    # ---------------------------------------------------------

    def rerank_with_scores(
        self,
        query,
        documents,
        top_k=5,
    ) -> List[Tuple[float, Document]]:
        """
        Re-rank documents and return relevance scores.
        """

        if not documents:
            return []

        pairs = [
            (
                query,
                document.page_content,
            )
            for document in documents
        ]

        scores = self.model.predict(
            pairs
        )

        ranked = sorted(
            zip(scores, documents),
            reverse=True,
            key=lambda item: item[0],
        )

        return ranked[:top_k]