"""
export.py

Export chat conversations.

Responsibilities
----------------
- Export chat as TXT
- Export chat as Markdown
"""

from typing import List


class ChatExporter:
    """
    Export chat history.
    """

    @staticmethod
    def export_txt(messages: List[dict]) -> str:
        """
        Export conversation as plain text.
        """

        lines = []

        lines.append("Document Analysis using LLMs")
        lines.append("=" * 50)
        lines.append("")

        for message in messages:

            role = message["role"].capitalize()

            lines.append(f"{role}:")
            lines.append(message["content"])
            lines.append("")
            lines.append("-" * 50)
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def export_markdown(messages: List[dict]) -> str:
        """
        Export conversation as Markdown.
        """

        lines = []

        lines.append("# Document Analysis using LLMs")
        lines.append("")
        lines.append("## Chat Conversation")
        lines.append("")

        for message in messages:

            role = message["role"].capitalize()

            lines.append(f"### {role}")
            lines.append("")
            lines.append(message["content"])
            lines.append("")

        return "\n".join(lines)