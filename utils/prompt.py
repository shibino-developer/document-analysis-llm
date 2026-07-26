"""
prompt.py

Builds prompts for Retrieval-Augmented Generation (RAG).
"""

from typing import List

from langchain_core.documents import Document


class PromptBuilder:
    """
    Builds prompts for Gemini.
    """

    def build_prompt(
        self,
        documents: List[Document],
        question: str,
        chat_history: list | None = None,
    ) -> str:
        """
        Build the RAG prompt.

        Parameters
        ----------
        documents : List[Document]
            Retrieved chunks.

        question : str
            User question.

        chat_history : list
            Previous conversation.
        """

        # ---------------------------------------------
        # Previous Conversation
        # ---------------------------------------------

        history = ""

        if chat_history:

            history += "PREVIOUS CONVERSATION\n"
            history += "=" * 40 + "\n\n"

            for message in chat_history:

                role = message["role"].capitalize()

                history += f"{role}: {message['content']}\n\n"

        # ---------------------------------------------
        # Document Context
        # ---------------------------------------------

        context = ""

        for i, doc in enumerate(documents, start=1):

            context += (
                f"\nDocument Chunk {i}\n"
                + "-" * 40
                + "\n"
            )

            context += doc.page_content + "\n"

        # ---------------------------------------------
        # Final Prompt
        # ---------------------------------------------

        prompt = f"""
You are an intelligent Document Analysis Assistant.

Answer ONLY using the uploaded document.

{history}

DOCUMENT CONTEXT
========================================

{context}

CURRENT QUESTION
========================================

{question}

RULES
========================================

1. Use ONLY the document context.
2. Use previous conversation if needed.
3. Do NOT invent information.
4. If the answer is not present, reply:

"I could not find the answer in the uploaded document."

5. Give clear, concise answers.
6. Use bullet points when appropriate.
7. If steps are requested, provide numbered steps.

ANSWER
========================================
"""

        return prompt.strip()