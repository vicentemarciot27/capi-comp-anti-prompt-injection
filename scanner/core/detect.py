"""Ensemble: regras + sinais de ofuscacao + classificador local.

LLM judge so quando regras e classificador ficam inconclusivos (zona 0.3-0.7).
judge=None => label SUSPICIOUS_INSTRUCTION para a zona cinzenta.
"""

from __future__ import annotations

from collections.abc import Callable

from .models import Artifact, Finding, Label

Judge = Callable[[str], tuple[Label, str]]  # texto -> (rotulo, justificativa)


def detect_fragment(text: str, judge: Judge | None = None) -> tuple[int, Label, list[str]]:
    """Score 0-100, rotulo e razoes para um unico trecho."""
    raise NotImplementedError


def detect(artifact: Artifact, judge: Judge | None = None) -> list[Finding]:
    """Roda detect_fragment em cada TextFragment e nos decoded_candidates."""
    raise NotImplementedError


DETECTOR_VERSION = 1  # bump invalida cache de deteccao sem rebaixar artefatos
