"""Fixer for numeric HTML entities."""

import re
from typing import Tuple

from .base import Fixer


class NumericEntitiesFixer(Fixer):
    """Fix numeric HTML entities that might cause issues.

    Ensures numeric entities are properly formatted.
    """

    @property
    def name(self) -> str:
        """Return the name of this fixer."""
        return "Numeric entity formatting"

    def fix(self, content: str) -> Tuple[str, int]:
        """Fix malformed numeric entities.

        :param content: The content to fix
        :returns: Tuple of (fixed_content, number_of_fixes_applied)
        """
        # Fix malformed numeric entities
        pattern = r"&#(?!x)(\d+)(?![;\d])"
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(pattern, r"&#\1;", content)
            return content, len(matches)

        return content, 0
