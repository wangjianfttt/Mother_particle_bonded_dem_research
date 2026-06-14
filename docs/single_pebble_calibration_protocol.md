# Single-pebble calibration protocol

## Decision

The 500-subparticle, 1.0 mm bonded Li4SiO4 template now has a **first single-pebble calibration candidate**. The weak-plane case `SP-002-weakplane-bulk90-weak22p5-cd90-0p1ms-0p3mm` matches the current 1.0 mm crush-load target and produces two major fragments rather than only surface chips. It should be treated as SP-002-CAL1, not yet as a final publishable calibration, because repeated seeds, slower/relaxed loading and exact experimental curve extraction are still pending.

## Experimental targets

The current literature target table is:

```text
tables/single_pebble_experimental_calibration_targets.csv
```

The most relevant targets are:

- Zhao et al., DOI `10.1016/j.engfracmech.2012.05.011`: 0.5 mm Li4SiO4 crush-load distributions under WC, AL and BK7/dry-inert conditions.
- Annabattula et al., DOI `10.13182/FST13-737`: OSi size-effect sequence from 250 to 800 um under BK7/dry-inert conditions; 800 um is about 15 N and the size trend suggests a 1.0 mm target near 18-20 N.
- Lo Frano and Puccini, DOI `10.1016/j.fusengdes.2021.112388`: near-size 1-1.5 mm Li4SiO4 anchor, average ultimate load about 14 N, displacement scale about 0.04 mm and 3-4 plate-like fragments.
- Kuang et al., DOI `10.1016/j.fusengdes.2023.114105`: nearest DEM comparison for 1.0 mm Li4SiO4 failure patterns and size effects.

Working target for the present 1.0 mm template:

- peak crush load: 18-20 N as the first target, with 15-22 N as the exploratory window;
- failure displacement: order 0.04-0.10 mm until exact curve extraction is complete;
- fragment mode: splitting or progressive fracture with a few major fragments, not only single-subparticle surface chipping;
- scatter: Weibull modulus order 2.5-4 based on 0.5 mm references, pending 1.0 mm-specific validation.

## Model-side status

The model-side calibration matrix is:

```text
tables/single_pebble_model_calibration_matrix.csv
```

Current interpretation:

- 50 MPa at 0.1 m/s gives about 6.45 N and is too weak for a 1.0 mm target.
- 100 MPa fast screening gives about 16.47 N, close to the lower edge of the target window but still not quasi-static and lacks fragment graph output.
- `kn=5e13` and `kn=1e14` are numerically usable stiffness settings; `kn=2e14` is rejected pending a smaller timestep check.
- The weak-plane SP-002-CAL1 case gives a peak top force of 18.64 N, a peak bottom force of 18.07 N, first break at 0.103 mm and final major fragments of 227 and 224 subparticles.

## Calibration stages

### Stage 1: Elastic stiffness

Goal: match the initial force-displacement slope before bond damage.

Fixed parameters:

- 500-subparticle 1.0 mm no-overlap template;
- `radiusMultiplierBond = 1.0`;
- `createDistanceBond = 2.00e-4 m`;
- `rho = 2400 kg m-3`, `young = 9.0e10 Pa`, `poisson = 0.25`;
- wall and particle friction kept at current values unless literature requires a plate-specific setting;
- load at `top_vz <= 0.1 m/s` or with a step-relax protocol.

Recommended stiffness scan:

| kn | kt |
| ---: | ---: |
| 2.5e13 | 1.25e13 |
| 5.0e13 | 2.5e13 |
| 7.5e13 | 3.75e13 |
| 1.0e14 | 5.0e13 |
| 1.25e14 | 6.25e13 |

Do not scan `radiusMultiplierBond` in the first pass. It changes bond area, bending/torsional inertia, stiffness and failure stress simultaneously.

### Stage 2: Mean crush load

After choosing a stiffness pair, tune `maxSigmaBond` and `maxTauBond`.

Initial strength scan for the current usable stiffness values:

| kn / kt | strengths |
| --- | --- |
| 1.0e14 / 5.0e13 | 100, 120, 140 MPa |
| 5.0e13 / 2.5e13 | 100, 120, 140 MPa |

Required outputs for every run:

- thermo force-displacement table;
- initial stiffness estimate;
- bond-local dump;
- final fragment graph;
- first-break displacement;
- peak top and bottom forces.

### Stage 3: Failure mode and Weibull scatter

Once the mean peak force is near 18-20 N:

1. Sweep `maxTauBond / maxSigmaBond = 0.5, 1.0, 2.0` to control splitting versus shear/local chipping.
2. Run 3-5 seeds as a pilot and then at least 30 samples for a publishable Weibull comparison.
3. If the model continues to produce mostly single-subparticle chipping, introduce material heterogeneity or template-level defect variability before changing bed simulations.

Current update: `SP-002-calib-kn1e14-120MPa-0p1ms` reaches a peak top force of 18.45 N with estimated stiffness 570 N/mm and first break at 0.116 mm, so the peak-load target is plausible. It is not accepted yet because the fragment graph remains 7 components with a 494-subparticle main fragment and 6 single-subparticle chips, which is closer to surface chipping than the experimental 3-4 plate-like/splitting fragments.

Strength-ratio update:

- `sigma=120 MPa, tau=60 MPa` reduces the peak top force to 13.74 N and still gives mostly surface chipping.
- `sigma=120 MPa, tau=240 MPa` gives a peak top force of 17.96 N but still gives the same 494-subparticle main fragment plus 6 single-subparticle chips.

Therefore, changing the global shear/tensile strength ratio alone does not solve the fracture-mode problem. The next calibration branch must introduce internal defects, weak planes or bond/property heterogeneity.

Weak-plane update:

- `SP-002-weakplane-bulk120-weak60-cd110-0p1ms-0p3mm` forms two major fragments but peaks at 31.09 N, so it is too strong.
- `SP-002-weakplane-bulk100-weak25-cd90-0p1ms-0p3mm` forms two major fragments and peaks at 21.78 N, near the upper edge of the exploratory window.
- `SP-002-weakplane-bulk90-weak22p5-cd90-0p1ms-0p3mm` forms two major fragments and peaks at 18.64 N, so it is the current SP-002-CAL1 candidate.

## Stage 4: Defect and heterogeneity branch

The homogeneous 500-subparticle template is too symmetric and strong internally: it can match peak load but prefers small surface chips. To reproduce experimental 3-4 plate-like or splitting fragments, test these mechanisms in order:

1. Template-level weak plane: assign two material types separated by a random plane and weaken bonds crossing the plane.
2. Bond-strength heterogeneity: draw each pebble/sample strength from a Weibull multiplier and, if possible, assign bond-level strength bins.
3. Network-density perturbation: reduce `createDistanceBond` or remove a small fraction of internal bonds along a seeded weak band while preserving initial stability.
4. Bond-radius scan only after the above, because `radiusMultiplierBond` changes stiffness and strength simultaneously.

Acceptance requirement for this branch: peak load remains within 15-22 N and final fragments include a few major pieces, not only single-subparticle chips. SP-002-CAL1 satisfies this model-side requirement for one deterministic weak-plane orientation.

## Timestep rule

`fix check/timestep/gran` checks granular contact stability but does not fully guarantee bonded-beam vibration stability. Use this rule until a better bond-specific timestep estimate is implemented:

- `kn <= 1.0e14`: `dt = 5e-9 s` is currently usable.
- `kn = 1.25e14`: test `dt = 2.5e-9 s` before production.
- `kn >= 2.0e14`: use `dt = 1.0e-9 s` for diagnostic reruns; current `dt = 5e-9 s` produced abrupt nonphysical bond loss.

## Acceptance criteria

The 1.0 mm template is accepted for bed-scale physical interpretation only when:

1. mean peak load matches the selected experimental target within 10-15%;
2. initial stiffness is within the experimental/derived uncertainty band;
3. first-break displacement is in the experimental displacement range;
4. fragment graph indicates splitting/progressive fracture rather than pure surface chipping;
5. repeated seeds reproduce the experimental scatter or Weibull modulus at least qualitatively.

The archived SP-002-CAL1 reference satisfies criteria 1 and 4 for a single deterministic weak-plane case. Criteria 2, 3 and 5 remain open until the experimental displacement/stiffness curves are extracted more precisely and a seed/orientation ensemble is run. The apparent 5846-bond reproducibility caveat has been traced to residual y-normal template state rather than to the x-normal CAL1 branch.

## Matched-rate sensitivity update

The true x-normal SP-002-CAL1 slow-rate rerun has been completed:

```text
SP-002-CAL1-x-slow0p05ms-0p3mm
```

It reaches 0.30 mm displacement and starts from 5876 intact bonds, matching the x-normal 0.10 m/s CAL1 branch. The 0.05 m/s run gives a peak top force of 21.64 N, first break at 0.1025 mm and final major fragments of 236 and 226 subparticles. Relative to the 0.10 m/s CAL1 reference, first break is unchanged, split morphology is retained and the peak force increases by 16.1%, remaining inside the current 15-22 N exploratory target window.

The previously named `SP-002-CAL1-matched0p10ms-0p3mm` and `SP-002-CAL1-slow0p05ms-0p3mm` cases are now classified as y-normal orientation sensitivity, not CAL1 reproduction. They start from 5846 intact bonds and reproduce the y-normal orientation pilot at about 28.3 N. The provenance split is recorded in `tables/sp002_cal1_template_provenance_audit.csv`.

## Orientation sensitivity update

The first orientation ensemble used the same SP-002-CAL1 material parameters and changed only the weak-plane normal. Results are summarized in:

```text
tables/sp002_cal1_orientation_summary.csv
```

All tested orientations produced two major fragments rather than the homogeneous-template surface-chipping mode:

| Orientation | Peak top force | Major fragments | Interpretation |
| --- | ---: | --- | --- |
| x, normal (1,0,0) | 18.64 N | 227 + 224 | Current load-calibrated orientation. |
| xy30, normal (0.866,0.5,0) | 27.37 N | 223 + 220 | Same morphology but too strong. |
| y, normal (0,1,0) | 28.38 N | 228 + 216 | Same morphology but too strong. |
| xy45, normal (1,1,0) | 24.57 N | 229 + 223 | Intermediate strength. |
| tilted, normal (1,0,0.5) | 14.52 N | 237 + 234 | Lower-strength progressive bulk-damage case. |

The current five-case pilot ensemble has a mean peak top force of 22.70 N and a standard deviation of 5.93 N, with only the x-normal case inside the current 15-22 N target window. The current interpretation is that weak-plane orientation should be treated as a stochastic microstructural variable, but orientation alone is not enough for final calibration. For publication, the next target is an ensemble of at least 20-30 weak-plane orientations combined with sample-level strength multipliers so that the mean and Weibull scatter can be matched simultaneously.

## Strength-multiplier update

A minimal statistical calibration script now links the literature target table, the SP-002-CAL1 orientation pilot and a truncated Weibull sampling plan:

```text
scripts/calibrate_minimal_weibull_strength.py
tables/minimal_weibull_strength_calibration_summary.csv
tables/minimal_weibull_strength_sampling_plan.csv
```

Using the current literature table, the fitted 1.0 mm target mean is 17.36 N and the target standard deviation is 3.47 N. The orientation-pilot mean is 22.70 N, so the suggested sample-level strength multiplier has mean 0.765 and a first target-window range of 0.661-0.969.

Two y-normal validation runs confirm that strength multipliers can tune the high-strength orientation without losing the two-major-fragment morphology:

```text
tables/sp002_strength_multiplier_validation.csv
```

| Case | Strength multiplier | Peak top force | Major fragments |
| --- | ---: | ---: | --- |
| y baseline, 90/22.5 MPa | 1.000 | 28.38 N | 228 + 216 |
| y reduced, 80/20 MPa | 0.889 | 20.60 N | 228 + 221 |
| y reduced, 74/18.5 MPa | 0.822 | 19.33 N | 228 + 222 |
| y reduced, 70/17.5 MPa | 0.778 | 15.69 N | 227 + 219 |
| y linear-plan centre, 55.1/13.8 MPa | 0.612 | 13.86 N | 225 + 216 |

This supports a two-level ensemble model: weak-plane orientation controls morphology and orientation scatter, while a sample-level strength multiplier shifts each realization into the experimental crush-load distribution. The y-normal validation also shows that peak force is not linear in strength multiplier over the full range; the 55.1/13.8 MPa linear-plan centre underpredicts the target. The next ensemble generator should therefore use orientation-specific response interpolation rather than a simple multiplier from the 90/22.5 MPa baseline.
