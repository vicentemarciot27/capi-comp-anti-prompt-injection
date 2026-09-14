"""zip/tar: cada membro vira um Artifact filho e volta para o pipeline.

Lê em memória, sem extractall e sem tocar no disco. Limite: tamanho por
membro, para o scanner não morrer com um arquivo absurdo ou corrompido.
Profundidade (zip dentro de zip) é controlada por MAX_DEPTH em __init__.py.
"""

from __future__ import annotations

from ..models import Artifact

MAX_MEMBER_SIZE = 100 * 1024 * 1024


def members(data: bytes, parent: Artifact) -> list[tuple[Artifact, bytes]]:
    """Filhos + bytes. Membro maior que MAX_MEMBER_SIZE é pulado com
    scan_incomplete. Archive com senha: devolve [] e marca scan_incomplete
    no parent, porque conteúdo não inspecionado também é sinal."""
    raise NotImplementedError
