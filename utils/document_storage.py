"""
document_storage.py

Stores uploaded documents permanently.

Responsibilities
----------------
- Save uploaded documents
- Delete documents
- List documents
- Clear all documents
"""

from pathlib import Path
import shutil


class DocumentStorage:

    STORAGE_PATH = Path("database/documents")

    def __init__(self):

        self.STORAGE_PATH.mkdir(
            parents=True,
            exist_ok=True
        )

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    def save(self, uploaded_file):
        """
        Save uploaded file.
        """

        destination = (
            self.STORAGE_PATH /
            uploaded_file.name
        )

        with open(destination, "wb") as file:

            file.write(
                uploaded_file.getbuffer()
            )

        return destination

    # ---------------------------------------------------------
    # Delete
    # ---------------------------------------------------------

    def delete(self, filename: str):

        file = self.STORAGE_PATH / filename

        if file.exists():
            file.unlink()

    # ---------------------------------------------------------
    # List
    # ---------------------------------------------------------

    def list_documents(self):

        return sorted(
            [
                file.name
                for file in self.STORAGE_PATH.iterdir()
                if file.is_file()
            ]
        )

    # ---------------------------------------------------------
    # Exists
    # ---------------------------------------------------------

    def exists(self, filename: str):

        return (
            self.STORAGE_PATH /
            filename
        ).exists()

    # ---------------------------------------------------------
    # Clear
    # ---------------------------------------------------------

    def clear(self):

        if self.STORAGE_PATH.exists():

            shutil.rmtree(
                self.STORAGE_PATH
            )

        self.STORAGE_PATH.mkdir(
            parents=True,
            exist_ok=True
        )

    # ---------------------------------------------------------
    # Storage Size
    # ---------------------------------------------------------

    def storage_size(self):

        total = 0

        for file in self.STORAGE_PATH.rglob("*"):

            if file.is_file():

                total += file.stat().st_size

        return total