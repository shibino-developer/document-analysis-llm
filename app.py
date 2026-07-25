import streamlit as st

from components.sidebar import render_sidebar
from components.uploader import upload_document
from components.stats import show_statistics
from components.search import search_interface

st.set_page_config(
    page_title="Document Analysis using LLMs",
    page_icon="📄",
    layout="wide",
)

render_sidebar()

st.title("📄 Document Analysis using LLMs")

st.write(
    "Upload a PDF, DOCX or TXT document and ask questions about its contents using Retrieval-Augmented Generation (RAG)."
)

upload_document()

show_statistics()

search_interface()