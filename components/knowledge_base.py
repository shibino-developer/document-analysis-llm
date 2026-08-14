"""
knowledge_base.py

Knowledge Base Manager UI

Responsibilities
----------------
- Display knowledge base status
- Display statistics
- Display indexed documents
- Delete individual documents
- Delete entire knowledge base
"""

import streamlit as st

from utils.knowledge_base import KnowledgeBaseManager


def knowledge_base_manager():
    """
    Render the Knowledge Base Manager.
    """

    st.divider()

    st.header("🗄 Knowledge Base Manager")

    # =========================================================
    # Get Metadata
    # =========================================================

    metadata = st.session_state.get(
        "metadata",
        {}
    )

    filenames = metadata.get(
        "filenames",
        []
    )

    # =========================================================
    # Empty Knowledge Base
    # =========================================================

    if not filenames:

        st.info(
            "📭 No documents are currently indexed."
        )

        return

    # =========================================================
    # Status
    # =========================================================

    st.success(
        "✅ Knowledge Base Ready"
    )

    # =========================================================
    # Statistics
    # =========================================================

    st.subheader("📊 Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Documents",
            metadata.get(
                "documents",
                0
            )
        )

    with col2:

        st.metric(
            "Chunks",
            metadata.get(
                "chunks",
                0
            )
        )

    with col3:

        st.metric(
            "Vectors",
            metadata.get(
                "vectors",
                0
            )
        )

    # =========================================================
    # Indexed Documents
    # =========================================================

    st.subheader(
        "📄 Indexed Documents"
    )

    kb_manager = KnowledgeBaseManager()

    for filename in filenames:

        col1, col2 = st.columns(
            [5, 1]
        )

        # -----------------------------------------------------
        # Filename
        # -----------------------------------------------------

        with col1:

            file_type = (
                filename
                .split(".")[-1]
                .upper()
            )

            st.write(
                f"📄 **{filename}** "
                f"({file_type})"
            )

        # -----------------------------------------------------
        # Delete Button
        # -----------------------------------------------------

        with col2:

            if st.button(
                "Delete",
                key=f"delete_{filename}",
                use_container_width=True,
            ):

                try:

                    with st.spinner(
                        f"Deleting {filename}..."
                    ):

                        new_metadata = (
                            kb_manager
                            .delete_document(
                                filename
                            )
                        )

                    # -----------------------------------------
                    # Update Session State
                    # -----------------------------------------

                    st.session_state.metadata = (
                        new_metadata
                    )

                    st.session_state.filenames = (
                        new_metadata[
                            "filenames"
                        ]
                    )

                    st.session_state.processed = (
                        new_metadata[
                            "documents"
                        ] > 0
                    )

                    st.session_state.knowledge_base_loaded = (
                        new_metadata[
                            "documents"
                        ] > 0
                    )

                    # -----------------------------------------
                    # Clear Chat
                    # -----------------------------------------

                    st.session_state.messages = []

                    # -----------------------------------------
                    # Reset Vector Store
                    # -----------------------------------------

                    st.session_state.vector_store = (
                        None
                    )

                    # -----------------------------------------
                    # Clear Cached RAG
                    # -----------------------------------------

                    st.cache_resource.clear()

                    st.success(
                        f"✅ {filename} deleted successfully."
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"❌ Failed to delete "
                        f"{filename}: {e}"
                    )

    # =========================================================
    # Knowledge Base Metadata
    # =========================================================

    st.divider()

    st.subheader(
        "ℹ️ Knowledge Base Information"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            "**Embedding Model**"
        )

        st.code(
            metadata.get(
                "embedding_model",
                "Unknown"
            )
        )

    with col2:

        st.write(
            "**LLM**"
        )

        st.code(
            metadata.get(
                "llm",
                "Unknown"
            )
        )

    st.write(
        "**Uploaded At**"
    )

    st.write(
        metadata.get(
            "uploaded_at",
            "Unknown"
        )
    )

    # =========================================================
    # Danger Zone
    # =========================================================

    st.divider()

    st.subheader(
        "⚠️ Danger Zone"
    )

    st.warning(
        "Deleting the knowledge base will permanently "
        "remove all indexed documents, FAISS vectors, "
        "BM25 data, metadata, and current chat history."
    )

    if st.button(
        "🗑️ Delete Entire Knowledge Base",
        type="secondary",
        use_container_width=True,
    ):

        try:

            with st.spinner(
                "Deleting knowledge base..."
            ):

                new_metadata = (
                    kb_manager.clear()
                )

            # ---------------------------------------------
            # Reset Session State
            # ---------------------------------------------

            st.session_state.metadata = (
                new_metadata
            )

            st.session_state.filenames = []

            st.session_state.processed = False

            st.session_state.knowledge_base_loaded = (
                False
            )

            st.session_state.vector_store = None

            st.session_state.documents = []

            st.session_state.chunks = []

            st.session_state.messages = []

            # ---------------------------------------------
            # Clear RAG Cache
            # ---------------------------------------------

            st.cache_resource.clear()

            st.success(
                "✅ Knowledge Base deleted successfully."
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"❌ Failed to delete knowledge base: {e}"
            )