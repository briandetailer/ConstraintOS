from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType


def load_source_backed_app() -> ModuleType:
    app_path = Path(__file__).with_name("app_v2.py")
    spec = importlib.util.spec_from_file_location("constraintos_workbench_source_backed", app_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load source-backed Workbench app: {app_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    return int(load_source_backed_app().main())


if __name__ == "__main__":
    raise SystemExit(main())
