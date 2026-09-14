"""docx/pptx/xlsx.

docx: corpo, headers, footers, comments, hyperlinks, alt text.
pptx: shapes, speaker notes, alt text.
xlsx: cells, planilhas ocultas, comments, named ranges.
"""

from __future__ import annotations

from ..models import TextFragment


def from_docx(data: bytes) -> list[TextFragment]:
    raise NotImplementedError


def from_pptx(data: bytes) -> list[TextFragment]:
    raise NotImplementedError


def from_xlsx(data: bytes) -> list[TextFragment]:
    raise NotImplementedError
