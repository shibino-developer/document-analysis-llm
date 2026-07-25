import streamlit as st

from utils.loader import DocumentLoader
from utils.cleaner import TextCleaner
from utils.splitter import DocumentSplitter


st.set_page_config(

    page_title="Document Analysis using LLMs",

    layout="wide"

)

st.title("📄 Document Processing")


uploaded_file = st.file_uploader(

    "Upload Document",

    type=["pdf", "docx", "txt"]

)


if uploaded_file:

    try:

        loader = DocumentLoader()

        documents = loader.load(uploaded_file)

        cleaner = TextCleaner()

        cleaned_documents = cleaner.clean(documents)

        splitter = DocumentSplitter()

        chunks = splitter.split(cleaned_documents)

        st.success("Document Processed Successfully")

        st.write("---")

        st.subheader("Document Information")

        st.write(f"Source : {chunks[0].metadata['source']}")

        st.write(f"File Type : {chunks[0].metadata['file_type']}")

        st.write(f"Total Chunks : {len(chunks)}")

        st.write("---")

        st.subheader("Generated Chunks")

        for i, chunk in enumerate(chunks):

            with st.expander(f"Chunk {i+1}"):

                st.write(chunk.page_content)

                st.caption(chunk.metadata)

    except Exception as e:

        st.error(str(e))