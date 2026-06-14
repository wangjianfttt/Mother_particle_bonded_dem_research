# Single-pebble calibration dossier for SP-002-CAL1

This note records the current defensible status of the 1 mm Li4SiO4 bonded template used in PB-006 random-bed simulations. It is written to answer the reviewer-style question: why is a 500-subparticle bonded mother pebble a credible template rather than an arbitrary numerical object?

## Current conclusion

SP-002-CAL1 is a **current calibration candidate** for bed insertion, not a final Li4SiO4 material law.

The candidate is defensible for the present PB-006 workflow because it satisfies two necessary model-side constraints:

1. **Load scale:** the deterministic weak-plane case reaches a peak top force of 18.64 N, inside the current exploratory 1 mm target window of 15-22 N.
2. **Failure morphology:** the final intact-bond graph contains two major fragments of 227 and 224 subparticles, unlike the homogeneous load-matched case, which remains essentially one 494-subparticle body plus small surface chips.

The candidate is not yet sufficient for strong predictive claims because three calibration dimensions remain incomplete:

1. experimental initial stiffness and force-displacement curve digitization;
2. a full-endpoint hold-relax or still-slower x-normal rate check if strong quasi-static peak-load wording is desired;
3. larger orientation/strength ensemble or subparticle-count sensitivity.

## Evidence package

| Evidence layer | File | Main use |
| --- | --- | --- |
| Literature target anchors | `tables/single_pebble_calibration_target_evidence_summary.csv` | Separates verified 0.5 mm anchors, digitized size-effect anchors, near-size approximations and near-neighbour DEM context. |
| Model calibration matrix | `tables/single_pebble_model_calibration_matrix.csv` | Tracks homogeneous scans, stiffness scans and weak-plane candidates. |
| Manuscript evidence summary | `tables/single_pebble_model_ensemble_evidence_summary.csv` | Compresses homogeneous rejection, CAL1 selection, orientation pilot, strength multiplier and Weibull trial into one reviewer-readable table. |
| Template provenance audit | `tables/sp002_cal1_template_provenance_audit.csv` | Separates the true x-normal CAL1 branch from later y-normal residual-template rate checks. |
| Orientation pilot | `tables/sp002_cal1_orientation_summary.csv` | Shows that weak-plane orientation creates load scatter while retaining two-major-fragment morphology. |
| Strength multiplier validation | `tables/sp002_strength_multiplier_validation.csv` | Shows that y-normal high-strength cases can be moved into the target load window without losing split morphology. |
| Quasi-static risk check | `tables/sp002_quasistatic_check.csv` | States what the current speed evidence does and does not support. |
| Main calibration figure | `figures/sp002/single_pebble_calibration_evidence.svg` | Visual summary of literature load window, model load evidence and fragment-mode filter. |

## Quantitative status

| Item | Current result | Interpretation |
| --- | ---: | --- |
| SP-002-CAL1 peak top force | 18.64 N | Inside current 15-22 N exploratory 1 mm target window. |
| SP-002-CAL1 first break | 0.1025 mm | Plausible order, but exact experimental displacement comparison is still weak. |
| SP-002-CAL1 final major fragments | 227 + 224 subparticles | Accepts the template as a split/fracture candidate rather than a surface-chipping candidate. |
| Homogeneous load-matched case | 18.45 N, 494 + 1 largest fragments | Reject as final template because the force is matched but the morphology is wrong. |
| CAL1 orientation pilot | 14.52-28.38 N across 5 orientations | Orientation gives meaningful scatter, but not yet a calibrated distribution. |
| Strength multiplier validation | 13.86-28.38 N across 5 y-normal cases | Strength scaling can tune the load while preserving morphology, but the response is nonlinear. |
| 50 MPa speed check | 0.25 to 0.10 m/s changes final broken bonds by 1.0% and peak force by -7.7% | Fragment count is encouraging; this is background screening evidence rather than CAL1 validation. |
| CAL1 x-normal 0.05 m/s rerun | 21.64 N peak, first break 0.1025 mm, final fragments 236 + 226 | True CAL1 slow-rate check: the 5876-bond template and first-break displacement are retained; peak increases by 16.1% but remains inside the 15-22 N target window. |
| CAL1 x-normal 0.03 m/s short run | first break 0.10245 mm, endpoint fragments 247 + 246 at 0.18 mm | True CAL1 still-slower onset check: the 5876-bond template, first-break window and split topology are retained. Because the run stops before the known peak region, it must not be used as peak-load validation. |
| y-normal 0.10/0.05 m/s reruns | 28.38 N and 28.32 N peaks, 5846 initial bonds | These residual-template runs reproduce the y-normal orientation pilot, not x-normal CAL1. They support orientation-specific rate insensitivity only. |

## Safe manuscript wording

Use:

- "current calibration candidate"
- "load-scale and fragment-mode matched bonded template"
- "weak-plane reduced-order defect representation"
- "model-side calibration evidence"

Avoid:

- "validated Li4SiO4 material law"
- "fully calibrated Weibull distribution"
- "quasi-static compression response"
- "experimentally proven weak-plane defect"

## Remaining work before strong validation language

1. Run one hold-relax or still-slower x-normal check only if the manuscript uses stronger quasi-static language than "screening-rate sensitivity".
2. Digitize or otherwise extract experimental initial stiffness and full force-displacement shape from the closest available literature.
3. Complete at least a 20-sample orientation/strength ensemble, using orientation-specific interpolation rather than a single linear strength multiplier.
4. Add a 250/500/1000 subparticle-count sensitivity study if the manuscript claims numerical convergence.

## Immediate claim boundary for PB-006

The PB-006 random-bed results can be interpreted as compression-driven breakage-event sequences for beds made of the **same intact SP-002-CAL1 calibration-candidate template**. The bed simulations should not be presented as predictive Li4SiO4 crush probabilities until the single-pebble calibration gaps above are closed.

## Template provenance and rate record

The true x-normal CAL1 slow-rate rerun is archived at:

```text
simulations/single_pebble/SP-002/archive/SP-002-CAL1-x-slow0p05ms-0p3mm-completed-20260531/
```

Outputs:

- `data/processed/SP-002-CAL1-x-slow0p05ms-0p3mm_thermo.csv`
- `data/processed/SP-002-CAL1-x-slow0p05ms-0p3mm_summary.csv`
- `data/processed/SP-002-CAL1-x-slow0p05ms-0p3mm_initial_stiffness.csv`
- `data/processed/SP-002-CAL1-x-slow0p05ms-0p3mm_fragments.csv`
- `data/processed/SP-002-CAL1-x-slow0p05ms-0p3mm_failure_metrics.csv`
- `tables/sp002_cal1_template_provenance_audit.csv`

The y-normal residual-template reruns are archived separately and retained as orientation-specific sensitivity evidence:

- `simulations/single_pebble/SP-002/archive/SP-002-CAL1-matched0p10ms-0p3mm-completed-20260531/`
- `simulations/single_pebble/SP-002/archive/SP-002-CAL1-slow0p05ms-0p3mm-completed-20260530/`
- `data/processed/SP-002-CAL1-matched0p10ms-0p3mm_thermo.csv`
- `data/processed/SP-002-CAL1-matched0p10ms-0p3mm_summary.csv`
- `data/processed/SP-002-CAL1-matched0p10ms-0p3mm_initial_stiffness.csv`
- `data/processed/SP-002-CAL1-matched0p10ms-0p3mm_fragments.csv`
- `data/processed/SP-002-CAL1-matched0p10ms-0p3mm_failure_metrics.csv`
- `data/processed/SP-002-CAL1-slow0p05ms-0p3mm_thermo.csv`
- `data/processed/SP-002-CAL1-slow0p05ms-0p3mm_summary.csv`
- `data/processed/SP-002-CAL1-slow0p05ms-0p3mm_initial_stiffness.csv`
- `data/processed/SP-002-CAL1-slow0p05ms-0p3mm_fragments.csv`
- `data/processed/SP-002-CAL1-slow0p05ms-0p3mm_failure_metrics.csv`

Interpretation: the apparent 5876-versus-5846 discrepancy is now resolved as an orientation/template-state issue. The x-normal CAL1 branch has 5876 initial bonds at both 0.10 and 0.05 m/s. The true x-normal slow rerun keeps first break fixed at 0.1025 mm and retains two-major-fragment splitting, while the peak rises from 18.64 to 21.64 N. The earlier 28.3 N pair belongs to the y-normal branch and must not be cited as CAL1 reproduction.

## Curve-level calibration overlay

On 2026-05-31 CST, a force-displacement overlay was added to address the template-level validation concern directly. The figure compares the x-normal CAL1 reference and true x-normal 0.05 m/s rerun as full force-displacement traces against the provisional 1 mm load target window and a near-size literature displacement/load anchor.

Outputs:

- `figures/sp002/sp002_force_displacement_overlay.svg`
- `figures/sp002/sp002_force_displacement_overlay.pdf`
- `figures/sp002/sp002_force_displacement_overlay.png`
- `figures/sp002/sp002_force_displacement_overlay.tiff`
- `tables/sp002_force_displacement_overlay_metrics.csv`

Key metrics:

- CAL1 x-normal 0.10 m/s: peak force 18.637 N, peak displacement 0.2445 mm, first break 0.1025 mm, final broken bonds 703.
- CAL1 x-normal 0.05 m/s: peak force 21.642 N, peak displacement 0.26075 mm, first break 0.1025 mm, final broken bonds 541.

Interpretation: the overlay supports curve-level calibration screening and partial rate robustness in first-break displacement, but it does not close stiffness calibration, subparticle-count convergence or full Li4SiO4 material-law validation.

## Additional 0.03 m/s onset check

On 2026-06-01 CST, a true x-normal 0.03 m/s SP-002-CAL1 short run was completed to 0.18 mm. It started from the same 5876-bond x-normal branch and first broke at 0.10245 mm, essentially matching the 0.10 and 0.05 m/s first-break window. At the endpoint, the intact-bond graph contained two major fragments of 247 and 246 subparticles plus small chips.

Outputs:

- `simulations/single_pebble/SP-002/archive/SP-002-CAL1-x-slow0p03ms-0p18mm-completed-20260601/`
- `data/processed/SP-002-CAL1-x-slow0p03ms-0p18mm_thermo.csv`
- `data/processed/SP-002-CAL1-x-slow0p03ms-0p18mm_summary.csv`
- `data/processed/SP-002-CAL1-x-slow0p03ms-0p18mm_initial_stiffness.csv`
- `data/processed/SP-002-CAL1-x-slow0p03ms-0p18mm_fragments.csv`
- `data/processed/SP-002-CAL1-x-slow0p03ms-0p18mm_failure_metrics.csv`
- `figures/sp002/SP-002-CAL1-x-slow0p03ms-0p18mm_curve.svg`

Interpretation: this run strengthens first-break and morphology robustness across 0.10, 0.05 and 0.03 m/s x-normal screening rates. It does not strengthen peak-load wording because it ends before the known peak-force displacement of the 0.10 and 0.05 m/s full-endpoint runs.
