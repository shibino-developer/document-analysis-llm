"""
hybrid.py

Hybrid Retriever

Responsibilities
----------------
- Search FAISS
- Search BM25
- Merge results
- Remove duplicates
"""

from langchain_core.documents import Document
from utils.retrieval.multi_query import MultiQueryRetriever
from utils.retrieval.rrf import ReciprocalRankFusion




class HybridRetriever:
    """
    Hybrid retrieval using FAISS + BM25.
    """

    def __init__(
        self,
        vector_store,
        bm25,
    ):
        self.rrf = ReciprocalRankFusion()
        self.multi_query = MultiQueryRetriever()
        self.vector_store = vector_store
        self.bm25 = bm25

    # ---------------------------------------------------------
    # Hybrid Search
    # ---------------------------------------------------------

    def search(
        self,
        query: str,
        faiss_k: int = 5,
        bm25_k: int = 5,
    ):

        queries = self.multi_query.generate(query)

        ranked_lists = []

        for q in queries:

            semantic = self.vector_store.similarity_search(
                query=q,
                k=faiss_k,
            )

            keyword = self.bm25.search(
                query=q,
                k=bm25_k,
            )

            ranked_lists.append(semantic)

            ranked_lists.append(keyword)

        return self.rrf.fuse(ranked_lists)