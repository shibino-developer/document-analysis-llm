"""
stats.py

Displays document statistics after processing.
"""

import streamlit as st


def show_statistics():
    """
    Display document statistics.
    """

    if not st.session_state.get("processed", False):
        return

    st.divider()

    st.header("📊 Knowledge Base Statistics")

    metadata = st.session_state.get("metadata", {})

    # -------------------------------------------------
    # Metadata
    # -------------------------------------------------

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

    vectors = metadata.get(
        "vectors",
        st.session_state.vector_store.vector_count()
        if st.session_state.get("vector_store")
        else 0
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

    # -------------------------------------------------
    # Metrics
    # -------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📂 Files",
        len(filenames)
    )

    col2.metric(
        "📑 Documents",
        documents
    )

    col3.metric(
        "✂️ Chunks",
        chunks
    )

    col4.metric(
        "🧠 Vectors",
        vectors
    )

    # -------------------------------------------------
    # Details
    # -------------------------------------------------

    st.subheader("Knowledge Base Information")

    left, right = st.columns(2)

    with left:

        st.write("**Files**")

        if filenames:
            for file in filenames:
                st.write(f"• {file}")
        else:
            st.write("-")

        st.write("**File Types**")

        if file_types:
            st.write(", ".join(file_types))
        else:
            st.write("-")

        st.write("**Embedding Model**")
        st.code(embedding_model)

    with right:

        st.write("**LLM**")
        st.code(llm)

        st.write("**Uploaded At**")
        st.write(uploaded_at)

        st.write("**Knowledge Base Status**")
        st.success("Ready")

    st.success(
        f"Knowledge Base contains {len(filenames)} document(s)."
    )