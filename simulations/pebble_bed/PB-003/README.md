# PB-003 staged compact bed

PB-003 changes the bed-initialization logic.

The pebbles are first created with a centre spacing of 1.35 mm, large enough to prevent cross-pebble cohesive bonds during the one-step bond-creation stage. Each 500-subparticle pebble is assigned to an atom-id group. After the internal bonds are created, the groups are translated into a compact 2 x 2 x 3 bed. The current diagnostic target centre spacing is 1.00 mm. This allows inter-pebble contacts in the compact bed while preserving only internal cohesive bonds.

The case is a diagnostic bridge between PB-002 and a production bed. It should be accepted only if:

- initial intact bonds equal `12 x 6723 = 80676`;
- no additional bonds are created after the first step;
- top and bottom wall forces both become non-zero during compression;
- bed particles move and rearrange rather than only local top-layer crushing.

## Diagnostic results

The `PB-003-staged-target1000` diagnostic used 1.00 mm target spacing, 1000 relaxation steps and 0.10 mm fast top displacement.

- inferred initial internal bonds: `80676 = 12 x 6723`;
- observed intact bonds after compact-bed relocation and relaxation: 80536;
- relocation/preload breakage before compression: about 140 bonds;
- top plate first reached the bed at about 0.075-0.080 mm displacement;
- peak top force at 0.10 mm displacement: 26.16 N;
- peak bottom preload force: 2.40 N, then relaxed to 0.37 N by the final step;
- final intact bonds: 80324.

Conclusion: the staged create-then-translate workflow solves the cross-pebble bond problem and gives non-zero top and bottom wall reactions. The remaining initialization issue is the early internal bond loss caused by compact-bed relocation and bottom preload. The next revision should use slightly larger target spacing, a smaller bottom preload and a longer low-speed relaxation stage before production compression.

The `PB-003-staged-target1020-supported` diagnostic used 1.02 mm target spacing, bottom plate `z = -1.506 mm`, 1000 relaxation steps and 0.12 mm fast top displacement.

- expected and observed pre-compression internal bonds: `80676 = 12 x 6723`;
- relocation/preload breakage before compression: 0 bonds;
- peak bottom force during support/relaxation: 6.42 N;
- first compression-stage bond breakage: about 0.100 mm top displacement;
- peak top force at 0.12 mm displacement: 26.15 N;
- final intact bonds: 80464;
- total broken bonds by 0.12 mm displacement: 212.
- final intact-bond graph: 24 connected components, consisting of the original 12 main pebble-scale components plus 12 single-subparticle fragments.

Conclusion: the 1.02 mm supported setup is the current baseline for bed-scale production work. It preserves the bonded-pebble templates before compression, prevents new cross-pebble cohesive bonds, and gives both support reaction and compression-induced bond failure.
