"""
search.py

Semantic Search + Gemini Chat Interface

Responsibilities
----------------
- Display chat interface
- Retrieve relevant document chunks
- Build RAG prompt
- Pass previous conversation to Gemini
- Display retrieved sources
"""

import streamlit as st

from utils.prompt import PromptBuilder
from utils.llm import LLMService


def search_interface():
    """
    Render the document chat interface.
    """

    # ---------------------------------------------------------
    # Check document status
    # ---------------------------------------------------------

    if not st.session_state.get("processed", False):
        return

    st.divider()
    st.header("💬 Chat with your Document")

    # ---------------------------------------------------------
    # Initialize Chat History
    # ---------------------------------------------------------

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ---------------------------------------------------------
    # Display Previous Messages
    # ---------------------------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if (
                message["role"] == "assistant"
                and "sources" in message
            ):

                with st.expander("📄 Retrieved Sources"):

                    for i, doc in enumerate(
                        message["sources"],
                        start=1
                    ):

                        st.write(f"### Source {i}")
                        st.json(doc.metadata)
                        st.write(doc.page_content)

    # ---------------------------------------------------------
    # Chat Input
    # ---------------------------------------------------------

    query = st.chat_input(
        "Ask anything about the uploaded document..."
    )

    if not query:
        return

    # ---------------------------------------------------------
    # Display User Message
    # ---------------------------------------------------------

    with st.chat_message("user"):
        st.markdown(query)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    # ---------------------------------------------------------
    # Build Conversation Memory
    # ---------------------------------------------------------

    # Keep only the last 6 messages
    chat_history = st.session_state.messages[-6:]

    # ---------------------------------------------------------
    # Retrieve Relevant Chunks
    # ---------------------------------------------------------

    with st.spinner("Searching document..."):

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
            documents=retrieved_docs,
            question=query,
            chat_history=chat_history
        )

        # -----------------------------------------------------
        # Generate Answer
        # -----------------------------------------------------

        llm = LLMService()

        answer = llm.generate_response(prompt)

    # ---------------------------------------------------------
    # Save Assistant Message
    # ---------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": retrieved_docs
        }
    )

    # ---------------------------------------------------------
    # Display Assistant Message
    # ---------------------------------------------------------

    with st.chat_message("assistant"):

        st.markdown(answer)

        with st.expander("📄 Retrieved Sources"):

            for i, doc in enumerate(
                retrieved_docs,
                start=1
            ):

                st.write(f"### Source {i}")

                st.json(doc.metadata)

                st.write(doc.page_content)