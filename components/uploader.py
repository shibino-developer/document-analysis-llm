"""
uploader.py

Handles document upload, processing and knowledge-base updates.

Pipeline
--------
Upload
    ↓
Document Storage
    ↓
Document Loader
    ↓
Text Cleaner
    ↓
Document Splitter
    ↓
FAISS Vector Store
    ↓
BM25 Index
    ↓
Metadata
    ↓
Session State
    ↓
RAG Service Refresh
"""

from datetime import datetime

import streamlit as st

from utils.loader import DocumentLoader
from utils.cleaner import TextCleaner
from utils.splitter import DocumentSplitter
from utils.vectorstore import VectorStoreService
from utils.metadata import MetadataManager
from utils.document_storage import DocumentStorage
from utils.retrieval.bm25 import BM25RetrieverService


# =========================================================
# SESSION INITIALIZATION
# =========================================================

def initialize_session():
    """
    Initialize Streamlit session state.
    """

    defaults = {
        "vector_store": None,
        "chunks": [],
        "documents": [],
        "processed": False,
        "filenames": [],
        "metadata": {},
        "messages": [],
        "knowledge_base_loaded": False,
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# =========================================================
# UPLOAD DOCUMENTS
# =========================================================

def upload_document():
    """
    Upload and process documents.

    New documents are added to the existing knowledge base.
    Duplicate filenames are skipped.
    """

    initialize_session()

    # =====================================================
    # UPLOAD SECTION
    # =====================================================

    uploaded_files = st.file_uploader(
        "Choose PDF, DOCX or TXT files",
        type=[
            "pdf",
            "docx",
            "txt",
        ],
        accept_multiple_files=True,
    )

    if not uploaded_files:

        return

    # =====================================================
    # LOAD EXISTING METADATA
    # =====================================================

    metadata_manager = MetadataManager()

    existing_metadata = (
        metadata_manager.load()
        or {}
    )

    existing_files = existing_metadata.get(
        "filenames",
        [],
    )

    # =====================================================
    # FIND NEW FILES
    # =====================================================

    new_uploaded_files = [
        file
        for file in uploaded_files
        if file.name not in existing_files
    ]

    # =====================================================
    # DUPLICATE CHECK
    # =====================================================

    if not new_uploaded_files:

        st.warning(
            "⚠️ All selected documents are already indexed."
        )

        return

    skipped_count = (
        len(uploaded_files)
        - len(new_uploaded_files)
    )

    # =====================================================
    # PROCESS DOCUMENTS
    # =====================================================

    progress = st.progress(
        0,
        text="Preparing documents...",
    )

    try:

        # -------------------------------------------------
        # Services
        # -------------------------------------------------

        loader = DocumentLoader()

        cleaner = TextCleaner()

        splitter = DocumentSplitter()

        storage = DocumentStorage()

        # -------------------------------------------------
        # Step 1 — Save + Load
        # -------------------------------------------------

        progress.progress(
            15,
            text="📂 Loading documents...",
        )

        new_documents = []

        for uploaded_file in new_uploaded_files:

            storage.save(
                uploaded_file
            )

            documents = loader.load(
                uploaded_file
            )

            new_documents.extend(
                documents
            )

        if not new_documents:

            progress.empty()

            st.error(
                "❌ No document content could be extracted."
            )

            return

        # -------------------------------------------------
        # Step 2 — Clean
        # -------------------------------------------------

        progress.progress(
            30,
            text="🧹 Cleaning document text...",
        )

        new_documents = cleaner.clean(
            new_documents
        )

        # -------------------------------------------------
        # Step 3 — Chunk
        # -------------------------------------------------

        progress.progress(
            45,
            text="✂️ Splitting documents into chunks...",
        )

        new_chunks = splitter.split(
            new_documents
        )

        if not new_chunks:

            progress.empty()

            st.error(
                "❌ No document chunks were generated."
            )

            return

        # =================================================
        # FAISS
        # =================================================

        progress.progress(
            60,
            text="🧠 Updating FAISS vector store...",
        )

        vector_store = VectorStoreService()

        if vector_store.vector_store_exists():

            vector_store.load_vector_store()

            vector_store.add_documents(
                new_chunks
            )

        else:

            vector_store.create_vector_store(
                new_chunks
            )

        vector_store.save_vector_store()

        # =================================================
        # BM25
        # =================================================

        progress.progress(
            75,
            text="🔎 Updating BM25 search index...",
        )

        bm25 = BM25RetrieverService()

        # -------------------------------------------------
        # Rebuild BM25 from ALL stored documents
        # -------------------------------------------------

        stored_documents = (
            storage.load_all_documents()
        )

        stored_documents = cleaner.clean(
            stored_documents
        )

        stored_chunks = splitter.split(
            stored_documents
        )

        bm25.build(
            stored_chunks
        )

        bm25.save()

        # =================================================
        # METADATA
        # =================================================

        progress.progress(
            88,
            text="📊 Updating knowledge-base metadata...",
        )

        all_files = (
            existing_metadata
            .get(
                "filenames",
                [],
            )
            .copy()
        )

        all_types = (
            existing_metadata
            .get(
                "file_types",
                [],
            )
            .copy()
        )

        for uploaded_file in new_uploaded_files:

            all_files.append(
                uploaded_file.name
            )

            all_types.append(
                uploaded_file.name
                .split(".")[-1]
                .upper()
            )

        metadata_data = {

            "filenames": all_files,

            "file_types": all_types,

            "documents": len(
                all_files
            ),

            "chunks": len(
                stored_chunks
            ),

            "vectors": (
                vector_store.vector_count()
            ),

            "embedding_model":
                "sentence-transformers/"
                "all-MiniLM-L6-v2",

            "llm":
                "Gemini Flash",

            "uploaded_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
        }

        metadata_manager.save(
            metadata_data
        )

        # =================================================
        # SESSION STATE
        # =================================================

        progress.progress(
            95,
            text="💾 Updating application state...",
        )

        st.session_state.documents = (
            stored_documents
        )

        st.session_state.chunks = (
            stored_chunks
        )

        st.session_state.vector_store = (
            vector_store
        )

        st.session_state.filenames = (
            all_files
        )

        st.session_state.metadata = metadata_data
        st.session_state.processed = True
        st.session_state.knowledge_base_loaded = True
        st.session_state.knowledge_base_initialized = True

        # -------------------------------------------------
        # Reset conversation
        # -------------------------------------------------

        st.session_state.messages = []

        # =================================================
        # IMPORTANT:
        # REFRESH CACHED RAG SERVICE
        # =================================================

        st.cache_resource.clear()

        # =================================================
        # COMPLETE
        # =================================================

        progress.progress(
            100,
            text="✅ Knowledge base updated!",
        )

        progress.empty()

        # =================================================
        # SUCCESS MESSAGE
        # =================================================

        processed_count = len(
            new_uploaded_files
        )

        message = (
            f"✅ **{processed_count} document(s) "
            f"indexed successfully.**"
        )

        if skipped_count > 0:

            message += (
                f" {skipped_count} duplicate "
                f"document(s) skipped."
            )

        st.success(
            message
        )

        # -------------------------------------------------
        # Show statistics
        # -------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "📄 Documents",
                metadata_data["documents"],
            )

        with col2:

            st.metric(
                "✂️ Chunks",
                metadata_data["chunks"],
            )

        with col3:

            st.metric(
                "🧠 Vectors",
                metadata_data["vectors"],
            )

    except Exception as e:

        progress.empty()

        st.error(
            "❌ Failed to process the documents."
        )

        st.exception(
            e
        )