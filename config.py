"""
config.py

Central configuration for the
Document Analysis using LLMs project.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------------
# Google Gemini
# --------------------------------------------------------

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "models/gemini-flash-latest"
)

# --------------------------------------------------------
# Embedding Model
# --------------------------------------------------------

EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

# --------------------------------------------------------
# Chunking
# --------------------------------------------------------

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

# --------------------------------------------------------
# Retrieval
# --------------------------------------------------------

TOP_K_RESULTS = 3

# --------------------------------------------------------
# FAISS
# --------------------------------------------------------

VECTOR_DB_PATH = "database/faiss_index"

# --------------------------------------------------------
# Streamlit
# --------------------------------------------------------

PAGE_TITLE = "Document Analysis using LLMs"

PAGE_ICON = "📄"