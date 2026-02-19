"""Fixers for Markdown/MDX files."""

from typing import List

from .base import Fixer
from .html_comments import HtmlCommentsFixer
from .invalid_attributes import InvalidAttributesFixer
from .invalid_jsx_tags import InvalidJsxTagsFixer
from .jsx_curly_braces import JsxCurlyBracesFixer
from .numeric_entities import NumericEntitiesFixer
from .self_closing_tags import SelfClosingTagsFixer
from .unclosed_tags import UnclosedTagsFixer


def get_all_fixers() -> List[Fixer]:
    """Get all available fixers.

    :returns: List of fixer instances
    """
    return [
        InvalidJsxTagsFixer(),
        HtmlCommentsFixer(),
        UnclosedTagsFixer(),
        InvalidAttributesFixer(),
        SelfClosingTagsFixer(),
        NumericEntitiesFixer(),
        JsxCurlyBracesFixer(),
    ]


__all__ = [
    "Fixer",
    "get_all_fixers",
    "InvalidJsxTagsFixer",
    "HtmlCommentsFixer",
    "UnclosedTagsFixer",
    "InvalidAttributesFixer",
    "SelfClosingTagsFixer",
    "NumericEntitiesFixer",
    "JsxCurlyBracesFixer",
]
