"""
search.py

Provides the semantic search interface for the application.

Responsibilities
----------------
- Accept user question
- Retrieve relevant document chunks
- Build RAG prompt
- Generate Gemini response
- Display answer and retrieved sources
"""

import streamlit as st

from utils.prompt import PromptBuilder
from utils.llm import LLMService


def search_interface():
    """
    Render the semantic search interface.
    """

    # ---------------------------------------------------------
    # Check document status
    # ---------------------------------------------------------

    if not st.session_state.get("processed", False):
        return

    st.divider()

    st.header("🔍 Ask Questions")

    query = st.text_input(
        "Ask anything about the uploaded document",
        placeholder="Example: What is Artificial Intelligence?"
    )

    if not st.button("Ask Gemini", type="primary"):
        return

    if not query.strip():
        st.warning("Please enter a question.")
        return

    with st.spinner("Searching document and generating answer..."):

        # -----------------------------------------------------
        # Retrieve relevant chunks
        # -----------------------------------------------------

        vector_store = st.session_state.vector_store

        retrieved_docs = vector_store.similarity_search(
            query=query,
            k=3
        )

        # -----------------------------------------------------
        # Build Prompt
        # -----------------------------------------------------

        prompt_builder = PromptBuilder()

        prompt = prompt_builder.build_prompt(
            retrieved_docs,
            query
        )

        # -----------------------------------------------------
        # Generate Answer
        # -----------------------------------------------------

        llm = LLMService()

        answer = llm.generate_response(prompt)

    # ---------------------------------------------------------
    # Display Answer
    # ---------------------------------------------------------

    st.success("Answer Generated")

    st.subheader("🤖 Gemini Answer")

    st.write(answer)

    # ---------------------------------------------------------
    # Display Sources
    # ---------------------------------------------------------

    st.divider()

    st.subheader("📄 Retrieved Sources")

    for index, document in enumerate(retrieved_docs, start=1):

        metadata = document.metadata

        title = f"Source {index}"

        if "page" in metadata:
            title += f" (Page {metadata['page']})"

        with st.expander(title):

            st.write("### Metadata")

            st.json(metadata)

            st.write("### Content")

            st.write(document.page_content)