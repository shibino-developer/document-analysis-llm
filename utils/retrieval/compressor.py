"""
compressor.py

Context Compression
"""

import re

from sentence_transformers import util


class ContextCompressor:

    def __init__(self, embedding_model):

        self.embedding_model = embedding_model

    # ---------------------------------------------------------
    # Compress
    # ---------------------------------------------------------

    def compress(
        self,
        query,
        documents,
        sentences_per_chunk=3,
    ):

        compressed = []

        query_embedding = self.embedding_model.embed_query(
            query
        )

        for document in documents:

            sentences = re.split(
                r"(?<=[.!?])\s+",
                document.page_content,
            )

            if len(sentences) <= sentences_per_chunk:

                compressed.append(document)

                continue

            sentence_embeddings = (
                self.embedding_model.embed_documents(
                    sentences
                )
            )

            similarities = util.cos_sim(
                query_embedding,
                sentence_embeddings,
            )[0]

            ranked = sorted(

                zip(
                    similarities,
                    sentences,
                ),

                reverse=True,

                key=lambda x: float(x[0]),

            )

            best = [
                sentence
                for _, sentence in ranked[
                    :sentences_per_chunk
                ]
            ]

            document.page_content = " ".join(best)

            compressed.append(document)

        return compressed