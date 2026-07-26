"""
search.py

Semantic Search + Gemini Chat Interface

Responsibilities
----------------
- Display chat interface
- Retrieve relevant document chunks
- Build RAG prompt
- Stream Gemini response
- Maintain conversation history
- Display retrieved sources
"""

import time
import streamlit as st

from utils.prompt import PromptBuilder
from utils.llm import LLMService


def search_interface():
    """
    Render the document chat interface.
    """

    # ---------------------------------------------------------
    # Check if document has been processed
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
    # Display Previous Conversation
    # ---------------------------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if (
                message["role"] == "assistant"
                and "sources" in message
            ):

                with st.expander(
                    "📄 Retrieved Sources",
                    expanded=False
                ):

                    for index, doc in enumerate(
                        message["sources"],
                        start=1
                    ):

                        metadata = doc.metadata

                        filename = metadata.get(
                            "source",
                            "Unknown"
                        )

                        page = metadata.get(
                            "page",
                            "-"
                        )

                        with st.container():

                            st.markdown(
                                f"### 📄 {filename} • Page {page}"
                            )

                            col1, col2 = st.columns(2)

                            with col1:
                                st.write("**File**")
                                st.write(filename)

                            with col2:
                                st.write("**Page**")
                                st.write(page)

                            st.caption(
                                f"Chunk Size: {len(doc.page_content)} characters"
                            )

                            st.write(doc.page_content)

                            st.divider()

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
    # Conversation Memory
    # ---------------------------------------------------------

    chat_history = st.session_state.messages[-6:]

    # ---------------------------------------------------------
    # Start Timer
    # ---------------------------------------------------------

    start_time = time.time()

    # ---------------------------------------------------------
    # Retrieve Documents
    # ---------------------------------------------------------

    with st.spinner("🔎 Searching document..."):

        vector_store = st.session_state.vector_store

        retrieved_docs = vector_store.similarity_search(
            query=query,
            k=3
        )

        prompt_builder = PromptBuilder()

        prompt = prompt_builder.build_prompt(
            documents=retrieved_docs,
            question=query,
            chat_history=chat_history
        )

    # ---------------------------------------------------------
    # Generate Streaming Response
    # ---------------------------------------------------------

    llm = LLMService()

    with st.chat_message("assistant"):

        answer = st.write_stream(
            llm.stream_response(prompt)
        )

        elapsed_time = time.time() - start_time

        st.caption(
            f"⏱ Response generated in {elapsed_time:.2f} seconds"
        )

        st.caption(
            f"📄 Retrieved {len(retrieved_docs)} relevant document chunk(s)"
        )

        with st.expander(
            "📄 Retrieved Sources",
            expanded=False
        ):

            for index, doc in enumerate(
                retrieved_docs,
                start=1
            ):

                metadata = doc.metadata

                filename = metadata.get(
                    "source",
                    "Unknown"
                )

                page = metadata.get(
                    "page",
                    "-"
                )

                st.markdown(
                    f"## 📄 Source {index}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.write("**File**")
                    st.write(filename)

                with col2:
                    st.write("**Page**")
                    st.write(page)

                st.caption(
                    f"Chunk Size: {len(doc.page_content)} characters"
                )

                st.write(doc.page_content)

                st.divider()

    # ---------------------------------------------------------
    # Save Assistant Response
    # ---------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": retrieved_docs
        }
    )