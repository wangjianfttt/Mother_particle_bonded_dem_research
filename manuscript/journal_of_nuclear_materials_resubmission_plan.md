# Journal of Nuclear Materials resubmission plan

## Reason for transfer

Nuclear Fusion declined the manuscript because the subject was considered too specialised for its audience and recommended a more specialised nuclear materials journal. This is a scope-fit rejection rather than a technical rejection. The appropriate response is therefore to reposition the manuscript as a nuclear-materials paper on Li4SiO4 ceramic breeder-bed degradation.

## Target fit

Journal of Nuclear Materials publishes materials research for nuclear applications, including fusion reactor materials and blankets. The manuscript should emphasize:

- Li4SiO4 as a functional nuclear ceramic breeder material.
- Mechanical degradation of ceramic breeder pebbles and pebble beds.
- Mother-pebble-resolved fracture-event extraction as a materials diagnostic.
- Conservative interpretation: event-sequence evidence, not converged design probability.

The current Elsevier scope statement also requires a high degree of novelty and a substantial discussion that advances understanding. It excludes generic ceramic or reactor-design studies that do not address a nuclear-materials problem. The manuscript must therefore keep Li4SiO4 breeder degradation, fragment generation and purge-path consequences at the centre of every section, rather than presenting the work as a general granular-mechanics study.

## Changes already made

- Created `manuscript/journal_of_nuclear_materials_submission_draft.md`.
- Created `scripts/build_journal_of_nuclear_materials_latex.py`.
- Generated `manuscript/journal_of_nuclear_materials_submission.tex`.
- Generated `manuscript/journal_of_nuclear_materials_submission.pdf`.
- Reframed title, abstract, keywords and opening introduction toward nuclear materials.
- Added blue numbered citations through `natbib` and `hyperref`.
- Added literature citations to all main figure captions and supplementary/extended captions.
- Added a model-parameter table covering material properties, bond parameters, weak-plane settings, time steps and loading protocol.
- Created `manuscript/journal_of_nuclear_materials_cover_letter_draft.md`.
- Added a controlled 250/500/1000-subparticle sensitivity study. First-break displacement and two-major-fragment topology are robust, while peak load retains moderate resolution sensitivity.
- Added the 2026 Li4SiO4 cyclic-compression and pressure-drop experiment by Fang et al. (Fusion Engineering and Design 224, 115604) to connect the simulated event sequence with measured breakage and purge-flow consequences.
- Completed matched full 0.10/0.05/0.03 m s-1 single-pebble runs using identical template and plate geometry. First-break displacement and two-fragment topology remain stable, while peak load decreases by 10.5% from 0.10 to 0.03 m s-1.
- Moved the ParaView-rendered three-dimensional fracture morphology into a separate Supplementary Fig. S1 so that the main manuscript remains compact.
- Simplified the main event-summary table to seven reader-facing variables and rebuilt the compact two-column manuscript without overflow or unresolved citations.
- Withdrew the former PB-006 bed-scale force-chain and fracture-propagation interpretation after the native force-transmission audit.
- Rebuilt the bed-scale story around the corrected PB-007 route with explicit zero-pre-damage, native force-connectivity and gravity-baseline-corrected force-balance gates.
- Added the corrected 60 micrometre PB-007 pilot event sequence: five lost internal bonds, all localized in one upper-bed mother pebble.
- Added an independent corrected seed02 bed, plus 0.5x and 0.25x strength-window audits, all of which remain intact to 60 micrometres while preserving native force connectivity.
- Rebuilt Fig. 6 and `tables/pb007_macro_topology_event_metrics.csv` to show force-history, event-sequence and native-force topology differences without using internal case-code labels as the scientific message.
- Added `docs/jnm_submission_readiness_audit_20260612.md` as the current claim-evidence and submission-risk audit.
- Rebuilt the Journal of Nuclear Materials reproducibility package with checksum manifest.
- Added a separate Elsevier-style graphical abstract in `figures/main/journal_of_nuclear_materials_graphical_abstract.*` and an upload asset manifest in `manuscript/journal_of_nuclear_materials_submission_asset_manifest.csv`.
- Prepared `submission_packages/journal_of_nuclear_materials_flat_source.zip`, a flat LaTeX source bundle for Elsevier Editorial Manager, and verified that it compiles locally without unresolved citations or LaTeX errors.
- Removed reader-facing internal case labels such as PB-006, PB-007, SP-002 and CAL1 from the active JNM manuscript draft and regenerated the LaTeX/PDF/flat-source/main submission packages. The underlying filenames remain in the reproducibility package for traceability, but the article text now uses reader-facing terms such as corrected route, corrected pilot bed, independent corrected bed and weak-plane calibration candidate.
- Added `manuscript/journal_of_nuclear_materials_editorial_manager_upload_checklist.md` and `manuscript/journal_of_nuclear_materials_editorial_manager_upload_matrix.csv` to map the prepared files to likely Elsevier Editorial Manager upload roles, including manuscript, flat source, highlights, cover letter, graphical abstract, supplementary material, declarations and repository package.

## Remaining before real submission

- Reduced reproducibility package deposited at https://doi.org/10.5281/zenodo.20687351.
- Confirm the current Editorial Manager requirements for graphical abstract and supplementary-file item types at the time of submission.
- Upload the prepared Highlights file and the separate Supplementary Fig. S1 PDF.
- Decide whether to upload the current compact two-column PDF or convert to Elsevier `elsarticle` single-column review format.
- If LaTeX source files are requested, use the prepared flat source-file upload bundle because Elsevier's Editorial Manager may not process subfolder paths in source submissions.
- Confirm the declaration wording for any generative-AI-assisted manuscript preparation before final upload.
