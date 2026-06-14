# JNM force-transmission validation audit (2026-06-12)

## Decision

The current Journal of Nuclear Materials submission package is on hold. The existing PB-006 bed calculations remain useful as numerical diagnostics of the template-insertion and bond-event extraction workflow, but they cannot support the manuscript's present bed-scale load-path or collective-fracture interpretation.

## Direct evidence

1. The complete PB-006 thermo histories report zero bottom-plate reaction throughout compression for all three 500-mother-pebble beds.
2. Full subparticle-trajectory reconstruction shows no cross-mother-pebble contact at the reported first-break state:
   - Bed B first-break region, approximately 0.0725 mm: zero inter-pebble edges and zero bottom reaction.
   - Bed C at 0.0724975 mm: recorded top force 5.4381 N, reconstructed elastic top-wall force 5.4256 N, zero inter-pebble edges and zero bottom reaction.
3. The reconstructed top-wall force agrees with the recorded DEM top-wall force to within approximately 0.23% for the Bed C onset snapshot. The reconstruction therefore resolves wall loading correctly; the absence of cross-mother contact is not an artefact of a grossly incorrect force conversion.
4. Cross-mother contacts appear only after approximately 3.5-3.6% axial strain, by which time numerous internal bonds have already failed. Even at the final saved state, the mother-pebble graph is small and non-spanning.

## Physical interpretation

The reported early bond losses were triggered by the moving top plate crushing isolated upper mother pebbles before a bed-spanning load-bearing skeleton formed. They are not evidence of force-chain-triggered fracture propagation through a mechanically connected pebble bed.

The failure originates from geometry transfer. Proxy spheres were settled at a nominal 1 mm diameter, whereas the random 500-subparticle bonded template has a rough directional support diameter below 1 mm. The old template has a median directional diameter of about 0.979 mm and a fifth-percentile diameter of about 0.965 mm. Replacing touching proxy spheres with these rough templates therefore introduces systematic inter-pebble gaps. The earlier wall construction also used proxy-radius bounds plus a vertical margin rather than the support of the rotated bonded templates.

## Consequences for the manuscript

- Withdraw claims that the PB-006 results demonstrate bed-spanning force chains, collective bed compression, or macroscopically transmitted fracture cascades.
- Do not interpret the old top-wall force as a bed stress while the bottom reaction is zero.
- Retain PB-006 only as a workflow diagnostic unless and until a corrected, initially connected bed is simulated.
- Replace the current bed-scale figures and associated Results/Discussion text before submission.

## Corrective calculation requirements

A replacement bed calculation must satisfy all of the following before fracture statistics are interpreted:

1. Zero internal-bond loss during deposition or seating.
2. Template placement and wall positions based on the actual rotated template support.
3. A connected or demonstrably load-bearing mother-pebble contact network before damage.
4. Nonzero and approximately balanced top and bottom reactions during the pre-damage compression interval.
5. Low initial preload and no severe artificial subparticle overlap.
6. Native contact-force output or a separately validated reconstruction at selected pre-onset, onset and post-onset states.

## Corrective model now under test

A 500-subparticle surface-resolved template has been generated with 260 near-uniform shell subparticles and 240 random-core subparticles. Its directional diameter is approximately 0.994-0.999 mm over the central 90% of sampled directions, while retaining the nominal 1 mm mother-pebble diameter, subparticle radius and solid fraction.

The completed single-pebble test supports this candidate:

- first internal-bond loss at 0.0915 mm, compared with 0.0950 mm for the random-core reference;
- peak top load of 18.75 N, compared with 19.40 N for the reference;
- two dominant final fragments containing 220 and 213 subparticles, compared with 237 and 230 for the reference.

Thus the surface correction preserves the calibrated load scale and split-type morphology while substantially reducing directional support gaps. The comparison is recorded in `tables/jnm_surface_resolved_template_validation.csv`.

The preferred replacement workflow is physical locked-clump gravity settling followed by strength activation and bonded-template compression. Any simplified pre-seating method must be independently checked against the six acceptance criteria above.

## PB-007 correction progress

The rigid-clump route has now passed three geometry and initialization checks:

1. A 20-mother-pebble smoke test completed with stable rigid-body integration and recoverable center/quaternion output.
2. A 100-mother-pebble multilayer pilot produced 164 inter-pebble edges and 292 subparticle contacts. Ninety-nine of 100 mother pebbles belong to one connected component; the maximum subparticle overlap is approximately 1.04 micrometres.
3. The rigid-to-bonded coordinate transfer was corrected for the template insertion-frame offset. For the 100-pebble pilot, the transferred bonded coordinates reproduce the rigid settling dump with an RMS mismatch of approximately 1.6 nanometres, and the initial internal-bond count is exactly 493,500 = 100 x 4,935.

Native pair- and wall-contact output is now enabled from the first integration step. A short soft-contact pilot recovered 164 native mother-mother force edges and a graph connecting the top-loaded mothers to 26 bottom-contacting mothers. This establishes geometric and force-graph connectivity, but the short pilot did not run long enough to equilibrate the top and bottom reactions. A gravity-preserving, lower-damping equilibration run is in progress; reaction balance remains a mandatory acceptance criterion.

The gravity-preserving 10 micrometre seating pilot subsequently completed with all 493,500 internal bonds intact and zero bond loss. The final native graph retained 163 mother-mother force edges; 99 mothers were reachable from the top-loaded set, including 26 bottom-contacting mothers. However, the raw final top and bottom reactions were 1.074 and 0.353 mN, respectively. This run is retained as a protocol-development result because the raw top/bottom ratio does not distinguish self-weight carried by the bottom wall from the increment generated by top-wall compression.

The accepted PB-007 pre-damage gate is now the 5 micrometre in-run step-relaxed case `PB-007-bonded-steprelaxed-100-pilot-5um-steprelaxed`. The force-balance metric is gravity-baseline-corrected: the baseline is the last zero-top-force state before compression, and the acceptance residual compares the magnitude of the incremental six-wall vertical force with the top-wall load. At the final valid physical thermo row, the top-wall load is 1.713e-4 N and the incremental six-wall force is 1.704e-4 N, giving a residual of 0.542%. The intact-bond count remains 493,500 throughout the run, with zero broken bonds. Native local contacts at the final state give 165 mother-mother force edges and 298 inter-pebble subcontacts; 99 of 100 mother pebbles are reachable from the top-loaded set, including 26 bottom-contacting pebbles. This case passes the corrected pre-damage force-transmission gate and can be used as the validated starting protocol for the PB-007 fracture-sequence calculation.

The final `run 0` thermo line written to trigger local dumps reports `bond_int = 0` and approximately doubled wall-stress values; it is treated as a local-output artefact and is not used for scalar force-balance acceptance. The last row with `bond_int > 0` is used for the acceptance table, while final local dumps are used only for native network topology.

Additional zero-displacement stiffness-restoration checks were performed while keeping the top wall fixed. Direct restoration to 9.0e10 Pa lost 14 internal bonds before any compression displacement was applied. A short Young's-modulus screen found zero pre-damage at 5.0e8, 5.0e9 and 2.0e10 Pa, but 1 spurious lost bond at 3.0e10 Pa and 3 at 5.0e10 Pa. The validated soft-contact transfer state therefore cannot be promoted directly to the single-pebble contact modulus. The present highest screened zero-damage contact modulus is 2.0e10 Pa; a graded stiffness-restoration or overlap-reduction step is required before using higher stiffness in corrected fracture-event statistics.

A 2.0e10 Pa, 5 micrometre compression pilot retained all 493,500 internal bonds through the short loading sequence. This confirms that the screened stiffness can support a zero-pre-damage compression pilot. However, the run does not yet pass the force-balance gate: the high-stiffness contact network relaxes a large initial wall-force state during the short compression, so the gravity-baseline-corrected incremental wall-force residual is not physically interpretable as a quasi-static balance metric. This case is therefore a stiffness-screening result, not manuscript-ready bed mechanics.

The extended 2.0e10 Pa protocol `PB-007-bonded-steprelaxed-100-pilot-y2e10-10krelax-5um-pilot` improves this route substantially. It uses 10,000 pre-compression relaxation steps, keeps all 493,500 internal bonds intact, and gives a final 5 micrometre top-wall load of 1.084e-2 N. Relative to the explicit gravity baseline at step 10001, the final six-wall incremental force is 1.023e-2 N and the incremental balance residual is 5.595%. Native final-state output contains 25 mother-mother force edges; the top-loaded set reaches 21 mother pebbles and 2 bottom-contacting pebbles, so the native graph remains spanning but less densely loaded than the soft-contact validation case. This result is near the force-balance gate and confirms the feasibility of restored-stiffness validation, but it remains protocol-development evidence. A longer pre-relaxation and/or longer step hold is required before launching the corrected fracture-sequence run.

Subsequent protocol searches show that longer hold time alone is not the remedy. The 20,000-step pre-relaxation cases with 2,000-, 500- and 400-step holds all retained zero internal-bond damage, but final force-balance residuals increased to 1754%, 42.8% and 37.1%, respectively. The native force graph was also weakened or intermittently disconnected in the longest-hold case. A slower step-relaxed loading case retained zero damage and native spanning but still ended at 54.2% residual. A continuous-compression pilot identified and corrected a separate input-file issue: the earlier validation input hard-coded five loading blocks, so the requested `n_increments` value was ignored. The input now uses a `load_i` loop. The corrected continuous 5 micrometre pilot retained zero damage and a native spanning graph, but it still did not pass the restored-stiffness balance gate. These checks reinforce the decision to keep the restored-stiffness PB-007 path in protocol development. The next audit item is to reduce dynamic contact-network oscillation, most directly by damping or by a lower restored contact modulus, before any fracture-event sequence is interpreted.

The first restored-stiffness gate-passing candidate is obtained at 1.5e10 Pa. The case `PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-5um-pilot` uses the same 10,000-step pre-compression relaxation and five 1 micrometre step-relaxation increments, keeps all 493,500 internal bonds intact, and gives a final incremental balance residual of 4.799%. The final top-wall load is 1.638e-2 N and the gravity-baseline-corrected six-wall incremental force is 1.559e-2 N. Native final-state output contains 36 mother-mother force edges; the top-loaded set reaches 28 mother pebbles and 3 bottom-contacting pebbles, so the force graph is spanning. This passes the current zero-pre-damage, native-spanning and force-balance gates and is the preferred entry protocol for the next corrected fracture-sequence pilot. The result should remain framed as a gate-passing numerical protocol, not a fully calibrated breeder-material contact modulus.

The PB-007 compression input has now been upgraded for the corrected fracture-sequence stage. It can emit periodic local internal-bond dumps and periodic native pair/wall contact dumps during compression, controlled by `bond_dump_every` and `native_dump_every`, plus final bond, pair and wall local dumps. The companion parser `scripts/analyze_pb007_bond_event_sequence.py` reads the local dump timestep, maps subparticle bonds to mother pebbles and writes per-mother bond series and event tables with pebble height and rank-from-top metadata. A short dump-smoke run verified the output and parser but was deleted after testing because it is not a valid mechanics case.
