"""Fixer for invalid JSX tag names."""

import re
from typing import Tuple

from .base import Fixer


class InvalidJsxTagsFixer(Fixer):
    """Fix JSX tags that start with numbers or invalid characters.

    Example: <1something> -> &lt;1something&gt;
    """

    @property
    def name(self) -> str:
        """Return the name of this fixer."""
        return "Invalid JSX tag names"

    def fix(self, content: str) -> Tuple[str, int]:
        """Fix JSX tags that start with invalid characters.

        :param content: The content to fix
        :returns: Tuple of (fixed_content, number_of_fixes_applied)
        """
        # Match HTML/JSX tags that start with invalid characters
        pattern = r"<(\d+[a-zA-Z_][\w-]*)"
        matches = re.findall(pattern, content)

        if matches:
            # Escape these as HTML entities instead
            for match in matches:
                content = content.replace(f"<{match}", f"&lt;{match}").replace(
                    f"</{match}>", f"&lt;/{match}&gt;"
                )

            return content, len(matches)

        return content, 0
