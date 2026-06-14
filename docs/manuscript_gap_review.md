# Manuscript gap review: bonded Li4SiO4 pebble-bed breakage

This document records the current manuscript-level risks that must be controlled before the PB-006 workflow can be presented as a publishable predictive study rather than a computational demonstration.

## Current defensible claims

1. A 1.0 mm Li4SiO4 mother pebble can be represented by a 500-subparticle bonded template in LIGGGHTS-INL.
2. The SP-002-CAL1 weak-plane template is a plausible single-pebble calibration candidate: peak top force 18.64 N, peak bottom force 18.07 N, first break at 0.103 mm, and two major fragments of 227 and 224 subparticles.
3. Proxy random packing followed by bonded-template injection prevents artificial internal damage during gravity deposition.
4. Three independent 500-pebble PB-006 random beds reproduce the same early first-break displacement, 0.0725 mm, while later breakage magnitude depends strongly on upper-bed packing descriptors.
5. The locked-bond workflow scales to 1000 mother pebbles at initialization: 500000 subparticles and 5876000 intact internal bonds, with zero broken bonds before compression.
6. Completed 1000-pebble restartable calculations to 0.15 mm are defensible as event-sequence evidence: seed01, orient02 and seed02 all trigger in the top layer, but their post-onset propagation differs from confined single-pebble damage to a five-pebble top-bin cascade.

## Claims that still need conservative wording

1. The single-pebble template is not yet a final calibrated material model. It matches the current load-scale and fragment-mode targets, but the literature table still lacks verified 1.0 mm force-displacement curves and initial stiffness values.
2. The weak plane should be described as a reduced-order defect representation, not as a resolved microstructural crack unless microscopy or manufacturing evidence is added.
3. The PB-006 three-seed 500-pebble result supports early-stage, top-loaded breakage statistics. It does not yet establish a full-bed crushing law or deep-bed damage propagation.
4. The overlap-derived force-path analysis is a Hertz-type geometric proxy. It should not be described as a native DEM contact-force-chain measurement.
5. The 1000-pebble result now supports initialization scalability and resolved 0.15 mm event sequences, but it should not be described as a converged 1000-pebble crushing-probability distribution because only two independent packings and one fixed-geometry orientation replicate are complete.

## Immediate evidence gaps

| Gap | Current file/evidence | Required next evidence |
| --- | --- | --- |
| 1.0 mm experimental crush-load distribution | `tables/single_pebble_experimental_calibration_targets.csv` contains approximate Annabattula size-effect and near-size Lo Frano anchors | Verify exact values from full-text figures/tables; add uncertainty and extraction notes |
| Initial stiffness calibration | `tables/single_pebble_model_calibration_matrix.csv` contains model stiffness estimates | Extract experimental elastic slopes or digitize force-displacement curves |
| Stochastic single-pebble calibration | `tables/sp002_cal1_orientation_summary.csv`, `tables/sp002_strength_multiplier_validation.csv` | Run orientation-specific strength multipliers and report mean, standard deviation and Weibull-like scatter |
| Quasi-static loading | SP-002 speed check shows broken-bond plateau but force oscillations remain | Add slower or step-relax protocol and kinetic-energy/load-equilibrium checks |
| Native force-chain evidence | `figures/pb006/pb006_seed02_seed03_overlap_force_proxy.png` | Design restart/rerun or first-run-compatible `pair/gran/local` workflow |
| 1000-pebble compression statistics | Completed 0.15 mm seed01, orient02 and seed02 restartable cases now give resolved event sequences with 98, 95 and 316 broken bonds respectively | Add at least one more independent 1000-pebble seed before making probability-distribution claims |

## Next manuscript/table edits to make

1. Add a compact calibration-target table to the manuscript that separates verified anchors from approximate/digitized anchors. The table should include Zhao 0.5 mm plate/environment sensitivity, Annabattula size-effect points, the Lo Frano 1.5 mm near-size anchor, and a final column stating whether each row is used for probability strength, size-effect trend, stiffness, fracture mode, or only as context. This is needed because the current 18-22 N 1.0 mm target rests mainly on approximate Annabattula extrapolation and near-size context.
2. Reword the SP-002-CAL1 paragraph from "calibrated template" to "current calibration candidate" unless the sentence is explicitly about computational calibration. The defensible statement is that SP-002-CAL1 simultaneously matches the current crush-load scale and avoids pure surface chipping; it is not yet a final material calibration because initial stiffness, full force-displacement shape, loading-rate equilibrium, and stochastic strength distribution are still incomplete.
3. Add a single-pebble ensemble summary table immediately after the weak-plane calibration text. Minimum columns: case set, number of orientations or multipliers, peak-force range, mean plus standard deviation where applicable, first-break displacement range, major-fragment sizes, and manuscript status. This will make clear that five orientations and a y-normal multiplier scan demonstrate feasibility and scatter, but do not yet constitute a publishable Weibull calibration.
4. Insert the conservative PB-006 500-vs-1000 comparison table rather than comparing endpoint magnitudes directly in prose. Use `tables/pb006_500_vs_1000_onset_comparison.csv`; add a footnote that 500-pebble and 1000-pebble endpoint forces/bond losses are different-displacement diagnostics.
5. Tighten the Discussion into three explicit evidence tiers: calibrated-template evidence, random-bed onset evidence, and force-path proxy evidence. The strongest current bed-scale claim should be "early top-layer trigger is reproduced across three 500-pebble seeds and one 1000-pebble short scan"; reserve "bed-scale crushing statistics", "force-chain mechanism", and "predictive damage law" for future deeper multi-seed runs with native contact-force output.

## Priority order

1. Add the 500-vs-1000 early-onset comparison table, with the 1000-pebble result labelled as a 0.10 mm thermo scan plus targeted local-dump window.
2. Complete the single-pebble literature calibration table before making final quantitative claims.
3. Add the single-pebble ensemble summary table that distinguishes the deterministic SP-002-CAL1 candidate, five-orientation pilot, and y-normal strength-multiplier scan.
4. Add a limitations paragraph that explicitly separates calibrated-template evidence, random-bed onset evidence and force-path proxy evidence.
5. Plan a deeper or repeated 1000-pebble run, using the successful targeted-window workflow to limit output volume.
