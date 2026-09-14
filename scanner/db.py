"""SQLite no MVP, Postgres depois. sqlite3 da stdlib, sem ORM.

Cache incremental: um recurso e reprocessado apenas se mudou revision/hash
ou se EXTRACTOR_VERSION/DETECTOR_VERSION subiram. Por isso raw, extracted e
detection sao registros separados: subir o detector nao rebaixa o PDF.
"""

from __future__ import annotations

import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS credential (
  id INTEGER PRIMARY KEY,
  google_subject_id TEXT NOT NULL UNIQUE,
  email TEXT,
  refresh_token_enc BLOB NOT NULL,
  scopes TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'ACTIVE',  -- ACTIVE | NEEDS_REAUTH
  last_successful_refresh TEXT
);

CREATE TABLE IF NOT EXISTS course_scanner (
  id INTEGER PRIMARY KEY,
  course_id TEXT NOT NULL,
  credential_id INTEGER NOT NULL REFERENCES credential(id),
  name TEXT,
  enabled INTEGER NOT NULL DEFAULT 1,
  interval_minutes INTEGER NOT NULL DEFAULT 60,
  last_scan_at TEXT,
  UNIQUE (course_id, credential_id)
);

CREATE TABLE IF NOT EXISTS artifact (
  id TEXT PRIMARY KEY,           -- source_type:external_id, ou sha256 p/ upload
  parent_id TEXT REFERENCES artifact(id),
  course_id TEXT,
  source_type TEXT NOT NULL,
  mime_type TEXT,
  filename TEXT,
  source_url TEXT,
  revision TEXT,                 -- updateTime / modifiedTime / md5Checksum
  sha256 TEXT,
  extractor_version INTEGER,
  detector_version INTEGER,
  scan_incomplete TEXT,
  seen_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS scan (
  id INTEGER PRIMARY KEY,
  course_scanner_id INTEGER REFERENCES course_scanner(id),
  started_at TEXT NOT NULL,
  finished_at TEXT,
  status TEXT NOT NULL,          -- RUNNING | OK | FAILED | NEEDS_REAUTH
  error TEXT
);

CREATE TABLE IF NOT EXISTS finding (
  id INTEGER PRIMARY KEY,
  scan_id INTEGER REFERENCES scan(id),
  artifact_id TEXT REFERENCES artifact(id),
  score INTEGER NOT NULL,
  risk TEXT NOT NULL,
  label TEXT NOT NULL,
  reasons TEXT NOT NULL,         -- JSON
  location TEXT NOT NULL,        -- pdf.page[4].annotation[2]
  path TEXT NOT NULL,            -- trilha legivel ate o conteudo
  excerpt TEXT NOT NULL,
  hidden INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL
);
"""


def connect(path: str = "scanner.db") -> sqlite3.Connection:
    raise NotImplementedError


def needs_rescan(conn: sqlite3.Connection, artifact_id: str, revision: str) -> bool:
    """Falso se revision e as versoes de extractor/detector nao mudaram."""
    raise NotImplementedError


def due_scanners(conn: sqlite3.Connection) -> list[dict]:
    """course_scanner habilitados cujo last_scan_at + interval ja passou."""
    raise NotImplementedError
