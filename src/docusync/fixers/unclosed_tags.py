"""Fixer for unclosed HTML tags."""

import re
from typing import Tuple

from .base import Fixer


class UnclosedTagsFixer(Fixer):
    """Fix common unclosed HTML tags.

    Tags like <br>, <hr>, <img> should be self-closing in JSX.
    """

    @property
    def name(self) -> str:
        """Return the name of this fixer."""
        return "Unclosed void elements"

    def fix(self, content: str) -> Tuple[str, int]:
        """Fix unclosed void elements.

        :param content: The content to fix
        :returns: Tuple of (fixed_content, number_of_fixes_applied)
        """
        # Self-closing tags that shouldn't have closing tags
        void_elements = [
            "area",
            "base",
            "br",
            "col",
            "embed",
            "hr",
            "img",
            "input",
            "link",
            "meta",
            "param",
            "source",
            "track",
            "wbr",
        ]

        fixes = 0
        for tag in void_elements:
            # Match <tag> or <tag attributes> but not <tag />
            pattern = rf"<{tag}(\s+[^>]*?)?(?<!/)>"
            matches = re.findall(pattern, content, re.IGNORECASE)

            if matches:
                # Replace with self-closing version
                content = re.sub(
                    pattern,
                    rf"<{tag}\1 />",
                    content,
                    flags=re.IGNORECASE,
                )
                fixes += len(matches)

        return content, fixes
