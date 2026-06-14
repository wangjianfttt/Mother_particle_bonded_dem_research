# Nuclear Fusion reviewer-risk prebuttal

Working scope: this document anticipates likely reviewer concerns for the current Nuclear Fusion manuscript and keeps the response strategy aligned with the present evidence. It is not a rebuttal letter and should not be copied verbatim into responses without updating run status, repository links and author metadata.

Core conservative boundaries:

- SP-002-CAL1 is the current calibration candidate, not a final Li4SiO4 material law.
- The 1000-pebble cases provide event-sequence evidence for onset and post-onset variability, not converged bed-scale probability statistics.
- The force-path interpretation is based on packing descriptors and overlap-derived proxies, not native contact-force-chain output.
- The bed loading protocol is a screening/restartable numerical protocol, not a fully quasi-static compression validation.

## 1. Is the single-pebble model sufficiently validated against Li4SiO4 experiments?

Likely reviewer concern: The paper may appear to claim a calibrated material model from limited single-pebble evidence.

Current evidence:

- SP-002-CAL1 reaches a peak top force of 18.64 N and bottom force of 18.07 N, consistent with the provisional 1 mm crush-load scale.
- The final intact-bond graph gives two major fragments of 227 and 224 subparticles plus small chips, avoiding the surface-chipping mode of homogeneous templates.
- A true x-normal 0.05 m s-1 rerun preserves first-break displacement at 0.1025 mm and split morphology, while peak force increases to 21.64 N.
- Orientation and strength-multiplier pilot cases show peak-load scatter while retaining the two-major-fragment mode.

Response strategy:

- State that SP-002-CAL1 is a current calibration candidate used to test a fracture-resolved bed workflow.
- Emphasize that the manuscript does not claim a final Li4SiO4 material law, Weibull strength distribution or predictive crush-probability model.
- Point reviewers to Fig. 2 and Extended Data Fig. 1 as calibration-screening evidence, not final validation.

Need new calculation?

- Not required for the present workflow paper if wording remains conservative.
- Helpful if requested: a slower x-normal or hold-relax single-pebble check, plus a larger orientation/strength ensemble.

## 2. Is the 500-subparticle pebble resolution converged?

Likely reviewer concern: The bonded template may be too coarse to represent crack paths or fragment statistics.

Current evidence:

- The 500-subparticle template is stable, has a reproducible internal bond network and produces interpretable intact-bond fragment graphs.
- The workflow tracks mother-pebble events consistently in 500- and 1000-pebble beds.
- No subparticle-count sensitivity is currently reported.

Response strategy:

- Present the 500-subparticle representation as a computationally tractable template for event sequencing in large beds.
- Avoid language implying microcrack-level convergence.
- Explain that the study targets mother-pebble-resolved event order and localization, whereas subparticle-resolution convergence is a next-stage material-model task.

Need new calculation?

- Not mandatory for a method/event-sequence submission.
- Strongly useful for a major revision: one higher-resolution single-pebble comparison, even if limited to calibration and fragment morphology.

## 3. Does the locked-template insertion truly avoid deposition-induced damage and artificial bonds?

Likely reviewer concern: Random bed preparation could pre-damage pebbles or create unphysical cross-pebble cohesive bonds.

Current evidence:

- The 500-pebble initialization contains 250000 subparticles and exactly 2938000 intact internal bonds, matching 500 times the 5876-bond template.
- The 1000-pebble initialization contains 500000 subparticles and exactly 5876000 intact internal bonds.
- Both initialization checks show zero broken internal bonds before compression.
- The method creates templates far apart, forms internal bonds only, then translates intact mother-pebble groups into settled proxy-sphere centres.

Response strategy:

- Treat this as one of the strongest manuscript claims.
- Make clear that proxy settling and bonded-template insertion are separated precisely to avoid deposition-induced internal fracture.
- Refer to Fig. 1 and the Methods bond-count checks.

Need new calculation?

- No. Existing exact bond-count checks are sufficient unless a reviewer asks for archived raw local-bond evidence.

## 4. Are the 500-pebble results statistically meaningful with only three random seeds?

Likely reviewer concern: Three seeds are not enough for probability distributions or confidence intervals.

Current evidence:

- Three independent 500-pebble beds all first break at 0.0725 mm in mother pebble 500.
- Later damage varies strongly: 246-559 localized broken bonds and 4-7 damaged mother pebbles by 0.20 mm.
- Damage remains confined to the upper height bins.

Response strategy:

- Claim reproducible onset across the tested 500-pebble seeds, not a converged probability distribution.
- Use the seed-dependent post-onset spread as a result rather than hiding it: it supports the manuscript's distinction between robust trigger and packing-sensitive growth.
- Avoid reporting means and standard deviations as if they were population estimates.

Need new calculation?

- Not essential for the current claim boundary.
- Useful for strengthening revision: two or more additional 500-pebble seeds, or a formal sampling plan for onset displacement and damaged-pebble count.

## 5. Do the 1000-pebble runs prove scale convergence or bed-scale fracture probability?

Likely reviewer concern: The manuscript may overinterpret three 1000-pebble cases.

Current evidence:

- 1000-pebble seed01, orient02 and seed02 all preserve a top-layer first-break trigger in or near mother pebble 1000.
- Post-onset growth varies: seed01 gives 98 broken bonds over three damaged pebbles, orient02 gives 95 broken bonds in one pebble and becomes quiet after 0.1200 mm, and seed02 gives 316 broken bonds over five top-bin pebbles.
- The endpoint is 0.15 mm, not the 0.20 mm endpoint used for the 500-pebble production set.

Response strategy:

- State explicitly that these 1000-pebble cases are event-sequence evidence and scalability checks, not convergence probability statistics.
- Avoid direct 500- versus 1000-pebble strength scaling because endpoints and output strategies differ.
- Emphasize that the 1000-pebble results support robust top-layer onset and variable post-onset propagation under larger-system initialization.

Need new calculation?

- Not required if the manuscript remains an event-sequence paper.
- Likely needed if reviewers demand probability claims: additional independent 1000-pebble packings to 0.15-0.20 mm.

## 6. Is the loading rate quasi-static enough?

Likely reviewer concern: Bed compression at 0.5 m s-1 and single-pebble screening speeds may introduce dynamic artifacts.

Current evidence:

- Single-pebble slower x-normal evidence preserves first-break displacement and split morphology, but peak force changes from 18.64 N to 21.64 N.
- Bed-scale calculations are framed as screening/restartable numerical loading.
- No full hold-relax or inertial-number analysis is currently reported for the bed cases.

Response strategy:

- Avoid "quasi-static" as a strong claim for the current bed calculations.
- Phrase results as compression-driven event sequences under the stated numerical protocol.
- Use the robustness of onset location and event assignment as the main evidence, not absolute force-displacement prediction.

Need new calculation?

- Recommended if revision time allows: a slower or hold-relax check for one 500-pebble bed and one single-pebble template.
- Not strictly required for initial submission if the rate limitation is acknowledged.

## 7. Are the force-path conclusions supported without native contact-force output?

Likely reviewer concern: Overlap-derived force proxies may not be acceptable as force-chain evidence.

Current evidence:

- Seed03 has lower bed height, larger top-bin population and higher top-bin geometric degree than seed01 and seed02.
- Overlap-derived Hertz-type proxies show a broader top-wall-loaded region and more inter-pebble proxy edges in seed03 than seed02.
- The proxy-loaded pebbles match lateral breakage spreading at selected displacements.
- Native contact-force-chain output is not yet used for the reported mechanism.

Response strategy:

- Keep the language to "consistent with load-path broadening" and "overlap-derived force-path proxy."
- Do not call the proxy a measured force chain.
- Present the proxy analysis as diagnostic support for the seed03 cascade, not a standalone proof.

Need new calculation?

- Not required for the current conservative mechanism.
- Strong revision upgrade: rerun or restart selected seed02/seed03 windows with native contact-local force output.

## 8. Is the damage localized only because the top plate contacts the highest pebble first?

Likely reviewer concern: The reported robust top-layer onset may be a trivial geometric artifact.

Current evidence:

- In all three 500-pebble seeds, first break occurs in the highest mother pebble at 0.0725 mm.
- In 1000-pebble cases, first break also occurs in or near the top-layer highest mother pebble, with onset shifts across packing and orientation.
- Later propagation differs strongly even when the initial top-layer trigger is preserved.

Response strategy:

- Acknowledge that the first trigger is strongly controlled by upper-bed loading geometry.
- Present this as a useful resolved sequence: the top-layer trigger is robust, while cascade growth depends on orientation and packing.
- Avoid implying that the onset mechanism generalizes to all blanket boundary conditions.

Need new calculation?

- Not needed for the present conclusion.
- Optional for broader generality: alternative plate roughness, confinement, or preloaded bed states.

## 9. Does the manuscript connect strongly enough to Nuclear Fusion and blanket design?

Likely reviewer concern: The paper could be seen as a DEM-method study with limited fusion-technology consequence.

Current evidence:

- The Introduction frames Li4SiO4 breeder beds in terms of compressive loads, heat-transfer pathways, purge-gas pathways and blanket integrity.
- The method resolves mother-pebble fracture events that experiments usually cannot observe inside opaque beds.
- Current results identify top-layer damage localization and packing-sensitive cascade growth, both relevant to bed mechanics and transport-pathway evolution.

Response strategy:

- Keep the title, abstract and first Introduction paragraph tied to ceramic breeder blankets.
- In Discussion, state the design relevance as diagnostic: the workflow can identify where and when local crushing begins, not yet prescribe blanket design limits.
- Avoid generic DEM novelty as the main selling point.

Need new calculation?

- No.
- A future coupling to permeability or thermal-contact changes would strengthen design impact but is beyond the present manuscript.

## 10. Is the reproducibility package sufficient without raw restart and full local-bond histories?

Likely reviewer concern: Reduced CSVs and scripts may not be enough to audit the event database.

Current evidence:

- A reduced reproducibility package exists with processed event tables, figure source data, plotting scripts, selected DEM input files and a checksum manifest.
- The package deliberately excludes very large restart files and full local-bond dump histories.
- The integrity audit confirms the current LaTeX build and package checksum.

Response strategy:

- Explain that the public reduced package supports figure and table reproduction, while large raw restart/local-bond histories are retained locally and can be provided on reasonable request.
- Make the data availability statement precise before submission by adding the repository DOI or URL.
- Preserve exact case names and checksums for traceability.

Need new calculation?

- No calculation needed.
- Before submission, add final author metadata and repository DOI/URL; keep raw archives organized for reviewer request.

## Highest-risk items to fix first if revision time is limited

1. Add a native contact-force output check for one seed02/seed03 window if reviewers challenge the force-path proxy.
2. Add a slower or hold-relax single-pebble check if reviewers challenge rate dependence.
3. Add one or two independent 1000-pebble packings only if reviewers push for probability statistics; otherwise keep the 1000-pebble claim as event-sequence evidence.
4. Add a concise subparticle-resolution limitation sentence if the final manuscript does not already make the 500-subparticle scope explicit.
5. Finalize the repository DOI/URL and data availability wording before upload.
