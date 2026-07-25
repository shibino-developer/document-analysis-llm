import re
from typing import List
from langchain_core.documents import Document


class TextCleaner:

    @staticmethod
    def clean(documents: List[Document]) -> List[Document]:

        cleaned_documents = []

        for document in documents:

            text = document.page_content

            # Normalize line endings
            text = text.replace("\r\n", "\n")
            text = text.replace("\r", "\n")

            # Replace tabs with spaces
            text = text.replace("\t", " ")

            # Join single newlines into spaces
            text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)

            # Keep paragraph breaks
            text = re.sub(r'\n\s*\n', '\n\n', text)

            # Remove extra spaces
            text = re.sub(r' +', ' ', text)

            cleaned_documents.append(
                Document(
                    page_content=text.strip(),
                    metadata=document.metadata
                )
            )

        return cleaned_documents