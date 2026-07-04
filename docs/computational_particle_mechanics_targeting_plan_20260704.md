# Computational Particle Mechanics targeting plan, 2026-07-04

## Recommended next target

Recommended first target: **Computational Particle Mechanics**.

Reason: the repaired manuscript is now a particle-methods paper. Its strongest contribution is a bonded-template DEM workflow that resolves parent-particle fracture events, local bond-loss increments, native force-network state variables and bond-strength response in packed brittle particles. This matches a computational particle-mechanics audience better than journals that require a reactor-materials or broad powder-technology contribution.

Official pages checked:

- Computational Particle Mechanics journal page and aims/scope page: https://link.springer.com/journal/40571 and https://link.springer.com/journal/40571/aims-and-scope
- Current Computational Particle Mechanics journal page at ScienceDirect: https://www.sciencedirect.com/journal/computational-particle-mechanics
- Granular Matter journal page and aims/scope page: https://link.springer.com/journal/10035 and https://link.springer.com/journal/10035/aims-and-scope
- Powder Technology journal page: https://www.sciencedirect.com/journal/powder-technology
- Particuology journal page: https://www.sciencedirect.com/journal/particuology

Important submission-route update:

- The Springer page says the journal is closed for submissions on Springer as
  of 2025-07-01 and directs authors to the Elsevier/ScienceDirect journal page.
- The same page describes the journal focus as modeling and simulation of
  systems involving particle mechanics and methods, including particles as
  physical units in media and as numerical methods.
- Elsevier/ScienceDirect pages blocked command-line access with HTTP 403, so
  the final submission screen, article type and file-limit details should be
  checked manually in the browser.

## Why this target is better than the rejected targets

Nuclear Fusion rejected the paper because the work was too specialized for its fusion-audience focus. Journal of Nuclear Materials asked for stronger material-property dependence and reactor-relevant materials behavior. Advanced Powder Technology rejected the paper because the literature gap and scientific significance were not clear enough for its broad powder-technology audience.

The repaired manuscript now addresses the strongest technical weakness raised across these decisions:

- it adds an eleven-row material-response table;
- it includes a six-case bond-strength matrix across two cracking geometries;
- it introduces mechanism variables beyond top-wall displacement;
- it links localized fracture onset to final inter-particle force sum, native reachability and bonded strength;
- it keeps the Li4SiO4 application as a representative brittle ceramic pebble instead of the full scope anchor.

This makes the paper a stronger fit for a computational-particle-methods journal than for a nuclear-materials journal.

## Reader-facing framing for the next version

Use this central claim:

> The work provides a bonded-template DEM route for converting packed-bed compression into parent-particle fracture-event sequences with source-data-backed force-network state variables and bond-strength response.

Avoid leading with:

- fusion blanket design;
- Li4SiO4 material-law claims;
- journal-rejection history;
- internal case names;
- top-wall force-displacement curves as the main finding.

## Required target-specific edits

1. Cover letter: aim the contribution at computational particle mechanics, DEM breakage, parent-particle event sequencing and source-data-backed reproducibility.
2. Abstract: keep the current repaired abstract, with the opening framed around packed brittle particles and particle methods.
3. Introduction: ensure the first page emphasizes the unresolved numerical problem: inserting many intact bonded particles into a random load-bearing bed while retaining parent identity and internal fracture records.
4. Results: keep the new mechanism-variable and strength-matrix sections. These now answer the "data mining is shallow" criticism.
5. Discussion: keep the finite-window boundary. Do not claim converged fracture probability or final Li4SiO4 material law.
6. Data/code availability: keep the DOI and GitHub wording, and note that full raw dumps are kept outside the compact package because of file-size limits.

## Remaining risk before submission

- The finite-window dataset is still small. The manuscript should present this as mechanism-variable evidence, not as statistical fracture probability.
- Some coauthor e-mail fields are still marked as not provided in the author-details document.
- Elsevier target pages need manual browser checking if the fallback target changes to Powder Technology or Particuology.
- The final submission route is the Elsevier/ScienceDirect page, not the closed
  Springer submission route.
- If the Elsevier submission system requests source files, use the CPM upload
  package's LaTeX source zip together with the manuscript PDF.

## Current local package status

Current repaired package:

- `submission_packages/repaired_editorial_upload_ready`
- `submission_packages/repaired_editorial_upload_ready.zip`
- `submission_packages/repaired_submission_package`
- `submission_packages/repaired_submission_package.zip`

Target-specific CPM package to build:

- `submission_packages/computational_particle_mechanics_upload_ready`
- `submission_packages/computational_particle_mechanics_upload_ready.zip`

The CPM upload package includes both the manuscript PDF and a LaTeX source zip
so it can satisfy either PDF-first or source-file upload flows.
