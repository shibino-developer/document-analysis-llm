"""
database.py

Knowledge Base Loader

Responsibilities
----------------
- Load saved FAISS vector store
- Load metadata
- Restore Streamlit session
"""

import streamlit as st

from utils.vectorstore import VectorStoreService
from utils.metadata import MetadataManager


def load_saved_database():
    """
    Load the saved Knowledge Base into Streamlit session.
    """

    # ---------------------------------------------------------
    # Already loaded
    # ---------------------------------------------------------

    if st.session_state.get("processed", False):
        return

    vector_store = VectorStoreService()
    metadata_manager = MetadataManager()

    # ---------------------------------------------------------
    # Check whether saved data exists
    # ---------------------------------------------------------

    if (
        not vector_store.vector_store_exists()
        or not metadata_manager.exists()
    ):
        return

    try:

        # -----------------------------------------------------
        # Load FAISS Index
        # -----------------------------------------------------

        vector_store.load_vector_store()

        # -----------------------------------------------------
        # Load Metadata
        # -----------------------------------------------------

        metadata = metadata_manager.load()

        # -----------------------------------------------------
        # Restore Session State
        # -----------------------------------------------------

        st.session_state.vector_store = vector_store
        st.session_state.processed = True

        st.session_state.metadata = metadata

        st.session_state.filenames = metadata.get(
            "filenames",
            []
        )

        # These cannot be reconstructed from FAISS,
        # so initialize them as empty.
        st.session_state.documents = []
        st.session_state.chunks = []

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        st.success("✅ Existing Knowledge Base loaded successfully.")

    except Exception as error:

        st.error(
            f"❌ Failed to load Knowledge Base.\n\n{error}"
        )