# This module contains the different spell checking backends.

from __future__ import annotations

from abc import ABC, abstractmethod
from logging import Logger
import re
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from mkdocs.structure.pages import Page


class Backend(ABC):
    """Abstract class for spelling backends."""

    @abstractmethod
    def __init__(self, config: dict[str, Any], known_words: set[str] | None = None) -> None:
        """Initialize the backend.

        Parameters:
            config: User configuration from `mkdocs.yml`.
            known_words: Globally known words.
        """
        raise NotImplementedError

    @abstractmethod
    def check(self, page: Page, word: str) -> None:
        """Check a word appearing in a page.

        Parameters:
            page: The MkDocs page the word appears in.
            word: The word to check.
        """
        raise NotImplementedError


def _get_mispell_contexts(page: str, word: str, max_ctx=29):
    #phrase_re = re.compile(re.escape(word), re.IGNORECASE)
    phrase_re = re.compile(r"\b" + re.escape(word) + r"\b", re.IGNORECASE)
    for line_num, line in enumerate(page.split('\n'), start=1):
        line = line.strip()
        for match in phrase_re.finditer(line):
            line_num_token = f'{line_num}: '
            match_start, match_end = match.span()
            ctx_left = min(max_ctx, match_start)
            underline_start = ctx_left + len(line_num_token)
            underline = " " * underline_start + "^" * (match_end - match_start)
            context = line.strip()[match_start-ctx_left:match_end+max_ctx]
            yield f"{line_num_token}{context}\n{underline}"
