"""
uploader.py

Handles document upload and processing.
"""

from datetime import datetime

import streamlit as st

from utils.loader import DocumentLoader
from utils.cleaner import TextCleaner
from utils.splitter import DocumentSplitter
from utils.vectorstore import VectorStoreService
from utils.metadata import MetadataManager
from utils.document_storage import DocumentStorage


def initialize_session():
    """Initialize Streamlit session state."""

    defaults = {
        "vector_store": None,
        "chunks": [],
        "documents": [],
        "processed": False,
        "filenames": [],
        "metadata": {},
        "messages": [],
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def upload_document():
    """Upload and process documents."""

    initialize_session()

    st.header("📂 Upload Document")

    uploaded_files = st.file_uploader(
        "Choose PDF, DOCX or TXT files",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
    )

    if not uploaded_files:
        return

    # ---------------------------------------------------------
    # Load Existing Metadata
    # ---------------------------------------------------------

    metadata_manager = MetadataManager()

    existing_metadata = metadata_manager.load() or {}

    existing_files = existing_metadata.get(
        "filenames",
        []
    )

    # ---------------------------------------------------------
    # Skip Duplicate Files
    # ---------------------------------------------------------

    new_uploaded_files = [
        file
        for file in uploaded_files
        if file.name not in existing_files
    ]

    if not new_uploaded_files:

        st.warning(
            "⚠ All selected documents are already indexed."
        )

        return

    # ---------------------------------------------------------
    # Process New Documents
    # ---------------------------------------------------------

    with st.spinner("Processing documents..."):

        loader = DocumentLoader()
        storage = DocumentStorage()

        all_documents = []

        for uploaded_file in new_uploaded_files:
            storage.save(uploaded_file)
            docs = loader.load(uploaded_file)
            all_documents.extend(docs)

        cleaner = TextCleaner()

        all_documents = cleaner.clean(
            all_documents
        )

        splitter = DocumentSplitter()

        chunks = splitter.split(
            all_documents
        )

        vector_store = VectorStoreService()

        # -----------------------------------------------------
        # Create or Update FAISS
        # -----------------------------------------------------

        if vector_store.vector_store_exists():

            vector_store.load_vector_store()

            vector_store.add_documents(
                chunks
            )

        else:

            vector_store.create_vector_store(
                chunks
            )

        vector_store.save_vector_store()

    # ---------------------------------------------------------
    # Update Metadata
    # ---------------------------------------------------------

    all_files = existing_metadata.get(
        "filenames",
        []
    ).copy()

    all_types = existing_metadata.get(
        "file_types",
        []
    ).copy()

    for file in new_uploaded_files:

        all_files.append(
            file.name
        )

        all_types.append(
            file.name.split(".")[-1].upper()
        )

    metadata_data = {
        "filenames": all_files,
        "file_types": all_types,
        "documents": len(all_files),
        "chunks": existing_metadata.get(
            "chunks",
            0,
        ) + len(chunks),
        "vectors": vector_store.vector_count(),
        "embedding_model":
            "sentence-transformers/all-MiniLM-L6-v2",
        "llm": "Gemini Flash",
        "uploaded_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
    }

    metadata_manager.save(
        metadata_data
    )

    # ---------------------------------------------------------
    # Update Session State
    # ---------------------------------------------------------

    st.session_state.documents = all_documents
    st.session_state.chunks = chunks
    st.session_state.vector_store = vector_store
    st.session_state.filenames = metadata_data[
        "filenames"
    ]
    st.session_state.metadata = metadata_data
    st.session_state.processed = True

    # Reset chat for new knowledge base updates

    st.session_state.messages = []

    # ---------------------------------------------------------
    # Success Message
    # ---------------------------------------------------------

    processed = len(new_uploaded_files)

    skipped = (
        len(uploaded_files)
        - processed
    )

    message = (
        f"✅ {processed} document(s) indexed successfully."
    )

    if skipped > 0:

        message += (
            f" ({skipped} duplicate document(s) skipped)"
        )

    st.success(message)