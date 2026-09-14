"""PDF via PyMuPDF: spans com coordenadas, metadata, annotations, links,
embedded files e imagens (repassadas para ocr.py).

hidden=True quando: fonte < 3pt, texto fora da mediabox, cor ~ igual ao fundo,
ou render mode invisivel (3).
"""

from __future__ import annotations

from ..models import Artifact, TextFragment

MIN_VISIBLE_FONT_SIZE = 3.0


def extract(data: bytes) -> tuple[list[TextFragment], list[Artifact]]:
    """Fragments + filhos (imagens, embedded files). PDF criptografado:
    devolve ([], []) e quem chama marca scan_incomplete."""
    raise NotImplementedError
