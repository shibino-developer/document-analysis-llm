"""
sidebar.py

Sidebar component for the Document Analysis using LLMs project.

Responsibilities
----------------
- Display project information
- Show current pipeline status
- Display loaded document information
- Clear current session
"""

import streamlit as st


def render_sidebar():
    """
    Render the application sidebar.
    """

    with st.sidebar:

        st.title("📄 Document Analysis")

        st.markdown("---")

        # ---------------------------------------------------
        # Project Status
        # ---------------------------------------------------

        st.subheader("Project Status")

        st.success("✅ Document Loader")
        st.success("✅ Text Cleaner")
        st.success("✅ Text Chunking")
        st.success("✅ Embeddings")
        st.success("✅ FAISS Vector Store")
        st.success("✅ Semantic Search")
        st.success("✅ Gemini LLM")
        st.success("✅ RAG Pipeline")

        st.markdown("---")

        # ---------------------------------------------------
        # Current Document
        # ---------------------------------------------------

        st.subheader("Current Document")

        if st.session_state.get("processed", False):

            st.write(
                f"**File:** {st.session_state.get('filename','-')}"
            )

            st.write(
                f"**Chunks:** {len(st.session_state.get('chunks', []))}"
            )

            if st.session_state.get("vector_store"):

                st.write(
                    f"**Vectors:** "
                    f"{st.session_state.vector_store.vector_count()}"
                )

        else:

            st.info("No document uploaded.")

        st.markdown("---")

        # ---------------------------------------------------
        # Model Information
        # ---------------------------------------------------

        st.subheader("Models")

        st.write("Embedding Model")

        st.code(
            "sentence-transformers/\nall-MiniLM-L6-v2"
        )

        st.write("LLM")

        st.code(
            "Gemini Flash"
        )

        st.markdown("---")

        # ---------------------------------------------------
# Clear Chat
# ---------------------------------------------------

        if st.session_state.get("processed", False):

            if st.button(
                "💬 Clear Chat",
                use_container_width=True
            ):

                st.session_state.messages = []

                st.success("Chat cleared.")

                st.rerun()

        st.markdown("---")
        # ---------------------------------------------------
        # Clear Session
        # ---------------------------------------------------

        if st.button(
            "🗑 Clear Session",
            use_container_width=True
        ):

            keys = list(st.session_state.keys())

            for key in keys:
                del st.session_state[key]

            st.success("Session cleared.")

            st.rerun()

        st.markdown("---")

        # ---------------------------------------------------
        # About
        # ---------------------------------------------------

        st.subheader("About")

        st.caption(
            """
Document Analysis using LLMs

Version 1.0

Built with

• Streamlit

• LangChain

• FAISS

• HuggingFace Embeddings

• Google Gemini
"""
        )