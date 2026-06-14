#!/usr/bin/env python3
"""Analyze SP-002 thermo CSV output."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def read_rows(path: Path) -> list[dict[str, float]]:
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        rows: list[dict[str, float]] = []
        for row in reader:
            rows.append({k: float(v) for k, v in row.items()})
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--plot", type=Path)
    args = parser.parse_args()

    rows = read_rows(args.csv_path)
    if not rows:
        raise SystemExit("No rows found")

    initial_bonds = max(r["bond_int"] for r in rows)
    for row in rows:
        row["top_disp_mm"] = row["top_disp"] * 1e3
        row["top_force_abs_N"] = abs(row["top_forc"])
        row["bottom_force_abs_N"] = abs(row["bottom_f"])
        row["broken_total"] = max(0.0, initial_bonds - row["bond_int"]) if row["bond_int"] > 0 else 0.0

    peak_top = max(rows, key=lambda r: r["top_force_abs_N"])
    peak_bottom = max(rows, key=lambda r: r["bottom_force_abs_N"])
    first_break = next((r for r in rows if r["broken_total"] > 0), None)
    final = rows[-1]

    args.summary.parent.mkdir(parents=True, exist_ok=True)
    with args.summary.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        writer.writerow(["source_csv", str(args.csv_path)])
        writer.writerow(["rows", len(rows)])
        writer.writerow(["peak_top_force_N", peak_top["top_force_abs_N"]])
        writer.writerow(["peak_top_force_displacement_mm", peak_top["top_disp_mm"]])
        writer.writerow(["peak_bottom_force_N", peak_bottom["bottom_force_abs_N"]])
        writer.writerow(["peak_bottom_force_displacement_mm", peak_bottom["top_disp_mm"]])
        writer.writerow(["final_intact_bonds", final["bond_int"]])
        writer.writerow(["final_broken_bonds", final["broken_total"]])
        if first_break:
            writer.writerow(["first_break_displacement_mm", first_break["top_disp_mm"]])
            writer.writerow(["first_break_step", first_break["Step"]])
        else:
            writer.writerow(["first_break_displacement_mm", ""])
            writer.writerow(["first_break_step", ""])

    if args.plot:
        args.plot.parent.mkdir(parents=True, exist_ok=True)
        x = [r["top_disp_mm"] for r in rows]
        top = [r["top_force_abs_N"] for r in rows]
        bottom = [r["bottom_force_abs_N"] for r in rows]
        broken = [r["broken_total"] for r in rows]
        svg = render_svg(x, top, bottom, broken)
        args.plot.write_text(svg)


def render_svg(x: list[float], top: list[float], bottom: list[float], broken: list[float]) -> str:
    width, height = 900, 560
    left, right, top_pad, bottom_pad = 82, 82, 40, 72
    plot_w = width - left - right
    plot_h = height - top_pad - bottom_pad
    xmin, xmax = min(x), max(x)
    ymax_force = max(max(top), max(bottom), 1e-12)
    ymax_break = max(max(broken), 1.0)

    def sx(v: float) -> float:
        if xmax == xmin:
            return left
        return left + (v - xmin) / (xmax - xmin) * plot_w

    def sy_force(v: float) -> float:
        return top_pad + plot_h - v / ymax_force * plot_h

    def sy_break(v: float) -> float:
        return top_pad + plot_h - v / ymax_break * plot_h

    def polyline(vals: list[float], yfn) -> str:
        pts = " ".join(f"{sx(xi):.2f},{yfn(yi):.2f}" for xi, yi in zip(x, vals))
        return pts

    def stepline(vals: list[float]) -> str:
        pts: list[str] = []
        for i, (xi, yi) in enumerate(zip(x, vals)):
            if i:
                pts.append(f"{sx(xi):.2f},{sy_break(vals[i-1]):.2f}")
            pts.append(f"{sx(xi):.2f},{sy_break(yi):.2f}")
        return " ".join(pts)

    grid = []
    for i in range(6):
        y = top_pad + i * plot_h / 5
        grid.append(f'<line x1="{left}" y1="{y:.2f}" x2="{width-right}" y2="{y:.2f}" stroke="#d9dee2" stroke-width="1"/>')
    for i in range(6):
        tx = left + i * plot_w / 5
        xv = xmin + i * (xmax - xmin) / 5
        grid.append(f'<line x1="{tx:.2f}" y1="{top_pad}" x2="{tx:.2f}" y2="{height-bottom_pad}" stroke="#edf0f2" stroke-width="1"/>')
        grid.append(f'<text x="{tx:.2f}" y="{height-34}" text-anchor="middle" font-size="18" fill="#30363d">{xv:.3f}</text>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="white"/>
<text x="{width/2}" y="26" text-anchor="middle" font-size="22" font-family="Arial, sans-serif" fill="#111827">SP-002 force-displacement and bond breakage</text>
{''.join(grid)}
<line x1="{left}" y1="{top_pad}" x2="{left}" y2="{height-bottom_pad}" stroke="#111827" stroke-width="1.5"/>
<line x1="{left}" y1="{height-bottom_pad}" x2="{width-right}" y2="{height-bottom_pad}" stroke="#111827" stroke-width="1.5"/>
<line x1="{width-right}" y1="{top_pad}" x2="{width-right}" y2="{height-bottom_pad}" stroke="#111827" stroke-width="1.5"/>
<polyline points="{polyline(top, sy_force)}" fill="none" stroke="#1b6ca8" stroke-width="3"/>
<polyline points="{polyline(bottom, sy_force)}" fill="none" stroke="#d1495b" stroke-width="3"/>
<polyline points="{stepline(broken)}" fill="none" stroke="#4b8f29" stroke-width="3"/>
<text x="{width/2}" y="{height-8}" text-anchor="middle" font-size="20" font-family="Arial, sans-serif" fill="#111827">Top displacement (mm)</text>
<text x="24" y="{height/2}" text-anchor="middle" transform="rotate(-90 24 {height/2})" font-size="20" font-family="Arial, sans-serif" fill="#111827">Force magnitude (N)</text>
<text x="{width-20}" y="{height/2}" text-anchor="middle" transform="rotate(90 {width-20} {height/2})" font-size="20" font-family="Arial, sans-serif" fill="#111827">Broken bonds</text>
<text x="{left+20}" y="{top_pad+24}" font-size="18" font-family="Arial, sans-serif" fill="#1b6ca8">Top plate</text>
<text x="{left+130}" y="{top_pad+24}" font-size="18" font-family="Arial, sans-serif" fill="#d1495b">Bottom plate</text>
<text x="{left+270}" y="{top_pad+24}" font-size="18" font-family="Arial, sans-serif" fill="#4b8f29">Broken bonds</text>
<text x="{left-10}" y="{top_pad+5}" text-anchor="end" font-size="17" fill="#30363d">{ymax_force:.2f}</text>
<text x="{left-10}" y="{height-bottom_pad}" text-anchor="end" font-size="17" fill="#30363d">0</text>
<text x="{width-right+10}" y="{top_pad+5}" text-anchor="start" font-size="17" fill="#30363d">{ymax_break:.0f}</text>
<text x="{width-right+10}" y="{height-bottom_pad}" text-anchor="start" font-size="17" fill="#30363d">0</text>
</svg>
'''


if __name__ == "__main__":
    main()
