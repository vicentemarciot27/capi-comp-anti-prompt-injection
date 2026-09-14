"""Controller: credencial -> artifacts -> extract -> detect -> findings.

Deduplicacao: mesmo drive file id ou mesmo sha256 e escaneado uma vez por scan,
mesmo que varias credenciais do curso enxerguem o arquivo.
"""

from __future__ import annotations

import sqlite3

from .core.models import Finding


def scan_course(conn: sqlite3.Connection, course_scanner_id: int) -> list[Finding]:
    """Um curso, um processo. Sem daemon, sem tokens de todos em memoria."""
    raise NotImplementedError


def scan_url(conn: sqlite3.Connection, url: str) -> list[Finding]:
    raise NotImplementedError


def scan_file(conn: sqlite3.Connection, path: str) -> list[Finding]:
    raise NotImplementedError
