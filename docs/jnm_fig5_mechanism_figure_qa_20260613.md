# JNM Fig. 5 mechanism-figure QA

## Figure contract

- Core conclusion: localized internal bond loss is embedded in a spanning but reorganizing native force network and coincides with macroscopic load-path relaxation.
- Figure archetype: asymmetric mixed-modality figure, with a macro-response hero panel and three quieter evidence panels.
- Backend: Python/matplotlib, matching the existing manuscript figure toolchain.
- Source data: corrected pilot thermo history, breakage-event table, bond-series table and native force-network series.
- Export contract: PNG preview plus PDF, SVG and TIFF manuscript exports from `scripts/plot_pb007_corrected_fracture_sequence.py`.

## Revision made

The previous Fig. 5 showed the correct evidence but read like four equally weighted diagnostics. The revised figure gives the top-wall force chronology the hero role, removes the raw noisy force trace, uses a light fill to emphasize the macro-response envelope, keeps E1-E3 event markers, and moves the supporting evidence into quieter lower panels.

The damage-localization panel now plots only the three event windows instead of all repeated post-event dump states. This avoids over-counting the visual evidence and makes the localized event sequence easier to read at the printed manuscript size.

## Evidence checks

- Event windows remain 25, 35 and 60 micrometres.
- Localized internal-bond increments remain +2, +2 and +1.
- All localized damage remains assigned to mother pebble 78, rank 2 from the bed top.
- Native force-network panel retains the measured inter-mother edge, top-reachability and reachable-bottom series.
- The peak-to-endpoint relaxation annotation remains 46.4%, computed from the processed thermo-derived macro response.

## Visual QA

- The regenerated manuscript PDF remains 10 pages.
- `scripts/check_jnm_figure_text_labels.py` passes after the redraw.
- `scripts/check_jnm_pdf_visual_qa.py` passes after rendering the rebuilt PDF pages.
- The Fig. 5 page in the rendered PDF contact sheet shows no obvious label clipping, duplicated caption or panel overlap.

## Claim boundary

The revised figure strengthens the event-sequence mechanism narrative but does not change the scientific boundary: the corrected pilot is event-sequence evidence, not a converged fracture-probability statistic or a coupled thermal-flow prediction.
