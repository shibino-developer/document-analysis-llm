"""
rag.py

Retrieval-Augmented Generation Service

Responsibilities
----------------
- Hybrid Retrieval
- Metadata Filtering
- Cross Encoder Re-ranking
- Relevance Filtering
- Maximum Marginal Relevance
- Context Compression
- Prompt Building
- Gemini Answer Generation
- Gemini Streaming Response
"""

from utils.vectorstore import VectorStoreService
from utils.prompt import PromptBuilder
from utils.llm import LLMService

from utils.retrieval.bm25 import BM25RetrieverService
from utils.retrieval.hybrid import HybridRetriever
from utils.retrieval.reranker import CrossEncoderReranker
from utils.retrieval.filter import MetadataFilter
from utils.retrieval.mmr import MaximumMarginalRelevance
from utils.retrieval.compressor import ContextCompressor


class RAGService:
    """
    Complete Retrieval-Augmented Generation pipeline.
    """

    # ---------------------------------------------------------
    # Retrieval Configuration
    # ---------------------------------------------------------

    INITIAL_TOP_K = 8

    RERANK_TOP_K = 5

    FINAL_TOP_K = 3

    # Cross Encoder scores are model scores, not probabilities.
    # This value should be tuned using your documents.
    RELEVANCE_THRESHOLD = 0.0

    def __init__(self):

        # -----------------------------------------------------
        # Vector Store
        # -----------------------------------------------------

        self.mmr = MaximumMarginalRelevance()

        self.vector_store = VectorStoreService()

        self.vector_store.load_vector_store()

        # -----------------------------------------------------
        # Context Compressor
        # -----------------------------------------------------

        self.compressor = ContextCompressor(
            self.vector_store.embedding_model
        )

        # -----------------------------------------------------
        # BM25
        # -----------------------------------------------------

        self.bm25 = BM25RetrieverService()

        if self.bm25.exists():

            self.bm25.load()

        else:

            raise FileNotFoundError(
                "BM25 index not found."
            )

        # -----------------------------------------------------
        # Hybrid Retriever
        # -----------------------------------------------------

        self.hybrid = HybridRetriever(
            self.vector_store,
            self.bm25,
        )

        # -----------------------------------------------------
        # Cross Encoder
        # -----------------------------------------------------

        self.reranker = CrossEncoderReranker()

        # -----------------------------------------------------
        # Prompt Builder
        # -----------------------------------------------------

        self.prompt_builder = PromptBuilder()

        # -----------------------------------------------------
        # Gemini
        # -----------------------------------------------------

        self.llm = LLMService()

    # =========================================================
    # INTERNAL RETRIEVAL PIPELINE
    # =========================================================

    def _retrieve(
        self,
        question,
        top_k=5,
        filename=None,
        page=None,
        file_type=None,
    ):
        """
        Execute complete retrieval pipeline.

        Pipeline:

        Hybrid Retrieval
                ↓
        Metadata Filtering
                ↓
        Cross Encoder Re-ranking
                ↓
        Relevance Filtering
                ↓
        MMR
                ↓
        Context Compression
        """

        # -----------------------------------------------------
        # 1. Hybrid Retrieval
        # -----------------------------------------------------

        retrieved_chunks = self.hybrid.search(
            query=question,
            faiss_k=self.INITIAL_TOP_K,
            bm25_k=self.INITIAL_TOP_K,
        )

        # -----------------------------------------------------
        # 2. Metadata Filtering
        # -----------------------------------------------------

        retrieved_chunks = MetadataFilter.filter(
            retrieved_chunks,
            filename=filename,
            page=page,
            file_type=file_type,
        )

        if not retrieved_chunks:
            return []

        # -----------------------------------------------------
        # 3. Cross Encoder Re-ranking
        # -----------------------------------------------------

        ranked_chunks = self.reranker.rerank_with_scores(
            query=question,
            documents=retrieved_chunks,
            top_k=self.RERANK_TOP_K,
        )

        # -----------------------------------------------------
        # 4. Relevance Filtering
        # -----------------------------------------------------

        relevant_chunks = [
            document
            for score, document in ranked_chunks
            if float(score) >= self.RELEVANCE_THRESHOLD
        ]

        # -----------------------------------------------------
        # Safety fallback
        # -----------------------------------------------------

        if not relevant_chunks and ranked_chunks:

            relevant_chunks = [
                ranked_chunks[0][1]
            ]

        # -----------------------------------------------------
        # 5. MMR
        # -----------------------------------------------------

        relevant_chunks = self.mmr.select(
            embedding_model=self.vector_store.embedding_model,
            documents=relevant_chunks,
            top_k=min(
                self.FINAL_TOP_K,
                len(relevant_chunks),
            ),
        )

        # -----------------------------------------------------
        # 6. Context Compression
        # -----------------------------------------------------

        if relevant_chunks:

            relevant_chunks = self.compressor.compress(
                query=question,
                documents=relevant_chunks,
                sentences_per_chunk=3,
            )

        return relevant_chunks

    # =========================================================
    # NORMAL ANSWER
    # =========================================================

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
        Run complete RAG pipeline and generate
        a normal Gemini response.
        """

        retrieved_chunks = self._retrieve(
            question=question,
            top_k=top_k,
            filename=filename,
            page=page,
            file_type=file_type,
        )

        # -----------------------------------------------------
        # No Relevant Context
        # -----------------------------------------------------

        if not retrieved_chunks:

            return (
                "I could not find relevant information "
                "in the uploaded documents.",
                [],
            )

        # -----------------------------------------------------
        # Build Prompt
        # -----------------------------------------------------

        prompt = self.prompt_builder.build_prompt(
            documents=retrieved_chunks,
            question=question,
            chat_history=chat_history,
        )

        # -----------------------------------------------------
        # Gemini
        # -----------------------------------------------------

        answer = self.llm.generate_response(
            prompt
        )

        return answer, retrieved_chunks

    # =========================================================
    # STREAMING ANSWER
    # =========================================================

    def stream_answer(
        self,
        question,
        chat_history,
        top_k=5,
        filename=None,
        page=None,
        file_type=None,
    ):
        """
        Run complete RAG pipeline and stream
        Gemini response.
        """

        retrieved_chunks = self._retrieve(
            question=question,
            top_k=top_k,
            filename=filename,
            page=page,
            file_type=file_type,
        )

        # -----------------------------------------------------
        # No Relevant Context
        # -----------------------------------------------------

        if not retrieved_chunks:

            def no_context_response():

                yield (
                    "I could not find relevant information "
                    "in the uploaded documents."
                )

            return no_context_response(), []

        # -----------------------------------------------------
        # Build Prompt
        # -----------------------------------------------------

        prompt = self.prompt_builder.build_prompt(
            documents=retrieved_chunks,
            question=question,
            chat_history=chat_history,
        )

        # -----------------------------------------------------
        # Stream Gemini
        # -----------------------------------------------------

        stream = self.llm.stream_response(
            prompt
        )

        return stream, retrieved_chunks