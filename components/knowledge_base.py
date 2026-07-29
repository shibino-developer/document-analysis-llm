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