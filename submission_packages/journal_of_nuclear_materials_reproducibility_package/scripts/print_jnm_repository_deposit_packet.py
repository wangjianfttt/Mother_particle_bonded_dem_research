#!/usr/bin/env python3
"""Print a concise author-facing summary of the JNM repository deposit packet."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "submission_packages/jnm_repository_deposit_staging"
MANIFEST = STAGING / "STAGING_MANIFEST.csv"
FROZEN = ROOT / "submission_packages/jnm_repository_deposit_FROZEN_20260614_ffa2c5d8"
GATE_JSON = ROOT / "docs/jnm_final_submission_gate_report.json"
PACKAGE_NAME = "journal_of_nuclear_materials_reproducibility_package.zip"
CHECKSUM_NAME = PACKAGE_NAME + ".sha256"
SUBMISSION_PACKAGE = ROOT / "submission_packages/journal_of_nuclear_materials_submission_package.zip"
SUBMISSION_CHECKSUM = ROOT / "submission_packages/journal_of_nuclear_materials_submission_package.zip.sha256"
FLAT_SOURCE_PACKAGE = ROOT / "submission_packages/journal_of_nuclear_materials_flat_source.zip"
UPLOAD_READY_PACKAGE = ROOT / "submission_packages/jnm_editorial_manager_upload_ready.zip"
AUTHOR_UPLOAD_README = ROOT / "docs/jnm_author_final_upload_readme_zh.md"
COAUTHOR_APPROVAL = ROOT / "docs/jnm_coauthor_final_approval_packet.md"
FINAL_ACTION_SUMMARY = ROOT / "docs/jnm_final_submission_action_summary.md"
PASTE_FIELDS = ROOT / "manuscript/journal_of_nuclear_materials_editorial_manager_paste_fields.md"
DOCX_QA = ROOT / "docs/jnm_upload_docx_qa.md"


def load_manifest() -> dict[str, dict[str, str]]:
    if not MANIFEST.exists():
        raise SystemExit(f"Missing staging manifest: {MANIFEST}")
    rows = list(csv.DictReader(MANIFEST.open()))
    return {row["file"]: row for row in rows}


def load_gate() -> dict[str, object]:
    if not GATE_JSON.exists():
        raise SystemExit(f"Missing final gate report: {GATE_JSON}")
    return json.loads(GATE_JSON.read_text())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def file_line(label: str, path: Path, *, include_hash: bool = False) -> None:
    if not path.exists():
        print(f"{label}: MISSING {path}")
        return
    size = path.stat().st_size / (1024 * 1024)
    print(f"{label}: {rel(path)} ({size:.2f} MiB)")
    if include_hash:
        print(f"{label} sha256: {sha256(path)}")


def main() -> int:
    manifest = load_manifest()
    gate = load_gate()

    package = manifest.get(PACKAGE_NAME)
    checksum = manifest.get(CHECKSUM_NAME)
    if package is None or checksum is None:
        raise SystemExit("Staging manifest is missing the package or checksum entry.")
    frozen_package = FROZEN / PACKAGE_NAME
    frozen_checksum = FROZEN / CHECKSUM_NAME
    if not frozen_package.exists() or not frozen_checksum.exists():
        raise SystemExit(f"Frozen repository-deposit packet is incomplete: {FROZEN}")

    counts = gate.get("counts", {})
    blockers = [
        check.get("name", "")
        for check in gate.get("checks", [])
        if check.get("status") == "BLOCKED_EXTERNAL"
    ]
    failures = [
        check.get("name", "")
        for check in gate.get("checks", [])
        if check.get("status") == "FAIL"
    ]
    expected_post_doi_pass = int(counts.get("PASS", 0)) + int(counts.get("BLOCKED_EXTERNAL", 0))

    print("JNM final submission dashboard / JNM 最终投稿仪表盘")
    print("=" * 72)
    print("Repository deposit packet / 数据仓库上传包")
    print("-" * 72)
    print(f"Frozen upload folder: {FROZEN.relative_to(ROOT)}")
    print(f"Upload file: {FROZEN.relative_to(ROOT) / PACKAGE_NAME}")
    print(f"Package size: {frozen_package.stat().st_size / (1024 * 1024):.2f} MiB")
    print(f"Package sha256: {sha256(frozen_package)}")
    print(f"Checksum file: {FROZEN.relative_to(ROOT) / CHECKSUM_NAME}")
    print(f"Checksum-file sha256: {sha256(frozen_checksum)}")
    print(f"Staging audit folder: {STAGING.relative_to(ROOT)}")
    print()

    print("Editorial Manager local support files / 投稿系统本地支持文件")
    print("-" * 72)
    file_line("Upload-ready package", UPLOAD_READY_PACKAGE, include_hash=True)
    file_line("Submission support package", SUBMISSION_PACKAGE, include_hash=True)
    file_line("Flat LaTeX source package", FLAT_SOURCE_PACKAGE, include_hash=True)
    print(f"Submission checksum file: {rel(SUBMISSION_CHECKSUM)}")
    print(f"Paste-ready fields: {rel(PASTE_FIELDS)}")
    print("Cover letter DOCX: manuscript/journal_of_nuclear_materials_cover_letter.docx")
    print("Declarations DOCX: manuscript/journal_of_nuclear_materials_elsevier_declarations.docx")
    print(f"DOCX QA note: {rel(DOCX_QA)}")
    print(f"Chinese final-upload README: {rel(AUTHOR_UPLOAD_README)}")
    print(f"Final action summary: {rel(FINAL_ACTION_SUMMARY)}")
    print(f"Coauthor approval packet: {rel(COAUTHOR_APPROVAL)}")
    print()

    print("Gate status / 本地投稿 gate")
    print("-" * 72)
    print(f"overall_status={gate.get('overall_status')}")
    print(
        "counts="
        f"PASS {counts.get('PASS', 0)}, "
        f"WARN {counts.get('WARN', 0)}, "
        f"BLOCKED_EXTERNAL {counts.get('BLOCKED_EXTERNAL', 0)}, "
        f"FAIL {counts.get('FAIL', 0)}"
    )
    print("external_blockers=" + (", ".join(blockers) if blockers else "none"))
    print("failures=" + (", ".join(failures) if failures else "none"))
    print(
        "expected_after_repository_identifier="
        f"PASS {expected_post_doi_pass}, WARN 0, BLOCKED_EXTERNAL 0, FAIL 0"
    )
    print()
    print("Upload guidance / 上传提示")
    print("-" * 72)
    print("1. Upload the frozen reproducibility package zip above to Zenodo, Figshare or an institutional repository.")
    print("2. Keep or upload the .sha256 checksum file as supporting metadata.")
    print("3. Do not use journal_of_nuclear_materials_submission_package.zip as the public data record.")
    print("4. After the repository gives a DOI or stable URL, run:")
    print("   python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --dry-run")
    print("   python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --apply --rebuild")
    print("5. Expected after DOI insertion: overall_status=PASS with no FAIL/WARN/BLOCKED_EXTERNAL.")
    print("6. Then use the local submission support package and paste-ready fields for Editorial Manager.")
    print()
    print("Chinese checklist / 中文清单")
    print("-" * 72)
    print(f"{FROZEN.relative_to(ROOT) / 'jnm_repository_deposit_action_checklist_zh.md'}")
    print(rel(AUTHOR_UPLOAD_README))
    print(rel(COAUTHOR_APPROVAL))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
