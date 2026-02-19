"""Fixer for self-closing tag spacing."""

import re
from typing import Tuple

from .base import Fixer


class SelfClosingTagsFixer(Fixer):
    """Ensure self-closing tags have proper spacing.

    <tag/> -> <tag />
    """

    @property
    def name(self) -> str:
        """Return the name of this fixer."""
        return "Self-closing tag spacing"

    def fix(self, content: str) -> Tuple[str, int]:
        """Fix self-closing tag spacing.

        :param content: The content to fix
        :returns: Tuple of (fixed_content, number_of_fixes_applied)
        """
        # Match self-closing tags without space before />
        pattern = r"<(\w+)([^>]*?)(?<!\s)/>"
        matches = re.findall(pattern, content)

        if matches:
            content = re.sub(
                pattern,
                r"<\1\2 />",
                content,
            )
            return content, len(matches)

        return content, 0
