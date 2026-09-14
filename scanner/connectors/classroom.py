"""Google Classroom: courses, courseWork, courseWorkMaterials, announcements.

Escaneia title, description, multiple-choice choices e materiais anexados
(driveFile, link, form, youtubeVideo). Cada material vira um Artifact filho.
"""
from __future__ import annotations

from google.oauth2.credentials import Credentials

from ..core.models import Artifact

SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.coursework.me.readonly",
    "https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly",
    "https://www.googleapis.com/auth/classroom.announcements.readonly",
]


def list_courses(creds: Credentials) -> list[dict]:
    raise NotImplementedError


def collect(creds: Credentials, course_id: str, since: str | None = None) -> list[Artifact]:
    """Arvore de artifacts do curso. `since` = updateTime do ultimo scan,
    para pular recursos inalterados (scan incremental)."""
    raise NotImplementedError
