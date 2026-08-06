"""
rrf.py

Reciprocal Rank Fusion
"""

from collections import defaultdict


class ReciprocalRankFusion:

    def fuse(
        self,
        ranked_lists,
        k=60,
    ):

        scores = defaultdict(float)

        documents = {}

        for ranked in ranked_lists:

            for rank, doc in enumerate(ranked, start=1):

                key = (
                    doc.metadata.get("source"),
                    doc.metadata.get("page"),
                    doc.page_content[:100],
                )

                scores[key] += 1 / (k + rank)

                documents[key] = doc

        ordered = sorted(

            scores.items(),

            key=lambda x: x[1],

            reverse=True,

        )

        return [

            documents[key]

            for key, score in ordered

        ]