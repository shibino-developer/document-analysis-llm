"""
sidebar.py

Sidebar component for the Document Analysis using LLMs project.
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
        # Knowledge Base
        # ---------------------------------------------------

        st.subheader("Knowledge Base")

        metadata = st.session_state.get("metadata", {})

        if st.session_state.get("processed", False):

            filenames = metadata.get(
                "filenames",
                st.session_state.get("filenames", [])
            )

            chunks = metadata.get(
                "chunks",
                len(st.session_state.get("chunks", []))
            )

            vectors = metadata.get(
                "vectors",
                st.session_state.vector_store.vector_count()
                if st.session_state.get("vector_store")
                else 0
            )

            st.write(f"**Documents:** {len(filenames)}")

            st.write("**Files:**")

            if filenames:
                for file in filenames:
                    st.write(f"• {file}")
            else:
                st.write("-")

            st.write(f"**Chunks:** {chunks}")
            st.write(f"**Vectors:** {vectors}")

        else:

            st.info("No knowledge base loaded.")

        st.markdown("---")

        # ---------------------------------------------------
        # Models
        # ---------------------------------------------------

        st.subheader("Models")

        st.write("Embedding Model")

        st.code(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        st.write("LLM")

        st.code("Gemini Flash")

        st.markdown("---")

        # ---------------------------------------------------
        # Clear Session
        # ---------------------------------------------------

        if st.button(
            "🗑 Clear Session",
            use_container_width=True
        ):

            for key in list(st.session_state.keys()):
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