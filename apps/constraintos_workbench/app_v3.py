from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType


def load_source_backed_core() -> ModuleType:
    app_path = Path(__file__).with_name("app_v2.py")
    spec = importlib.util.spec_from_file_location(
        "constraintos_workbench_source_backed_core",
        app_path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load source-backed Workbench core: {app_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CORE = load_source_backed_core()
BASE_HTML_PAGE = CORE.html_page


def html_page() -> str:
    content = BASE_HTML_PAGE()
    content = content.replace(
        '<p id="technicalLinks"></p>',
        '<div id="technicalSummary" class="status">Repeat-render evidence will appear here after a source-backed run.</div><p id="technicalLinks"></p>',
    )
    content = content.replace(
        "status.textContent='Complete.\\nMode: '+data.run_mode+'\\nRun directory: '+data.run_dir+'\\nApproval allowed: false';",
        "const comparison=data.technical_render?.repeat_render_comparison?.status||'not_applicable';const currentHash=data.technical_render?.output_sha256||'not_applicable';const previousHash=data.technical_render?.repeat_render_comparison?.previous_output_sha256||'none';status.textContent='Complete.\\nMode: '+data.run_mode+'\\nRun directory: '+data.run_dir+'\\nRepeat-render comparison: '+comparison+'\\nCurrent output SHA-256: '+currentHash+'\\nPrevious output SHA-256: '+previousHash+'\\nApproval allowed: false';",
    )
    content = content.replace(
        "document.getElementById('technicalLinks').innerHTML='<a href=\"'+data.technical_render_url+'\" target=\"_blank\">Open source-backed SVG</a> · <a href=\"'+data.technical_render_manifest_url+'\" target=\"_blank\">Open technical render manifest</a>';",
        "const repeat=data.technical_render.repeat_render_comparison;document.getElementById('technicalSummary').textContent='Repeat-render comparison: '+repeat.status+'\\nCurrent output SHA-256: '+repeat.current_output_sha256+'\\nPrevious output SHA-256: '+(repeat.previous_output_sha256||'none')+'\\nSource SHA-256: '+data.technical_render.source_sha256;document.getElementById('technicalLinks').innerHTML='<a href=\"'+data.technical_render_url+'\" target=\"_blank\">Open source-backed plate</a> · <a href=\"'+data.technical_render_manifest_url+'\" target=\"_blank\">Open repeatability manifest</a>';",
    )
    return content


CORE.html_page = html_page


def main() -> int:
    return int(CORE.main())


if __name__ == "__main__":
    raise SystemExit(main())
