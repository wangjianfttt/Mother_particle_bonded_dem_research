#!/usr/bin/env python3
"""Export a fractured single-pebble dump to ParaView-readable VTP files."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PARTICLES = ROOT / (
    "simulations/single_pebble/SP-002/archive/"
    "SP-002-CAL1-x-slow0p05ms-0p3mm-completed-20260531/post/"
    "particles_1200000.dump"
)
DEFAULT_BONDS = ROOT / (
    "simulations/single_pebble/SP-002/archive/"
    "SP-002-CAL1-x-slow0p05ms-0p3mm-completed-20260531/post/"
    "bonds_1200000.local"
)
DEFAULT_OUT_PREFIX = ROOT / "figures/sp002/single_pebble_fragment"
DEFAULT_SUMMARY = ROOT / "tables/sp002_single_pebble_fragment_visualization_summary.csv"


def read_lammps_atoms(path: Path) -> tuple[int, list[dict[str, float]]]:
    lines = path.read_text().splitlines()
    timestep = None
    atoms: list[dict[str, float]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line == "ITEM: TIMESTEP":
            timestep = int(lines[i + 1])
            i += 2
            continue
        if line.startswith("ITEM: ATOMS"):
            names = line.split()[2:]
            for row in lines[i + 1 :]:
                if row.startswith("ITEM:"):
                    break
                values = row.split()
                record: dict[str, float] = {}
                for name, value in zip(names, values):
                    if name in {"id", "type"}:
                        record[name] = int(value)
                    else:
                        record[name] = float(value)
                atoms.append(record)
            break
        i += 1
    if timestep is None or not atoms:
        raise ValueError(f"Could not parse atom dump: {path}")
    atoms.sort(key=lambda row: int(row["id"]))
    return timestep, atoms


def read_lammps_bonds(path: Path) -> tuple[int, list[tuple[int, int]]]:
    lines = path.read_text().splitlines()
    timestep = None
    bonds: list[tuple[int, int]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line == "ITEM: TIMESTEP":
            timestep = int(lines[i + 1])
            i += 2
            continue
        if line.startswith("ITEM: ENTRIES"):
            for row in lines[i + 1 :]:
                if row.startswith("ITEM:"):
                    break
                a, b = row.split()[:2]
                bonds.append((int(a), int(b)))
            break
        i += 1
    if timestep is None:
        raise ValueError(f"Could not parse bond dump: {path}")
    return timestep, bonds


def connected_components(atom_ids: list[int], bonds: list[tuple[int, int]]) -> dict[int, tuple[int, int]]:
    parent = {atom_id: atom_id for atom_id in atom_ids}

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for a, b in bonds:
        if a in parent and b in parent:
            union(a, b)

    groups: dict[int, list[int]] = defaultdict(list)
    for atom_id in atom_ids:
        groups[find(atom_id)].append(atom_id)
    ranked = sorted(groups.values(), key=lambda ids: (-len(ids), min(ids)))
    out: dict[int, tuple[int, int]] = {}
    for rank, ids in enumerate(ranked, start=1):
        size = len(ids)
        for atom_id in ids:
            out[atom_id] = (rank, size)
    return out


def data_array(name: str, values: list[float | int], dtype: str = "Float32", comps: int | None = None) -> str:
    comp_attr = f' NumberOfComponents="{comps}"' if comps else ""
    text = " ".join(str(v) for v in values)
    return f'<DataArray type="{dtype}" Name="{name}"{comp_attr} format="ascii">{text}</DataArray>'


def write_particles_vtp(path: Path, atoms: list[dict[str, float]], comp: dict[int, tuple[int, int]]) -> None:
    coords: list[float] = []
    radii: list[float] = []
    ranks: list[int] = []
    display_classes: list[int] = []
    sizes: list[int] = []
    chip_flags: list[int] = []
    atom_ids: list[int] = []
    atom_types: list[int] = []
    for atom in atoms:
        atom_id = int(atom["id"])
        coords.extend([atom["x"] * 1000.0, atom["y"] * 1000.0, atom["z"] * 1000.0])
        radii.append(atom["radius"] * 1000.0)
        rank, size = comp[atom_id]
        ranks.append(rank)
        display_classes.append(rank if rank <= 2 else 3)
        sizes.append(size)
        chip_flags.append(1 if size < 10 else 0)
        atom_ids.append(atom_id)
        atom_types.append(int(atom["type"]))

    n = len(atoms)
    verts_conn = list(range(n))
    verts_offsets = list(range(1, n + 1))
    xml = f"""<?xml version="1.0"?>
<VTKFile type="PolyData" version="0.1" byte_order="LittleEndian">
  <PolyData>
    <Piece NumberOfPoints="{n}" NumberOfVerts="{n}" NumberOfLines="0" NumberOfStrips="0" NumberOfPolys="0">
      <PointData Scalars="fragment_rank">
        {data_array("atom_id", atom_ids, "Int32")}
        {data_array("atom_type", atom_types, "Int32")}
        {data_array("radius_mm", radii)}
        {data_array("fragment_rank", ranks, "Int32")}
        {data_array("fragment_display_class", display_classes, "Int32")}
        {data_array("fragment_size", sizes, "Int32")}
        {data_array("small_chip_flag", chip_flags, "Int32")}
      </PointData>
      <CellData/>
      <Points>
        {data_array("Points", coords, comps=3)}
      </Points>
      <Verts>
        {data_array("connectivity", verts_conn, "Int32")}
        {data_array("offsets", verts_offsets, "Int32")}
      </Verts>
    </Piece>
  </PolyData>
</VTKFile>
"""
    path.write_text(xml)


def write_bonds_vtp(
    path: Path,
    atoms: list[dict[str, float]],
    bonds: list[tuple[int, int]],
    comp: dict[int, tuple[int, int]],
) -> None:
    id_to_index = {int(atom["id"]): idx for idx, atom in enumerate(atoms)}
    coords: list[float] = []
    for atom in atoms:
        coords.extend([atom["x"] * 1000.0, atom["y"] * 1000.0, atom["z"] * 1000.0])
    conn: list[int] = []
    offsets: list[int] = []
    same_fragment: list[int] = []
    fragment_rank: list[int] = []
    for idx, (a, b) in enumerate(bonds, start=1):
        if a not in id_to_index or b not in id_to_index:
            continue
        conn.extend([id_to_index[a], id_to_index[b]])
        offsets.append(2 * idx)
        same_fragment.append(1 if comp[a][0] == comp[b][0] else 0)
        fragment_rank.append(comp[a][0] if comp[a][0] == comp[b][0] else 0)
    n = len(atoms)
    m = len(offsets)
    xml = f"""<?xml version="1.0"?>
<VTKFile type="PolyData" version="0.1" byte_order="LittleEndian">
  <PolyData>
    <Piece NumberOfPoints="{n}" NumberOfVerts="0" NumberOfLines="{m}" NumberOfStrips="0" NumberOfPolys="0">
      <PointData/>
      <CellData Scalars="fragment_rank">
        {data_array("same_fragment", same_fragment, "Int32")}
        {data_array("fragment_rank", fragment_rank, "Int32")}
      </CellData>
      <Points>
        {data_array("Points", coords, comps=3)}
      </Points>
      <Lines>
        {data_array("connectivity", conn, "Int32")}
        {data_array("offsets", offsets, "Int32")}
      </Lines>
    </Piece>
  </PolyData>
</VTKFile>
"""
    path.write_text(xml)


def write_summary(path: Path, timestep: int, atoms: list[dict[str, float]], bonds: list[tuple[int, int]], comp: dict[int, tuple[int, int]]) -> None:
    sizes = sorted({size for _, size in comp.values()}, reverse=True)
    ranks = sorted({rank for rank, _ in comp.values()})
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        writer.writerow(["source_timestep", timestep])
        writer.writerow(["subparticles", len(atoms)])
        writer.writerow(["intact_bonds", len(bonds)])
        writer.writerow(["fragment_count", len(ranks)])
        writer.writerow(["largest_fragment_particles", sizes[0]])
        writer.writerow(["second_fragment_particles", sizes[1] if len(sizes) > 1 else 0])
        writer.writerow(["single_particle_fragments", sum(1 for size in sizes if size == 1)])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--particles", type=Path, default=DEFAULT_PARTICLES)
    parser.add_argument("--bonds", type=Path, default=DEFAULT_BONDS)
    parser.add_argument("--out-prefix", type=Path, default=DEFAULT_OUT_PREFIX)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    args = parser.parse_args()

    timestep, atoms = read_lammps_atoms(args.particles)
    bond_timestep, bonds = read_lammps_bonds(args.bonds)
    if bond_timestep != timestep:
        raise ValueError(f"Timestep mismatch: atoms={timestep}, bonds={bond_timestep}")

    comp = connected_components([int(atom["id"]) for atom in atoms], bonds)
    args.out_prefix.parent.mkdir(parents=True, exist_ok=True)
    particles_out = args.out_prefix.with_name(args.out_prefix.name + "_particles.vtp")
    bonds_out = args.out_prefix.with_name(args.out_prefix.name + "_bonds.vtp")
    write_particles_vtp(particles_out, atoms, comp)
    write_bonds_vtp(bonds_out, atoms, bonds, comp)
    write_summary(args.summary, timestep, atoms, bonds, comp)

    print(f"Wrote {particles_out}")
    print(f"Wrote {bonds_out}")
    print(f"Wrote {args.summary}")


if __name__ == "__main__":
    main()
