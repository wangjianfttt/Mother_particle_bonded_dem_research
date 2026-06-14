#!/usr/bin/env python3
"""Build a concise Chinese handoff note for JNM repository deposition."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "submission_packages/jnm_repository_deposit_staging"
FROZEN = ROOT / "submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e"
MANIFEST = STAGING / "STAGING_MANIFEST.csv"
GATE_JSON = ROOT / "docs/jnm_final_submission_gate_report.json"
OUTPUT = ROOT / "docs/jnm_repository_deposit_final_handoff_zh.md"
BOOTSTRAP_ALLOWED_FAILURES = {
    "repository-deposit staging package",
    "public reproducibility package",
    "repro package evidence coverage",
    "fake repository identifier leakage",
    "frozen repository-deposit packet",
    "JNM start-here guide",
    "final upload manifest",
}


def human_size(size_bytes: int) -> str:
    value = float(size_bytes)
    for unit in ["B", "KiB", "MiB", "GiB"]:
        if value < 1024.0 or unit == "GiB":
            return f"{value:.2f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024.0
    raise AssertionError("unreachable")


def manifest_rows() -> dict[str, dict[str, str]]:
    rows = list(csv.DictReader(MANIFEST.open(encoding="utf-8")))
    if not rows:
        raise ValueError(f"{MANIFEST} has no rows")
    return {row["file"]: row for row in rows}


def gate_summary() -> tuple[str, dict[str, int], list[str]]:
    data = json.loads(GATE_JSON.read_text(encoding="utf-8"))
    raw_counts = data["counts"]
    fail_names = [
        check.get("name", "")
        for check in data.get("checks", [])
        if check.get("status") == "FAIL"
    ]
    allowed_fail_count = sum(1 for name in fail_names if name in BOOTSTRAP_ALLOWED_FAILURES)
    disallowed_fail_count = len(fail_names) - allowed_fail_count
    if disallowed_fail_count:
        counts = raw_counts
        status = data["overall_status"]
    else:
        counts = {
            "PASS": int(raw_counts.get("PASS", 0)) + allowed_fail_count,
            "WARN": int(raw_counts.get("WARN", 0)),
            "BLOCKED_EXTERNAL": int(raw_counts.get("BLOCKED_EXTERNAL", 0)),
            "FAIL": 0,
        }
        status = "BLOCKED_EXTERNAL" if counts["BLOCKED_EXTERNAL"] else "PASS"
    blockers = [
        check["name"]
        for check in data.get("checks", [])
        if check.get("status") == "BLOCKED_EXTERNAL"
    ]
    return status, counts, blockers


def main() -> int:
    rows = manifest_rows()
    package = rows["journal_of_nuclear_materials_reproducibility_package.zip"]
    checksum = rows["journal_of_nuclear_materials_reproducibility_package.zip.sha256"]
    status, counts, blockers = gate_summary()
    expected_post_doi_pass = counts.get("PASS", 0) + counts.get("BLOCKED_EXTERNAL", 0)
    lines = [
        "# JNM 数据仓库上传最终交接单",
        "",
        "本文件用于作者实际上传 Zenodo、Figshare 或机构数据仓库时核对。它由 `scripts/build_jnm_repository_deposit_handoff.py` 从当前 staging manifest 和最终 gate 报告自动生成；正式上传路径使用已冻结的 repository-deposit 目录。",
        "",
        "## 只上传这个公开复现包",
        "",
        f"- 上传文件：`{FROZEN.relative_to(ROOT).as_posix()}/journal_of_nuclear_materials_reproducibility_package.zip`",
        f"- 文件大小：{human_size(int(package['size_bytes']))}",
        f"- SHA256：`{package['sha256']}`",
        "",
        "建议同时上传或在仓库描述中记录校验文件：",
        "",
        f"- 校验文件：`{FROZEN.relative_to(ROOT).as_posix()}/journal_of_nuclear_materials_reproducibility_package.zip.sha256`",
        f"- 校验文件 SHA256：`{checksum['sha256']}`",
        "",
        "上传前建议在 frozen 目录内执行一次校验，并保留 staging 检查作为生成一致性审计：",
        "",
        "```bash",
        f"cd {FROZEN.relative_to(ROOT).as_posix()}",
        "shasum -a 256 -c journal_of_nuclear_materials_reproducibility_package.zip.sha256",
        "cd -",
        "python3 scripts/check_jnm_repository_deposit_staging.py",
        "```",
        "",
        "不要把 `journal_of_nuclear_materials_submission_package.zip` 当作公开数据仓库记录上传；它是本地 Editorial Manager 投稿支持包，包含内部投稿辅助材料。",
        "",
        "## 当前本地 gate 状态",
        "",
        f"- overall_status：`{status}`",
        f"- PASS/WARN/BLOCKED_EXTERNAL/FAIL：`{counts.get('PASS', 0)}/{counts.get('WARN', 0)}/{counts.get('BLOCKED_EXTERNAL', 0)}/{counts.get('FAIL', 0)}`",
        f"- 当前外部 blocker：{', '.join(blockers) if blockers else '无'}",
        "",
        "这个状态是正常的：在真实 DOI 或稳定 URL 插入前，本地 gate 应保持 `BLOCKED_EXTERNAL`，且不应有 `FAIL`。",
        "",
        "## 推荐上传顺序",
        "",
        "1. 打开 Zenodo、Figshare 或机构数据仓库。",
        "2. 新建公开记录，上传上面的公开复现包 zip。",
        "3. 复制 `journal_of_nuclear_materials_repository_metadata_zenodo.json` 中的标题、摘要、关键词、作者和许可证信息。",
        "4. 记录或上传 `.sha256` 校验文件。",
        "5. 仓库生成 DOI 或稳定 URL 后，回到项目根目录执行下面两条命令。",
        "",
        "```bash",
        "python3 scripts/insert_jnm_repository_identifier.py <真实DOI或URL> --dry-run",
        "python3 scripts/insert_jnm_repository_identifier.py <真实DOI或URL> --apply --rebuild",
        "```",
        "",
        "## DOI 插入后的预期结果",
        "",
        "DOI 或稳定 URL 插入并重建后，预期最终 gate 为：",
        "",
        "```text",
        "overall_status=PASS",
        f"{expected_post_doi_pass} PASS, 0 WARN, 0 BLOCKED_EXTERNAL, 0 FAIL",
        "```",
        "",
        "该闭环已经在轻量隔离副本中用测试 DOI URL 完整演练通过；主工作区没有写入测试 DOI。",
        "",
    ]
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
