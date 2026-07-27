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

    st.header("📊 Document Statistics")

    chunks = st.session_state.get("chunks", [])
    documents = st.session_state.get("documents", [])
    vector_store = st.session_state.get("vector_store", None)

    filenames = st.session_state.get("filenames", [])

    # -----------------------------
    # Extract Metadata
    # -----------------------------

    if documents:

        metadata = documents[0].metadata

        file_type = metadata.get("file_type", "Unknown").upper()

        if file_type == "PDF":
            pages = metadata.get("total_pages", len(documents))
        else:
            pages = len(documents)

    else:

        file_type = "-"
        pages = 0

    vectors = (
        vector_store.vector_count()
        if vector_store
        else 0
    )

    # -----------------------------
    # Metrics
    # -----------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="📄 Files",
            value=len(filenames)
        )

    with col2:
        st.metric(
            label="📑 Pages",
            value=pages
        )

    with col3:
        st.metric(
            label="✂️ Chunks",
            value=len(chunks)
        )

    with col4:
        st.metric(
            label="🧠 Vectors",
            value=vectors
        )

    # -----------------------------
    # Additional Information
    # -----------------------------

    st.subheader("Document Information")

    info_col1, info_col2 = st.columns(2)

    with info_col1:

        st.write("**Uploaded Files**")

        for file in filenames:
            st.write(f"📄 {file}")

        st.write("**File Type**")
        st.write(file_type)