import hashlib
import json
from pathlib import Path

import pytest

import runtime.research_to_render.source_plate as source_plate
from runtime.research_to_render.source_plate import (
    EmbeddedRasterCandidate,
    extract_registered_source_plate,
    select_largest_embedded_raster,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "config"
    / "research-source-plate-extraction"
    / "raspberry-pi-5-product-brief-v1.json"
)
SCRIPT = ROOT / "scripts" / "prepare-raspberry-pi-5-source-plate.ps1"
PYPROJECT = ROOT / "pyproject.toml"


class FakePage:
    def get_images(self, full: bool):
        assert full is True
        return [
            (10, 0, 120, 80, 8, "DeviceRGB", "", "small", "FlateDecode"),
            (20, 0, 900, 450, 8, "DeviceRGB", "", "board", "DCTDecode"),
            (30, 0, 500, 250, 8, "DeviceRGB", "", "medium", "FlateDecode"),
        ]


class FakeDocument:
    page_count = 2

    def __init__(self) -> None:
        self.closed = False

    def load_page(self, page_index: int) -> FakePage:
        assert page_index == 1
        return FakePage()

    def extract_image(self, xref: int) -> dict:
        assert xref == 20
        return {
            "image": b"deterministic-raspberry-pi-source-raster",
            "ext": "jpg",
            "width": 900,
            "height": 450,
        }

    def close(self) -> None:
        self.closed = True


class FakeFitz:
    def __init__(self, document: FakeDocument) -> None:
        self.document = document

    def open(self, path: Path) -> FakeDocument:
        assert path.exists()
        return self.document


def install_package(tmp_path: Path) -> tuple[Path, Path]:
    package_root = tmp_path / "reference-sources" / "raspberry_pi_5_io_plate"
    source_document = package_root / "files" / "raspberry-pi-5-official-top-view-source-plate.pdf"
    source_document.parent.mkdir(parents=True)
    source_document.write_bytes(b"registered-product-brief-pdf")
    digest = hashlib.sha256(source_document.read_bytes()).hexdigest()
    manifest = {
        "manifest_id": "constraintos-reference-source-package/v1",
        "manifest_version": "1.1.0",
        "scenario_id": "raspberry_pi_5_io_plate",
        "preflight_status": "source_files_materialized",
        "materialized_sources": [
            {
                "source_id": "rpi5-official-top-view-source-plate-2026",
                "local_file": "files/raspberry-pi-5-official-top-view-source-plate.pdf",
                "sha256": digest,
                "status": "materialized",
            }
        ],
    }
    (package_root / "source-package-manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return package_root, source_document


def test_largest_embedded_raster_selection_is_deterministic() -> None:
    candidates = (
        EmbeddedRasterCandidate(3, 0, 800, 400, 8, "RGB", "DCT"),
        EmbeddedRasterCandidate(2, 0, 800, 400, 8, "RGB", "DCT"),
        EmbeddedRasterCandidate(1, 0, 400, 200, 8, "RGB", "Flate"),
    )
    requirements = {
        "minimum_width": 400,
        "minimum_height": 200,
        "minimum_pixel_area": 80000,
    }

    selected = select_largest_embedded_raster(candidates, requirements)

    assert selected.xref == 2
    assert selected.pixel_area == 320000


def test_source_plate_extraction_verifies_digest_and_preserves_bytes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    package_root, _ = install_package(tmp_path)
    fake_document = FakeDocument()
    monkeypatch.setattr(
        source_plate,
        "_load_fitz",
        lambda: FakeFitz(fake_document),
    )

    result = extract_registered_source_plate(package_root, CONTRACT)

    output_path = Path(result["output_file"])
    assert result["status"] == "extracted"
    assert result["selected_raster"]["xref"] == 20
    assert result["selected_raster"]["extracted_width"] == 900
    assert result["selected_raster"]["extracted_height"] == 450
    assert output_path.suffix == ".jpg"
    assert output_path.read_bytes() == b"deterministic-raspberry-pi-source-raster"
    assert result["output_sha256"] == hashlib.sha256(output_path.read_bytes()).hexdigest()
    assert result["production_ready"] is False
    assert result["approval_allowed"] is False
    assert "component_anchor_registry_not_built" in result["production_blockers"]
    assert Path(result["derived_manifest"]).exists()
    assert fake_document.closed is True


def test_source_plate_extraction_fails_closed_on_digest_mismatch(
    tmp_path: Path,
) -> None:
    package_root, source_document = install_package(tmp_path)
    source_document.write_bytes(b"changed-after-manifest")

    with pytest.raises(RuntimeError, match="digest does not match"):
        extract_registered_source_plate(package_root, CONTRACT)


def test_extraction_contract_and_windows_script_are_registered() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    script = SCRIPT.read_text(encoding="utf-8")
    pyproject = PYPROJECT.read_text(encoding="utf-8")

    assert contract["status"] == "active"
    assert contract["document_page_index"] == 1
    assert contract["selection_strategy"] == "largest_embedded_raster_on_page"
    assert contract["capability_limits"]["fixed_view_only"] is True
    assert contract["capability_limits"]["automatic_component_identification_allowed"] is False
    assert "runtime.research_to_render.source_plate" in script
    assert "source-plate-extraction-manifest.json" in script
    assert 'cos-extract-source-plate = "runtime.research_to_render.source_plate:main"' in pyproject
    assert '"pymupdf>=1.24,<2"' in pyproject
