"""Revela texto ofuscado. Nunca destroi o original.

normalize() devolve o texto revelado; signals() devolve os indicios encontrados
(zero_width_chars, letter_spacing, base64_instruction, ...) que entram no score.
"""

from __future__ import annotations


def normalize(text: str) -> str:
    """NFKC, remove zero-width/RTL, decodifica entidades HTML e %XX,
    desfaz l e t t e r  s p a c i n g, colapsa whitespace."""
    raise NotImplementedError


def decoded_candidates(text: str) -> list[tuple[str, str]]:
    """Base64/hex/\\uXXXX que decodificam para texto legivel.

    Devolve [(codec, texto_decodificado)]. Cada um vira fragment extra p/ deteccao.
    """
    raise NotImplementedError


def signals(raw: str) -> list[str]:
    """Indicios de ofuscacao presentes no texto original."""
    raise NotImplementedError
