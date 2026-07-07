# CPM Literature Gap Map

Date: 2026-07-04

Purpose: record how the current Computational Particle Mechanics manuscript responds to the previous literature-context and novelty concern. This is an internal author-facing map; the manuscript text should remain concise.

| Literature class | Current references | What they provide | Remaining gap | Present evidence | Boundary |
| --- | --- | --- | --- | --- | --- |
| Single-particle crush and fragment-mode evidence | `PlateMaterialLi4SiO4; Zhao2013FailureInitiationLi4SiO4; Annabattula2014SizeDependentCrush; Bhartia2020ElasticResponse; Tavares2022SingleParticleBreakageReview` | Load scale, size dependence, failure-initiation context and single-particle fragment-mode targets. | Single-particle tests do not identify the first damaged parent particle inside a load-bearing random bed. | Fig. 2; Table 1; tables/single_pebble_model_calibration_matrix.csv; data/figure_source/fig2_single_pebble_*.csv | Sensitivity-bounded template representation, not a final Li4SiO4 material law. |
| Packed-bed compression and crushed-bed consequences | `ZaccariLoFrano2009CeramicPebbleBeds; PreliminaryLi4SiO4StructuralPerformance; CrushProbabilityPebbleBed2011; CrushedPebblePressureDrop2024; Fang2026Li4SiO4BedCrushing` | Bed stiffness, compaction, crush-probability, breakage-ratio, pressure-drop and packing-structure trends. | Bed-level responses do not resolve the chronological source of the first localized internal damage. | Fig. 4; Table 2; tables/pb007_macro_topology_event_metrics.csv; data/figure_source/fig4_fracture_sequence_pilot_events.csv | Finite 100-parent-particle event windows with two 200-parent-particle intact scale/strength endpoints. |
| DEM force-chain and load-path studies | `An2007DEMCeramicBreederBeds; GanKamlah2010DEMPebbleBeds; Wang2024ForceChainPebbleBed` | Coordination number, contact-force distribution and load-path evolution in particulate beds. | Force-chain descriptors are rarely linked to internal bond-loss increments of named parent particles. | Fig. 5; Table 3; tables/pb007_event_aligned_topology.csv; tables/pb007_mechanism_variable_separation.csv | State-space separation in the current finite windows, not a universal classifier. |
| Particle-replacement and crushable-bed DEM | `JimenezHerrera2018BreakageModels; Barrios2020ParticleBedBreakage; Zhou2020FragmentReplacementModes; Wang2021CrushableCeramicPebbleBed; CrushableDEMPebbleBed2026` | Efficient bed-scale particle replacement, fragment insertion and crushed-fraction effects. | Replacement routes usually begin after an overload criterion and do not preserve a pre-loaded internal bond graph for every parent particle. | Fig. 1; Fig. 3; Table 1; tables/pb007_*_acceptance_summary.csv | Workflow evidence for accepted windows and the completed 200-parent-particle intact scale/strength endpoints. |
| Bonded-particle fracture modelling | `PotyondyCundall2004` | A subparticle-bond representation that can resolve internal crack growth and fragment topology. | The single-object bonded-particle idea needs a bed insertion and event-extraction route for many parent particles. | Figs. 1, 4 and 6; Tables 2 and 4; tables/pb007_material_parameter_response.csv | Event chronology and material-response evidence in finite bed windows. |

## Manuscript action

- The Introduction now states the five literature classes directly.
- The stated gap is the chronological link between a load-bearing contact network and the first internal bond losses inside named parent particles.
- The discussion bounds the claim to finite event windows, material-response evidence and the completed 200-parent-particle intact scale/strength endpoints.
