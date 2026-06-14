#!/usr/bin/env python3
"""Reconstruct time-resolved mother-pebble contact networks from saved dumps.

Cross-mother subparticle overlaps are converted to elastic normal forces with
the Hertz law used by the DEM contact model. The reconstruction omits damping
and tangential-history terms, so outputs are elastic-network diagnostics rather
than native contact-force histories.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path

import networkx as nx
import numpy as np
from scipy.spatial import cKDTree


def read_dump(path: Path, nspheres: int) -> tuple[int, np.ndarray, np.ndarray, np.ndarray]:
    with path.open() as handle:
        if not handle.readline().startswith("ITEM: TIMESTEP"):
            raise ValueError(f"{path} is not a particle dump")
        step = int(handle.readline())
        handle.readline()
        natoms = int(handle.readline())
        handle.readline()
        for _ in range(3):
            handle.readline()
        names = handle.readline().split()[2:]
    columns = {name: index for index, name in enumerate(names)}
    required = ("id", "x", "y", "z", "radius")
    missing = [name for name in required if name not in columns]
    if missing:
        raise ValueError(f"{path} missing columns {missing}")
    raw = np.loadtxt(path, skiprows=9)
    if raw.shape[0] != natoms:
        raise ValueError(f"{path}: expected {natoms} atoms, read {raw.shape[0]}")
    atom_ids = raw[:, columns["id"]].astype(np.int64)
    mother_ids = (atom_ids - 1) // nspheres + 1
    positions = raw[:, [columns["x"], columns["y"], columns["z"]]]
    radii = raw[:, columns["radius"]]
    return step, mother_ids, positions, radii


def hertz_force(overlap: np.ndarray, effective_radius: np.ndarray, young: float, poisson: float) -> np.ndarray:
    effective_modulus = young / (2.0 * (1.0 - poisson**2))
    return (4.0 / 3.0) * effective_modulus * np.sqrt(effective_radius) * overlap**1.5


def participation(weights: np.ndarray) -> float:
    total = float(weights.sum())
    denominator = float(np.square(weights).sum())
    return total * total / denominator if denominator > 0.0 else 0.0


def normalized_entropy(weights: np.ndarray) -> float:
    positive = weights[weights > 0.0]
    if positive.size <= 1:
        return 0.0
    probabilities = positive / positive.sum()
    return float(-(probabilities * np.log(probabilities)).sum() / math.log(positive.size))


def gini(weights: np.ndarray) -> float:
    positive = np.sort(weights[weights > 0.0])
    if positive.size == 0:
        return 0.0
    indices = np.arange(1, positive.size + 1)
    return float((2.0 * np.sum(indices * positive) / (positive.size * positive.sum())) - (positive.size + 1) / positive.size)


def event_history(path: Path) -> list[tuple[int, int]]:
    totals: dict[int, int] = defaultdict(int)
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            totals[int(row["timestep"])] += int(float(row["new_broken_bonds"]))
    running = 0
    history = []
    for step, increment in sorted(totals.items()):
        running += increment
        history.append((step, running))
    return history


def cumulative_at(step: int, history: list[tuple[int, int]]) -> int:
    value = 0
    for event_step, cumulative in history:
        if event_step > step:
            break
        value = cumulative
    return value


def thermo_history(path: Path) -> list[tuple[int, float]]:
    rows = []
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("Step") and row.get("top_forc"):
                rows.append((int(float(row["Step"])), abs(float(row["top_forc"]))))
    return rows


def nearest_force(step: int, history: list[tuple[int, float]]) -> float:
    return min(history, key=lambda item: abs(item[0] - step))[1]


def connected_metrics(edge_forces: dict[tuple[int, int], float]) -> tuple[int, int, float, float]:
    graph = nx.Graph()
    for (a, b), force in edge_forces.items():
        graph.add_edge(a, b, weight=force)
    if graph.number_of_nodes() == 0:
        return 0, 0, 0.0, 0.0
    largest = max(nx.connected_components(graph), key=len)
    strengths = np.array([value for _, value in graph.degree(weight="weight")], dtype=float)
    return graph.number_of_nodes(), len(largest), participation(strengths), normalized_entropy(strengths)


def analyze_dump(
    dump_path: Path,
    nspheres: int,
    wall_zhi: float,
    pre_steps: int,
    top_speed: float,
    dt: float,
    young: float,
    poisson: float,
    event_rows: list[tuple[int, int]],
    thermo_rows: list[tuple[int, float]],
    plate_area_m2: float,
    bed_height_m: float,
) -> tuple[dict[str, float | int], list[dict[str, float | int]]]:
    step, mothers, positions, radii = read_dump(dump_path, nspheres)
    tree = cKDTree(positions)
    candidates = tree.query_pairs(2.0 * float(radii.max()), output_type="ndarray")
    if candidates.size:
        different = mothers[candidates[:, 0]] != mothers[candidates[:, 1]]
        candidates = candidates[different]

    edge_stats: dict[tuple[int, int], dict[str, float | int]] = defaultdict(
        lambda: {"contacts": 0, "force": 0.0, "max_force": 0.0, "overlap": 0.0}
    )
    fabric = np.zeros((3, 3), dtype=float)
    contact_force_total = 0.0
    if candidates.size:
        vectors = positions[candidates[:, 1]] - positions[candidates[:, 0]]
        distances = np.linalg.norm(vectors, axis=1)
        overlap = radii[candidates[:, 0]] + radii[candidates[:, 1]] - distances
        active = overlap > 0.0
        candidates = candidates[active]
        vectors = vectors[active]
        distances = distances[active]
        overlap = overlap[active]
        normals = vectors / distances[:, None]
        effective_radius = (
            radii[candidates[:, 0]] * radii[candidates[:, 1]]
            / (radii[candidates[:, 0]] + radii[candidates[:, 1]])
        )
        forces = hertz_force(overlap, effective_radius, young, poisson)
        contact_force_total = float(forces.sum())
        fabric = np.einsum("i,ij,ik->jk", forces, normals, normals)
        if contact_force_total > 0.0:
            fabric /= contact_force_total
        for pair, delta, force in zip(candidates, overlap, forces):
            a, b = sorted((int(mothers[pair[0]]), int(mothers[pair[1]])))
            stats = edge_stats[(a, b)]
            stats["contacts"] += 1
            stats["force"] += float(force)
            stats["max_force"] = max(float(stats["max_force"]), float(force))
            stats["overlap"] += float(delta)

    top_z = wall_zhi - max(0.0, top_speed * (step - pre_steps) * dt)
    wall_overlap = positions[:, 2] + radii - top_z
    wall_active = wall_overlap > 0.0
    wall_forces = hertz_force(wall_overlap[wall_active], radii[wall_active], young, poisson)
    wall_mothers = mothers[wall_active]
    wall_by_mother: dict[int, float] = defaultdict(float)
    wall_contacts_by_mother: dict[int, int] = defaultdict(int)
    for mother, force in zip(wall_mothers, wall_forces):
        wall_by_mother[int(mother)] += float(force)
        wall_contacts_by_mother[int(mother)] += 1
    wall_weights = np.array(list(wall_by_mother.values()), dtype=float)

    edge_forces = {edge: float(stats["force"]) for edge, stats in edge_stats.items()}
    active_nodes, largest_component, network_neff, network_entropy = connected_metrics(edge_forces)
    edge_weights = np.array(list(edge_forces.values()), dtype=float)
    fabric_deviator = fabric - np.eye(3) / 3.0
    fabric_anisotropy = math.sqrt(1.5 * float(np.square(fabric_deviator).sum())) if contact_force_total else 0.0
    top_force = nearest_force(step, thermo_rows)
    displacement_m = max(0.0, top_speed * (step - pre_steps) * dt)

    summary: dict[str, float | int] = {
        "timestep": step,
        "top_displacement_mm": displacement_m * 1000.0,
        "engineering_strain_percent": 100.0 * displacement_m / bed_height_m,
        "top_plate_force_N": top_force,
        "top_plate_pressure_MPa": top_force / plate_area_m2 / 1.0e6,
        "cumulative_localized_broken_bonds": cumulative_at(step, event_rows),
        "inter_pebble_edges": len(edge_stats),
        "inter_subparticle_contacts": int(sum(int(stats["contacts"]) for stats in edge_stats.values())),
        "reconstructed_inter_normal_force_N": contact_force_total,
        "active_network_pebbles": active_nodes,
        "largest_component_pebbles": largest_component,
        "network_effective_pebbles": network_neff,
        "network_strength_entropy": network_entropy,
        "edge_force_effective_count": participation(edge_weights),
        "edge_force_gini": gini(edge_weights),
        "force_weighted_fabric_xx": float(fabric[0, 0]),
        "force_weighted_fabric_yy": float(fabric[1, 1]),
        "force_weighted_fabric_zz": float(fabric[2, 2]),
        "force_weighted_fabric_anisotropy": fabric_anisotropy,
        "topwall_loaded_pebbles": len(wall_by_mother),
        "topwall_subparticle_contacts": int(wall_active.sum()),
        "reconstructed_topwall_normal_force_N": float(wall_forces.sum()),
        "topwall_effective_pebbles": participation(wall_weights),
        "topwall_load_entropy": normalized_entropy(wall_weights),
        "topwall_load_gini": gini(wall_weights),
        "topwall_max_load_share": float(wall_weights.max() / wall_weights.sum()) if wall_weights.size else 0.0,
    }
    edge_rows = []
    for (a, b), stats in sorted(edge_stats.items(), key=lambda item: float(item[1]["force"]), reverse=True):
        edge_rows.append(
            {
                "timestep": step,
                "top_displacement_mm": displacement_m * 1000.0,
                "pebble_i": a,
                "pebble_j": b,
                "subparticle_contacts": int(stats["contacts"]),
                "overlap_sum_um": float(stats["overlap"]) * 1.0e6,
                "reconstructed_normal_force_N": float(stats["force"]),
                "max_subcontact_normal_force_N": float(stats["max_force"]),
            }
        )
    return summary, edge_rows


def write_csv(path: Path, rows: list[dict[str, float | int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dumps", nargs="+", type=Path)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--thermo", type=Path, required=True)
    parser.add_argument("--summary-output", type=Path, required=True)
    parser.add_argument("--edge-output", type=Path, required=True)
    parser.add_argument("--nspheres", type=int, default=500)
    parser.add_argument("--wall-zhi", type=float, default=0.00876684)
    parser.add_argument("--pre-steps", type=int, default=1001)
    parser.add_argument("--top-speed", type=float, default=0.5)
    parser.add_argument("--dt", type=float, default=5.0e-9)
    parser.add_argument("--young", type=float, default=9.0e10)
    parser.add_argument("--poisson", type=float, default=0.25)
    parser.add_argument("--plate-area", type=float, default=0.011 * 0.011)
    parser.add_argument("--bed-height", type=float, required=True)
    args = parser.parse_args()

    events = event_history(args.events)
    thermo = thermo_history(args.thermo)
    summaries = []
    edges = []
    for dump in sorted(args.dumps, key=lambda path: int(path.stem.split("_")[-1])):
        print(f"analyzing {dump}", flush=True)
        summary, dump_edges = analyze_dump(
            dump,
            args.nspheres,
            args.wall_zhi,
            args.pre_steps,
            args.top_speed,
            args.dt,
            args.young,
            args.poisson,
            events,
            thermo,
            args.plate_area,
            args.bed_height,
        )
        summaries.append(summary)
        edges.extend(dump_edges)
    write_csv(args.summary_output, summaries)
    write_csv(args.edge_output, edges)
    print(args.summary_output)
    print(args.edge_output)


if __name__ == "__main__":
    main()
