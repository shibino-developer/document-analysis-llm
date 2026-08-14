import os
import json
import streamlit as st

from styles.theme import apply_theme
from components.uploader import upload_document
from components.search import search_interface
from components.knowledge_base import knowledge_base_manager



# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="DocuMind | Document Analysis",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# THEME
# =========================================================

apply_theme()


# =========================================================
# KNOWLEDGE BASE PATHS
# =========================================================

KNOWLEDGE_BASE_DIR = "database/knowledge_base"

METADATA_PATH = os.path.join(
    KNOWLEDGE_BASE_DIR,
    "metadata.json",
)

FAISS_PATH = os.path.join(
    KNOWLEDGE_BASE_DIR,
    "faiss_index",
)

BM25_PATH = os.path.join(
    KNOWLEDGE_BASE_DIR,
    "bm25.pkl",
)


# =========================================================
# INITIALIZE SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "knowledge_base_initialized" not in st.session_state:
    st.session_state.knowledge_base_initialized = False

if "knowledge_base_loaded" not in st.session_state:
    st.session_state.knowledge_base_loaded = False

if "processed" not in st.session_state:
    st.session_state.processed = False

if "metadata" not in st.session_state:
    st.session_state.metadata = {}


# =========================================================
# KNOWLEDGE BASE INITIALIZATION
# =========================================================

def initialize_knowledge_base():

    if st.session_state.knowledge_base_initialized:
        return

    knowledge_base_exists = (
        os.path.exists(METADATA_PATH)
        and os.path.exists(FAISS_PATH)
        and os.path.exists(BM25_PATH)
    )

    # -----------------------------------------------------
    # No Knowledge Base
    # -----------------------------------------------------

    if not knowledge_base_exists:

        st.session_state.processed = False
        st.session_state.knowledge_base_loaded = False
        st.session_state.knowledge_base_initialized = True

        return

    # -----------------------------------------------------
    # Load Existing Knowledge Base
    # -----------------------------------------------------

    try:

        with open(
            METADATA_PATH,
            "r",
            encoding="utf-8",
        ) as file:

            metadata = json.load(file)

        st.session_state.metadata = metadata

        st.session_state.filenames = metadata.get(
            "filenames",
            [],
        )

        st.session_state.processed = True

        st.session_state.knowledge_base_loaded = True

        st.session_state.knowledge_base_initialized = True

    except Exception as e:

        st.session_state.processed = False
        st.session_state.knowledge_base_loaded = False
        st.session_state.knowledge_base_initialized = True

        st.error(
            f"❌ Failed to load knowledge base: {e}"
        )


initialize_knowledge_base()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 📄 DocuMind")

    st.caption(
        "AI-powered document intelligence"
    )

    st.divider()

    # -----------------------------------------------------
    # Knowledge Base Status
    # -----------------------------------------------------

    if st.session_state.knowledge_base_loaded:

        st.success(
            "🟢 Knowledge Base Ready"
        )

    else:

        st.info(
            "⚪ No Knowledge Base"
        )

    st.divider()

    # -----------------------------------------------------
    # Quick Statistics
    # -----------------------------------------------------

    metadata = st.session_state.get(
        "metadata",
        {},
    )

    documents_count = metadata.get(
        "documents",
        0,
    )

    chunks_count = metadata.get(
        "chunks",
        0,
    )

    vectors_count = metadata.get(
        "vectors",
        0,
    )

    st.markdown("### 📊 Knowledge Base")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Documents",
            documents_count,
        )

    with col2:

        st.metric(
            "Chunks",
            chunks_count,
        )

    st.metric(
        "Vectors",
        vectors_count,
    )

    st.divider()

    # -----------------------------------------------------
    # Models
    # -----------------------------------------------------

    st.markdown("### 🧠 Models")

    st.caption("Embedding")

    st.code(
        metadata.get(
            "embedding_model",
            "Not loaded",
        ),
        language="text",
    )

    st.caption("LLM")

    st.code(
        metadata.get(
            "llm",
            "Not loaded",
        ),
        language="text",
    )

    st.divider()

    # -----------------------------------------------------
    # Indexed Documents
    # -----------------------------------------------------

    st.markdown("### 📚 Indexed Documents")

    filenames = metadata.get(
        "filenames",
        [],
    )

    if filenames:

        for filename in filenames:

            st.write(
                f"📄 {filename}"
            )

    else:

        st.caption(
            "No documents indexed."
        )

    st.divider()

    # -----------------------------------------------------
    # Clear Chat
    # -----------------------------------------------------

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.caption(
        "DocuMind v1.0"
    )

    st.caption(
        "Document Analysis using LLMs"
    )


# =========================================================
# MAIN HEADER
# =========================================================

st.markdown(
    "# 📄 DocuMind"
)

st.caption(
    "AI-powered document analysis and knowledge assistant"
)

st.divider()


# =========================================================
# KNOWLEDGE BASE STATUS
# =========================================================

if st.session_state.knowledge_base_loaded:

    st.success(
        "✅ Existing Knowledge Base loaded successfully."
    )

else:

    st.info(
        "📂 No knowledge base loaded. "
        "Upload documents to create one."
    )


# =========================================================
# KNOWLEDGE BASE OVERVIEW
# =========================================================

st.markdown(
    "### 📊 Knowledge Base Overview"
)

metadata = st.session_state.get(
    "metadata",
    {},
)

documents_count = metadata.get(
    "documents",
    0,
)

chunks_count = metadata.get(
    "chunks",
    0,
)

vectors_count = metadata.get(
    "vectors",
    0,
)

files_count = len(
    metadata.get(
        "filenames",
        [],
    )
)


col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "📂 Files",
        files_count,
    )

with col2:

    st.metric(
        "📄 Documents",
        documents_count,
    )

with col3:

    st.metric(
        "✂️ Chunks",
        chunks_count,
    )

with col4:

    st.metric(
        "🧠 Vectors",
        vectors_count,
    )


# =========================================================
# DOCUMENT INFORMATION
# =========================================================

if filenames:

    st.markdown(
        "### 📚 Indexed Documents"
    )

    document_columns = st.columns(
        min(len(filenames), 3)
    )

    for index, filename in enumerate(
        filenames
    ):

        column = document_columns[
            index % len(document_columns)
        ]

        with column:

            st.info(
                f"📄 **{filename}**"
            )


# =========================================================
# UPLOAD SECTION
# =========================================================

st.divider()

st.markdown(
    "### 📂 Upload Documents"
)

st.caption(
    "Upload PDF, DOCX or TXT files to build or update your knowledge base."
)

upload_document()
knowledge_base_manager()

# =========================================================
# CHAT
# =========================================================

search_interface()


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "DocuMind · Document Analysis using LLMs · Version 1.0"
)