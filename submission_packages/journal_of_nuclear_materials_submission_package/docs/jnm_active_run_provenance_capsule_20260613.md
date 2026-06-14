# JNM active-run provenance capsule (2026-06-13)

This capsule records the current accepted run-to-figure chain for the Journal of
Nuclear Materials submission. It is deliberately narrower than a project log:
only evidence used by the active manuscript is listed here.

## Active corrected-bed fracture-sequence run

| Role | Path or value | Evidence use |
| --- | --- | --- |
| Accepted fracture-sequence case | `PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot` | Main corrected-bed event sequence used by Fig. 5 and Table 1. |
| Case directory | `simulations/pebble_bed/PB-007/cases/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot` | Contains the copied input, screen log, LIGGGHTS log, mesh files, template-transfer files and raw local dumps. |
| Run wrapper | `scripts/run_pb007_bonded_step_relaxed_validation.sh` | Creates the bonded case from the rigid settled state and passes all runtime parameters to the solver. |
| Copied case input | `simulations/pebble_bed/PB-007/cases/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot/in.pb007_bonded_step_relaxed_validation.lmp` | Template input after case creation. The copied input still contains conservative default variables; wrapper and screen log are the runtime authority. |
| Runtime screen log | `simulations/pebble_bed/PB-007/cases/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot/screen_PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot.log` | Authoritative evidence for expanded runtime variables, loading loop and final thermo rows. |
| LIGGGHTS log | `simulations/pebble_bed/PB-007/cases/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot/log.liggghts` | Thermo source parsed into the processed history. |
| Template-transfer metadata | `simulations/pebble_bed/PB-007/cases/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot/data/bonded_template_metadata.csv` | Confirms 100 transferred mother pebbles and nanometre-scale coordinate fits. |
| Raw internal-bond local dumps | `post/bonds_event_*.local`; `post/bonds_final.local` in the case directory | Source for mother-pebble bond series and event table. |
| Raw native-force local dumps | `post/pairs_event_*.local`; `post/walls_event_*.local`; `post/pairs_final.local`; `post/walls_final.local` in the case directory | Source for native inter-mother force-network metrics. |

## Runtime parameters verified from wrapper/log

| Quantity | Runtime value | Evidence |
| --- | ---: | --- |
| Subparticles per bed | 50,000 | Screen/log thermo rows report 50,000 atoms for the 100 mother-pebble bed. |
| Mother pebbles | 100 | Template-transfer metadata contains 100 rows. |
| Internal bonds at start | 493,500 | Acceptance summary and screen/log thermo rows. |
| Restored contact modulus used by this corrected-bed protocol | 1.5e10 Pa | Screen log expands `youngsModulus peratomtype` to `1.5e10 1.5e10 1.5e10`. This is a protocol value, not a final Li4SiO4 material law. |
| Timestep | 5.0 ns | Screen log expands `timestep 5.0e-9`. |
| Compression increment | 1 micrometre | `top_speed = 0.2`, `dt = 5.0e-9`, and `increment_steps = 1000`, so each increment is 1.0e-6 m. |
| Final displacement | 60 micrometres | Screen log expands the final expression to `60*0.2*5.0e-9*1000`, and the accepted final physical thermo row has `top_disp = 6e-05`. |
| Hold steps per increment | 1000 | Screen log expands `run ${hold_steps}` to `run 1000`. |
| Final intact internal bonds | 493,495 | Acceptance summary and final physical thermo row. |
| Final recorded broken bonds | 5 | Difference between 493,500 initial and 493,495 minimum intact bonds. |

## Raw-to-processed chain

| Stage | Script | Output |
| --- | --- | --- |
| Thermo extraction | `scripts/extract_liggghts_thermo.py` | `data/processed/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_thermo.csv` |
| Postprocess driver | `scripts/postprocess_pb007_corrected_fracture_pilot.sh` | Regenerates the accepted thermo, native-force, acceptance, validation, bond-series and event outputs for this case. |
| Native final network | `scripts/analyze_pb007_native_force_network.py` | `tables/pb007_PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_native_summary.csv`; `tables/pb007_PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_native_edges.csv` |
| Native network series | `scripts/analyze_pb007_native_force_network_series.py` | `data/processed/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_native_force_network_series.csv` |
| Load-path/acceptance summary | `scripts/summarize_pb007_loadpath_validation.py` | `tables/pb007_PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_acceptance_summary.csv` |
| Bond-event sequence | `scripts/analyze_pb007_bond_event_sequence.py` | `data/processed/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_bond_series.csv`; `data/processed/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_breakage_events.csv` |
| Main acceptance-gate figure | `scripts/plot_pb007_acceptance_gate_validation.py` | `figures/pb007/pb007_acceptance_gate_validation.pdf`; `figures/pb007/pb007_acceptance_gate_validation.png` |
| Main fracture-sequence figure | `scripts/plot_pb007_corrected_fracture_sequence.py` | `figures/pb007/pb007_corrected_fracture_sequence.pdf`; `figures/pb007/pb007_corrected_fracture_sequence.png` |

## Manuscript-use boundary

- The 5 micrometre entry protocol at the same restored modulus passes the
  zero-pre-damage/native-spanning/force-balance gate and establishes the
  loading route.
- The 60 micrometre fracture-sequence run is used as event-sequence evidence:
  the accepted event table contains bond-loss increments at 25, 35 and 60
  micrometres, all localized to one rank-2 upper-bed mother pebble.
- The 60 micrometre endpoint is not treated as a quasi-static force-balance
  validation state. Its acceptance summary records a final incremental
  wall-balance residual of 59.6%, so the manuscript uses this run for the
  chronology of internal-bond loss and native force-network reorganization, not
  as a converged bed-scale constitutive response.
- The final `run 0` after local-dump commands changes the displayed wall-force
  row and bond counters; scalar acceptance values therefore use the final
  physical thermo row and processed acceptance summary, not the post-dump
  `run 0` row.

