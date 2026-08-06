"""
mmr.py

Maximum Marginal Relevance
"""

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class MaximumMarginalRelevance:

    def select(
        self,
        embedding_model,
        documents,
        top_k=5,
        lambda_param=0.7,
    ):

        if len(documents) <= top_k:
            return documents

        embeddings = np.array(
            embedding_model.embed_documents(
                [
                    d.page_content
                    for d in documents
                ]
            )
        )

        selected = [0]

        remaining = list(
            range(1, len(documents))
        )

        while (
            len(selected) < top_k
            and remaining
        ):

            mmr_scores = []

            for idx in remaining:

                relevance = cosine_similarity(
                    embeddings[idx].reshape(1, -1),
                    embeddings[0].reshape(1, -1),
                )[0][0]

                diversity = max(

                    cosine_similarity(

                        embeddings[idx].reshape(1, -1),

                        embeddings[s].reshape(1, -1),

                    )[0][0]

                    for s in selected

                )

                score = (
                    lambda_param * relevance
                    -
                    (1 - lambda_param) * diversity
                )

                mmr_scores.append(
                    (
                        score,
                        idx,
                    )
                )

            _, best = max(mmr_scores)

            selected.append(best)

            remaining.remove(best)

        return [

            documents[i]

            for i in selected

        ]