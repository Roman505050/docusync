"""Fixer for invalid HTML attributes."""

import re
from typing import Tuple

from .base import Fixer


class InvalidAttributesFixer(Fixer):
    """Fix invalid HTML attributes for JSX.

    Convert class -> className, for -> htmlFor, etc.
    """

    @property
    def name(self) -> str:
        """Return the name of this fixer."""
        return "HTML to JSX attributes"

    def fix(self, content: str) -> Tuple[str, int]:
        """Fix invalid HTML attributes.

        :param content: The content to fix
        :returns: Tuple of (fixed_content, number_of_fixes_applied)
        """
        fixes = 0

        # class -> className
        pattern = r"<(\w+)([^>]*?\s)class="
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(
                pattern,
                r"<\1\2className=",
                content,
            )
            fixes += len(matches)

        # for -> htmlFor (in label tags)
        pattern = r"<label([^>]*?\s)for="
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(
                pattern,
                r"<label\1htmlFor=",
                content,
            )
            fixes += len(matches)

        return content, fixes
