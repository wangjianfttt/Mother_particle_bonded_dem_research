# Journal of Nuclear Materials Editorial Manager paste fields

Generated from the active manuscript, highlights, declaration and author-metadata files.
The corresponding author should paste these fields into Editorial Manager after final repository deposit.

## Title

Acceptance-gated bonded-template DEM reveals localized fracture sequences in Li4SiO4 ceramic breeder beds

## Article type

Research article

## Authors

Jian Wang*, Siyu Wang, Hang Zhang, Ming-Zhun Lei, Wei Wen, Qi-Gang Wu, Gang Shen, Haishun Deng

## Corresponding author

wjfttt@mail.ustc.edu.cn

## Affiliations

1. Anhui University of Science and Technology, Huainan, Anhui 232001, China
2. Institute of Plasma Physics, Chinese Academy of Sciences, Hefei, Anhui 230031, China

## Author-affiliation metadata

- Jian Wang: affiliation ids 1;2; Anhui University of Science and Technology; Institute of Plasma Physics, Chinese Academy of Sciences; email: wjfttt@mail.ustc.edu.cn (corresponding author)
- Siyu Wang: affiliation ids 1; Anhui University of Science and Technology
- Hang Zhang: affiliation ids 1; Anhui University of Science and Technology
- Ming-Zhun Lei: affiliation ids 2; Institute of Plasma Physics, Chinese Academy of Sciences
- Wei Wen: affiliation ids 1;2; Anhui University of Science and Technology; Institute of Plasma Physics, Chinese Academy of Sciences
- Qi-Gang Wu: affiliation ids 2; Institute of Plasma Physics, Chinese Academy of Sciences
- Gang Shen: affiliation ids 1; Anhui University of Science and Technology
- Haishun Deng: affiliation ids 1; Anhui University of Science and Technology

## Abstract

Lithium orthosilicate pebbles are functional ceramic breeder materials whose mechanical degradation
can alter bed stiffness, contact topology and purge-gas pathways in solid breeder blankets. Existing
single-pebble and bed-compression studies provide crush-load and bulk-response information, but they
do not resolve the hidden time order of mother-pebble fracture inside an opaque random bed. Here we
develop a bonded-template discrete-element workflow in which each nominal 1.0 mm Li4SiO4 mother
pebble is represented by 500 bonded subparticles, inserted intact into a gravity-settled bed and
allowed to break only during subsequent compression. A weak-plane template reproduces the target
crush-load scale and split-type morphology as a current calibration candidate; resolution and
loading-rate checks preserve first-break displacement and fragment topology while bounding peak-load
sensitivity. The corrected 100-mother-pebble bed route passes zero-pre-damage, native force graph
connectivity and gravity-baseline-corrected force-balance gates before fracture is interpreted.
Three corrected 60 micrometre bed compressions show distinct event paths: a pilot loses five of
493,500 internal bonds in one upper-bed mother pebble, a second random bed remains intact even under
0.5x and 0.25x strength audits, and a third random bed develops delayed microcracking after 50
micrometres with ten final broken bonds in two upper-bed mother pebbles. The output is a set of
material-degradation state variables: event time, damaged mother-pebble identity, bond-loss
increment, native force graph connectivity and macroscopic force relaxation. The workflow converts
crushable breeder-bed simulations into auditable fracture-event sequences for nuclear-materials
assessment, while larger ensembles remain required before predictive lifetime or design-margin
statements are made.

## Keywords

lithium orthosilicate; ceramic breeder material; pebble bed; bonded-particle DEM; pebble crushing; fracture-event sequence; nuclear materials

## Highlights

- Li4SiO4 breeder pebbles are resolved as intact bonded mother templates.
- Acceptance gates reject pre-damaged or non-transmitting bed states.
- Single-pebble onset and split topology survive resolution/rate checks.
- Upper-bed microcracking localizes within a still-spanning force graph.
- Independent-bed audits show local force-path sensitivity of first damage.

## Data availability statement

The processed event tables, native force-network summaries, event-aligned topology table,
macro-topology-event metrics, figure source data, manuscript figures and post-processing scripts
supporting this study have been assembled in a reduced reproducibility package with a checksum
manifest. The package includes the corrected pilot, the intact independent corrected bed, the
delayed-cracking third corrected bed and the 0.5x/0.25x strength-audit thermo histories,
mother-pebble bond-series tables, breakage-event tables, native force-network series, Fig. 6 source
data and the scripts used to regenerate the replicate-comparison figure, event-aligned topology
table and mechanism-metric table. For submission, this package should be deposited in a persistent
repository such as Zenodo, Figshare or an institutional repository, and the final DOI or stable URL
should be inserted here before upload: [repository DOI/URL to be added]. Very large raw restart
files and full local-bond dump histories are retained as local case archives and can be provided as
larger audit bundles on reasonable request, subject to repository file-size limits and institutional
storage constraints.

## Code availability statement

The template-generation, run-control, figure-generation and post-processing scripts are included in
the reduced reproducibility package under `scripts/`, with representative DEM input files under
`simulations/`. The deposited package is intended to reproduce the manuscript-level processed data
audits, figures and evidence matrices from the included CSV tables and representative inputs; it
does not redistribute the local DEM executable, very large restart files or full raw local-bond dump
histories. The simulation environment used for the reported calculations is stated in the Methods
Summary, and the package manifest provides SHA256 checksums for the deposited scripts, inputs,
processed data and figures.

## Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships
that could have appeared to influence the work reported in this paper.

## Funding declaration

This work was supported by the Anhui Provincial Natural Science Foundation (2408085QA030), the
Science Foundation of the Institute of Plasma Physics, Chinese Academy of Sciences (DSJJ-2025-08),
the Anhui Intelligent Mine Technology and Equipment Engineering Research Center (AIMTEERC202307),
the China Post-doctoral Science Foundation under Grant Number 2024M753266, the Excellent Research
and Innovation Team of Anhui Province, China (2022AH010052), the Scientific Research Foundation for
High-level Talents of Anhui University of Science and Technology, China (2021yjrc51), and the
Collaborative Innovation Program of Hefei Science Center, CAS, China (2019HSC-CIP006).

## Role of the funding source

The funding sources had no role in the design of the computational study, the collection, analysis
or interpretation of the simulation data, the writing of the manuscript, or the decision to submit
the article for publication.

## Declaration of generative AI and AI-assisted technologies in the writing process

During the preparation of this work, the authors used OpenAI's ChatGPT/Codex tools to assist with
manuscript organization, language editing, code review, figure-generation scripting and
submission-package preparation. After using these tools, the authors reviewed, edited and verified
the manuscript text, code, figures and data products as needed, and take full responsibility for the
content of the publication.  Note for the corresponding author: edit or remove this statement
according to the actual tools used and the current Elsevier submission-form requirement. Do not list
an AI tool as an author.

## CRediT authorship contribution statement

Jian Wang: Validation; Supervision; Project administration; Methodology; Investigation; Conceptualization. Siyu Wang: Writing - original draft; Formal analysis; Data curation; Visualization. Hang Zhang: Writing - original draft; Formal analysis; Data curation; Visualization. Ming-Zhun Lei: Writing - review and editing; Validation; Project administration; Formal analysis. Wei Wen: Writing - review and editing; Supervision; Project administration; Methodology; Conceptualization. Qi-Gang Wu: Validation; Resources; Data curation. Gang Shen: Writing - review and editing; Supervision; Project administration. Haishun Deng: Supervision; Project administration.

## Repository DOI action

Repository DOI or stable URL is still pending. Deposit the reduced reproducibility package first, then run `python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --apply --rebuild` before final upload.
