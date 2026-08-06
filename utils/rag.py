"""
rag.py

Retrieval-Augmented Generation Service

Responsibilities
----------------
- Hybrid Retrieval
- Cross Encoder Re-ranking
- Prompt Building
- Gemini Answer Generation
"""

from utils.vectorstore import VectorStoreService
from utils.prompt import PromptBuilder
from utils.llm import LLMService

from utils.retrieval.bm25 import BM25RetrieverService
from utils.retrieval.hybrid import HybridRetriever
from utils.retrieval.reranker import CrossEncoderReranker
from utils.retrieval.filter import MetadataFilter
from utils.retrieval.mmr import MaximumMarginalRelevance


class RAGService:
    """
    Complete Retrieval-Augmented Generation pipeline.
    """

    def __init__(self):

        # ---------------------------------------------------------
        # Vector Store
        # ---------------------------------------------------------
        self.mmr = MaximumMarginalRelevance()
        self.vector_store = VectorStoreService()

        self.vector_store.load_vector_store()

        # ---------------------------------------------------------
        # BM25
        # ---------------------------------------------------------

        self.bm25 = BM25RetrieverService()

        if self.bm25.exists():

            self.bm25.load()

        else:

            raise FileNotFoundError(
                "BM25 index not found."
            )

        # ---------------------------------------------------------
        # Hybrid Retriever
        # ---------------------------------------------------------

        self.hybrid = HybridRetriever(
            self.vector_store,
            self.bm25,
        )

        # ---------------------------------------------------------
        # Cross Encoder
        # ---------------------------------------------------------

        self.reranker = CrossEncoderReranker()

        # ---------------------------------------------------------
        # Prompt Builder
        # ---------------------------------------------------------

        self.prompt_builder = PromptBuilder()

        # ---------------------------------------------------------
        # Gemini
        # ---------------------------------------------------------

        self.llm = LLMService()

    # ---------------------------------------------------------
    # Answer Question
    # ---------------------------------------------------------

    def answer(
        self,
        question,
        chat_history,
        top_k=5,
        filename=None,
        page=None,
        file_type=None,
    ):
        """
        Complete RAG pipeline.
        """

        # ---------------------------------------------------------
        # Hybrid Retrieval
        # ---------------------------------------------------------

        retrieved_chunks = self.hybrid.search(
            query=question,
            faiss_k=top_k,
            bm25_k=top_k,
        )

        # ---------------------------------------------------------
        # Metadata Filtering
        # ---------------------------------------------------------
        retrieved_chunks = MetadataFilter.filter(
            retrieved_chunks,
            filename=filename,
            page=page,
            file_type=file_type,
        )
        # ---------------------------------------------------------
        # Cross Encoder Re-ranking
        # ---------------------------------------------------------

        retrieved_chunks = self.reranker.rerank(
            query=question,
            documents=retrieved_chunks,
            top_k=top_k,
        )
        # ---------------------------------------------------------
        # Maximum Marginal Relevance
        # ---------------------------------------------------------
        
        retrieved_chunks = self.mmr.select(
            embedding_model=self.vector_store.embedding_model,
            documents=retrieved_chunks,
            top_k=top_k,
        )
        # ---------------------------------------------------------
        # Prompt
        # ---------------------------------------------------------

        prompt = self.prompt_builder.build_prompt(
            documents=retrieved_chunks,
            question=question,
            chat_history=chat_history,
        )

        # ---------------------------------------------------------
        # Gemini Response
        # ---------------------------------------------------------

        answer = self.llm.generate_response(
            prompt
        )

        # ---------------------------------------------------------
        # Return
        # ---------------------------------------------------------

        return {
            "answer": answer,
            "sources": retrieved_chunks,
            "chunks_used": len(retrieved_chunks),
        }

    