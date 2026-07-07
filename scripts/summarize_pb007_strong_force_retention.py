#!/usr/bin/env python3
"""Compute PB-007 strong-force tail and contact-retention metrics.

The script reads existing native pair-contact local dumps, aggregates
subparticle contacts to parent-particle edges and compares the strongest
parent-parent contacts between adjacent saved states. It does not infer new
fracture events or require a DEM rerun.
"""

from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
CASES_ROOT = ROOT / "simulations" / "pebble_bed" / "PB-007" / "cases"
STATE_OUT = ROOT / "tables" / "pb007_strong_force_tail_state_metrics.csv"
RETENTION_OUT = ROOT / "tables" / "pb007_strong_force_retention.csv"
AUDIT_OUT = ROOT / "docs" / "pb007_strong_force_retention_audit_20260707.md"


@dataclass(frozen=True)
class Case:
    label: str
    case_id: str


CASES = [
    Case("Pilot", "PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot"),
    Case("Intact", "PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed02"),
    Case("Delayed", "PB-007-bonded-steprelaxed-100-seed03-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed03"),
    Case("Early", "PB-007-bonded-steprelaxed-100-seed04-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed04"),
    Case("Synchronous", "PB-007-bonded-steprelaxed-100-seed06-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed06"),
    Case("Intact 0.5x", "PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p5-trigger-seed02"),
    Case("Intact 0.25x", "PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p25-trigger-seed02"),
    Case("200-bed", "PB-007-bonded-steprelaxed-200-seed09-midbox-fast600ksettle-y1p5e10-10kstage-hold100-60um-fracture-200bed"),
    Case("200-bed 0.25x", "PB-007-bonded-steprelaxed-200-seed09-midbox-fast600ksettle-60um-strength0p25-200bed"),
]


def dump_timestep(path: Path) -> int:
    with path.open(errors="ignore") as handle:
        for line in handle:
            if line.strip() == "ITEM: TIMESTEP":
                return int(next(handle).strip())
    raise ValueError(f"No timestep found in {path}")


def entry_count(path: Path) -> int | None:
    with path.open(errors="ignore") as handle:
        for line in handle:
            if line.startswith("ITEM: NUMBER OF ENTRIES"):
                return int(next(handle).strip())
    return None


def iter_local_rows(path: Path):
    n_entries = entry_count(path)
    with path.open(errors="ignore") as handle:
        for line in handle:
            if line.startswith("ITEM: ENTRIES"):
                break
        for index, line in enumerate(handle):
            if n_entries is not None and index >= n_entries:
                break
            parts = line.split()
            if len(parts) < 10:
                continue
            try:
                yield [float(value) for value in parts[:10]]
            except ValueError:
                continue


def parent_id(atom_id: int, nspheres: int) -> int:
    return (atom_id - 1) // nspheres + 1


def aggregate_edges(path: Path, nspheres: int) -> dict[tuple[int, int], dict[str, float]]:
    edge_data: dict[tuple[int, int], dict[str, float]] = {}
    for row in iter_local_rows(path):
        delta = row[9]
        if delta <= 0.0:
            continue
        first = parent_id(int(row[0]), nspheres)
        second = parent_id(int(row[1]), nspheres)
        if first == second:
            continue
        edge = tuple(sorted((first, second)))
        force = math.sqrt(row[3] ** 2 + row[4] ** 2 + row[5] ** 2)
        stat = edge_data.setdefault(
            edge,
            {"subcontacts": 0.0, "force_sum_N": 0.0, "force_max_N": 0.0, "overlap_max_m": 0.0},
        )
        stat["subcontacts"] += 1.0
        stat["force_sum_N"] += force
        stat["force_max_N"] = max(stat["force_max_N"], force)
        stat["overlap_max_m"] = max(stat["overlap_max_m"], delta)
    return edge_data


def load_edges_csv(path: Path) -> dict[tuple[int, int], dict[str, float]]:
    edges: dict[tuple[int, int], dict[str, float]] = {}
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if not row:
                continue
            edge = tuple(sorted((int(float(row["mother_i"])), int(float(row["mother_j"])))))
            edges[edge] = {
                "subcontacts": float(row.get("subcontacts", 0.0) or 0.0),
                "force_sum_N": float(row.get("force_sum_N", 0.0) or 0.0),
                "force_max_N": float(row.get("force_max_N", 0.0) or 0.0),
                "overlap_max_m": float(row.get("overlap_max_m", 0.0) or 0.0),
            }
    return edges


def state_paths(case_dir: Path) -> list[tuple[int, str, Path]]:
    post = case_dir / "post"
    paths: list[tuple[int, str, Path]] = []
    for path in post.glob("pairs_event_*.local"):
        paths.append((dump_timestep(path), "event", path))
    final = post / "pairs_final.local"
    if final.exists() and final.stat().st_size > 0:
        paths.append((dump_timestep(final), "final", final))
    paths.sort(key=lambda item: (item[0], item[1] != "event"))
    dedup: dict[int, tuple[int, str, Path]] = {}
    for step, state_kind, path in paths:
        if step not in dedup or state_kind == "final":
            dedup[step] = (step, state_kind, path)
    return [dedup[step] for step in sorted(dedup)]


def final_timestep_from_summary(case_id: str) -> int:
    acceptance = ROOT / "tables" / f"pb007_{case_id}_acceptance_summary.csv"
    if acceptance.exists():
        with acceptance.open(newline="") as handle:
            row = next(csv.DictReader(handle))
            if row.get("last_valid_bond_step"):
                return int(float(row["last_valid_bond_step"]))
    return -1


def final_edges_path(case_id: str) -> Path:
    return ROOT / "tables" / f"pb007_{case_id}_native_edges.csv"


def top_edges(edges: dict[tuple[int, int], dict[str, float]], fraction: float) -> set[tuple[int, int]]:
    if not edges:
        return set()
    ordered = sorted(edges.items(), key=lambda item: item[1]["force_sum_N"], reverse=True)
    count = max(1, math.ceil(len(ordered) * fraction))
    return {edge for edge, _ in ordered[:count]}


def force_tail_metrics(edges: dict[tuple[int, int], dict[str, float]]) -> dict[str, float | int]:
    values = np.array([stat["force_sum_N"] for stat in edges.values()], dtype=float)
    subcontacts = int(sum(stat["subcontacts"] for stat in edges.values()))
    if values.size == 0:
        return {
            "inter_parent_edges": 0,
            "inter_parent_subcontacts": subcontacts,
            "inter_parent_force_sum_N": 0.0,
            "mean_edge_force_N": 0.0,
            "median_edge_force_N": 0.0,
            "F95_edge_force_N": 0.0,
            "F99_edge_force_N": 0.0,
            "max_edge_force_N": 0.0,
            "top5_force_share": 0.0,
            "top1_force_share": 0.0,
            "top5_edge_count": 0,
            "top1_edge_count": 0,
        }
    values_sorted = np.sort(values)[::-1]
    total = float(values.sum())
    top5_count = max(1, math.ceil(values.size * 0.05))
    top1_count = max(1, math.ceil(values.size * 0.01))
    return {
        "inter_parent_edges": int(values.size),
        "inter_parent_subcontacts": subcontacts,
        "inter_parent_force_sum_N": total,
        "mean_edge_force_N": float(values.mean()),
        "median_edge_force_N": float(np.median(values)),
        "F95_edge_force_N": float(np.percentile(values, 95)),
        "F99_edge_force_N": float(np.percentile(values, 99)),
        "max_edge_force_N": float(values.max()),
        "top5_force_share": float(values_sorted[:top5_count].sum() / total) if total else 0.0,
        "top1_force_share": float(values_sorted[:top1_count].sum() / total) if total else 0.0,
        "top5_edge_count": top5_count,
        "top1_edge_count": top1_count,
    }


def retention_row(
    case: Case,
    previous: dict[str, object],
    current: dict[str, object],
    fraction: float,
    label: str,
) -> dict[str, object]:
    before = top_edges(previous["edges"], fraction)  # type: ignore[arg-type]
    after = top_edges(current["edges"], fraction)  # type: ignore[arg-type]
    union = before | after
    intersection = before & after
    jaccard = len(intersection) / len(union) if union else 1.0
    retention = len(intersection) / len(before) if before else 1.0
    current_capture = len(intersection) / len(after) if after else 1.0
    return {
        "case_label": case.label,
        "case_id": case.case_id,
        "previous_timestep": previous["timestep"],
        "current_timestep": current["timestep"],
        "previous_state_kind": previous["state_kind"],
        "current_state_kind": current["state_kind"],
        "strong_fraction": label,
        "previous_strong_edge_count": len(before),
        "current_strong_edge_count": len(after),
        "shared_strong_edge_count": len(intersection),
        "jaccard_overlap": jaccard,
        "pre_event_retention": retention,
        "current_set_capture": current_capture,
        "previous_force_sum_N": previous["inter_parent_force_sum_N"],
        "current_force_sum_N": current["inter_parent_force_sum_N"],
        "force_sum_ratio_current_to_previous": (
            float(current["inter_parent_force_sum_N"]) / float(previous["inter_parent_force_sum_N"])
            if float(previous["inter_parent_force_sum_N"])
            else float("nan")
        ),
        "previous_F95_edge_force_N": previous["F95_edge_force_N"],
        "current_F95_edge_force_N": current["F95_edge_force_N"],
        "previous_F99_edge_force_N": previous["F99_edge_force_N"],
        "current_F99_edge_force_N": current["F99_edge_force_N"],
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def build_audit(
    path: Path,
    state_rows: list[dict[str, object]],
    retention_rows: list[dict[str, object]],
    missing_cases: list[str],
) -> None:
    cracking = [row for row in state_rows if row["case_label"] in {"Pilot", "Delayed", "Early", "Synchronous"}]
    intact = [row for row in state_rows if "Intact" in str(row["case_label"]) or str(row["case_label"]).startswith("200-bed")]
    final_rows = [row for row in state_rows if row["state_kind"] == "final"]

    def mean_value(rows: list[dict[str, object]], key: str) -> float:
        values = [float(row[key]) for row in rows if row.get(key) not in {"", None}]
        return float(np.mean(values)) if values else float("nan")

    lines = [
        "# PB-007 strong-force retention audit (2026-07-07)",
        "",
        "## Scope",
        "",
        "This audit mines existing PB-007 native pair-contact local dumps. It does not launch new DEM simulations and does not restore full raw trajectories from the NAS.",
        "",
        "## Generated artifacts",
        "",
        f"- `{STATE_OUT.relative_to(ROOT)}`: state-wise strong-force-tail metrics.",
        f"- `{RETENTION_OUT.relative_to(ROOT)}`: adjacent-state strong-contact overlap and retention.",
        "",
        "## Coverage",
        "",
        f"- State rows: `{len(state_rows)}`",
        f"- Adjacent-state retention rows: `{len(retention_rows)}`",
        f"- Missing or unavailable cases: `{len(missing_cases)}`",
    ]
    if missing_cases:
        lines.extend(["", "Missing case ids:", ""])
        lines.extend(f"- `{case_id}`" for case_id in missing_cases)
    lines.extend(
        [
            "",
            "## Conservative interpretation",
            "",
            f"- Mean top-5% force share in cracking-case saved states: `{mean_value(cracking, 'top5_force_share'):.3f}`.",
            f"- Mean top-5% force share in intact/200-parent saved states: `{mean_value(intact, 'top5_force_share'):.3f}`.",
            f"- Mean final-state F95 edge force across available endpoints: `{mean_value(final_rows, 'F95_edge_force_N'):.6g} N`.",
            "",
            "These metrics strengthen the mechanism-variable route by separating load-bearing intensity and strong-contact persistence from top-wall displacement history. They should be used as source-backed state descriptors, not as a converged failure-probability law.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nspheres", type=int, default=500)
    parser.add_argument("--state-output", type=Path, default=STATE_OUT)
    parser.add_argument("--retention-output", type=Path, default=RETENTION_OUT)
    parser.add_argument("--audit-output", type=Path, default=AUDIT_OUT)
    args = parser.parse_args()

    state_rows: list[dict[str, object]] = []
    retention_rows: list[dict[str, object]] = []
    missing_cases: list[str] = []

    for case in CASES:
        case_dir = CASES_ROOT / case.case_id
        if not case_dir.exists():
            missing_cases.append(case.case_id)
            continue
        states = []
        seen_final = False
        for timestep, state_kind, path in state_paths(case_dir):
            edges = aggregate_edges(path, args.nspheres)
            metrics = force_tail_metrics(edges)
            row: dict[str, object] = {
                "case_label": case.label,
                "case_id": case.case_id,
                "timestep": timestep,
                "state_kind": state_kind,
                "source_kind": "pair_local_dump",
                "pair_file": str(path),
            }
            row.update(metrics)
            state_rows.append(row)
            state_with_edges = dict(row)
            state_with_edges["edges"] = edges
            states.append(state_with_edges)
            seen_final = seen_final or state_kind == "final"

        edge_csv = final_edges_path(case.case_id)
        if not seen_final and edge_csv.exists() and edge_csv.stat().st_size > 0:
            timestep = final_timestep_from_summary(case.case_id)
            edges = load_edges_csv(edge_csv)
            metrics = force_tail_metrics(edges)
            row = {
                "case_label": case.label,
                "case_id": case.case_id,
                "timestep": timestep,
                "state_kind": "final",
                "source_kind": "native_edges_csv",
                "pair_file": str(edge_csv),
            }
            row.update(metrics)
            state_rows.append(row)
            state_with_edges = dict(row)
            state_with_edges["edges"] = edges
            states.append(state_with_edges)
            states.sort(key=lambda item: int(item["timestep"]))

        for previous, current in zip(states, states[1:]):
            retention_rows.append(retention_row(case, previous, current, 0.05, "top5pct"))
            retention_rows.append(retention_row(case, previous, current, 0.01, "top1pct"))

    write_csv(args.state_output, state_rows)
    write_csv(args.retention_output, retention_rows)
    build_audit(args.audit_output, state_rows, retention_rows, missing_cases)
    print(args.state_output)
    print(args.retention_output)
    print(args.audit_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
