"""Classificador local. Llama Prompt Guard 2 22M, CPU, sem API paga.

Carregado sob demanda: importar este modulo nao deve baixar modelo.
"""

from __future__ import annotations

MODEL_ID = "meta-llama/Llama-Prompt-Guard-2-22M"


def score(text: str) -> float:
    """Probabilidade 0..1 de prompt injection. 0.0 se o modelo nao estiver disponivel."""
    raise NotImplementedError


def available() -> bool:
    """Modelo presente em disco/ONNX. Falso => detect.py roda so com regras."""
    raise NotImplementedError
