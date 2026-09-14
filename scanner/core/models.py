"""Artifact, TextFragment, Finding, RiskScore."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


@dataclass
class TextFragment:
    text: str
    location: str  # "pdf.page[4].annotation[2]"
    kind: str  # text | metadata | annotation | comment | notes | alt | ocr
    hidden: bool = False
    normalized: str | None = None  # preenchido por canonicalize


@dataclass
class Artifact:
    id: str
    source_type: str  # classroom_coursework | drive_file | form | url | upload
    parent_id: str | None = None
    mime_type: str | None = None
    filename: str | None = None
    source_url: str | None = None
    sha256: str | None = None
    depth: int = 0
    metadata: dict = field(default_factory=dict)
    text_fragments: list[TextFragment] = field(default_factory=list)
    scan_incomplete: str | None = None  # motivo: "encrypted archive", etc


class Label(str, Enum):
    BENIGN = "BENIGN"
    AI_RELATED_CONTENT = "AI_RELATED_CONTENT"
    PROMPT_INJECTION_DISCUSSION = "PROMPT_INJECTION_DISCUSSION"
    SUSPICIOUS_INSTRUCTION = "SUSPICIOUS_INSTRUCTION"
    LIKELY_PROMPT_INJECTION = "LIKELY_PROMPT_INJECTION"
    OBFUSCATED_PROMPT_INJECTION = "OBFUSCATED_PROMPT_INJECTION"
    UNSCANNABLE = "UNSCANNABLE"


@dataclass
class Finding:
    artifact_id: str
    fragment: TextFragment
    score: int  # 0-100
    label: Label
    reasons: list[str]  # ids das regras/sinais que contribuiram
    path: str  # "Trabalho 5 > material.zip > slides.pdf > page 7 > annotation"

    @property
    def risk(self) -> str:
        return (
            "CRITICAL"
            if self.score >= 80
            else "HIGH"
            if self.score >= 60
            else "REVIEW"
            if self.score >= 30
            else "LOW"
        )


class RiskScore:
    """Acumulador de sinais. Thresholds calibrados depois, com dados reais."""

    def __init__(self) -> None:
        self.signals: list[tuple[str, int]] = []

    def add(self, reason: str, points: int) -> None:
        raise NotImplementedError

    def add_classifier_probability(self, p: float) -> None:
        raise NotImplementedError

    def total(self) -> int:
        raise NotImplementedError
