"""
query_expansion.py

Query Expansion Service

Responsibilities
----------------
- Expand abbreviations
- Add synonyms
- Improve recall
"""

from typing import List


class QueryExpansionService:

    EXPANSIONS = {

        "ai": [
            "Artificial Intelligence",
        ],

        "ml": [
            "Machine Learning",
        ],

        "llm": [
            "Large Language Model",
            "Large Language Models",
        ],

        "nlp": [
            "Natural Language Processing",
        ],

        "rag": [
            "Retrieval Augmented Generation",
            "Retrieval-Augmented Generation",
        ],

        "cv": [
            "Computer Vision",
        ],

        "dl": [
            "Deep Learning",
        ],
    }

    def expand(
        self,
        query: str,
    ) -> List[str]:

        expanded = [query]

        words = query.lower().split()

        for word in words:

            if word in self.EXPANSIONS:

                expanded.extend(
                    self.EXPANSIONS[word]
                )

        return list(dict.fromkeys(expanded))