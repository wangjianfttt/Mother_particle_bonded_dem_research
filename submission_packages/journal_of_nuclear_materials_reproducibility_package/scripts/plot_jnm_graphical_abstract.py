#!/usr/bin/env python3
"""Create an Elsevier-style graphical abstract for the JNM submission."""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.path import Path as MplPath


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures" / "main" / "journal_of_nuclear_materials_graphical_abstract"

INK = "#222222"
MUTED = "#66717E"
LIGHT = "#F7F5EF"
BED = "#E7EDF2"
BLUE = "#335C81"
ORANGE = "#C76036"
TEAL = "#2D7F7A"
RED = "#A63D52"
GREEN = "#4F7F52"
WASH = "#FBFAF7"
LINE = "#D8DDE2"


def add_text(ax: plt.Axes, x: float, y: float, text: str, **kwargs) -> None:
    defaults = dict(ha="center", va="center", fontsize=8.0, color=INK)
    defaults.update(kwargs)
    ax.text(x, y, text, **defaults)


def circle(ax: plt.Axes, x: float, y: float, r: float, face: str, edge: str = INK, lw: float = 0.8) -> None:
    ax.add_patch(patches.Circle((x, y), r, facecolor=face, edgecolor=edge, linewidth=lw))


def arrow(ax: plt.Axes, x0: float, y0: float, x1: float, y1: float, color: str = MUTED, lw: float = 1.4) -> None:
    ax.annotate(
        "",
        xy=(x1, y1),
        xytext=(x0, y0),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=14, shrinkA=0, shrinkB=0),
    )


def panel_title(ax: plt.Axes, x: float, text: str) -> None:
    add_text(ax, x, 3.02, text, fontsize=8.0, fontweight="bold")


def add_pill(ax: plt.Axes, x: float, y: float, text: str, color: str, width: float = 0.72) -> None:
    ax.add_patch(
        patches.FancyBboxPatch(
            (x - width / 2, y - 0.075),
            width,
            0.15,
            boxstyle="round,pad=0.018,rounding_size=0.055",
            facecolor=color,
            edgecolor="none",
            alpha=0.12,
        )
    )
    add_text(ax, x, y, text, fontsize=5.8, color=color, fontweight="bold")


def draw_template_panel(ax: plt.Axes, x0: float) -> None:
    panel_title(ax, x0, "Intact bonded template")
    add_pill(ax, x0, 2.73, "zero seating damage", TEAL, width=0.80)
    circle(ax, x0, 1.82, 0.63, LIGHT, lw=1.15)
    pts = [
        (-0.34, 0.08), (-0.24, -0.22), (-0.16, 0.30), (-0.04, -0.02),
        (0.08, 0.24), (0.20, -0.04), (0.33, 0.16), (0.28, -0.27),
        (-0.02, -0.33), (0.00, 0.47), (-0.40, -0.08), (0.42, -0.08),
    ]
    for i, (x1, y1) in enumerate(pts):
        for x2, y2 in pts[i + 1 :]:
            if (x1 - x2) ** 2 + (y1 - y2) ** 2 < 0.13:
                ax.plot([x0 + x1, x0 + x2], [1.82 + y1, 1.82 + y2], color="#C7C7C7", lw=0.55)
    for dx, dy in pts:
        circle(ax, x0 + dx, 1.82 + dy, 0.07, BLUE if dx < 0 else ORANGE, edge="white", lw=0.45)
    ax.plot([x0, x0], [1.24, 2.40], color=RED, lw=1.25, ls=(0, (4, 2)))
    add_text(ax, x0 + 0.52, 2.34, "weak\nplane", ha="left", fontsize=7.0, color=RED)
    add_text(ax, x0, 0.81, "1 mm Li4SiO4 mother pebble\n500 bonded subparticles", fontsize=7.2)


def draw_gate_panel(ax: plt.Axes, x0: float) -> None:
    panel_title(ax, x0, "Accepted bed load path")
    add_pill(ax, x0, 2.73, "native force graph verified", TEAL, width=1.02)
    ax.add_patch(patches.Rectangle((x0 - 0.70, 1.05), 1.40, 1.34, fill=False, edgecolor=INK, linewidth=1.05))
    ax.add_patch(patches.Rectangle((x0 - 0.72, 2.39), 1.44, 0.08, facecolor="#3C3C3C", edgecolor="none"))
    arrow(ax, x0, 2.86, x0, 2.52, color=INK, lw=1.2)
    coords = [
        (-0.48, -0.34), (-0.24, -0.36), (0.00, -0.34), (0.25, -0.35), (0.48, -0.34),
        (-0.36, -0.08), (-0.12, -0.09), (0.13, -0.08), (0.38, -0.08),
        (-0.48, 0.18), (-0.24, 0.18), (0.00, 0.19), (0.25, 0.18), (0.48, 0.18),
    ]
    for dx, dy in coords:
        circle(ax, x0 + dx, 1.70 + dy, 0.092, BED, edge="#5D6872", lw=0.6)
    chains = [
        [(-0.48, 1.88), (-0.24, 1.88), (0.00, 1.89), (0.25, 1.88), (0.48, 1.88)],
        [(-0.36, 1.62), (-0.12, 1.61), (0.13, 1.62), (0.38, 1.62)],
        [(-0.24, 1.34), (0.00, 1.36), (0.25, 1.35)],
    ]
    for chain in chains:
        xs = [x0 + p[0] for p in chain]
        ys = [p[1] for p in chain]
        ax.plot(xs, ys, color=TEAL, lw=1.25, alpha=0.9, zorder=0)
    add_text(ax, x0, 0.82, "spanning load path\nforce-balance gate passed", fontsize=7.25)
    add_text(ax, x0 - 0.62, 2.11, "accepted\ngates", ha="left", fontsize=6.0, color=TEAL, fontweight="bold")


def draw_event_panel(ax: plt.Axes, x0: float) -> None:
    panel_title(ax, x0, "Localized fracture chronology")
    add_pill(ax, x0, 2.73, "one upper-bed pebble", RED, width=0.88)
    ax.add_patch(patches.Rectangle((x0 - 0.72, 1.12), 1.44, 1.22, fill=False, edgecolor=INK, linewidth=1.0))
    coords = [
        (-0.46, -0.32), (-0.20, -0.33), (0.06, -0.32), (0.32, -0.33),
        (-0.33, -0.06), (-0.07, -0.06), (0.20, -0.06), (0.46, -0.06),
        (-0.46, 0.20), (-0.20, 0.20), (0.06, 0.20), (0.32, 0.20),
    ]
    damaged = (0.06, 0.20)
    for dx, dy in coords:
        edge = RED if (dx, dy) == damaged else "#5D6872"
        lw = 1.7 if (dx, dy) == damaged else 0.6
        circle(ax, x0 + dx, 1.68 + dy, 0.092, LIGHT, edge=edge, lw=lw)
        if (dx, dy) == damaged:
            ax.plot([x0 + dx - 0.055, x0 + dx + 0.055], [1.68 + dy - 0.055, 1.68 + dy + 0.055], color=RED, lw=1.1)
            ax.plot([x0 + dx - 0.055, x0 + dx + 0.055], [1.68 + dy + 0.055, 1.68 + dy - 0.055], color=RED, lw=1.1)
    add_text(ax, x0, 2.52, "5 of 493,500 bonds break", fontsize=7.45, color=RED, fontweight="bold")

    x_start, y_base = x0 - 0.68, 0.75
    x_end = x0 + 0.60
    ax.plot([x_start, x_end], [y_base, y_base], color=INK, lw=0.8)
    events = [(25, 2), (35, 2), (60, 1)]
    for disp, inc in events:
        x = x_start + (disp / 60.0) * (x_end - x_start)
        ax.plot([x, x], [y_base, y_base + 0.18 + 0.06 * inc], color=RED, lw=1.15)
        circle(ax, x, y_base + 0.18 + 0.06 * inc, 0.035, RED, edge=RED, lw=0.8)
        add_text(ax, x, y_base - 0.16, f"{disp}", fontsize=6.6, color=MUTED)
        add_text(ax, x, y_base + 0.36 + 0.06 * inc, f"+{inc}", fontsize=6.7, color=RED)
    add_text(ax, x0, 0.41, "top displacement (um)", fontsize=6.45, color=MUTED)


def draw_summary_box(ax: plt.Axes) -> None:
    ax.plot([0.35, 7.15], [0.30, 0.30], color=LINE, lw=0.7)
    add_text(
        ax,
        3.75,
        0.16,
        "A hidden ceramic-breeder damage event becomes an auditable bond-loss and force-network history.",
        fontsize=6.55,
        color=INK,
    )


def main() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
        }
    )
    fig, ax = plt.subplots(figsize=(7.5, 2.95))
    fig.patch.set_facecolor(WASH)
    ax.set_facecolor(WASH)
    ax.set_xlim(0.0, 7.5)
    ax.set_ylim(0.0, 3.2)
    ax.axis("off")

    add_text(ax, 3.75, 3.16, "Acceptance-gated DEM for Li4SiO4 breeder-bed degradation", fontsize=7.1, color=MUTED)

    draw_template_panel(ax, 1.25)
    arrow(ax, 2.10, 1.82, 2.74, 1.82)
    draw_gate_panel(ax, 3.75)
    arrow(ax, 4.62, 1.82, 5.28, 1.82)
    draw_event_panel(ax, 6.25)
    draw_summary_box(ax)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT.with_suffix(".svg"), bbox_inches="tight", pad_inches=0.04)
    fig.savefig(OUT.with_suffix(".pdf"), bbox_inches="tight", pad_inches=0.04)
    fig.savefig(OUT.with_suffix(".png"), dpi=600, bbox_inches="tight", pad_inches=0.04)
    fig.savefig(OUT.with_suffix(".tiff"), dpi=600, bbox_inches="tight", pad_inches=0.04)
    print(OUT)


if __name__ == "__main__":
    main()
