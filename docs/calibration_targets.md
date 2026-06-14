# Calibration targets for bonded Li4SiO4 pebbles

## Current extracted experimental data

The first verified crush-load dataset is Zhao et al., *Engineering Fracture Mechanics* 100 (2013) 28-37, DOI `10.1016/j.engfracmech.2012.05.011`.

The paper reports 0.5 mm Li4SiO4 pebble crush tests under different plate/environment conditions:

| Diameter | Plate/environment | Loading rate | Mean crush load | Standard deviation | Sample count |
| ---: | --- | ---: | ---: | ---: | ---: |
| 0.5 mm | WC plates, air | 0.015 mm/min | 7.55 N | 1.55 N | 92 |
| 0.5 mm | AL plates, air | 0.015 mm/min | 10.6 N | 3.02 N | 86 |
| 0.5 mm | BK7 plates, dry inert gas | 0.015 mm/min | 5.88 N | 1.14 N | 200 |

These values should not be used as a direct one-point calibration for the present 1.0 mm model without applying a size-effect correction. They are nevertheless important because they show that apparent crush load depends strongly on plate material and environment. The single-pebble calibration table must therefore retain plate material, loading rate and atmosphere.

The second calibration anchor is Annabattula et al., *Fusion Science and Technology* (2014), DOI `10.13182/FST13-737`. The paper reports BK7/dry-inert crush tests for OSi pebbles with mean diameters from 250 to 800 um. Approximate values digitized from the reported size-effect figure are stored in `tables/single_pebble_experimental_calibration_targets.csv`. The 800 um point is about 15 N, and the fitted size-effect trend suggests that a 1.0 mm pebble should be calibrated near the 18-20 N range first, with a broader acceptable exploratory window of about 15-22 N.

Lo Frano and Puccini, DOI `10.1016/j.fusengdes.2021.112388`, provide a near-size experimental anchor: approximately 1-1.5 mm Li4SiO4 pebbles, average ultimate crushing load near 14 N, displacement scale near 0.04 mm and 3-4 plate-like fragments. This dataset should be used as a qualitative near-size check until the exact figure/table values are verified.

## Implications for the present model

The current 1.0 mm bonded-pebble model at 50 MPa bond strength gives peak top forces of approximately 6.4-7.2 N depending on loading speed, while the 100 MPa case gives about 16.5 N under the fast screening protocol. The model is therefore under-strength at 50 MPa for a 1.0 mm target and likely near the lower edge of the experimental target at 100 MPa. The next calibration stage should focus on 100-140 MPa bond strengths, not on the earlier 25-50 MPa range.

1. Extract 1.0-1.5 mm Li4SiO4 crush-load distributions from structural-performance and size-effect papers.
2. Establish whether the experimental crush load increases, decreases or follows a Weibull size effect across 0.5-1.5 mm.
3. Use force-displacement slope to constrain `normalBondStiffnessPerUnitArea` and `tangentialBondStiffnessPerUnitArea`.
4. Use crush-load distribution to constrain `maxSigmaBond`, `maxTauBond` and possible bond-strength heterogeneity.
5. Validate breakage mode using fragment statistics, not only peak force.

## Current model calibration status

| Parameter family | Current evidence | Status |
| --- | --- | --- |
| Bond strength | 25/50/100 MPa scan gives monotonic peak-force increase and lower broken-bond count with higher strength. | Trend validated; absolute calibration pending. |
| Bond stiffness | 5.0e13 and 1.0e14 N m-3 are numerically usable; 2.0e14 N m-3 causes abrupt bond loss under the current timestep. | Usable range identified; elastic-slope calibration pending. |
| Loading rate | 50 MPa cases approach a broken-bond-count plateau between 0.25 and 0.1 m/s. | Quasi-static direction identified; final slower/relaxation protocol pending. |
| Weak-plane template | A two-type weak-plane template can reproduce both 18-20 N peak load and major-fragment splitting. | First candidate calibrated case identified; replicate and rate checks pending. |
| Bed initialization | PB-003 1.02 mm supported case preserves all 80676 internal bonds before compression and gives supported bed breakage. | Baseline established; slower production run pending. |

## Immediate calibration target

For the current 1.0 mm, 500-subparticle template:

- target peak crush load: start with 18-20 N, exploratory acceptable range 15-22 N;
- target displacement at catastrophic failure: order 0.04-0.10 mm, with exact value pending full figure extraction;
- target breakage mode: splitting/progressive fracture producing a few major fragments, not only single-subparticle chipping;
- target stochasticity: crush-load Weibull modulus of order 2.5-4 for 0.5 mm references, to be revisited after size-specific data extraction.

The current best model-side cases are:

- `SP-002-strength-100MPa`: peak top force 16.47 N, final broken bonds 123, but fast loading and no fragment graph;
- `SP-002-calib-kn1e14-120MPa-0p1ms`: peak top force 18.45 N and stiffness 570 N/mm, inside the current 1.0 mm target load window, but fragment graph still shows surface chipping rather than 3-4 major fragments;
- `SP-002-weakplane-bulk90-weak22p5-cd90-0p1ms-0p3mm`: current SP-002-CAL1 candidate, peak top force 18.64 N, bottom peak 18.07 N, first break at 0.103 mm and final major fragments of 227 and 224 subparticles;
- `SP-002-weakplane-bulk100-weak25-cd90-0p1ms-0p3mm`: near-calibrated weak-plane case, peak top force 21.78 N with final major fragments of 230 and 222 subparticles;
- `SP-002-speed-0p1ms-50MPa-bonds`: peak top force 6.45 N and 7 fragments, but too weak for a 1.0 mm target;
- `SP-002-stiffness-kn1e14`: estimated initial stiffness 570 N/mm, but only 50 MPa strength and no final fragment graph.

The next simulation scan should combine the usable stiffness range with higher bond strength:

| Priority | kn / kt | Strengths | Speed/protocol | Required outputs |
| --- | --- | --- | --- | --- |
| 1 | 1.0e14 / 5.0e13 | 100, 120, 140 MPa | 0.1 m/s, then slower/relax | thermo + initial stiffness + bond dump |
| 2 | 5.0e13 / 2.5e13 | 100, 120, 140 MPa | 0.1 m/s | thermo + stiffness + bond dump |
| 3 | 1.0e14 / 5.0e13 | best strength, 3-5 seeds | final protocol | Weibull scatter and fragment statistics |
| 4 | 2.0e14 / 1.0e14 | 100 MPa only | smaller timestep | numerical-risk check only |

The first 120 MPa run shows that the average load target can be reached without changing the 500-subparticle geometry. The next limiting issue is fracture morphology: the current homogeneous-bond model reaches the correct peak force but releases mainly single-subparticle chips. Further calibration must therefore test strength-ratio, bond-radius/network and heterogeneity effects before accepting the template.

The first strength-ratio diagnostics show that the global `maxTauBond/maxSigmaBond` ratio is not sufficient: `tau/sigma = 0.5` lowers the peak force to 13.74 N without improving fragments, while `tau/sigma = 2.0` keeps the peak near target at 17.96 N but still produces the same surface-chipping pattern. The next route should therefore be weak-plane or heterogeneity modelling.

Weak-plane update: a type-resolved multisphere template with a vertical internal plane was introduced. Reducing cross-plane bond density with `createDistanceBond = 9.0e-5 m` for type 1-2 contacts and using bulk/weak strengths of 90/22.5 MPa produced the first candidate that matches both load and morphology. The final connected-component graph contains two major fragments, 227 and 224 subparticles, plus small chips; this rejects the earlier homogeneous-template surface-chipping mode.

Orientation update: keeping the SP-002-CAL1 material parameters fixed but changing weak-plane normal produces peak forces from 14.52 to 28.38 N while preserving major-fragment splitting. The five-case pilot ensemble gives mean peak force 22.70 N and standard deviation 5.93 N. This confirms that orientation/defect variability can provide a physically meaningful source of single-pebble strength scatter, but final Weibull calibration should also include a sample-level strength multiplier.

Strength-multiplier update: a minimal Weibull calibration estimates a 1.0 mm target mean of 17.36 N and a target standard deviation of 3.47 N from the current literature table. Relative to the five-case orientation-pilot mean, the suggested strength multiplier is 0.765, with an initial target-window range of 0.661-0.969. y-normal validation cases show that reducing bulk/weak strengths from 90/22.5 MPa to 80/20 MPa lowers peak force from 28.38 N to 20.60 N, while 74/18.5 MPa gives 19.33 N; all preserve two major fragments. A lower 55.1/13.8 MPa linear-plan centre gives only 13.86 N, so future ensemble sampling should use orientation-specific response interpolation.
