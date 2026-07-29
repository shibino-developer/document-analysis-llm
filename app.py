"""
app.py

Document Analysis using LLMs
"""

import streamlit as st

from components.sidebar import render_sidebar
from components.uploader import upload_document
from components.stats import show_statistics
from components.search import search_interface
from utils.database import load_saved_database
from components.knowledge_base import render_knowledge_base

st.set_page_config(
    page_title="Document Analysis using LLMs",
    page_icon="📄",
    layout="wide",
)

render_sidebar()

load_saved_database()

st.title("📄 Document Analysis using LLMs")

upload_document()

show_statistics()
render_knowledge_base()

search_interface()

st.write(st.session_state)
st.write(st.session_state.metadata)