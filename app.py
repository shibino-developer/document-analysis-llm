import streamlit as st

from utils.loader import DocumentLoader

st.set_page_config(
    page_title="Document Analysis",
    layout="wide"
)

st.title("📄 Document Loader")

uploaded_file = st.file_uploader(
    "Upload Document",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:

    loader = DocumentLoader()

    try:

        document = loader.load_document(uploaded_file)

        st.success("Document Loaded Successfully")

        st.subheader("Metadata")

        metadata = document.copy()

        metadata.pop("text")

        st.json(metadata)

        st.subheader("Extracted Text")

        st.text_area(
            "",
            document["text"],
            height=400
        )

    except Exception as e:

        st.error(str(e))