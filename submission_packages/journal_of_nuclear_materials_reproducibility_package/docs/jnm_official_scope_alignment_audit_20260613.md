# JNM official-scope alignment audit, 2026-06-13

## Official sources checked

Journal page:

- Elsevier Shop, Journal of Nuclear Materials, ISSN 0022-3115: `https://shop.elsevier.com/journals/journal-of-nuclear-materials/0022-3115`
- Live re-check on 2026-06-13: the page still frames JNM as materials research for nuclear applications, including fission and fusion reactors, and explicitly welcomes computational studies when they advance nuclear-materials understanding.

Elsevier graphical abstract guidance:

- Elsevier author resources, graphical abstracts: `https://www.elsevier.com/researcher/author/tools-and-resources/graphical-abstract`

Elsevier Highlights guidance:

- Elsevier author resources, Highlights: `https://www.elsevier.com/researcher/author/tools-and-resources/highlights`
- Live re-check on 2026-06-13: Highlights should be 3-5 short bullet points, each no more than 85 characters, and should communicate novel results or methods in searchable reader-facing language.

Elsevier LaTeX and Editorial Manager guidance:

- Elsevier author policies and guidelines, LaTeX instructions: `https://www.elsevier.com/researcher/author/policies-and-guidelines/latex-instructions`
- Live re-check on 2026-06-13: the submission should use the Elsevier article class/frontmatter when source files are needed, bundle all source files in a single archive, keep the LaTeX files at one folder level for Editorial Manager processing, and avoid uploading LaTeX source as supplementary material.

## 2026-06-13 official re-check matrix

| Official requirement or boundary | Current manuscript/package response | Local evidence |
| --- | --- | --- |
| JNM publishes nuclear-materials research, including fusion-reactor materials and blankets. | The title, abstract, introduction and discussion frame the object as Li4SiO4 ceramic breeder pebbles in a solid breeder blanket. | `manuscript/journal_of_nuclear_materials_submission_draft.md`; `manuscript/journal_of_nuclear_materials_submission.tex` |
| JNM welcomes computational work only when it advances materials understanding and is not incremental. | The contribution is presented as a material-degradation diagnostic: zero-pre-damage template insertion, acceptance-gated load paths, mother-pebble fracture-event histories and native force-network topology. | `docs/jnm_materials_novelty_positioning_matrix_20260613.md`; `docs/jnm_scientific_storyline_audit_20260613.md` |
| JNM excludes reactor design/technology, thermal hydraulics/fluid properties and general non-nuclear ceramic studies. | The manuscript explicitly avoids claiming blanket design rules, helium-flow solutions, thermal-hydraulic modelling or general ceramic DEM conclusions. | `scripts/check_jnm_official_scope_alignment.py`; `scripts/check_jnm_reader_facing_hygiene.py` |
| Highlights should contain 3-5 short reader-facing bullets within the Elsevier length limit. | The active Highlights file contains five bullets and is checked against the 85-character limit. | `manuscript/journal_of_nuclear_materials_highlights.md`; `scripts/check_jnm_highlights.py` via final gate |
| Graphical abstract should be uploaded as a separate visual file. | The graphical abstract is provided separately in PNG/TIFF/PDF-style submission assets and is not treated as an in-text figure. | `figures/main/journal_of_nuclear_materials_graphical_abstract.png`; `submission_packages/jnm_editorial_manager_upload_ready/05_graphical_abstract_tiff.tiff` |
| LaTeX source should be bundled for Editorial Manager rather than uploaded as supplementary material. | The package contains an `elsarticle`/`frontmatter` source, bundled bibliography style and a flat source archive with an upload matrix item type of LaTeX source files. | `submission_packages/journal_of_nuclear_materials_flat_source.zip`; `manuscript/journal_of_nuclear_materials_editorial_manager_upload_matrix.csv`; `scripts/check_jnm_elsevier_upload_compliance.py` |
| Public data/code availability needs a stable repository record. | The reduced reproducibility package is frozen for repository deposition, but DOI/stable URL insertion remains the only external blocker. | `submission_packages/jnm_repository_deposit_FROZEN_20260614_ffa2c5d8`; `docs/jnm_final_submission_gate_report.md` |

## Scope implications for this manuscript

The official Journal of Nuclear Materials description says that the journal publishes materials research for nuclear applications, including fission reactors, fusion reactors and similar environments, and welcomes experimental, theoretical and computational studies. It also states that submitted papers should have high novelty and a substantial discussion that interprets results and advances understanding, rather than incremental work.

The same official page marks several neighbouring areas as out of scope when they do not address a nuclear-materials problem, including reactor design and technology, thermal hydraulics or fluid properties, particle transport or shielding, and general ceramic studies. This exclusion boundary is directly relevant after the Nuclear Fusion desk rejection: the manuscript must read as nuclear ceramic breeder-material degradation, not as blanket design, thermal hydraulics or generic granular/ceramic simulation.

This manuscript is aligned with that scope because it treats Li4SiO4 breeder pebbles as functional ceramic nuclear materials in a solid breeder blanket, not as a generic granular assembly. The manuscript emphasizes mechanical degradation, local force-path evolution, mother-pebble fracture-event sequences, native force-network topology and purge-path/thermal-contact implications for ceramic breeder-bed integrity.

The manuscript deliberately avoids presenting the work as reactor design, thermal hydraulics, particle transport or generic ceramic DEM. Its stated contribution is a materials-degradation diagnostic for ceramic breeder beds, with explicit limitations against quantitative blanket design margins until larger ensembles and thermomechanical coupling are available.

For this reason, transport-relevant terms such as purge pathways and thermal contacts are used only as materials-service implications of force-network and fracture evolution. The manuscript does not claim to solve helium flow, thermal hydraulics, isotope transport or blanket design.

## Novelty and non-incremental framing

The manuscript's novelty is framed around three connected elements:

1. Zero-pre-damage bonded-template insertion of 500-subparticle mother pebbles into a random bed.
2. Acceptance gates that reject invalid load-path cases before fracture is interpreted.
3. Mother-pebble-resolved fracture-event and native force-network histories that connect localized damage to bed-scale topology and macroscopic response.

This framing is stronger for Journal of Nuclear Materials than a narrower claim that the study simply performs a DEM compression simulation.

## Discussion-strength check

The current discussion links the corrected numerical evidence to ceramic breeder-bed degradation mechanisms:

- localized top-near microcracking,
- spanning force connectivity without deterministic fracture onset,
- force-network densification and redistribution,
- limits of displacement-only and strength-multiplier threshold interpretations,
- need for larger stochastic ensembles, lower-rate/cyclic loading, temperature dependence, thermal-contact coupling and purge-flow metrics before design-margin claims.

This meets the intended direction of a significant discussion section, while preserving conservative boundaries.

## Graphical abstract alignment

The graphical abstract is provided as a separate file in PNG/PDF/TIFF forms. It uses a left-to-right visual flow, labels only manuscript-supported evidence, and avoids presenting itself as an in-article figure replacement. It should remain separate in Editorial Manager.

## Remaining author-side checks

Before final submission, the corresponding author should still verify:

- target article type selected in Editorial Manager,
- graphical abstract upload slot and preferred file selected,
- final data DOI/stable URL inserted,
- author approval and declaration checklist completed,
- repository metadata license and ORCID choices confirmed.
