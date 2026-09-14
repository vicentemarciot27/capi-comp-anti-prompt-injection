"""Google Forms via forms.get(). Sem scraping da interface."""
from __future__ import annotations

from google.oauth2.credentials import Credentials

from ..core.models import Artifact

SCOPES = ["https://www.googleapis.com/auth/forms.body.readonly"]


def collect(creds: Credentials, form_id: str, parent: Artifact) -> Artifact:
    """Titulo, descricao, perguntas, descricoes de item e opcoes."""
    raise NotImplementedError
