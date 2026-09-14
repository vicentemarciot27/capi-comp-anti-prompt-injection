"""scanner scan-course 1 | scan-url URL | scan-file PATH | connect | list-courses.

argparse da stdlib. Um comando, um processo, sai no fim: e isso que o
Cloud Run Job / cron executa.
"""

from __future__ import annotations

import argparse


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="scanner")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("connect").add_argument("--redirect-uri", required=True)
    sub.add_parser("list-courses").add_argument("--credential", type=int, required=True)
    sub.add_parser("scan-course").add_argument("scanner_id", type=int)
    sub.add_parser("scan-url").add_argument("url")
    sub.add_parser("scan-file").add_argument("path")
    sub.add_parser("scan-due")  # chamado pelo scheduler

    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
