"""Fetch de URL arbitraria. Sem isso o scanner vira um SSRF proxy.

Bloqueia: schemes != http/https, hosts que resolvem para privado/loopback/
link-local (169.254.169.254), redirects para esses (revalidar a cada hop).
Limita redirects, bytes e tempo. HTML estatico, sem executar JavaScript.
"""
from __future__ import annotations

from ..core.models import Artifact

MAX_BYTES = 10 * 1024 * 1024
MAX_REDIRECTS = 3
TIMEOUT_S = 15
ALLOWED_SCHEMES = ("http", "https")


def fetch(url: str, parent: Artifact | None = None) -> tuple[Artifact, bytes]:
    """Levanta ValueError se a URL for bloqueada pelas regras acima."""
    raise NotImplementedError
