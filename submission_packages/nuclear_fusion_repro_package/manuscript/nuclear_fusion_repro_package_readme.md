# Reduced reproducibility package for Nuclear Fusion submission

This package contains the reduced data, scripts, simulation inputs and figure assets needed to audit the manuscript:

`Mother-pebble-resolved fracture sequences in random Li4SiO4 breeder beds for fusion blankets by bonded-particle DEM`

## Contents

- `manuscript/`: Nuclear Fusion manuscript draft, cover letter draft, captions, references and package plans.
- `figures/`: preferred PDF figure files for the main manuscript figures. TIFF production backups are retained locally and can be supplied if requested.
- `tables/`: single-pebble calibration tables, PB-006 event summary tables, packing descriptors, overlap-proxy diagnostics and reference audit.
- `data/processed/`: reduced event, per-pebble, height-bin and thermo CSV files used for the reported 500- and 1000-pebble analyses.
- `scripts/`: Python and shell scripts used for template generation, run control, event extraction, summary-table construction and plotting.
- `simulations/pebble_bed/PB-006/`: selected LIGGGHTS-INL input files and proxy/template metadata needed to document the locked-template workflow.
- `MANIFEST.csv`: file list and byte counts for this package.

The manifest includes SHA-256 checksums when the package is built with:

```bash
python3 scripts/build_nuclear_fusion_repro_package.py --checksums
```

The current upload/staging archive is `submission_packages/nuclear_fusion_repro_package.zip`, with a top-level checksum in `submission_packages/nuclear_fusion_repro_package.zip.sha256`.

## Scope

This is a reduced package for peer review and public archiving. It excludes raw restart files, full local-bond dump histories, incomplete partial checkpoint tables and TIFF figure backups because those files are large or redundant for reproducing the processed CSV tables and manuscript figures. Large raw files and production-format backups should be retained separately and provided on reasonable request.

## Claim boundaries

The package supports a computational workflow and event-sequence paper. SP-002-CAL1 is a current calibration candidate, not a final Li4SiO4 material law. The 1000-pebble runs provide event-sequence evidence, not converged bed-scale probability statistics.
