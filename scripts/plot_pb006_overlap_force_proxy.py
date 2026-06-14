#!/usr/bin/env python3
"""Plot overlap-derived force-proxy networks for weak and strong cascades."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def col(rows_: list[dict[str, str]], name: str) -> list[float]:
    return [float(r[name]) for r in rows_]


def main() -> None:
    s2 = rows(ROOT / "tables/pb006_seed02_overlap_force_proxy_summary.csv")
    s3 = rows(ROOT / "tables/pb006_seed03_overlap_force_proxy_summary.csv")
    s2_top = rows(ROOT / "tables/pb006_seed02_overlap_force_proxy_topwall.csv")
    s3_top = rows(ROOT / "tables/pb006_seed03_overlap_force_proxy_topwall.csv")
    s3_edges = rows(ROOT / "tables/pb006_seed03_overlap_force_proxy_edges.csv")

    colors = {"seed02": "#C46A30", "seed03": "#6B5EA8"}
    display_names = {"seed02": "weaker cascade", "seed03": "stronger cascade"}
    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 8,
            "axes.linewidth": 0.8,
            "xtick.major.width": 0.8,
            "ytick.major.width": 0.8,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
        }
    )
    fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.2), constrained_layout=True)

    ax = axes[0, 0]
    for label, data in [("seed02", s2), ("seed03", s3)]:
        ax.plot(col(data, "top_displacement_mm"), col(data, "topwall_pebbles"), marker="o", color=colors[label], label=display_names[label])
    ax.set_xlabel("Top displacement (mm)")
    ax.set_ylabel("Top-wall loaded pebbles")
    ax.set_title("a  Loaded top pebbles", loc="left", fontweight="bold")
    ax.legend(frameon=False)

    ax = axes[0, 1]
    for label, data in [("seed02", s2), ("seed03", s3)]:
        ax.plot(
            col(data, "top_displacement_mm"),
            [v * 1.0e8 for v in col(data, "topwall_hertz_proxy_sum_m32")],
            marker="o",
            color=colors[label],
            label=display_names[label],
        )
    ax.set_xlabel("Top displacement (mm)")
    ax.set_ylabel("Top-wall proxy (x10$^{-8}$ m$^{3/2}$)")
    ax.set_title("b  Top-wall overlap proxy", loc="left", fontweight="bold")

    ax = axes[1, 0]
    for label, data in [("seed02", s2), ("seed03", s3)]:
        ax.plot(col(data, "top_displacement_mm"), col(data, "inter_pebble_edges"), marker="o", color=colors[label], label=display_names[label])
    ax.set_xlabel("Top displacement (mm)")
    ax.set_ylabel("Inter-pebble contact edges")
    ax.set_title("c  Inter-pebble network growth", loc="left", fontweight="bold")

    ax = axes[1, 1]
    step = "80000"
    final_top = [r for r in s3_top if r["timestep"] == step]
    final_edges = [r for r in s3_edges if r["timestep"] == step]
    labels = [str(r["pebble_id"]) for r in final_top[:4]]
    vals = [float(r["hertz_proxy_sum_m32"]) * 1.0e8 for r in final_top[:4]]
    bars = ax.bar(range(len(vals)), vals, color="#6B5EA8", width=0.58, label="Top-wall proxy per pebble")
    ax.set_xticks(range(len(vals)), labels)
    ax.set_xlabel("Top-wall pebble id")
    ax.set_ylabel("Proxy (x10$^{-8}$ m$^{3/2}$)")
    ax.set_title("d  Stronger-case top pebbles", loc="left", fontweight="bold")
    edge_text = "strong edges: " + ", ".join(f"{r['pebble_i']}-{r['pebble_j']}" for r in final_edges[:3])
    ax.text(0.02, 0.93, edge_text, transform=ax.transAxes, ha="left", va="top", fontsize=6.8, color="#4E4A45")
    ax.set_ylim(0, max(vals) * 1.32)
    ax.legend(handles=[bars], frameon=False, fontsize=6.8, loc="upper right")

    for ax in axes.flat:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.tick_params(direction="out", length=3)
        ax.grid(True, color="#D7D3CB", linewidth=0.6, alpha=0.65)

    out_prefixes = [
        ROOT / "figures/pb006/pb006_seed02_seed03_overlap_force_proxy",
        ROOT / "figures/pb006/pb006_force_path_proxy",
    ]
    out_prefixes[0].parent.mkdir(parents=True, exist_ok=True)
    for out in out_prefixes:
        for suffix in [".svg", ".pdf", ".png", ".tiff"]:
            dpi = 600 if suffix in [".png", ".tiff"] else None
            fig.savefig(out.with_suffix(suffix), dpi=dpi)


if __name__ == "__main__":
    main()
