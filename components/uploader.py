"""
uploader.py

Handles document upload and processing.
"""

import streamlit as st

from utils.loader import DocumentLoader
from utils.cleaner import TextCleaner
from utils.splitter import DocumentSplitter
from utils.vectorstore import VectorStoreService


def initialize_session():

    defaults = {
        "processed": False,
        "filename": "",
        "documents": [],
        "chunks": [],
        "vector_store": None,
        "messages": [],
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


def upload_document():

    initialize_session()

    st.header("📂 Upload Document")

    uploaded_file = st.file_uploader(
        "Choose a PDF, DOCX or TXT file",
        type=["pdf", "docx", "txt"]
    )

    if uploaded_file is None:
        return

    # Reprocess only if a different file is uploaded
    if (
        st.session_state.processed
        and uploaded_file.name == st.session_state.filename
    ):
        return

    with st.spinner("Processing document..."):

        loader = DocumentLoader()
        documents = loader.load(uploaded_file)

        cleaner = TextCleaner()
        documents = cleaner.clean(documents)

        splitter = DocumentSplitter()
        chunks = splitter.split(documents)

        vector_store = VectorStoreService()
        vector_store.create_vector_store(chunks)

    st.session_state.documents = documents
    st.session_state.chunks = chunks
    st.session_state.vector_store = vector_store
    st.session_state.filename = uploaded_file.name
    st.session_state.processed = True

# New document → new conversation
    st.session_state.messages = []
    st.success("✅ Document processed successfully.")