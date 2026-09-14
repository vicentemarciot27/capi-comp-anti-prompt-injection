"""Dispatch por mime/extensao. Preenche artifact.text_fragments.

Este pacote abre arquivos hostis. Deve rodar sem credenciais e, em producao,
em container separado (ver README, secao sandbox). Nenhum modulo aqui importa
scanner.oauth, scanner.db ou connectors.
"""
from __future__ import annotations

from ..models import Artifact

MAX_DEPTH = 4


def extract(artifact: Artifact, data: bytes) -> list[Artifact]:
    """Extrai fragments em artifact e devolve artifacts filhos (zip, anexos, imagens).

    Escolhe o extractor por mime_type, com fallback por extensao e sniffing.
    Nunca levanta por arquivo corrompido: marca artifact.scan_incomplete.
    """
    raise NotImplementedError


EXTRACTOR_VERSION = 1
