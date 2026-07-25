from typing import List
import re

from langchain_core.documents import Document


class TextCleaner:

    @staticmethod
    def clean(documents: List[Document]) -> List[Document]:

        cleaned_documents = []

        for document in documents:

            text = document.page_content

            text = text.replace("\t", " ")
            text = text.replace("\r", " ")

            text = re.sub(r"[ ]{2,}", " ", text)
            text = re.sub(r"\n{3,}", "\n\n", text)

            text = "".join(
                ch for ch in text
                if ch.isprintable() or ch == "\n"
            )

            cleaned_documents.append(

                Document(

                    page_content=text.strip(),

                    metadata=document.metadata

                )

            )

        return cleaned_documents