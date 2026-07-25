"""
llm.py

Google Gemini LLM Service

Responsibilities
----------------
- Load Gemini
- Generate responses
- Build RAG prompts
- Answer questions using retrieved documents
"""

from google import genai

from config import GOOGLE_API_KEY, GEMINI_MODEL
from utils.prompt import PromptBuilder


class LLMService:
    """
    Google Gemini Service
    """

    def __init__(self):

        if not GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY not found."
            )

        self.client = genai.Client(
            api_key=GOOGLE_API_KEY
        )

        self.model = GEMINI_MODEL

        print(f"Gemini model loaded: {self.model}")

    # --------------------------------------------------------
    # Basic Generation
    # --------------------------------------------------------

    def generate_response(
        self,
        prompt: str,
        temperature: float = 0.2,
    ) -> str:

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
                    "temperature": temperature
                }
            )

            return response.text

        except Exception as e:

            return f"Error: {e}"

    # --------------------------------------------------------
    # RAG Answer
    # --------------------------------------------------------

    def answer_question(
        self,
        documents,
        question: str,
    ) -> str:
        """
        Answer a question using retrieved documents.
        """

        prompt = PromptBuilder.build_from_documents(
            documents,
            question
        )

        return self.generate_response(prompt)