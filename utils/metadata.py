"""
metadata.py

Metadata Manager

Responsibilities
----------------
- Save knowledge base metadata
- Load metadata
- Delete metadata
"""

import json
from pathlib import Path


class MetadataManager:

    DEFAULT_PATH = "database/knowledge_base/metadata.json"

    def __init__(self, path: str = DEFAULT_PATH):
        self.path = Path(path)

    def save(self, metadata: dict):
        self.path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(metadata, file, indent=4)

    def load(self):
        if not self.path.exists():
            return None

        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)

    def delete(self):
        if self.path.exists():
            self.path.unlink()

    def exists(self):
        return self.path.exists()
    
        # ---------------------------------------------------------
    # File Size
    # ---------------------------------------------------------

    def file_size(self) -> int:
        """
        Return metadata file size in bytes.
        """

        if not self.path.exists():
            return 0

        return self.path.stat().st_size