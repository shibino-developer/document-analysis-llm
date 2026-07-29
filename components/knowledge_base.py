"""
knowledge_base.py

Knowledge Base Dashboard

Responsibilities
----------------
- Display Knowledge Base status
- Display indexed documents
- Display metadata
- Display statistics
"""

import streamlit as st
from utils.vectorstore import VectorStoreService
from utils.metadata import MetadataManager


def format_size(size: int) -> str:
    """
    Convert bytes into a readable size.
    """

    units = ["B", "KB", "MB", "GB"]

    value = float(size)

    for unit in units:

        if value < 1024 or unit == units[-1]:
            return f"{value:.2f} {unit}"

        value /= 1024

def render_knowledge_base():
    """
    Render the Knowledge Base dashboard.
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
    # Storage Information
    # ---------------------------------------------------------

    vector_store_service = VectorStoreService()
    metadata_manager = MetadataManager()

    faiss_size = vector_store_service.storage_size()
    metadata_size = metadata_manager.file_size()
    total_size = faiss_size + metadata_size

    st.subheader("💾 Storage Information")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "FAISS Index",
        format_size(faiss_size)
    )

    col2.metric(
        "Metadata",
        format_size(metadata_size)
    )

    col3.metric(
        "Total Storage",
        format_size(total_size)
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

    with col1:
        st.metric(
            label="Documents",
            value=documents
        )

    with col2:
        st.metric(
            label="Chunks",
            value=chunks
        )

    with col3:
        st.metric(
            label="Vectors",
            value=vectors
        )

    # ---------------------------------------------------------
    # Indexed Documents
    # ---------------------------------------------------------

    st.subheader("📄 Indexed Documents")

    if filenames:

        for index, filename in enumerate(filenames):

            if index < len(file_types):
                file_type = file_types[index]
            else:
                file_type = "-"

            st.write(
                f"**{index + 1}. {filename}** ({file_type})"
            )

    else:

        st.info("No indexed documents found.")

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