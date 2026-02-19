"""Base class for all fixers."""

from abc import ABC, abstractmethod
from typing import Tuple


class Fixer(ABC):
    """Base class for all markdown fixers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of this fixer."""
        pass

    @abstractmethod
    def fix(self, content: str) -> Tuple[str, int]:
        """Apply the fix to content.

        :param content: The content to fix
        :returns: Tuple of (fixed_content, number_of_fixes_applied)
        """
        pass
