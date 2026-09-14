"""OAuth offline. Persistimos refresh token, nunca access token.

MVP: refresh token cifrado na coluna credential.refresh_token_enc (Fernet,
chave em env). Secret Manager so quando o numero de usuarios justificar.
"""

from __future__ import annotations

from google.oauth2.credentials import Credentials

from .connectors import classroom, drive, forms

SCOPES = classroom.SCOPES + drive.SCOPES + forms.SCOPES


def authorize_url(redirect_uri: str, state: str) -> str:
    """access_type=offline, prompt=consent, para receber refresh token."""
    raise NotImplementedError


def exchange_code(code: str, redirect_uri: str) -> tuple[str, str, list[str]]:
    """code -> (google_subject_id, refresh_token, scopes concedidos)."""
    raise NotImplementedError


def credentials(refresh_token: str) -> Credentials:
    """Access token em memoria, valido so para este processo.

    Token revogado: levanta ReauthRequired, e scan.py marca NEEDS_REAUTH.
    """
    raise NotImplementedError


class ReauthRequired(Exception):
    pass
