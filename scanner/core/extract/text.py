"""txt/md/csv/json/xml/yaml e HTML.

HTML: texto visivel, comments, alt, title, aria-label, e elementos escondidos
(display:none, visibility:hidden, font-size ~0, cor igual ao fundo) -> hidden=True.
Sem executar JavaScript.
"""

from __future__ import annotations

from ..models import TextFragment


def from_plain(data: bytes, encoding_hint: str | None = None) -> list[TextFragment]:
    raise NotImplementedError


def from_html(data: bytes) -> list[TextFragment]:
    raise NotImplementedError


def from_structured(data: bytes, mime: str) -> list[TextFragment]:
    """JSON/XML/YAML: valores e chaves textuais."""
    raise NotImplementedError
