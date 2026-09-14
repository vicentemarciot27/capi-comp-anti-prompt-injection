"""Regras deterministicas PT/EN. Combinacao importa mais que palavra isolada.

Cada regra: verbo de override + alvo. "ignore" sozinho nao pontua.
"""

from __future__ import annotations

# id -> (pontos, descricao). Padroes ficam em RULES abaixo.
CATEGORIES: dict[str, tuple[int, str]] = {
    "instruction_override": (40, "ignore/desconsidere + previous/system/instrucoes"),
    "system_prompt_reference": (20, "referencia a system prompt / instrucoes internas"),
    "role_override": (15, "you are now / agora voce e / act as / developer mode"),
    "prompt_extraction": (20, "reveal/mostre + prompt/instrucoes"),
    "tool_instruction": (20, "call/use/execute + tool/function/api/ferramenta"),
    "exfiltration": (30, "send/envie + context/history/secrets/informacoes + destino"),
    "policy_override": (25, "bypass/ignore + rules/safety/policy/regras"),
}

RULES: dict[str, list] = {}  # category -> patterns compilados (PT + EN)


def match(text: str) -> list[str]:
    """Categorias disparadas pelo texto. Usar tambem no texto normalizado."""
    raise NotImplementedError
