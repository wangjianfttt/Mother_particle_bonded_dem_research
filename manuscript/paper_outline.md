# Paper outline

## Working title

Bonded-sphere discrete-element modelling of lithium orthosilicate pebble crushing for fusion blanket pebble beds

## One-sentence argument

In ceramic breeder pebble beds for fusion blankets, we show that a bonded-sphere DEM workflow can connect calibrated single-pebble crushing to fragment-resolved bed-scale compression, supported by single-pebble force-displacement, bond-breakage and fragment statistics, with current evidence limited to the single-pebble validation stage.

## Target contribution

1. A reproducible LIGGGHTS-INL workflow for representing one Li4SiO4 pebble as more than 500 bonded subparticles.
2. A single-pebble compression protocol that outputs force-displacement, bond failure and fragment statistics.
3. A parameter-screening strategy for bond strength and loading-rate sensitivity.
4. A planned extension to inject calibrated crushable pebbles into a bed-scale compression model.

## Paper architecture

1. **Introduction**
   - Ceramic breeder pebble integrity affects tritium breeder blanket mechanical and flow performance.
   - Experiments provide single-pebble crush loads and bed-level responses, but cannot easily resolve internal breakage pathways.
   - Existing DEM approaches often treat breakage by probability, replacement or simplified crushable particles.
   - This work develops a bonded-subparticle route aimed at linking single-pebble calibration with bed-scale breakage evolution.

2. **Model construction**
   - Generate a 500-subparticle Li4SiO4 pebble template.
   - Use LIGGGHTS-INL cohesive bond model based on a parallel-bond concept.
   - Use mesh compression plates and thermo/bond-local outputs.

3. **Single-pebble validation workflow**
   - Check initial bond stability.
   - Establish rigid-plate compression.
   - Extract force-displacement and bond-count curves.
   - Derive graph-based fragment statistics from intact-bond networks.

4. **Parameter sensitivity**
   - Bond strength scan: 25, 50 and 100 MPa.
   - Loading-rate scan at 50 MPa: 1.0, 0.5, 0.25 and 0.1 m/s.
   - Current result: increasing bond strength increases peak force and reduces final bond breakage; lower loading speed stabilizes fragment count.

5. **Toward pebble-bed compression**
   - Inject calibrated pebble template into a packed bed.
   - Compress bed using rigid plates.
   - Track bed force-displacement, bond breakage, fragment count and packing evolution.

6. **Discussion**
   - What bonded subparticles add over empirical crush-probability models.
   - Numerical limitations: artificial loading rate, bond stiffness/strength calibration, fragment resolution and computational cost.
   - Experimental data needed for calibration.

7. **Methods**
   - Template generation.
   - LIGGGHTS-INL build and contact model.
   - Compression boundary conditions.
   - Post-processing scripts.

## Figure plan

| Figure | Content | Status |
| --- | --- | --- |
| Fig. 1 | Workflow schematic: bonded pebble generation, single-pebble compression, bed injection | To create |
| Fig. 2 | Single-pebble mesh-plate compression setup and bond network | Partly available from dumps |
| Fig. 3 | Bond strength scan force-displacement curves and summary | Available |
| Fig. 4 | Loading-rate sensitivity at 50 MPa | Available |
| Fig. 5 | Fragment evolution from intact-bond graph | Available as CSV; needs plot |
| Fig. 6 | Pebble-bed compression and breakage evolution | Pending |

## Immediate evidence gaps

1. Literature-extracted Li4SiO4 crush-load and elastic-slope data.
2. Bond stiffness calibration.
3. A quasi-static or step-relax loading protocol.
4. Bed-scale simulations using multiple calibrated crushable pebbles.
5. Visual snapshots of fragment evolution.
