"""
app.py

Document Analysis using LLMs

Features
--------
✓ Upload PDF, DOCX, TXT
✓ Document Loader
✓ Text Cleaning
✓ Text Chunking
✓ Embedding Generation
✓ FAISS Vector Store
✓ Semantic Search

(Current version retrieves relevant chunks only.)
"""

import streamlit as st

from utils.loader import DocumentLoader
from utils.cleaner import TextCleaner
from utils.splitter import DocumentSplitter
from utils.vectorstore import VectorStoreService

# ----------------------------------------------------------
# Page Configuration
# ----------------------------------------------------------

st.set_page_config(
    page_title="Document Analysis using LLMs",
    page_icon="📄",
    layout="wide"
)

# ----------------------------------------------------------
# Session State
# ----------------------------------------------------------

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "processed" not in st.session_state:
    st.session_state.processed = False

if "current_file" not in st.session_state:
    st.session_state.current_file = None

# ----------------------------------------------------------
# Title
# ----------------------------------------------------------

st.title("📄 Document Analysis using LLMs")
st.write(
    "Upload a PDF, DOCX or TXT file and perform semantic search."
)

# ----------------------------------------------------------
# Sidebar
# ----------------------------------------------------------

with st.sidebar:

    st.header("Project Status")

    st.success("✅ Document Loader")
    st.success("✅ Text Cleaner")
    st.success("✅ Text Splitter")
    st.success("✅ Embedding Model")
    st.success("✅ FAISS Vector Store")
    st.success("✅ Semantic Search")

    st.divider()

    st.info("Next Phase")
    st.write("🤖 Gemini LLM Integration")

# ----------------------------------------------------------
# File Upload
# ----------------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload a document",
    type=["pdf", "docx", "txt"]
)

# ----------------------------------------------------------
# Reset if a new file is uploaded
# ----------------------------------------------------------

if uploaded_file is not None:

    if st.session_state.current_file != uploaded_file.name:

        st.session_state.current_file = uploaded_file.name
        st.session_state.processed = False
        st.session_state.vector_store = None
        st.session_state.chunks = []

# ----------------------------------------------------------
# Process Document
# ----------------------------------------------------------

if uploaded_file is not None and not st.session_state.processed:

    try:

        with st.spinner("Processing document..."):

            # Loader
            loader = DocumentLoader()
            documents = loader.load(uploaded_file)

            # Cleaner
            cleaner = TextCleaner()
            cleaned_documents = cleaner.clean(documents)

            # Splitter
            splitter = DocumentSplitter()
            chunks = splitter.split(cleaned_documents)

            # Vector Store
            vector_store = VectorStoreService()
            vector_store.create_vector_store(chunks)

            # Store in session
            st.session_state.vector_store = vector_store
            st.session_state.chunks = chunks
            st.session_state.processed = True

        st.success("✅ Document processed successfully!")

    except Exception as e:

        st.error("Error while processing the document.")
        st.exception(e)

# ----------------------------------------------------------
# Document Information
# ----------------------------------------------------------

if st.session_state.processed:

    st.divider()

    st.subheader("📊 Document Statistics")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Chunks",
            len(st.session_state.chunks)
        )

    with col2:
        st.metric(
            "Vectors",
            st.session_state.vector_store.vector_count()
        )

# ----------------------------------------------------------
# Semantic Search
# ----------------------------------------------------------

if st.session_state.processed:

    st.divider()

    st.subheader("🔍 Ask Questions")

    query = st.text_input(
        "Ask a question about your document"
    )

    if st.button("Search"):

        if not query.strip():

            st.warning("Please enter a question.")

        else:

            try:

                with st.spinner("Searching..."):

                    results = (
                        st.session_state.vector_store
                        .similarity_search(query, k=3)
                    )

                st.success(
                    f"Retrieved {len(results)} relevant chunk(s)"
                )

                for index, document in enumerate(results, start=1):

                    with st.expander(
                        f"Result {index}",
                        expanded=(index == 1)
                    ):

                        st.markdown("### Metadata")
                        st.json(document.metadata)

                        st.markdown("### Content")
                        st.write(document.page_content)

            except Exception as e:

                st.error("Search failed.")
                st.exception(e)

# ----------------------------------------------------------
# Footer
# ----------------------------------------------------------

st.divider()

st.caption(
    "Document Analysis using LLMs • Phase 2 Complete"
)