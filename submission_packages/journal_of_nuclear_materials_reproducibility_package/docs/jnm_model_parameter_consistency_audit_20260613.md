# JNM model-parameter consistency audit

Purpose: record a reviewer-facing check that the material, contact, bond and loading parameters stated in the Journal of Nuclear Materials manuscript match the representative inputs and actual PB-007 run logs used for the accepted evidence chain.

The manuscript-facing parameter phrases verified here are: density 2400 kg m-3, Young's modulus 90 GPa, Poisson ratio 0.25, restitution coefficient 0.3, friction coefficient 0.5, bond stiffnesses of 1.0e14 and 5.0e13 N m-3, bulk and weak-plane strengths of 90 MPa and 22.5 MPa, creation distances of 0.20 mm and 0.09 mm, a 5.0 ns timestep, restored contact modulus 1.5e10 Pa, 10,000 pre-compression relaxation steps, 4935 internal bonds per mother pebble and 493,500 bonds for the 100-mother-pebble bed.

## Active evidence route

The active JNM route is the corrected PB-007 route, not the superseded PB-006 event database. The accepted fracture-sequence pilot is:

- `PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot`
- run input template: `simulations/pebble_bed/PB-007/in.pb007_bonded_step_relaxed_validation.lmp`
- copied case input: `simulations/pebble_bed/PB-007/cases/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot/in.pb007_bonded_step_relaxed_validation.lmp`
- wrapper: `scripts/run_pb007_bonded_step_relaxed_validation.sh`
- actual echo log: `simulations/pebble_bed/PB-007/cases/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot/screen_PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot.log`
- accepted result table: `tables/pb007_PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_acceptance_summary.csv`

## Parameter trace

| Parameter group | Manuscript value | Script/log evidence | Audit conclusion |
| --- | --- | --- | --- |
| Mother-pebble diameter | 1.0 mm | The transferred template is the 500-subparticle `surface500_shell260` 1 mm template used throughout the active route. | Consistent with the stated mother-pebble scale. |
| Subparticles per mother pebble | 500 | PB-007 input uses `variable nspheres index 500`; accepted bed contains 50,000 atoms for 100 mother pebbles. | Consistent. |
| Internal bonds per template and bed | 4935 and 493,500 | The accepted summary records `initial_intact_bonds=493500`; metadata and analysis assume 100 templates of 4935 bonds each. | Consistent. |
| Density | 2400 kg m-3 | PB-007 and single-pebble inputs set `rho=2400.0` and create the multiple-sphere template with `density constant ${rho}`. | Consistent. |
| Single-pebble contact modulus | 90 GPa | The single-pebble reference input sets `young=9.0e10`; the Methods table states 90 GPa for Hertzian contacts. | Consistent for single-pebble calibration/sensitivity evidence. |
| Corrected-bed restored contact modulus | 1.5e10 Pa | The PB-007 template default is lower, but the wrapper passes `-var young`; the accepted screen log expands `youngsModulus` to `1.5e10 1.5e10 1.5e10`. | Consistent; the actual bed-run value comes from the wrapper/log, not the template default. |
| Poisson ratio | 0.25 | PB-007 and single-pebble inputs set `poisson=0.25`. | Consistent. |
| Restitution coefficient | 0.3 | PB-007 and single-pebble inputs set `cor=0.3`. | Consistent. |
| Friction coefficient | 0.5 | PB-007 and single-pebble inputs set `mu=0.5`. | Consistent. |
| Bond normal/tangential stiffness | 1.0e14 and 5.0e13 N m-3 | PB-007 and single-pebble inputs set `normalBondStiffnessPerUnitArea=1.0e14` and `tangentialBondStiffnessPerUnitArea=5.0e13`. | Consistent. |
| Bulk bond strengths | 90 MPa normal/tangential | Inputs set `sigma_bulk/tau_bulk=9.0e7` Pa or `sigma_max/tau_max=9.0e7` Pa. | Consistent. |
| Weak-plane strengths | 22.5 MPa normal/tangential | Inputs set `sigma_weak/tau_weak=2.25e7` Pa. | Consistent. |
| Bulk and weak-plane creation distances | 0.20 and 0.09 mm | Inputs set `create_dist=2.00e-4` m and `create_weak=9.00e-5` m. | Consistent. |
| Bonded timestep | 5.0 ns | PB-007 and single-pebble inputs set `dt=5.0e-9`; the accepted screen log echoes `timestep 5.0e-9`. | Consistent. |
| Step-relaxed increment | 1 micrometre | The accepted run uses `top_speed=0.2`, `dt=5.0e-9` and `increment_steps=1000`, giving 1.0e-6 m per increment. The screen log shows the 60th increment as `60*0.2*5.0e-9*1000 = 6e-05`. | Consistent. |
| Pre-compression relaxation | 10,000 steps | The accepted summary uses baseline step 10001, consistent with one initial run step plus 10,000 pre-compression relaxation steps. | Consistent. |

## Reviewer-risk notes

1. The PB-007 copied input file still contains conservative default values such as `young=5.0e6`, `hold_steps=20000` and `n_increments=5`. These are not the actual accepted-pilot values when the wrapper supplies command-line overrides. The screen log is the authoritative source for expanded runtime values.
2. The final `run 0` line in the LIGGGHTS log can show zero in selected thermo variables after final local dumps are written. The accepted mechanics and bond-count values should therefore be read from the post-processed acceptance summary and event tables, not by blindly taking the last raw thermo row.
3. The manuscript correctly distinguishes the single-pebble 90 GPa contact-modulus calibration evidence from the corrected-bed restored-contact protocol at 1.5e10 Pa. The latter is a gate-passing numerical protocol, not a final Li4SiO4 material law.

## Status

This audit supports the current JNM Methods and Table 2 wording. The remaining submission blocker is external repository DOI/stable URL insertion, not model-parameter inconsistency.
