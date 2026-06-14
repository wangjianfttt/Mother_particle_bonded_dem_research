# Nuclear Fusion submission integrity audit

Audit date: 2026-06-01 CST

## Checked files

| Item | Path | Status |
| --- | --- | --- |
| Compiled manuscript PDF | `manuscript/nuclear_fusion_iop_submission.pdf` | Present; 2022500 bytes after adding the ParaView-rendered single-pebble fragment morphology visualization. |
| LaTeX source | `manuscript/nuclear_fusion_iop_submission.tex` | Present; compiles with local XeLaTeX. |
| Reproducibility package zip | `submission_packages/nuclear_fusion_repro_package.zip` | Present; rebuilt after adding ParaView visualization assets and scripts. |
| Package checksum | `submission_packages/nuclear_fusion_repro_package.zip.sha256` | Present; `shasum -a 256 -c` passes. |
| Package manifest | `submission_packages/nuclear_fusion_repro_package/MANIFEST.csv` | Present; includes byte counts and SHA-256 checksums. |

## LaTeX audit

Command used:

```bash
cd manuscript && latexmk -xelatex -interaction=nonstopmode -halt-on-error nuclear_fusion_iop_submission.tex
```

Result:

- Build completed successfully after tightening the abstract, updating Data/Code Availability wording, inserting author metadata, reducing repeated software naming outside Methods, replacing visible internal case codes in the figures with reader-facing labels, moving figure-embedded tabular content into editable manuscript tables, strengthening ITER/CFETR-class solid-breeder blanket motivation, expanding unexplained figure abbreviations and adding a ParaView-rendered single-pebble fracture morphology visualization.
- No `undefined`, `LaTeX Error`, `Emergency stop`, `Fatal error` or `Overfull` strings were found in the final log scan.
- The abstract is 189 words in the LaTeX source and follows a Background/Methods/Results/Conclusions order.
- LaTeX captions no longer contain hand-written `Fig.` or `Extended Data Fig.` prefixes, so the compiled PDF uses only the automatic figure labels.
- Figure-label scan found no remaining `orth.`, `orient.`, `mult.`, `homog.`, `repl.` or `WB` abbreviations in the manuscript-facing Fig. 2, Fig. 3 and Fig. 6 SVGs; Fig. 2 caption defines the expanded label groups.
- The current PDF is a working Nuclear Fusion submission draft, pending only final repository and author-affiliation confirmations listed below.

## Checksum audit

Command used:

```bash
cd submission_packages && shasum -a 256 -c nuclear_fusion_repro_package.zip.sha256
```

Result:

- `submission_packages/nuclear_fusion_repro_package.zip: OK`

## Package hygiene audit

- Current reduced package contains 114 collected payload files plus `MANIFEST.csv`.
- No incomplete `partial` checkpoint tables are included.
- No `.tiff` production-backup figures are included in the reduced package; TIFF backups remain in the workspace and can be supplied if requested.
- Current zip size is about 4.64 MB.
- Figure SVG scan found no visible internal calibration or packing-seed labels in the manuscript figure set.
- Figure-script/SVG scan found no remaining `ax.table`, `cellText`, `colLabels`, `Stage summary` or `Event-sequence metrics` table panels in Fig. 5 or Fig. 6.
- The reduced package includes the editable stage-window source table (`tables/pb006_1000_bed_a_stage_summary.csv`) and the neutral Fig. 4 source file (`figures/pb006/pb006_force_path_proxy.pdf`).
- The reduced package includes the ParaView-rendered morphology PNG, the particle/bond VTP source files, the fragment summary table and the two scripts needed to regenerate the visualization.

## Enhancement audit

- Added a true x-normal slow-rate short endpoint check to 0.18 mm for the selected single-pebble template.
- Result: first break 0.10245 mm, 115 broken bonds at endpoint and final major fragments 247 + 246 subparticles.
- Interpretation: supports first-break and morphology robustness across 0.10, 0.05 and 0.03 m/s screening rates; does not support peak-load comparison because the run stops before the known peak-force region.

## Remaining blockers before real submission

1. ORCID ids if the authors want them included.
2. Confirmation of Qi-Gang Wu's affiliation; it is provisionally assigned to the Institute of Plasma Physics, Chinese Academy of Sciences.
3. Data repository DOI or URL for the reduced reproducibility package; the manuscript now contains an explicit `[repository DOI/URL to be added]` placeholder.
4. Optional final polish after inserting the repository link.
