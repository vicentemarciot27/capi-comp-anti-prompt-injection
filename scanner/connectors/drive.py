"""Download de arquivos do Drive e export de Docs/Sheets/Slides.

drive.readonly e scope restricted (verificacao do app na Google). Confirmar
cedo se drive.file atende; provavelmente nao, porque o material e do professor.
"""
from __future__ import annotations

from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

# Google-native -> mime de export
EXPORT_MIME = {
    "application/vnd.google-apps.document": (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ),
    "application/vnd.google-apps.presentation": (
        "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    ),
    "application/vnd.google-apps.spreadsheet": (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ),
}


def metadata(creds: Credentials, file_id: str) -> dict:
    """id, name, mimeType, modifiedTime, md5Checksum, size. Alimenta o cache incremental."""
    raise NotImplementedError


def download(creds: Credentials, file_id: str, mime: str) -> bytes:
    """Download direto ou export, conforme EXPORT_MIME. Respeita limite de tamanho."""
    raise NotImplementedError
