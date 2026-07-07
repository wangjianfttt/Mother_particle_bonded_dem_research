#!/usr/bin/env python3
"""Draw a clean manuscript workflow schematic for the bonded-template study."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import patches


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures/main/fig1_workflow"

INK = "#222831"
MUTED = "#69737F"
GRID = "#C9D1D9"
BLUE = "#2F6F9F"
TEAL = "#16877A"
ORANGE = "#D27A3F"
RED = "#B83B52"
PALE_BLUE = "#E8EEF4"
PALE_TEAL = "#E9F4F1"
PALE_RED = "#F7E8EC"
WASH = "#FBFAF7"


def text(ax: plt.Axes, x: float, y: float, s: str, **kwargs) -> None:
    opts = dict(ha="center", va="center", color=INK, fontsize=7.0)
    opts.update(kwargs)
    ax.text(x, y, s, **opts)


def panel_label(ax: plt.Axes, x: float, y: float, label: str) -> None:
    text(ax, x, y, label, ha="left", va="top", fontsize=10.5, fontweight="bold")


def circle(
    ax: plt.Axes,
    x: float,
    y: float,
    r: float,
    fc: str,
    ec: str = INK,
    lw: float = 0.8,
    z: int = 2,
    alpha: float = 1.0,
) -> None:
    ax.add_patch(patches.Circle((x, y), r, facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z, alpha=alpha))


def arrow(ax: plt.Axes, x0: float, y0: float, x1: float, y1: float, color: str = MUTED, lw: float = 1.05) -> None:
    ax.annotate(
        "",
        xy=(x1, y1),
        xytext=(x0, y0),
        arrowprops=dict(arrowstyle="-|>", lw=lw, color=color, shrinkA=0, shrinkB=0, mutation_scale=12),
        zorder=10,
    )


def draw_panel_base(ax: plt.Axes, x0: float, label: str) -> None:
    panel_label(ax, x0 - 0.72, 2.83, label)


def draw_template(ax: plt.Axes, x0: float) -> None:
    draw_panel_base(ax, x0, "a")
    circle(ax, x0, 1.88, 0.55, WASH, ec=INK, lw=1.05, z=1)
    pts = [
        (-0.32, 0.10),
        (-0.22, -0.16),
        (-0.08, 0.28),
        (0.02, 0.02),
        (0.14, 0.32),
        (0.28, 0.06),
        (0.36, -0.22),
        (-0.37, -0.30),
        (-0.04, -0.34),
        (0.20, -0.38),
        (0.00, 0.50),
    ]
    for i, (dx1, dy1) in enumerate(pts):
        for dx2, dy2 in pts[i + 1 :]:
            if (dx1 - dx2) ** 2 + (dy1 - dy2) ** 2 < 0.115:
                ax.plot([x0 + dx1, x0 + dx2], [1.88 + dy1, 1.88 + dy2], color="#C8C8C8", lw=0.48, zorder=1)
    for dx, dy in pts:
        circle(ax, x0 + dx, 1.88 + dy, 0.062, BLUE if dx < 0 else ORANGE, ec="white", lw=0.35, z=3)
    ax.plot([x0, x0], [1.33, 2.43], color=RED, lw=1.1, ls=(0, (3, 2)), zorder=4)
    text(ax, x0 + 0.50, 2.28, "weak\nplane", color=RED, fontsize=5.5)
    text(ax, x0, 0.70, "500 bonded\nsubparticles", fontsize=6.8)


def draw_packing(ax: plt.Axes, x0: float) -> None:
    draw_panel_base(ax, x0, "b")
    ax.add_patch(patches.Rectangle((x0 - 0.49, 1.28), 0.98, 1.02, fill=False, edgecolor=INK, linewidth=0.95))
    coords = [
        (-0.31, -0.30),
        (-0.09, -0.31),
        (0.14, -0.30),
        (0.34, -0.31),
        (-0.22, -0.06),
        (0.01, -0.07),
        (0.25, -0.06),
        (-0.31, 0.18),
        (-0.09, 0.18),
        (0.14, 0.18),
        (0.35, 0.18),
    ]
    for dx, dy in coords:
        circle(ax, x0 + dx, 1.75 + dy, 0.095, PALE_BLUE, ec="#607080", lw=0.62)
    text(ax, x0, 0.70, "gravity-settled\nproxy centres", fontsize=6.8)


def draw_transfer(ax: plt.Axes, x0: float) -> None:
    draw_panel_base(ax, x0, "c")
    ax.add_patch(patches.Rectangle((x0 - 0.49, 1.28), 0.98, 1.02, fill=False, edgecolor=INK, linewidth=0.95))
    coords = [
        (-0.29, -0.27),
        (-0.07, -0.27),
        (0.15, -0.27),
        (-0.18, -0.02),
        (0.05, -0.02),
        (0.28, -0.02),
        (-0.29, 0.24),
        (-0.07, 0.24),
        (0.16, 0.24),
    ]
    for dx, dy in coords:
        cx, cy = x0 + dx, 1.75 + dy
        circle(ax, cx, cy, 0.092, PALE_TEAL, ec=INK, lw=0.60)
        ax.plot([cx - 0.050, cx + 0.050], [cy, cy], color=RED, lw=0.48)
        ax.plot([cx, cx], [cy - 0.050, cy + 0.050], color=BLUE, lw=0.48)
    text(ax, x0, 0.70, "intact replacement\n493,500 bonds", fontsize=6.8)


def draw_loading(ax: plt.Axes, x0: float) -> None:
    draw_panel_base(ax, x0, "d")
    ax.add_patch(patches.Rectangle((x0 - 0.49, 1.28), 0.98, 1.02, fill=False, edgecolor=INK, linewidth=0.95))
    ax.add_patch(patches.Rectangle((x0 - 0.52, 2.28), 1.04, 0.085, facecolor="#3A3A3A", edgecolor="none"))
    coords = [
        (-0.29, -0.27),
        (-0.07, -0.27),
        (0.15, -0.27),
        (-0.18, -0.02),
        (0.05, -0.02),
        (0.28, -0.02),
        (-0.29, 0.24),
        (-0.07, 0.24),
        (0.16, 0.24),
    ]
    damaged = {(-0.07, 0.24), (0.16, 0.24)}
    for dx, dy in coords:
        cx, cy = x0 + dx, 1.75 + dy
        if (dx, dy) in damaged:
            circle(ax, cx, cy, 0.092, PALE_RED, ec=RED, lw=1.25)
            ax.plot([cx - 0.050, cx + 0.050], [cy + 0.050, cy - 0.050], color=RED, lw=0.90)
            ax.plot([cx - 0.050, cx + 0.050], [cy - 0.050, cy + 0.050], color=RED, lw=0.90)
        else:
            circle(ax, cx, cy, 0.092, WASH, ec=INK, lw=0.62)
    text(ax, x0, 0.70, "bond loss only\nduring loading", fontsize=6.8)


def draw_database(ax: plt.Axes, x0: float) -> None:
    draw_panel_base(ax, x0, "e")
    ox, oy = x0 - 0.46, 1.24
    ax.plot([ox, ox + 0.95], [oy, oy], color=INK, lw=0.85)
    ax.plot([ox, ox], [oy, oy + 1.05], color=INK, lw=0.85)
    xs = [ox + 0.14, ox + 0.34, ox + 0.55, ox + 0.75, ox + 0.86]
    ys = [oy + 0.16, oy + 0.44, oy + 0.54, oy + 0.82, oy + 0.90]
    ss = [50, 73, 56, 112, 88]
    ax.scatter(xs, ys, s=ss, color=RED, alpha=0.80, edgecolors=RED, linewidths=0.8, zorder=3)
    for tx in xs[::2]:
        ax.plot([tx, tx], [oy, oy - 0.055], color=INK, lw=0.45)
    for ty in ys[1::2]:
        ax.plot([ox, ox - 0.055], [ty, ty], color=INK, lw=0.45)
    text(ax, ox + 0.54, oy + 1.20, "step -> displacement", fontsize=6.0, color=MUTED)
    text(ax, ox - 0.24, oy + 0.55, "damage\nrank", fontsize=6.6, color=MUTED, rotation=90)
    text(ax, x0, 0.70, "assign events to\nparticle id + height", fontsize=6.8)


def main() -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "font.size": 7,
            "axes.linewidth": 0.8,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
        }
    )
    fig, ax = plt.subplots(figsize=(7.15, 1.90))
    fig.patch.set_facecolor(WASH)
    ax.set_facecolor(WASH)
    ax.set_xlim(0.0, 12.8)
    ax.set_ylim(0.25, 2.95)
    ax.set_aspect("equal")
    ax.axis("off")

    centers = [0.95, 3.55, 6.10, 8.65, 11.20]
    for x0, x1 in zip(centers[:-1], centers[1:]):
        arrow(ax, x0 + 0.78, 1.72, x1 - 0.75, 1.72, color="#818A93", lw=1.0)

    draw_template(ax, centers[0])
    draw_packing(ax, centers[1])
    draw_transfer(ax, centers[2])
    draw_loading(ax, centers[3])
    draw_database(ax, centers[4])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    for suffix, kwargs in {
        ".svg": {},
        ".pdf": {},
        ".png": {"dpi": 600},
        ".tiff": {"dpi": 600},
    }.items():
        fig.savefig(OUT.with_suffix(suffix), bbox_inches="tight", pad_inches=0.03, **kwargs)
    print(OUT)


if __name__ == "__main__":
    main()
