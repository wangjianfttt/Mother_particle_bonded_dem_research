#!/usr/bin/env python3
"""Create a publication-style workflow schematic for the bonded-template study."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import patches


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures/main/fig1_workflow"

INK = "#222222"
MUTED = "#66717E"
LIGHT = "#F5F2EA"
BLUE = "#3E75A8"
TEAL = "#2D7F7A"
ORANGE = "#D1743F"
RED = "#A8364B"
BED = "#DCE3EA"


def add_text(ax: plt.Axes, x: float, y: float, text: str, **kwargs) -> None:
    defaults = dict(ha="center", va="center", fontsize=7.1, color=INK)
    defaults.update(kwargs)
    ax.text(x, y, text, **defaults)


def add_stage_label(ax: plt.Axes, x: float, y: float, label: str) -> None:
    ax.text(
        x,
        y,
        label,
        ha="left",
        va="top",
        fontsize=8.8,
        fontweight="bold",
        color=INK,
    )


def add_circle(
    ax: plt.Axes,
    x: float,
    y: float,
    r: float,
    face: str,
    edge: str = INK,
    lw: float = 0.75,
    z: int = 2,
    alpha: float = 1.0,
) -> None:
    ax.add_patch(patches.Circle((x, y), r, facecolor=face, edgecolor=edge, linewidth=lw, zorder=z, alpha=alpha))


def add_arrow(ax: plt.Axes, x0: float, y0: float, x1: float, y1: float, color: str = MUTED) -> None:
    ax.annotate(
        "",
        xy=(x1, y1),
        xytext=(x0, y0),
        arrowprops=dict(arrowstyle="-|>", lw=1.0, color=color, shrinkA=0, shrinkB=0, mutation_scale=10),
        zorder=5,
    )


def draw_template(ax: plt.Axes, x0: float) -> None:
    add_stage_label(ax, x0 - 0.78, 2.98, "a")
    add_circle(ax, x0, 2.04, 0.58, LIGHT, edge=INK, lw=0.9, z=1)
    pts = [
        (-0.32, 0.12), (-0.20, -0.10), (-0.10, 0.26), (0.02, 0.02),
        (0.14, 0.30), (0.24, 0.05), (0.34, -0.15), (-0.36, -0.22),
        (-0.05, -0.28), (0.18, -0.34), (0.00, 0.48),
    ]
    for i, (dx1, dy1) in enumerate(pts):
        for dx2, dy2 in pts[i + 1 :]:
            if (dx1 - dx2) ** 2 + (dy1 - dy2) ** 2 < 0.11:
                ax.plot([x0 + dx1, x0 + dx2], [2.04 + dy1, 2.04 + dy2], color="#C8C8C8", lw=0.45, zorder=1)
    for dx, dy in pts:
        add_circle(ax, x0 + dx, 2.04 + dy, 0.063, BLUE if dx < 0 else ORANGE, edge="white", lw=0.35, z=3)
    ax.plot([x0, x0], [1.50, 2.58], color=RED, lw=1.1, ls=(0, (3, 2)), zorder=4)
    add_text(ax, x0 + 0.48, 2.45, "weak\nplane", fontsize=6.0, color=RED)
    add_text(ax, x0, 0.63, "bonded template\n500 subparticles", fontsize=6.7)


def draw_proxy_bed(ax: plt.Axes, x0: float) -> None:
    add_stage_label(ax, x0 - 0.78, 2.98, "b")
    ax.add_patch(patches.Rectangle((x0 - 0.55, 1.20), 1.10, 1.22, fill=False, edgecolor=INK, linewidth=0.85))
    coords = [
        (-0.34, -0.35), (-0.11, -0.36), (0.13, -0.35), (0.36, -0.36),
        (-0.24, -0.10), (0.00, -0.10), (0.25, -0.09),
        (-0.34, 0.18), (-0.10, 0.18), (0.14, 0.19), (0.37, 0.18),
    ]
    for dx, dy in coords:
        add_circle(ax, x0 + dx, 1.70 + dy, 0.105, BED, edge="#5E6975", lw=0.55)
    add_arrow(ax, x0, 2.82, x0, 2.52, color=INK)
    add_text(ax, x0 + 0.33, 2.68, "gravity", ha="left", fontsize=7.0)
    add_text(ax, x0, 0.63, "gravity-settled\nproxy packing", fontsize=6.7)


def draw_locked_insertion(ax: plt.Axes, x0: float) -> None:
    add_stage_label(ax, x0 - 0.78, 2.98, "c")
    ax.add_patch(patches.Rectangle((x0 - 0.55, 1.20), 1.10, 1.22, fill=False, edgecolor=INK, linewidth=0.85))
    coords = [
        (-0.32, -0.32), (-0.08, -0.32), (0.16, -0.31),
        (-0.23, -0.05), (0.02, -0.05), (0.28, -0.05),
        (-0.32, 0.24), (-0.08, 0.25), (0.18, 0.25),
    ]
    for dx, dy in coords:
        cx, cy = x0 + dx, 1.70 + dy
        add_circle(ax, cx, cy, 0.108, LIGHT, edge=INK, lw=0.55)
        ax.plot([cx - 0.055, cx + 0.055], [cy, cy], color=RED, lw=0.45)
        ax.plot([cx, cx], [cy - 0.055, cy + 0.055], color=BLUE, lw=0.45)
    add_text(ax, x0 + 0.12, 2.70, "locked insertion", fontsize=7.0, color=TEAL)
    add_text(ax, x0, 0.63, "intact replacement\nzero pre-damage", fontsize=6.7)


def draw_compression(ax: plt.Axes, x0: float) -> None:
    add_stage_label(ax, x0 - 0.78, 2.98, "d")
    ax.add_patch(patches.Rectangle((x0 - 0.55, 1.20), 1.10, 1.12, fill=False, edgecolor=INK, linewidth=0.85))
    ax.add_patch(patches.Rectangle((x0 - 0.57, 2.32), 1.14, 0.08, facecolor="#3C3C3C", edgecolor="none"))
    add_arrow(ax, x0, 2.82, x0, 2.46, color=INK)
    coords = [
        (-0.32, -0.32), (-0.08, -0.32), (0.16, -0.31),
        (-0.23, -0.05), (0.02, -0.05), (0.28, -0.05),
        (-0.32, 0.24), (-0.08, 0.25), (0.18, 0.25),
    ]
    damaged = {(-0.08, 0.25), (0.18, 0.25)}
    for dx, dy in coords:
        cx, cy = x0 + dx, 1.70 + dy
        edge, lw = (RED, 1.25) if (dx, dy) in damaged else (INK, 0.55)
        add_circle(ax, cx, cy, 0.108, LIGHT, edge=edge, lw=lw)
        if (dx, dy) in damaged:
            ax.plot([cx - 0.055, cx + 0.052], [cy + 0.052, cy - 0.052], color=RED, lw=0.9)
            ax.plot([cx - 0.045, cx + 0.058], [cy - 0.052, cy + 0.048], color=RED, lw=0.75)
    add_text(ax, x0, 2.66, "compression", fontsize=7.2, color=RED)
    add_text(ax, x0, 0.63, "compression-driven\nbond breaks", fontsize=6.7)


def draw_event_database(ax: plt.Axes, x0: float) -> None:
    add_stage_label(ax, x0 - 0.78, 2.98, "e")
    ax.plot([x0 - 0.50, x0 + 0.55], [1.28, 1.28], color=INK, lw=0.8)
    ax.plot([x0 - 0.50, x0 - 0.50], [1.28, 2.35], color=INK, lw=0.8)
    xs = [x0 - 0.35, x0 - 0.12, x0 + 0.10, x0 + 0.32, x0 + 0.47]
    ys = [1.42, 1.72, 1.82, 2.17, 2.23]
    sizes = [38, 58, 47, 92, 68]
    ax.scatter(xs, ys, s=sizes, color=RED, alpha=0.78, edgecolors=RED, linewidths=0.7)
    for tx in xs:
        ax.plot([tx, tx], [1.28, 1.23], color=INK, lw=0.45)
    for ty in [1.55, 1.88, 2.20]:
        ax.plot([x0 - 0.50, x0 - 0.55], [ty, ty], color=INK, lw=0.45)
    add_text(ax, x0, 2.68, "event database", fontsize=7.2)
    add_text(ax, x0 + 0.02, 2.48, "step -> displacement", fontsize=6.6, color=MUTED)
    add_text(ax, x0 - 0.78, 1.82, "damage\nrank", fontsize=6.6, color=MUTED, rotation=90)
    add_text(ax, x0, 0.63, "assign events to\npebble id + height", fontsize=6.7)


def main() -> None:
    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 7,
            "axes.linewidth": 0.8,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
        }
    )
    fig, ax = plt.subplots(figsize=(7.25, 2.15))
    ax.set_xlim(0, 13.4)
    ax.set_ylim(0.25, 3.05)
    ax.set_aspect("equal")
    ax.axis("off")

    centers = [0.95, 3.75, 6.50, 9.25, 12.00]
    for x0, x1 in zip(centers[:-1], centers[1:]):
        add_arrow(ax, x0 + 0.83, 1.82, x1 - 0.86, 1.82, color="#7A8188")

    draw_template(ax, centers[0])
    draw_proxy_bed(ax, centers[1])
    draw_locked_insertion(ax, centers[2])
    draw_compression(ax, centers[3])
    draw_event_database(ax, centers[4])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT.with_suffix(".svg"), bbox_inches="tight", pad_inches=0.03)
    fig.savefig(OUT.with_suffix(".pdf"), bbox_inches="tight", pad_inches=0.03)
    fig.savefig(OUT.with_suffix(".png"), dpi=600, bbox_inches="tight", pad_inches=0.03)
    fig.savefig(OUT.with_suffix(".tiff"), dpi=600, bbox_inches="tight", pad_inches=0.03)
    print(OUT)


if __name__ == "__main__":
    main()
