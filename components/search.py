"""
search.py

Semantic Search + Gemini Chat Interface
"""

import streamlit as st

from utils.prompt import PromptBuilder
from utils.llm import LLMService


def search_interface():

    if not st.session_state.get("processed", False):
        return

    st.divider()

    st.header("💬 Chat with your Document")

    # -------------------------------
    # Initialize Chat
    # -------------------------------

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # -------------------------------
    # Display Previous Messages
    # -------------------------------

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

    # -------------------------------
    # Chat Input
    # -------------------------------

    query = st.chat_input(
        "Ask a question about your document..."
    )

    if query is None:
        return

    # -------------------------------
    # Show User Message
    # -------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):
        st.markdown(query)

    # -------------------------------
    # Retrieve Documents
    # -------------------------------

    with st.spinner("Searching document..."):

        docs = st.session_state.vector_store.similarity_search(
            query=query,
            k=3
        )

        prompt = PromptBuilder().build_prompt(
            docs,
            query
        )

        answer = LLMService().generate_response(prompt)

    # -------------------------------
    # Save Assistant Message
    # -------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": docs
        }
    )

    # -------------------------------
    # Display Assistant Message
    # -------------------------------

    with st.chat_message("assistant"):

        st.markdown(answer)

        with st.expander("📄 Retrieved Sources"):

            for i, doc in enumerate(docs, start=1):

                st.write(f"### Source {i}")

                st.json(doc.metadata)

                st.write(doc.page_content)