from __future__ import annotations

import sys
from typing import TextIO

from runtime.cli import EVIDENCE_CLI_USAGE_ERROR, run_evidence_cli


USAGE = "Usage: python -m runtime evidence --spec SPEC --workers WORKERS --output-dir OUTPUT_DIR [--format json|text]"


def run_runtime_cli(
    argv: list[str] | None = None,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    """Dispatch Runtime module commands."""
    args = list(sys.argv[1:] if argv is None else argv)
    errors = stderr or sys.stderr
    if not args or args[0] in {"-h", "--help"}:
        print(USAGE, file=errors)
        return EVIDENCE_CLI_USAGE_ERROR
    command = args.pop(0)
    if command == "evidence":
        return run_evidence_cli(args, stdout=stdout, stderr=stderr)
    print(f"Unknown Runtime command: {command}", file=errors)
    print(USAGE, file=errors)
    return EVIDENCE_CLI_USAGE_ERROR


def main(argv: list[str] | None = None) -> None:
    raise SystemExit(run_runtime_cli(argv))


if __name__ == "__main__":
    main()
