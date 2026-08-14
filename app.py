import os
import json
import streamlit as st

from styles.theme import apply_theme
from components.uploader import upload_document
from components.search import search_interface


st.set_page_config(
    page_title="Document Analysis using LLMs",
    page_icon="📄",
    layout="wide",
)

apply_theme()


# =========================================================
# KNOWLEDGE BASE PATHS
# =========================================================

KNOWLEDGE_BASE_DIR = "database/knowledge_base"

METADATA_PATH = os.path.join(
    KNOWLEDGE_BASE_DIR,
    "metadata.json"
)

FAISS_PATH = os.path.join(
    KNOWLEDGE_BASE_DIR,
    "faiss_index"
)

BM25_PATH = os.path.join(
    KNOWLEDGE_BASE_DIR,
    "bm25.pkl"
)


# =========================================================
# SESSION STATE
# =========================================================

def initialize_session():

    defaults = {
        "processed": False,
        "knowledge_base_loaded": False,
        "knowledge_base_initialized": False,
        "metadata": {},
        "filenames": [],
        "messages": [],
        "documents": [],
        "chunks": [],
        "vector_store": None,
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


# =========================================================
# KNOWLEDGE BASE INITIALIZATION
# =========================================================

def initialize_knowledge_base():

    initialize_session()

    # Already initialized during this session
    if st.session_state.knowledge_base_initialized:
        return

    # -----------------------------------------------------
    # Check whether a saved knowledge base exists
    # -----------------------------------------------------

    knowledge_base_exists = (
        os.path.exists(METADATA_PATH)
        and os.path.exists(FAISS_PATH)
        and os.path.exists(BM25_PATH)
    )

    # -----------------------------------------------------
    # No knowledge base
    # -----------------------------------------------------

    if not knowledge_base_exists:

        st.session_state.processed = False
        st.session_state.knowledge_base_loaded = False
        st.session_state.metadata = {}
        st.session_state.filenames = []

        st.session_state.knowledge_base_initialized = True

        return

    # -----------------------------------------------------
    # Load existing knowledge base
    # -----------------------------------------------------

    try:

        with open(
            METADATA_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            metadata = json.load(file)

        st.session_state.metadata = metadata

        st.session_state.filenames = metadata.get(
            "filenames",
            []
        )

        st.session_state.processed = True

        st.session_state.knowledge_base_loaded = True

        st.session_state.knowledge_base_initialized = True

    except Exception as e:

        st.session_state.processed = False
        st.session_state.knowledge_base_loaded = False
        st.session_state.metadata = {}
        st.session_state.filenames = []

        st.session_state.knowledge_base_initialized = True

        st.warning(
            f"⚠️ Could not load existing knowledge base: {e}"
        )


# =========================================================
# INITIALIZE
# =========================================================

initialize_knowledge_base()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="app-header">

        <div class="app-title">
            📄 DocuMind
        </div>

        <div class="app-subtitle">
            AI-powered document analysis and knowledge assistant
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# KNOWLEDGE BASE STATUS
# =========================================================

if st.session_state.get(
    "knowledge_base_loaded",
    False
):

    st.success(
        "✅ Knowledge Base Ready"
    )

else:

    st.info(
        "📂 No knowledge base loaded. "
        "Upload documents below to create one."
    )


# =========================================================
# UPLOAD
# =========================================================

upload_document()


# =========================================================
# CHAT
# =========================================================

search_interface()


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="app-footer">
        DocuMind · Document Analysis using LLMs · Version 1.0
    </div>
    """,
    unsafe_allow_html=True,
)