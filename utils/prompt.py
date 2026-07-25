"""
prompt.py

Prompt Builder for Retrieval-Augmented Generation (RAG).

Responsibilities
----------------
- Build prompts for Gemini.
- Inject retrieved document context.
- Ensure answers are based only on the provided context.
"""


class PromptBuilder:
    """
    Builds prompts for Gemini using retrieved document chunks.
    """

    @staticmethod
    def build_prompt(
        context: str,
        question: str
    ) -> str:
        """
        Create a prompt for the LLM.

        Parameters
        ----------
        context : str
            Retrieved document context.

        question : str
            User question.

        Returns
        -------
        str
            Complete prompt.
        """

        prompt = f"""
You are an intelligent Document Analysis Assistant.

Your job is to answer ONLY from the provided document context.

=========================
DOCUMENT CONTEXT
=========================

{context}

=========================
USER QUESTION
=========================

{question}

=========================
INSTRUCTIONS
=========================

1. Answer ONLY using the document context.

2. Do NOT use outside knowledge.

3. If the answer cannot be found in the document, reply exactly:

"I could not find the answer in the uploaded document."

4. Be accurate.

5. Be concise.

6. Use bullet points whenever appropriate.

7. If the question asks for steps, provide numbered steps.

8. Quote important terms exactly as they appear in the document.

=========================
ANSWER
=========================
"""

        return prompt

    # ----------------------------------------------------------

    @staticmethod
    def combine_documents(documents) -> str:
        """
        Combine retrieved LangChain Documents into a single context string.

        Parameters
        ----------
        documents : list[Document]

        Returns
        -------
        str
        """

        context = ""

        for i, doc in enumerate(documents, start=1):

            context += f"\n\nDocument Chunk {i}\n"
            context += "-" * 40
            context += "\n"
            context += doc.page_content

        return context

    # ----------------------------------------------------------

    @staticmethod
    def build_from_documents(
        documents,
        question: str
    ) -> str:
        """
        Build a prompt directly from LangChain Documents.

        Parameters
        ----------
        documents : list[Document]

        question : str

        Returns
        -------
        str
        """

        context = PromptBuilder.combine_documents(documents)

        return PromptBuilder.build_prompt(
            context=context,
            question=question
        )