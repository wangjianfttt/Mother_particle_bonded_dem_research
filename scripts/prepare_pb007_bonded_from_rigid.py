#!/usr/bin/env python3
"""Prepare bonded-template placement from a rigid multisphere settling state."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import numpy as np
from scipy.spatial.transform import Rotation


def read_local_clumps(path: Path) -> list[dict[str, float]]:
    lines = path.read_text().splitlines()
    header_index = next(i for i, line in enumerate(lines) if line.startswith("ITEM: ENTRIES"))
    columns = lines[header_index].split()[2:]
    data = np.loadtxt(lines[header_index + 1 :])
    if data.ndim == 1:
        data = data[None, :]
    records = []
    for row in data:
        record = {column: float(value) for column, value in zip(columns, row)}
        records.append(record)
    return sorted(records, key=lambda record: int(record["c_idms"]))


def read_template(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    data = np.loadtxt(path)
    if data.ndim == 1:
        data = data[None, :]
    return data[:, :3], data[:, 3], data[:, 4].astype(int)


def read_sphere_dump(path: Path) -> dict[str, np.ndarray]:
    lines = path.read_text().splitlines()
    header_index = next(i for i, line in enumerate(lines) if line.startswith("ITEM: ATOMS"))
    columns = lines[header_index].split()[2:]
    data = np.loadtxt(lines[header_index + 1 :])
    if data.ndim == 1:
        data = data[None, :]
    return {name: data[:, index] for index, name in enumerate(columns)}


def far_centres(
    count: int,
    spacing: float,
    origin: tuple[float, float, float],
) -> list[tuple[float, float, float]]:
    nx = math.ceil(count ** (1.0 / 3.0))
    ny = nx
    nz = math.ceil(count / (nx * ny))
    xs = [origin[0] + (index - (nx - 1) / 2.0) * spacing for index in range(nx)]
    ys = [origin[1] + (index - (ny - 1) / 2.0) * spacing for index in range(ny)]
    zs = [origin[2] + index * spacing for index in range(nz)]
    return [(x, y, z) for z in zs for y in ys for x in xs][:count]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clumps", type=Path, required=True)
    parser.add_argument("--sphere-dump", type=Path, required=True)
    parser.add_argument("--template", type=Path, required=True)
    parser.add_argument("--insertion-reference-dump", type=Path, required=True)
    parser.add_argument("--create-output", type=Path, required=True)
    parser.add_argument("--move-output", type=Path, required=True)
    parser.add_argument("--metadata-output", type=Path, required=True)
    parser.add_argument("--bounds-output", type=Path, required=True)
    parser.add_argument("--far-spacing", type=float, default=0.00135)
    parser.add_argument("--far-origin-x", type=float, default=0.0)
    parser.add_argument("--far-origin-y", type=float, default=0.0)
    parser.add_argument("--far-origin-z", type=float, default=-0.00135)
    parser.add_argument("--side-margin", type=float, default=0.0005)
    args = parser.parse_args()

    clumps = read_local_clumps(args.clumps)
    centers_local, radii, _ = read_template(args.template)
    spheres = read_sphere_dump(args.sphere_dump)
    insertion_reference = read_sphere_dump(args.insertion_reference_dump)
    nspheres = len(centers_local)
    reference_order = np.argsort(insertion_reference["id"])
    reference_centers = np.column_stack(
        (insertion_reference["x"], insertion_reference["y"], insertion_reference["z"])
    )[reference_order]
    if len(reference_centers) != nspheres:
        raise ValueError("insertion reference dump does not match template sphere count")
    insertion_offset_local = np.mean(reference_centers - centers_local, axis=0)
    far = far_centres(
        len(clumps),
        args.far_spacing,
        (args.far_origin_x, args.far_origin_y, args.far_origin_z),
    )
    clump_lookup = {int(clump["c_idms"]): clump for clump in clumps}
    rigid_ids = sorted(np.unique(spheres["mol"].astype(int)).tolist())
    if len(rigid_ids) != len(clumps):
        raise ValueError("sphere dump and clump dump contain different numbers of rigid bodies")

    args.create_output.parent.mkdir(parents=True, exist_ok=True)
    args.move_output.parent.mkdir(parents=True, exist_ok=True)
    args.metadata_output.parent.mkdir(parents=True, exist_ok=True)
    args.bounds_output.parent.mkdir(parents=True, exist_ok=True)

    all_lower = []
    all_upper = []
    metadata = []
    with args.create_output.open("w") as create_file, args.move_output.open("w") as move_file:
        create_file.write("# Bonded templates created with rigid-settling orientations\n")
        move_file.write("# Bonded templates relocated to rigid-settling centers\n")
        for index, (source, rigid_id) in enumerate(zip(far, rigid_ids), start=1):
            mask = spheres["mol"].astype(int) == rigid_id
            atom_order = np.argsort(spheres["id"][mask])
            settled = np.column_stack((spheres["x"][mask], spheres["y"][mask], spheres["z"][mask]))[atom_order]
            if len(settled) != nspheres:
                raise ValueError(f"rigid body {rigid_id} contains {len(settled)} rather than {nspheres} spheres")

            local_centered = centers_local - centers_local.mean(axis=0)
            settled_centered = settled - settled.mean(axis=0)
            u_matrix, _, vt_matrix = np.linalg.svd(local_centered.T @ settled_centered)
            row_rotation = u_matrix @ vt_matrix
            if np.linalg.det(row_rotation) < 0.0:
                u_matrix[:, -1] *= -1.0
                row_rotation = u_matrix @ vt_matrix
            rotation = Rotation.from_matrix(row_rotation.T)
            fitted = rotation.apply(centers_local)
            target_geometric = settled.mean(axis=0) - fitted.mean(axis=0)
            target = target_geometric - rotation.apply(insertion_offset_local)
            fit_rms = float(np.sqrt(np.mean(np.sum((fitted + target_geometric - settled) ** 2, axis=1))))
            quaternion_xyzw = rotation.as_quat()
            q1 = quaternion_xyzw[3]
            q2, q3, q4 = quaternion_xyzw[:3]
            create_file.write(
                "create_particles clump single "
                f"{source[0]:.12e} {source[1]:.12e} {source[2]:.12e} "
                "velocity 0.0 0.0 0.0 "
                f"orientation {q1:.12e} {q2:.12e} {q3:.12e} {q4:.12e}\n"
            )
            first = (index - 1) * nspheres + 1
            last = index * nspheres
            move_file.write(f"group pebble_tmp id {first}:{last}\n")
            move_file.write(
                "displace_atoms pebble_tmp move "
                f"{target[0] - source[0]:.12e} {target[1] - source[1]:.12e} "
                f"{target[2] - source[2]:.12e} units box\n"
            )
            move_file.write("group pebble_tmp delete\n")

            transformed = rotation.apply(centers_local + insertion_offset_local) + target
            all_lower.append(transformed - radii[:, None])
            all_upper.append(transformed + radii[:, None])
            clump = clump_lookup[rigid_id]
            metadata.append(
                {
                    "pebble_id": index,
                    "rigid_id": rigid_id,
                    "insertion_origin_x": target[0],
                    "insertion_origin_y": target[1],
                    "insertion_origin_z": target[2],
                    "rigid_xcm": clump["c_xcm[1]"],
                    "rigid_ycm": clump["c_xcm[2]"],
                    "rigid_zcm": clump["c_xcm[3]"],
                    "q1_w": q1,
                    "q2_x": q2,
                    "q3_y": q3,
                    "q4_z": q4,
                    "coordinate_fit_rms_m": fit_rms,
                    "insertion_offset_local_x": insertion_offset_local[0],
                    "insertion_offset_local_y": insertion_offset_local[1],
                    "insertion_offset_local_z": insertion_offset_local[2],
                }
            )

    with args.metadata_output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(metadata[0]))
        writer.writeheader()
        writer.writerows(metadata)

    sphere_centers = np.column_stack((spheres["x"], spheres["y"], spheres["z"]))
    sphere_radii = spheres["radius"]
    lower = sphere_centers - sphere_radii[:, None]
    upper = sphere_centers + sphere_radii[:, None]
    bounds = {
        "xlo": float(lower[:, 0].min() - args.side_margin),
        "xhi": float(upper[:, 0].max() + args.side_margin),
        "ylo": float(lower[:, 1].min() - args.side_margin),
        "yhi": float(upper[:, 1].max() + args.side_margin),
        "zlo": float(lower[:, 2].min()),
        "zhi": float(upper[:, 2].max()),
        "npebbles": len(clumps),
        "nspheres": nspheres,
    }
    with args.bounds_output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(bounds))
        writer.writeheader()
        writer.writerow(bounds)

    print(args.create_output)
    print(args.move_output)
    print(args.metadata_output)
    print(args.bounds_output)


if __name__ == "__main__":
    main()
