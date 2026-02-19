"""Fixer for JSX curly braces."""

import re
from typing import Tuple

from .base import Fixer


class JsxCurlyBracesFixer(Fixer):
    """Fix unescaped curly braces that might be interpreted as JSX.

    Handles curly braces in two ways:
    1. In inline code with single backticks: converts to double backticks
    2. In text that looks like code (e.g., key:{value}): wraps in backticks
    """

    @property
    def name(self) -> str:
        """Return the name of this fixer."""
        return "Curly brace escaping"

    def fix(self, content: str) -> Tuple[str, int]:
        """Fix curly braces in inline code and code-like contexts.

        :param content: The content to fix
        :returns: Tuple of (fixed_content, number_of_fixes_applied)
        """
        in_code_block = False
        lines = content.split("\n")
        fixed_lines = []
        fixes = 0

        for line in lines:
            # Track code blocks (``` blocks) - ignore any format like ```mermaid, ```python, etc.
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                # Add code block delimiter without processing
                fixed_lines.append(line)
                continue

            # Skip processing if we're inside a code block
            # This ensures curly braces in code blocks (mermaid, python, etc.) are not modified
            if not in_code_block:
                original_line = line

                # Step 1: Convert single backticks to double if content has braces
                def convert_to_double_backticks(match: re.Match[str]) -> str:
                    """Convert single backticks to double if content has braces."""
                    code_content = match.group(1)
                    if "{" in code_content or "}" in code_content:
                        return f"``{code_content}``"
                    return str(match.group(0))

                pattern1 = r"(?<!`)`([^`\n]+)`(?!`)"
                line = re.sub(pattern1, convert_to_double_backticks, line)

                # Step 2: Wrap code-like patterns with curly braces in backticks
                # Split line by existing backticks to process only text segments
                def wrap_code_like_patterns(text: str) -> str:
                    """Wrap code-like patterns with curly braces in backticks."""
                    # Pattern 1: key:value:{variable} or key:{variable} (e.g., bot:health:{bot_id})
                    # Match word:word:{word} or word:{word}
                    text = re.sub(
                        r"(?<!`)(\w+:\w+:\{[\w_]+\}|\w+:\{[\w_]+\})(?!`)",
                        r"`\1`",
                        text,
                    )
                    # Pattern 2: standalone {variable_name} that looks like code
                    # Only if not already in backticks and not part of JSX expression
                    text = re.sub(
                        r"(?<!`)(?<!\w)\{[\w_]+\}(?!`)(?!\s*[:=])",
                        r"`\0`",
                        text,
                    )
                    return text

                # Process text segments outside of backticks
                parts = re.split(r"(`+[^`]*`+)", line)
                processed_parts = []
                for i, part in enumerate(parts):
                    if part.startswith("`") and part.endswith("`"):
                        # Already in backticks, keep as is
                        processed_parts.append(part)
                    else:
                        # Process text segments
                        processed_parts.append(wrap_code_like_patterns(part))

                line = "".join(processed_parts)

                if line != original_line:
                    fixes += 1
            # If in_code_block is True, line remains unchanged and is added as-is

            # Add processed line (or original if inside code block)
            fixed_lines.append(line)

        return "\n".join(fixed_lines), fixes
