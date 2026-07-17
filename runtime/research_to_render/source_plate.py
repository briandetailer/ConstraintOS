from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class EmbeddedRasterCandidate:
    xref: int
    soft_mask_xref: int
    width: int
    height: int
    bits_per_component: int
    colorspace: str
    image_filter: str

    @property
    def pixel_area(self) -> int:
        return self.width * self.height

    def to_dict(self) -> dict[str, Any]:
        return {
            "xref": self.xref,
            "soft_mask_xref": self.soft_mask_xref,
            "width": self.width,
            "height": self.height,
            "pixel_area": self.pixel_area,
            "bits_per_component": self.bits_per_component,
            "colorspace": self.colorspace,
            "image_filter": self.image_filter,
        }


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_image_records(records: Iterable[tuple[Any, ...]]) -> tuple[EmbeddedRasterCandidate, ...]:
    parsed: list[EmbeddedRasterCandidate] = []
    seen_xrefs: set[int] = set()
    for record in records:
        if len(record) < 9:
            continue
        xref = int(record[0])
        if xref in seen_xrefs:
            continue
        seen_xrefs.add(xref)
        parsed.append(
            EmbeddedRasterCandidate(
                xref=xref,
                soft_mask_xref=int(record[1] or 0),
                width=int(record[2]),
                height=int(record[3]),
                bits_per_component=int(record[4] or 0),
                colorspace=str(record[5] or ""),
                image_filter=str(record[8] or ""),
            )
        )
    return tuple(parsed)


def select_largest_embedded_raster(
    candidates: Iterable[EmbeddedRasterCandidate],
    requirements: Mapping[str, Any],
) -> EmbeddedRasterCandidate:
    minimum_width = int(requirements.get("minimum_width", 1))
    minimum_height = int(requirements.get("minimum_height", 1))
    minimum_pixel_area = int(requirements.get("minimum_pixel_area", 1))
    reject_soft_masks = bool(requirements.get("reject_soft_masks", False))
    eligible = [
        candidate
        for candidate in candidates
        if candidate.width >= minimum_width
        and candidate.height >= minimum_height
        and candidate.pixel_area >= minimum_pixel_area
        and (not reject_soft_masks or candidate.soft_mask_xref == 0)
    ]
    if not eligible:
        raise RuntimeError(
            "No embedded raster satisfied the registered source-plate extraction requirements."
        )
    return max(
        eligible,
        key=lambda item: (
            item.pixel_area,
            item.width,
            item.height,
            -item.xref,
        ),
    )


def _load_fitz() -> Any:
    try:
        import fitz  # type: ignore[import-not-found]
    except ImportError as exc:
        raise RuntimeError(
            "Deterministic PDF source-plate extraction requires PyMuPDF. "
            "Install the ConstraintOS project dependencies, then retry."
        ) from exc
    return fitz


def extract_registered_source_plate(
    package_root: Path,
    contract_path: Path,
    output_root: Path | None = None,
) -> dict[str, Any]:
    package_root = package_root.resolve()
    contract_path = contract_path.resolve()
    manifest_path = package_root / "source-package-manifest.json"
    if not manifest_path.exists():
        raise RuntimeError(f"Missing source package manifest: {manifest_path}")
    if not contract_path.exists():
        raise RuntimeError(f"Missing source-plate extraction contract: {contract_path}")

    manifest = read_json(manifest_path)
    contract = read_json(contract_path)
    if manifest.get("preflight_status") != "source_files_materialized":
        raise RuntimeError("Source package is not in source_files_materialized state.")
    if contract.get("status") != "active":
        raise RuntimeError("Source-plate extraction contract is not active.")
    if manifest.get("scenario_id") != contract.get("scenario_id"):
        raise RuntimeError("Source package scenario does not match the extraction contract.")

    source_id = str(contract["source_id"])
    source_record = next(
        (
            item
            for item in manifest.get("materialized_sources", [])
            if item.get("source_id") == source_id
        ),
        None,
    )
    if source_record is None:
        raise RuntimeError(f"Materialized package does not contain source {source_id}.")

    source_path = package_root / str(source_record["local_file"])
    if not source_path.exists():
        raise RuntimeError(f"Registered source document is missing: {source_path}")
    expected_source_digest = str(source_record.get("sha256", "")).lower()
    observed_source_digest = sha256_file(source_path)
    if not expected_source_digest or expected_source_digest != observed_source_digest:
        raise RuntimeError("Registered source document digest does not match the package manifest.")

    fitz = _load_fitz()
    document = fitz.open(source_path)
    try:
        page_index = int(contract["document_page_index"])
        if page_index < 0 or page_index >= document.page_count:
            raise RuntimeError(
                f"Registered page index {page_index} does not exist in the source document."
            )
        page = document.load_page(page_index)
        candidates = parse_image_records(page.get_images(full=True))
        selected = select_largest_embedded_raster(
            candidates,
            contract["selection_requirements"],
        )
        extracted = document.extract_image(selected.xref)
    finally:
        document.close()

    image_bytes = extracted.get("image")
    if not isinstance(image_bytes, (bytes, bytearray)) or not image_bytes:
        raise RuntimeError("PyMuPDF did not return bytes for the selected embedded raster.")
    extension = str(extracted.get("ext") or "bin").lower().lstrip(".")
    if not extension.replace("_", "").isalnum():
        raise RuntimeError(f"Unsupported extracted image extension: {extension}")

    configured_output = contract["output"]
    derived_root = (
        output_root.resolve()
        if output_root is not None
        else package_root / str(configured_output.get("directory", "derived"))
    )
    derived_root.mkdir(parents=True, exist_ok=True)
    filename_stem = str(configured_output["filename_stem"])
    output_path = derived_root / f"{filename_stem}.{extension}"
    output_path.write_bytes(bytes(image_bytes))
    output_digest = sha256_file(output_path)

    result = {
        "manifest_id": "constraintos-derived-source-plate/v1",
        "manifest_version": "1.0.0",
        "status": "extracted",
        "scenario_id": contract["scenario_id"],
        "source_id": source_id,
        "source_package_manifest": str(manifest_path),
        "source_document": str(source_path),
        "source_document_sha256": observed_source_digest,
        "extraction_contract": str(contract_path),
        "extraction_contract_id": contract["contract_id"],
        "document_page_index": page_index,
        "selection_strategy": contract["selection_strategy"],
        "selected_raster": {
            **selected.to_dict(),
            "extracted_extension": extension,
            "extracted_width": int(extracted.get("width") or selected.width),
            "extracted_height": int(extracted.get("height") or selected.height),
        },
        "eligible_candidate_count": len(candidates),
        "output_file": str(output_path),
        "output_sha256": output_digest,
        "production_ready": False,
        "production_blockers": [
            "manual_source_plate_review_required",
            "component_anchor_registry_not_built",
            "fixed_view_render_contract_not_registered",
            "render_preset_not_registered",
            "source_usage_terms_review_required",
        ],
        "approval_allowed": False,
        "review_decision": "needs_review",
    }
    derived_manifest_path = derived_root / "source-plate-extraction-manifest.json"
    write_json(derived_manifest_path, result)
    result["derived_manifest"] = str(derived_manifest_path)
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cos-extract-source-plate",
        description="Extract a deterministic embedded raster from a registered PDF source package.",
    )
    parser.add_argument("--package-root", type=Path, required=True)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--output-root", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = extract_registered_source_plate(
        args.package_root,
        args.contract,
        args.output_root,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
