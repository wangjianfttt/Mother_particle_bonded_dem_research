# JNM materials-novelty positioning matrix

Purpose: keep the Journal of Nuclear Materials submission framed as a nuclear-materials degradation paper rather than as a generic DEM workflow. This file is an author-side positioning audit; it should not be uploaded as a manuscript file unless an editor asks for additional context.

## Core editorial thesis

The manuscript uses bonded-template DEM as a diagnostic instrument for Li4SiO4 ceramic breeder-material degradation. Its central contribution is to make an otherwise hidden fracture chronology visible inside an opaque breeder bed: intact 1 mm mother-pebble templates are inserted without seating damage, invalid load paths are rejected before interpretation, and later bond loss is linked to native force-network and macroscopic-response changes.

## Positioning matrix

| Editorial question | Current manuscript answer | Evidence files | Boundary that protects the claim |
| --- | --- | --- | --- |
| What is the nuclear-materials object? | Li4SiO4 breeder pebbles in a solid breeder bed, where mechanical degradation can modify bed stiffness, thermal-contact constrictions and helium purge pathways. | `manuscript/journal_of_nuclear_materials_submission_draft.md`; `manuscript/journal_of_nuclear_materials_cover_letter_draft.md`; `docs/jnm_official_scope_alignment_audit_20260613.md` | The manuscript does not claim a coupled thermal-flow prediction or a reactor design calculation. |
| What is new beyond ordinary bed-compression DEM? | The workflow inserts bonded 500-subparticle mother-pebble templates intact into a random bed, proves zero pre-damage and native force transmission, and extracts mother-pebble-resolved fracture-event sequences. | Fig. 1; Fig. 4; `manuscript/journal_of_nuclear_materials_claim_evidence_boundary_matrix.csv`; `docs/jnm_final_scientific_traceability_audit_20260613.md` | The workflow is treated as a materials diagnostic, not as a universal DEM method or final design rule. |
| What material-degradation mechanism is supported? | In the corrected pilot, a top-near mother pebble loses five internal bonds in three event increments while the native force network remains spanning and reorganizes. The event order indicates local force-path sensitivity and mesoscale shielding/activation of ceramic microcracking. | Fig. 5; Fig. 6; `tables/pb007_event_aligned_topology.csv`; `tables/jnm_material_degradation_mechanism_indices.csv`; `docs/jnm_event_topology_mechanism_audit_20260613.md` | The evidence supports event-sequence and sensitivity interpretation, not a converged fracture probability. |
| Why can the independent intact bed strengthen rather than weaken the story? | The independent bed stays intact to 60 micrometres despite a spanning native force graph and 0.5x/0.25x strength-window audits, showing that displacement and strength multiplier alone do not determine the first event. | Fig. 6; independent-bed thermo, bond-series and native-force-network CSV files listed in the source-data matrix | The result is not interpreted as universal toughness or an absence of risk; it is local force-path sensitivity evidence. |
| Why is the paper appropriate for Journal of Nuclear Materials after the Nuclear Fusion scope decision? | The problem is specialized nuclear ceramic breeder-material degradation. The Nuclear Fusion decision is treated as a scope-fit signal, and the manuscript has been sharpened toward materials mechanisms, evidence boundaries and reproducibility. | `docs/jnm_transfer_positioning_audit_20260613.md`; cover letter; reviewer-risk prebuttal | The paper is not broadened into blanket lifetime prediction or thermal-hydraulic design. |

## Reviewer-facing one-paragraph argument

This work belongs in Journal of Nuclear Materials because it studies the mechanical degradation of Li4SiO4, a functional ceramic breeder material, and provides a mesoscopic diagnostic that experiments cannot directly supply: the time order, location and native force-network environment of the first mother-pebble fracture events inside a random bed. The numerical method is not presented as the result by itself; it is used to expose how a small amount of ceramic microcracking can occur within a still-spanning contact skeleton and how this local event relates to bed stiffness, contact topology and transport-relevant contact pathways. The claims remain bounded to a calibrated candidate template and corrected 100-mother-pebble event-sequence evidence.

## Do-not-cross boundaries

- Do not claim a final Li4SiO4 constitutive or fracture law.
- Do not claim converged bed-scale failure probability.
- Do not claim predictive lifetime, allowable blanket stress or design margin.
- Do not claim coupled heat-transfer or purge-flow results.
- Do not revive superseded large-bed diagnostic claims as active evidence.

## Current status

The local package is ready except for the external repository DOI/stable URL. The pre-DOI gate is expected to remain `BLOCKED_EXTERNAL`; this is a repository-deposit status, not a scientific-evidence failure.
