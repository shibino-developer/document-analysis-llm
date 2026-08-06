"""
multi_query.py

Multi Query Generator

Responsibilities
----------------
- Generate alternative search queries
"""

from typing import List
from utils.retrieval.query_expansion import QueryExpansionService

class MultiQueryRetriever:
    """
    Generate multiple search queries.
    """
    def __init__(self):

        self.expander = QueryExpansionService()

    def generate(
        self,
        query: str,
    ):

        queries = []

        expansions = self.expander.expand(query)

        for q in expansions:

            queries.extend([
                q,
                f"Explain {q}",
                f"Definition of {q}",
                f"{q} overview",
            ])

        return list(dict.fromkeys(queries))