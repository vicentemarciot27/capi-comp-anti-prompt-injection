"""OCR via Tesseract. Fase 2 do MVP: por padrao desligado.

Texto de imagem entra como TextFragment(kind="ocr"), nunca como texto visivel
do documento, porque a confiabilidade e menor.
"""

from __future__ import annotations

from ..models import TextFragment

LANGS = "por+eng"


def from_image(data: bytes, location: str) -> list[TextFragment]:
    raise NotImplementedError
