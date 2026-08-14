"""
search.py

DocuMind RAG Chat Interface

Responsibilities
----------------
- Display chat interface
- Execute complete RAG pipeline
- Stream Gemini response
- Maintain conversation history
- Display retrieved sources
- Display retrieval statistics
"""

import time

import streamlit as st

from utils.rag import RAGService


# =========================================================
# RAG SERVICE
# =========================================================

@st.cache_resource
def get_rag_service():
    """
    Create and cache the RAG service.

    This prevents expensive models such as the embedding
    model and cross encoder from loading on every rerun.
    """
    return RAGService()


# =========================================================
# SOURCE DISPLAY
# =========================================================

def display_sources(documents):
    """
    Display retrieved document chunks.
    """

    if not documents:

        st.info(
            "No relevant document chunks were retrieved."
        )

        return

    for index, document in enumerate(
        documents,
        start=1,
    ):

        metadata = document.metadata

        filename = metadata.get(
            "source",
            "Unknown",
        )

        page = metadata.get(
            "page",
            "-",
        )

        file_type = metadata.get(
            "file_type",
            "-",
        )

        total_pages = metadata.get(
            "total_pages",
            "-",
        )

        # -------------------------------------------------
        # Source Header
        # -------------------------------------------------

        st.markdown(
            f"**📄 Source {index} — {filename}**"
        )

        # -------------------------------------------------
        # Metadata
        # -------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.caption("FILE")

            st.write(filename)

        with col2:

            st.caption("PAGE")

            st.write(
                f"{page} / {total_pages}"
            )

        with col3:

            st.caption("TYPE")

            st.write(
                str(file_type).upper()
            )

        # -------------------------------------------------
        # Context Size
        # -------------------------------------------------

        st.caption(
            f"Context size: "
            f"{len(document.page_content)} characters"
        )

        # -------------------------------------------------
        # Document Content
        # -------------------------------------------------

        with st.container(
            border=True
        ):

            st.write(
                document.page_content
            )

        if index < len(documents):

            st.divider()


# =========================================================
# CHAT INTERFACE
# =========================================================

def search_interface():
    """
    Render the DocuMind document chat interface.
    """

    # =====================================================
    # CHECK KNOWLEDGE BASE
    # =====================================================

    if not st.session_state.get(
        "processed",
        False,
    ):

        return

    st.divider()

    # =====================================================
    # HEADER
    # =====================================================

    st.markdown(
        "## 💬 Chat with your Document"
    )

    st.caption(
        "Ask questions and get answers grounded in your "
        "uploaded documents."
    )

    # =====================================================
    # RAG PIPELINE INDICATOR
    # =====================================================

    pipeline_col1, pipeline_col2, pipeline_col3, pipeline_col4 = (
        st.columns(4)
    )

    with pipeline_col1:

        st.caption(
            "🔎 Hybrid Retrieval"
        )

    with pipeline_col2:

        st.caption(
            "🎯 Cross Encoder"
        )

    with pipeline_col3:

        st.caption(
            "🧠 Context Compression"
        )

    with pipeline_col4:

        st.caption(
            "✨ Gemini"
        )

    # =====================================================
    # INITIALIZE CHAT HISTORY
    # =====================================================

    if "messages" not in st.session_state:

        st.session_state.messages = []

    # =====================================================
    # DISPLAY PREVIOUS MESSAGES
    # =====================================================

    for message in st.session_state.messages:

        role = message.get(
            "role",
        )

        content = message.get(
            "content",
            "",
        )

        with st.chat_message(
            role
        ):

            st.markdown(
                content
            )

            # -------------------------------------------------
            # Previous Sources
            # -------------------------------------------------

            if (
                role == "assistant"
                and message.get("sources")
            ):

                sources = message["sources"]

                with st.expander(
                    f"📚 {len(sources)} Retrieved Sources",
                    expanded=False,
                ):

                    display_sources(
                        sources
                    )

    # =====================================================
    # CHAT INPUT
    # =====================================================

    query = st.chat_input(
        "Ask anything about your uploaded documents..."
    )

    if not query:

        return

    # =====================================================
    # DISPLAY USER MESSAGE
    # =====================================================

    with st.chat_message(
        "user"
    ):

        st.markdown(
            query
        )

    # =====================================================
    # SAVE USER MESSAGE
    # =====================================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query,
        }
    )

    # =====================================================
    # CONVERSATION HISTORY
    # =====================================================

    chat_history = (
        st.session_state.messages[-6:]
    )

    # =====================================================
    # START TIMER
    # =====================================================

    start_time = time.time()

    # =====================================================
    # INITIALIZE RAG
    # =====================================================

    try:

        rag = get_rag_service()

    except Exception as e:

        st.error(
            "❌ Failed to initialize the RAG pipeline."
        )

        st.exception(
            e
        )

        return

    # =====================================================
    # ASSISTANT RESPONSE
    # =====================================================

    with st.chat_message(
        "assistant"
    ):

        try:

            # -------------------------------------------------
            # RAG Retrieval
            # -------------------------------------------------

            with st.spinner(
                "🔎 Searching, reranking and compressing context..."
            ):

                stream, retrieved_documents = (
                    rag.stream_answer(
                        question=query,
                        chat_history=chat_history,
                        top_k=5,
                    )
                )

            # -------------------------------------------------
            # Stream Gemini
            # -------------------------------------------------

            answer = st.write_stream(
                stream
            )

            # -------------------------------------------------
            # Response Time
            # -------------------------------------------------

            elapsed_time = (
                time.time() - start_time
            )

            # -------------------------------------------------
            # Statistics
            # -------------------------------------------------

            st.divider()

            stat_col1, stat_col2 = st.columns(2)

            with stat_col1:

                st.caption(
                    f"⏱️ Response time: "
                    f"{elapsed_time:.2f} seconds"
                )

            with stat_col2:

                st.caption(
                    f"📚 Sources used: "
                    f"{len(retrieved_documents)}"
                )

            # -------------------------------------------------
            # Sources
            # -------------------------------------------------

            with st.expander(
                f"📚 Retrieved Sources ({len(retrieved_documents)})",
                expanded=False,
            ):

                display_sources(
                    retrieved_documents
                )

            # -------------------------------------------------
            # Save Assistant Message
            # -------------------------------------------------

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": retrieved_documents,
                }
            )

        except Exception as e:

            st.error(
                "❌ An error occurred while processing your question."
            )

            st.exception(
                e
            )