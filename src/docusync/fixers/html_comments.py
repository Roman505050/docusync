"""Fixer for HTML comments."""

import re
from typing import Tuple

from .base import Fixer


class HtmlCommentsFixer(Fixer):
    """Convert HTML comments to JSX comments in JSX context.

    HTML comments <!-- --> can cause issues in MDX.
    """

    @property
    def name(self) -> str:
        """Return the name of this fixer."""
        return "HTML comments to JSX"

    def fix(self, content: str) -> Tuple[str, int]:
        """Convert HTML comments to JSX comments.

        :param content: The content to fix
        :returns: Tuple of (fixed_content, number_of_fixes_applied)
        """
        # Find HTML comments not in code blocks
        in_code_block = False
        lines = content.split("\n")
        fixed_lines = []
        fixes = 0

        for line in lines:
            # Track code blocks
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                fixed_lines.append(line)
                continue

            if not in_code_block:
                # Replace HTML comments with JSX comments
                if "<!--" in line and "-->" in line:
                    # Simple inline HTML comment
                    new_line = re.sub(
                        r"<!--\s*(.*?)\s*-->",
                        r"{/* \1 */}",
                        line,
                    )
                    if new_line != line:
                        fixes += 1
                        line = new_line

            fixed_lines.append(line)

        return "\n".join(fixed_lines), fixes
