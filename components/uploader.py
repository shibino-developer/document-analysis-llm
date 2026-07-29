"""
uploader.py

Handles document upload and processing.
"""

import streamlit as st

from utils.loader import DocumentLoader
from utils.cleaner import TextCleaner
from utils.splitter import DocumentSplitter
from utils.vectorstore import VectorStoreService
from utils.metadata import MetadataManager
from datetime import datetime


def initialize_session():

    defaults = {
        "vector_store": None,
        "chunks": [],
        "documents": [],
        "processed": False,
        "filenames": [],
        "metadata": {},
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


def upload_document():

    initialize_session()

    st.header("📂 Upload Document")

    uploaded_files = st.file_uploader(
        "Choose a PDF, DOCX or TXT files",
        type=["pdf", "docx", "txt"], accept_multiple_files=True
    )

    if not uploaded_files:
        return

   # ---------------------------------------------------------
# Reprocess only if a different set of files is uploaded
# ---------------------------------------------------------

    current_files = sorted(
        [file.name for file in uploaded_files]
    )

    previous_files = sorted(
        st.session_state.get("filenames", [])
    )

    if (
        st.session_state.processed
        and current_files == previous_files
    ):
        return

# ---------------------------------------------------------
# Process Documents
# ---------------------------------------------------------

    with st.spinner("Processing documents..."):

        loader = DocumentLoader()

        all_documents = []

        for uploaded_file in uploaded_files:

            documents = loader.load(uploaded_file)

            all_documents.extend(documents)

        cleaner = TextCleaner()
        all_documents = cleaner.clean(all_documents)

        splitter = DocumentSplitter()
        chunks = splitter.split(all_documents)

        vector_store = VectorStoreService()
        vector_store.create_vector_store(chunks)
        vector_store.save_vector_store()

        metadata = MetadataManager()

        metadata_data = {
            "filenames": current_files,
            "file_types": [
                file.name.split(".")[-1].upper()
                for file in uploaded_files
        ],
            "documents": len(all_documents),
            "chunks": len(chunks),
            "vectors": vector_store.vector_count(),
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "llm": "Gemini Flash",
            "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }



    metadata.save(metadata_data)

    st.session_state.metadata = metadata_data
# ---------------------------------------------------------
# Save Session State
# ---------------------------------------------------------

    st.session_state.documents = all_documents
    st.session_state.chunks = chunks
    st.session_state.vector_store = vector_store
    st.session_state.filenames = current_files
    st.session_state.processed = True

# New document collection → new conversation
    st.session_state.messages = []

    st.success(
        f"✅ {len(uploaded_files)} document(s) processed successfully."
    )