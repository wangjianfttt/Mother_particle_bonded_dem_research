# JNM figure editorial-polish audit

Purpose: record a high-impact-journal figure audit for the active Journal of Nuclear Materials submission. This author-side note checks whether the figures read as a materials-degradation argument rather than as disconnected DEM diagnostics.

## Figure contract summary

Core visual conclusion: acceptance-gated bonded templates make the hidden chronology of Li4SiO4 breeder-pebble microcracking visible and link it to native load-path reorganization in a corrected random bed.

Figure archetype: asymmetric mixed-modality manuscript set. Fig. 1 and the graphical abstract establish the workflow and visual vocabulary; Figs. 2-4 validate the template and load-path gates; Figs. 5-6 carry the mechanism claim.

Target output: Journal of Nuclear Materials submission with editable PDF/vector figures, high-resolution PNG/TIFF previews, source-data tables and figure-generation scripts.

Backend: Python/matplotlib for the active quantitative and schematic figures.

Review-risk stance: no figure should imply a converged fracture probability, final Li4SiO4 material law, coupled thermal-flow result or blanket design-margin prediction.

## Figure-by-figure audit

| Display item | Visual role | Evidence logic | Export/source-data status | Reviewer risk and boundary |
| --- | --- | --- | --- | --- |
| Graphical abstract | Editorial hook | Shows intact bonded template, accepted load path and localized fracture chronology in one left-to-right mechanism. | PNG/PDF/SVG/TIFF available; graphical-abstract dimension gate passes. | Keep as a conceptual summary; do not treat it as quantitative evidence. |
| Fig. 1 workflow | Method vocabulary | Explains locked template insertion, zero seating damage, force-network gate and event database extraction. | PNG/PDF/SVG/TIFF available; included in manuscript and support package. | Workflow figure must not oversell predictive design capability. |
| Fig. 2 single-pebble calibration | Template plausibility | Shows load-window placement, weak-plane candidate and fragment-mode evidence. | PNG/PDF/SVG/TIFF plus calibration tables. | Caption states calibration candidate, not final Li4SiO4 law. |
| Fig. 3 resolution/rate sensitivity | Numerical boundary | Shows first-break onset and split topology are robust while peak load retains sensitivity. | PNG/PDF/SVG/TIFF plus resolution/rate tables. | Avoid convergence language for absolute peak force. |
| Fig. 4 acceptance gate | Validity gate | Shows zero pre-damage, native spanning force graph and gravity-baseline-corrected force balance before fracture interpretation. | PNG/PDF/SVG/TIFF plus acceptance/native summaries. | This is a protocol gate, not an elastic modulus measurement. |
| Fig. 5 fracture-event sequence | Main mechanism figure | Links three localized bond-loss increments to macro-response and native force-network reorganization in the corrected pilot. | PNG/PDF/SVG/TIFF plus bond-event, bond-series, native-network and event-aligned topology tables. | One pilot sequence; no error bars because it is not an ensemble statistic. |
| Fig. 6 corrected-case comparison | Robustness and boundary figure | Separates force connectivity from fracture onset by showing the independent bed and weakened-bond audits remain intact. | PNG/PDF/SVG/TIFF plus replicate-comparison and mechanism-index source data. | Supports local force-path sensitivity, not universal toughness. |
| Supplementary Fig. S1 | Morphology support | Shows actual split-type single-pebble morphology from particle/bond records. | PNG plus VTP particle/bond sources and summary table. | Visual support for morphology only; not a full fracture-statistics ensemble. |
| Supplementary Fig. S2 | Calibration overlay | Compares selected weak-plane traces and literature window. | PNG/PDF/SVG/TIFF plus overlay metric table. | Supports screening-level calibration, not final material law. |

## Visual QA observations

- The compiled 11-page PDF contact sheet shows the figures placed close to the related Results/Discussion text without obvious figure-text overlap.
- Fig. 5 uses a large macro-response chronology panel as the hero panel, with subordinate evidence panels for localized bond loss, native topology and damaged-pebble height rank.
- Fig. 6 uses the pilot versus independent-bed contrast as the hero comparison and keeps the endpoint fingerprint as a compact mechanism summary.
- The graphical abstract is visually aligned with the manuscript claim: one hidden ceramic-breeder damage event becomes an auditable bond-loss and force-network history.
- Reader-facing figure captions avoid internal case labels and point to source data or evidence tables.

## Remaining author-side checks

- Inspect the final Editorial Manager-generated PDF proof after upload, because journal-side PDF conversion can change figure placement.
- Confirm that the graphical abstract is uploaded as a separate graphical-abstract file rather than embedded as a main figure.
- Keep old diagnostic PB/SP/CAL-labelled plots out of reader-facing upload files; they may remain only as local provenance or reproducibility-package internals.
