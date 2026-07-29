"""
knowledge_base.py

Knowledge Base Dashboard

Responsibilities
----------------
- Display Knowledge Base status
- Display indexed documents
- Display metadata
- Display statistics
- Display storage information
- Delete knowledge base
"""

import streamlit as st

from utils.vectorstore import VectorStoreService
from utils.metadata import MetadataManager


def format_size(size: int) -> str:
    """
    Convert bytes into human-readable format.
    """

    units = ["B", "KB", "MB", "GB"]

    value = float(size)

    for unit in units:

        if value < 1024 or unit == units[-1]:
            return f"{value:.2f} {unit}"

        value /= 1024


def render_knowledge_base():
    """
    Render Knowledge Base dashboard.
    """

    if not st.session_state.get("processed", False):
        return

    metadata = st.session_state.get("metadata", {})

    st.divider()
    st.header("🗄 Knowledge Base Manager")

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    filenames = metadata.get(
        "filenames",
        st.session_state.get("filenames", [])
    )

    file_types = metadata.get(
        "file_types",
        []
    )

    documents = metadata.get(
        "documents",
        len(st.session_state.get("documents", []))
    )

    chunks = metadata.get(
        "chunks",
        len(st.session_state.get("chunks", []))
    )

    vector_store = st.session_state.get("vector_store")

    vectors = metadata.get(
        "vectors",
        vector_store.vector_count() if vector_store else 0
    )

    uploaded_at = metadata.get(
        "uploaded_at",
        "-"
    )

    embedding_model = metadata.get(
        "embedding_model",
        "-"
    )

    llm = metadata.get(
        "llm",
        "-"
    )

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------

    st.success("✅ Knowledge Base Ready")

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    st.subheader("Statistics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Documents", documents)
    col2.metric("Chunks", chunks)
    col3.metric("Vectors", vectors)

    # ---------------------------------------------------------
    # Indexed Documents
    # ---------------------------------------------------------

    st.subheader("📄 Indexed Documents")

    if filenames:

        for i, filename in enumerate(filenames):

            file_type = "-"

            if i < len(file_types):
                file_type = file_types[i]

            st.write(
                f"**{i+1}. {filename}** ({file_type})"
            )

    else:

        st.info("No indexed documents.")

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    st.subheader("Metadata")

    left, right = st.columns(2)

    with left:

        st.write("**Embedding Model**")

        st.code(
            embedding_model,
            language="text"
        )

        st.write("**LLM**")

        st.code(
            llm,
            language="text"
        )

    with right:

        st.write("**Uploaded At**")
        st.write(uploaded_at)

        st.write("**Status**")
        st.success("Ready")

    # ---------------------------------------------------------
    # Storage Information
    # ---------------------------------------------------------

    vector_service = VectorStoreService()
    metadata_manager = MetadataManager()

    faiss_size = vector_service.storage_size()
    metadata_size = metadata_manager.file_size()

    total_size = faiss_size + metadata_size

    st.subheader("💾 Storage Information")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "FAISS Index",
        format_size(faiss_size)
    )

    c2.metric(
        "Metadata",
        format_size(metadata_size)
    )

    c3.metric(
        "Total",
        format_size(total_size)
    )

    # ---------------------------------------------------------
    # Delete Knowledge Base
    # ---------------------------------------------------------

    st.divider()

    st.subheader("Danger Zone")

    st.warning(
        "Deleting the Knowledge Base will permanently remove "
        "the FAISS index, metadata and current chat history."
    )

    if st.button(
        "🗑 Delete Knowledge Base",
        type="primary",
        use_container_width=True
    ):

        vector_service.delete_vector_store()
        metadata_manager.delete()

        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.success("Knowledge Base deleted successfully.")

        st.rerun()