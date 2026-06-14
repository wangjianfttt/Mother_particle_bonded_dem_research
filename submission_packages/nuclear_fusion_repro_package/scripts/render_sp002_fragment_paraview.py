#!/usr/bin/env pvpython
"""Render the fractured single-pebble morphology with ParaView."""

from __future__ import annotations

from pathlib import Path

from paraview.simple import (  # type: ignore
    ColorBy,
    CreateView,
    Delete,
    GetColorTransferFunction,
    Glyph,
    Hide,
    Render,
    ResetCamera,
    SaveScreenshot,
    SetActiveView,
    Show,
    Tube,
    XMLPolyDataReader,
)


ROOT = Path(__file__).resolve().parents[1]
PARTICLES = ROOT / "figures/sp002/single_pebble_fragment_particles.vtp"
BONDS = ROOT / "figures/sp002/single_pebble_fragment_bonds.vtp"
OUT = ROOT / "figures/sp002/single_pebble_fragment_morphology_paraview.png"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)

    view = CreateView("RenderView")
    SetActiveView(view)
    view.ViewSize = [2200, 1800]
    view.Background = [1.0, 1.0, 1.0]
    view.Background2 = [1.0, 1.0, 1.0]
    view.UseColorPaletteForBackground = 0
    view.BackgroundColorMode = "Single Color"
    view.OrientationAxesVisibility = 0

    particles = XMLPolyDataReader(registrationName="fragment_particles", FileName=[str(PARTICLES)])
    bonds = XMLPolyDataReader(registrationName="fragment_bonds", FileName=[str(BONDS)])

    tubes = Tube(registrationName="intact_bond_tubes", Input=bonds)
    tubes.Radius = 0.0035
    tubes.NumberofSides = 8
    tube_display = Show(tubes, view)
    tube_display.Representation = "Surface"
    tube_display.DiffuseColor = [0.78, 0.78, 0.78]
    tube_display.Opacity = 0.16

    glyph = Glyph(registrationName="subparticle_spheres", Input=particles, GlyphType="Sphere")
    glyph.GlyphMode = "All Points"
    glyph.ScaleArray = ["POINTS", "radius_mm"]
    glyph.ScaleFactor = 1.95
    glyph.GlyphType.ThetaResolution = 24
    glyph.GlyphType.PhiResolution = 24

    glyph_display = Show(glyph, view)
    glyph_display.Representation = "Surface"
    ColorBy(glyph_display, ("POINTS", "fragment_display_class"))
    lut = GetColorTransferFunction("fragment_display_class")
    lut.InterpretValuesAsCategories = 1
    lut.Annotations = [
        "1",
        "largest fragment",
        "2",
        "second fragment",
        "3",
        "smaller fragments",
    ]
    lut.IndexedColors = [
        0.1216,
        0.4667,
        0.7059,
        0.8510,
        0.3255,
        0.0980,
        0.55,
        0.55,
        0.55,
    ]
    glyph_display.SetScalarBarVisibility(view, False)

    Hide(particles, view)
    Hide(bonds, view)

    ResetCamera(view)
    view.CameraPosition = [1.85, -2.20, 1.45]
    view.CameraFocalPoint = [0.0, 0.0, 0.0]
    view.CameraViewUp = [0.10, 0.32, 0.94]
    view.CameraParallelProjection = 1
    view.CameraParallelScale = 0.60
    Render(view)
    SaveScreenshot(str(OUT), view, ImageResolution=[2400, 1800], TransparentBackground=0)

    Delete(glyph)
    Delete(tubes)
    Delete(particles)
    Delete(bonds)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
