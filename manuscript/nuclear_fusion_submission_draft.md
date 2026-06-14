# Mother-pebble-resolved fracture sequences in random Li4SiO4 breeder beds for fusion blankets by bonded-particle DEM

Target journal: Nuclear Fusion

Article type: Paper

Keywords: lithium orthosilicate; ceramic breeder blanket; pebble bed; bonded-particle DEM; pebble crushing; fracture-event sequence

Authors: Jian Wang*, Siyu Wang, Hang Zhang, Ming-Zhun Lei, Wei Wen, Qi-Gang Wu, Gang Shen, Haishun Deng

Affiliations:

1. Anhui University of Science and Technology, Huainan, Anhui 232001, China
2. Institute of Plasma Physics, Chinese Academy of Sciences, Hefei, Anhui 230031, China

Author affiliations:

- Jian Wang: 1, 2
- Siyu Wang: 1
- Hang Zhang: 1
- Ming-Zhun Lei: 2
- Wei Wen: 1, 2
- Qi-Gang Wu: 2
- Gang Shen: 1
- Haishun Deng: 1

*Corresponding author: wjfttt@mail.ustc.edu.cn

## Abstract

Background: Ceramic breeder beds in ITER/CFETR-class solid blankets must preserve structural integrity, heat-transfer contacts and tritium purge-gas pathways under constrained compression and cyclic service loading. However, the mesoscopic sequence by which individual Li4SiO4 pebbles fracture inside an opaque bed is difficult to measure and is usually reduced to bulk stiffness or crush-probability metrics. Methods: We develop a bonded-template DEM workflow in which each nominal 1.0 mm mother pebble is represented by 500 bonded subparticles, inserted intact into a gravity-settled random bed and allowed to break only during subsequent compression. Internal bond graphs are compared between local dumps to extract mother-pebble-resolved fracture events. Results: Three independent 500-pebble beds show a reproducible first-break trigger in the highest mother pebble, followed by packing-dependent cascade growth in the upper bed. Restartable 1000-pebble calculations preserve the same top-layer onset mechanism and reveal orientation- and packing-sensitive post-onset propagation, including a three-stage onset-quiet-burst sequence. Conclusions: The workflow converts bonded-particle blanket simulations into fracture-event databases that can support micromechanistic assessment of breeder-bed integrity, lifetime margins and design margins, while larger ensembles and native contact-force diagnostics remain required for predictive design.

## Introduction

Lithium orthosilicate ceramic pebbles are candidate tritium-breeder materials for helium-cooled solid blankets in ITER/CFETR-class fusion systems [@Piazza2002CeramicBreederMaterials; @Reimann2000ThermomechanicalPebbleBeds]. In these blankets, the breeder bed is an active functional region: it provides lithium inventory for tritium generation, conducts heat toward coolant structures, and must retain connected purge-gas pathways for tritium extraction. Mechanical degradation is therefore not a purely granular-mechanics problem. Pebble crushing can change contact networks, local bed stiffness, thermal pathways and helium purge-flow resistance, thereby affecting structural integrity, lifetime assessment and design margins for blanket modules [@CrushedPebblePressureDrop2024].

Single-pebble crush tests provide essential contact-strength, size-effect and elastic-response targets, and bed-compression experiments reveal collective stiffness, compaction and failure trends [@PlateMaterialLi4SiO4; @Annabattula2014SizeDependentCrush; @Bhartia2020ElasticResponse; @ZaccariLoFrano2009CeramicPebbleBeds]. However, experiments on opaque beds cannot easily identify which mother pebble breaks first, whether damage remains local or spreads laterally, or how fracture events evolve under increasing compression. Existing DEM studies have advanced breeder-bed analysis by relating macroscopic response to coordination number, contact-force distributions and packing structure, and by estimating crush probability from single-pebble strength distributions [@An2007DEMCeramicBreederBeds; @GanKamlah2010DEMPebbleBeds; @CrushProbabilityPebbleBed2011; @Wang2021CrushableCeramicPebbleBed]. The unresolved gap is event-level: most bed-scale models still treat pebbles as rigid particles, or infer failure after the fact, so they cannot directly produce a time-ordered, mother-pebble-resolved fracture sequence.

Bonded-particle DEM provides a route to this missing representation because a brittle object can be assembled from subparticles connected by breakable bonds, allowing bond loss and fragment generation to be followed directly [@PotyondyCundall2004]. Recent Li4SiO4 sub-ball DEM work has shown that such models can reproduce size-dependent single-pebble crush behaviour [@Li4SiO4SizeDEM2023], and prior breeder-bed simulations have explored crushable-bed response [@Wang2021CrushableCeramicPebbleBed; @CrushableDEMPebbleBed2026]. For blanket design, however, a method must also ensure that a breakable pebble is inserted into a random bed without artificial pre-damage; otherwise the simulated fracture sequence may partly reflect initialization artefacts rather than service loading. This zero-precompression-damage requirement becomes especially important when the results are used to reason about safety margins, lifetime degradation and transport-path preservation.

We therefore introduce a locked-template workflow for fracture-resolved breeder-bed compression, schematized in Fig. 1. Whole-pebble proxy spheres first settle under gravity to create a random packing. The settled centres are then replaced by 500-subparticle bonded templates, which are created far apart to form only internal bonds and translated as intact groups into the packed bed. This separates bed generation from pebble crushing, verifies zero internal bond loss before loading, and enables mother-pebble-resolved fracture events to be extracted by comparing internal bond graphs across compression dumps. The resulting event database is intended as mesoscopic evidence for how local pebble damage may initiate and propagate in solid breeder blankets, rather than as a final design rule.

![Fig. 1 | Locked-template workflow for fracture-resolved Li4SiO4 breeder-bed compression](/Users/wangjian-macbook13/Documents/颗粒破碎统计研究/figures/main/fig1_workflow.png)

**Fig. 1 | Locked-template workflow for fracture-resolved Li4SiO4 breeder-bed compression.** A nominal 1 mm mother pebble is represented by a 500-subparticle bonded template with 5876 internal bonds in the selected calibration candidate. Proxy spheres first settle under gravity without internal bonds. The settled proxy centres are then replaced by intact bonded templates, so internal bond failure is absent during bed formation and is activated only during compression. This zero-precompression-bond-loss control is verified for both 500- and 1000-pebble beds. Local bond dumps are converted into a mother-pebble-resolved fracture-event database.

## Results

### A bonded 1 mm template provides an internal failure state for each pebble

We first generated a nominal 1.0 mm Li4SiO4 pebble from 500 spherical subparticles. The final non-overlapping template produced a stable internal bond network and no preloading failure. A homogeneous strength scan showed the intended trend: increasing bond strength increased peak compressive load while reducing final bond loss. However, homogeneous load-matched templates failed mainly by surface chipping, leaving one large fragment and several single-subparticle chips.

To obtain a more realistic split-type failure mode, we introduced a weak-plane template in which cross-plane bonds were assigned lower strength and a shorter bond-creation distance. The calibration evidence is summarized in Fig. 2. The selected x-normal weak-plane template reached a peak top force of 18.64 N and a peak bottom force of 18.07 N, while the final intact-bond graph contained two major fragments of 227 and 224 subparticles plus small chips. A true x-normal 0.05 m s-1 rerun retained the 5876-bond initial network, reproduced first break at 0.1025 mm and formed two major fragments of 236 and 226 subparticles, although the peak top force increased to 21.64 N. A still-slower 0.03 m s-1 short run to 0.18 mm retained the same first-break window at 0.10245 mm and already formed two major fragments of 247 and 246 subparticles; because this short run stops before the known peak-force region, it is used only as onset and morphology evidence. The corresponding final fragment morphology from the 0.05 m s-1 rerun is shown in the supplementary ParaView visualization. Pilot orientation and strength-multiplier scans retained the two-major-fragment mode while producing peak-load scatter, supporting the use of template orientation and sample strength as stochastic variables in later ensemble studies. Two y-normal residual-template reruns at 0.10 and 0.05 m s-1 started from 5846 intact bonds and gave nearly identical responses near 28.3 N; these are retained as orientation-specific rate evidence, not as direct x-normal reproduction. The full force-displacement comparison is provided in Extended Data Fig. 1.

![Fig. 2 | Single-pebble calibration evidence for the current 500-subparticle template](/Users/wangjian-macbook13/Documents/颗粒破碎统计研究/figures/sp002/single_pebble_calibration_evidence.png)

**Fig. 2 | Single-pebble calibration evidence for the current 500-subparticle template.** In panels b and c, "homogeneous" denotes a uniform-bond-strength template, "selected template" denotes the x-normal weak-plane calibration candidate, "orthogonal" denotes y-normal residual-template rate checks, "orientation pilot" denotes weak-plane orientation variants, "strength multiplier" denotes deterministic bond-strength scaling, and "Weibull trial" denotes a stochastic strength sample. The selected weak-plane template lies in the provisional 1 mm crush-load target window and preserves a two-major-fragment mode. The true x-normal 0.05 m s-1 rerun supports partial rate robustness in first-break displacement and fragment morphology, but the template is treated as a current calibration candidate rather than a final Li4SiO4 material law.

### Intact bonded templates can be inserted into random beds without precompression damage

The random-bed workflow was designed to enforce one condition: gravity deposition must not damage the internal pebble template. In the first stage, monodisperse 1 mm proxy spheres were poured and settled under gravity. These proxy particles have no internal subparticle bonds and therefore cannot undergo internal breakage. In the second stage, each settled proxy centre was replaced by one bonded 500-subparticle template. Templates were created far apart to form internal cohesive bonds only and then translated as intact atom-id groups into the packed bed.

This procedure preserved the intended bond count. A 500-pebble bed contained 250000 subparticles and 2938000 intact internal bonds before compression, exactly 500 times the 5876-bond template count. A 1000-pebble bed similarly contained 500000 subparticles and 5876000 intact internal bonds, with zero broken internal bonds before compression. Thus, subsequent bond loss can be attributed to compression-driven pebble crushing rather than deposition artefacts.

### Random 500-pebble beds show reproducible onset but seed-dependent growth

We compressed three independent 500-pebble random beds to 0.20 mm top displacement. All three seeds shared the same first-break location and displacement: the first localized event occurred at 0.0725 mm in the highest mother pebble, pebble 500. This reproducible onset indicates that early fracture is controlled by the top-layer loading geometry rather than by random numerical noise.

After onset, the event sequence became packing-dependent, as compiled in the event database in Fig. 3. The three 500-pebble beds accumulated 246-559 localized broken bonds across 9-22 events involving 4-7 mother pebbles. Damage remained confined to the top two height bins in all three cases, but the strongest cascade case showed lateral top-layer spreading by 0.0975 mm, when pebbles 498, 499 and 500 all accumulated new internal bond loss. These results separate two features of bed crushing: an onset trigger that is reproducible across random packs and a later cascade magnitude that depends on upper-bed structure.

![Fig. 3 | Event database for 500- and 1000-pebble compression cases](/Users/wangjian-macbook13/Documents/颗粒破碎统计研究/figures/pb006/pb006_breakage_event_database.png)

**Fig. 3 | Event database for 500- and 1000-pebble compression cases.** The combined event database shows reproducible first breakage in the highest mother pebble for the three 500-pebble beds and for the resolved 1000-pebble cases. Later event accumulation differs across random beds and template-orientation replicates, so final broken-bond counts are interpreted as event-sequence evidence rather than converged probability statistics.

### Upper-bed packing controls the strength of the breakage cascade

To interpret the seed dependence, we computed geometric descriptors from the settled mother-pebble centres. Seed03, the strongest breakage case, had the lowest bed height, the largest top-bin population and the highest top-bin mean geometric degree. This denser upper-bed structure is consistent with a broader loading footprint near the moving plate.

We then reconstructed overlap-derived inter-pebble contact proxies from saved particle dumps for the weaker and stronger 500-pebble cascades (Fig. 4). Each cross-mother subparticle overlap contributed a weight proportional to overlap to the 3/2 power, giving a Hertz-type force proxy for identical material parameters. At matched displacement, the stronger cascade case developed more top-wall-loaded mother pebbles and more inter-pebble proxy edges than the weaker cascade case. At 0.0975 mm, the proxy loaded pebbles 498-500 in the stronger cascade case, matching the lateral spread of breakage at the same timestep. This analysis does not replace native contact-force output, but it is consistent with a mechanism in which upper-bed packing broadens load transfer and amplifies the breakage cascade.

![Fig. 4 | Upper-bed packing and overlap-derived force-path proxy](/Users/wangjian-macbook13/Documents/颗粒破碎统计研究/figures/pb006/pb006_force_path_proxy.png)

**Fig. 4 | Upper-bed packing and overlap-derived force-path proxy.** The stronger 500-pebble cascade case develops a broader top-wall loading footprint and more inter-pebble overlap-proxy edges than the weaker cascade case at matched displacement. The proxy is used only as geometry-derived evidence consistent with load-path broadening; native contact-force output is still needed before claiming direct force-chain confirmation.

### A 1000-pebble bed preserves the early top-layer trigger

We next scaled the workflow to 1000 mother pebbles. The 1000-pebble proxy bed settled to a height of 7.912 mm and, after template replacement, contained 500000 subparticles and 5876000 intact bonds. A short compression scan to 0.10 mm showed first cumulative bond loss at 0.0675 mm, slightly earlier than the 0.0725 mm onset in the three 500-pebble beds.

Targeted local bond dumps resolved this 1000-pebble onset sequence without writing full-history local output. Six event increments occurred at 0.0675, 0.0700, 0.0775, 0.0900, 0.0925 and 0.0950 mm, with event sizes of 15, 8, 20, 6, 2 and 2 broken bonds. All 53 broken internal bonds were assigned to mother pebble 1000 in the top height bin. Restartable 0.15 mm calculations then tested whether post-onset damage remained confined to this pebble or spread into neighbouring upper-layer pebbles.

| Case | Mother pebbles | Endpoint (mm) | Output mode | Events | Broken bonds | Damaged pebbles | First break (mm) | First break pebble | Interpretation |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 500-pebble bed A | 500 | 0.20 | full local-dump sequence | 11 | 271 | 5 | 0.0725 | 500 | 500-pebble random-packing replicate |
| 500-pebble bed B | 500 | 0.20 | full local-dump sequence | 9 | 246 | 4 | 0.0725 | 500 | 500-pebble random-packing replicate |
| 500-pebble bed C | 500 | 0.20 | full local-dump sequence | 22 | 559 | 7 | 0.0725 | 500 | 500-pebble random-packing replicate |
| 1000-pebble onset scan | 1000 | 0.10 | thermo scan plus selected local dumps | 6 | 53 | 1 | 0.0675 | 1000 | short-displacement onset check |
| 1000-pebble bed A | 1000 | 0.15 | onset events plus late-window dumps | 15 | 98 | 3 | 0.0675 | 1000 | post-onset window check |
| 1000-pebble orientation replicate | 1000 | 0.15 | selected local dumps | 9 | 95 | 1 | 0.0725 | 1000 | fixed-geometry orientation sensitivity |
| 1000-pebble bed B | 1000 | 0.15 | selected local dumps | 31 | 316 | 5 | 0.0600 | 1000 | independent-packing replicate |

The endpoint forces and total broken-bond counts in this comparison should not be interpreted as direct 500- versus 1000-pebble strength scaling because the 500-pebble cases were continued to 0.20 mm, whereas the 1000-pebble cases were designed as onset and post-onset window checks. The comparison is used only to place the first-break displacement, event localization and output strategy on the same scale.

In 1000-pebble bed A, the resolved onset path accumulated 53 broken bonds by 0.0950 mm, and the late-window dumps showed no additional bond loss until 0.1325 mm. A second late-window burst then appeared between 0.1325 and 0.1500 mm, adding 45 broken bonds and bringing the 0.15 mm total to 98 broken bonds across 15 localized events. The late events involved mother pebbles 961, 980 and 1000, showing that damage can spread within the upper layer after the initial single-pebble onset cluster. Thus this 1000-pebble bed resolves the three-stage sequence shown in Fig. 5: localized onset in pebble 1000, a damage-quiet plateau, and renewed top-layer fracture activity near 0.13-0.15 mm.

**Table 2 | Stage-window summary for 1000-pebble bed A.**

| Stage | Window (mm) | Events | Broken bonds | Damaged pebbles |
| --- | ---: | ---: | ---: | ---: |
| Onset | 0.0675-0.0950 | 6 | 53 | 1 |
| Quiet plateau | 0.0950-0.1300 | 0 | 0 | 0 |
| Late burst | 0.1325-0.1500 | 9 | 45 | 3 total |

![Fig. 5 | Three-stage 1000-pebble breakage sequence to 0.15 mm](/Users/wangjian-macbook13/Documents/颗粒破碎统计研究/figures/pb006/pb006_1000_0p15_three_stage_sequence.png)

**Fig. 5 | Three-stage 1000-pebble breakage sequence to 0.15 mm.** One 1000-pebble bed resolves an onset cluster, a quiet plateau and a late upper-layer burst. The late burst spreads damage from the first damaged mother pebble 1000 to neighbouring upper-layer pebbles 961 and 980.

A fixed-geometry orientation replicate separated the robust onset trigger from post-onset variability. This replicate used the same 1000 proxy centres as bed A but a different bonded-template orientation set. It first broke in pebble 1000 at 0.0725 mm, close to the 500-pebble onset and only 0.0050 mm later than the 1000-pebble bed A onset. However, all 95 broken bonds remained in pebble 1000, and no new bond loss occurred after 0.1200 mm through the final 0.1500 mm displacement.

The independent 1000-pebble bed B shows the opposite post-onset limit, and Fig. 6 compares this behaviour with bed A and the fixed-geometry orientation replicate. It first broke earlier, at 0.0600 mm in pebble 1000, and accumulated 316 broken bonds across 31 localized events by 0.1500 mm. Damage remained in the top height bin but spread across five mother pebbles: 1000, 999, 998, 997 and 949. The largest contributions were 121 broken bonds in pebble 1000, 80 in pebble 998 and 61 in pebble 997. Together, bed A, the orientation replicate and bed B support a constrained interpretation: the top-layer trigger is robust in these 1000-pebble calculations, whereas propagation after onset is highly sensitive to template orientation and upper-bed packing.

![Fig. 6 | 1000-pebble event-sequence variability](/Users/wangjian-macbook13/Documents/颗粒破碎统计研究/figures/pb006/pb006_1000_orientation_sensitivity.png)

**Fig. 6 | 1000-pebble event-sequence variability.** Bed A and the orientation replicate use the same 1000-pebble proxy centres but different bonded-template orientations, whereas bed B is an independent packing. All three cases preserve a top-layer first-break trigger in or near the highest mother pebble. Bed A accumulates 98 broken bonds over three damaged pebbles, the orientation replicate accumulates 95 broken bonds entirely in pebble 1000 and remains quiet from 0.1200 to 0.1500 mm, and bed B accumulates 316 broken bonds over five top-bin pebbles.

## Discussion

This work demonstrates a computational chain for resolving pebble-level fracture events inside random ceramic breeder beds in a fusion-blanket context. The key advance is not merely using a bonded particle model, but preserving each bonded template as an intact 1 mm mother pebble during bed formation and then tracking its internal bond graph during compression. This zero-precompression-damage insertion step, combined with mother-pebble-resolved event extraction, turns a conventional bed-compression calculation into a mesoscopic fracture-sequence diagnostic. Such diagnostics are directly relevant to blanket structural-integrity assessment because they identify where damage starts, whether it remains confined, and when it spreads into neighbouring upper-layer pebbles that help carry heat, load and purge-gas pathways.

The current evidence is organized into three tiers. First, at the single-pebble scale, the selected weak-plane template is a calibration candidate consistent with the available crush-load scale and split-type fragmentation morphology (Fig. 2 and Extended Data Fig. 1), but it is not yet a final Li4SiO4 material law. Second, at the 500-pebble bed scale, three independent random packs show that first fracture is reproducibly triggered in the highest mother pebble, whereas the subsequent cascade is controlled by upper-bed packing (Figs. 3 and 4). Third, at the 1000-pebble scale, restart-enabled calculations support initialization scalability, robust top-layer onset and strongly variable post-onset propagation across orientation and independent-packing replicates (Figs. 5 and 6). These results suggest that breeder-bed degradation may contain a robust initiation site but a packing-sensitive growth path, a distinction that matters for lifetime evaluation and design-margin optimization. The present scope remains diagnostic rather than prescriptive: it provides event-sequence evidence for damage initiation and spread, but does not yet define allowable blanket stresses or converged failure probabilities.

Several limitations define the next stage before the method can support quantitative blanket design. The single-pebble template is a current calibration candidate, not a final Li4SiO4 material law; fuller stiffness calibration, subparticle-count sensitivity and larger stochastic strength ensembles are still needed. The present compression protocol is a numerical screening protocol and should be followed by hold-relax or still-slower checks before strong quasi-static wording. The force-path analysis is geometry-derived and should be replaced or validated by native contact-force output so that links to heat-transfer contacts and purge-gas-channel evolution can be assessed more directly. Finally, robust bed-scale probability statements and design-margin estimates will require additional independent 1000-pebble random packings, cyclic loading paths and coupling to thermal and purge-flow performance metrics.

## Methods Summary

Simulations used a local no-VTK LIGGGHTS-INL 4.0.0 build [@LIGGGHTSINL] with SI units, granular atoms and `pair_style gran model hertz tangential history cohesion bond stressBreak on createBondAlways off`. Unless otherwise noted, bonded-template calculations used a 5.0 ns timestep, density 2400 kg m-3, Young's modulus 90 GPa, Poisson ratio 0.25, restitution coefficient 0.3 and friction coefficient 0.5. The selected weak-plane template used 500 subparticles, bond stiffnesses of 1.0e14 and 5.0e13 N m-3, bulk normal and tangential strengths of 90 MPa in the bed runs, weak-plane strengths of 22.5 MPa, a 0.20 mm bulk bond-creation distance and a 0.09 mm weak-plane creation distance. Single-pebble calibration runs used the same contact formulation, with parameter scans around this weak-plane family retained only as calibration evidence.

Random beds were generated in two stages. First, 1.0 mm proxy spheres were inserted into a 11 mm by 11 mm lateral box and settled under gravity using an unbonded Hertzian contact law, a 1.0 us timestep and viscous damping until the tail kinetic energy was small. Second, the settled proxy centres were replaced by bonded 500-subparticle templates. Templates were initially created far apart so that bonds formed only within each mother pebble; the atom-id groups were then translated to the proxy centres. The initialization check required the exact expected bond count, 5876 internal bonds per mother pebble, before any compression step was accepted.

Compression used rigid plate or wall boundaries and a downward top-wall velocity of 0.5 m s-1 for the bed-scale screening calculations. For 1000-pebble cases, restart-enabled runs first wrote thermo data and alternating restart files, then activated selected local bond dumps near or before the expected onset window to avoid storing a full local-bond history. The present 1000-pebble workflows used the same locked-template construction but different proxy packings or template-orientation sets as stated in the Results.

Bond status was recorded with `compute bond/counter`; intact bond pairs were written using `compute pair/gran/local/bond` and `dump local`. Mother-pebble events were obtained by comparing each local dump with the largest intact internal bond graph in the dump sequence, assigning atom-id ranges to mother-pebble ids, and counting positive increments in broken internal bonds as localized events. Random packing descriptors were calculated from settled proxy centres, and overlap-derived force-path proxies were reconstructed from saved subparticle dumps. The overlap proxy was used only as a geometric diagnostic and not as native contact-force evidence.

## Data availability statement

The processed event tables, figure source data, manuscript figures, DEM input files and post-processing scripts supporting this study have been assembled in a reduced reproducibility package with a checksum manifest. For submission, this package should be deposited in a persistent repository such as Zenodo, Figshare or an institutional repository, and the final DOI or stable URL should be inserted here before upload: [repository DOI/URL to be added]. Very large raw restart files and full local-bond dump histories are retained as local case archives and can be provided as larger audit bundles on reasonable request, subject to repository file-size limits and institutional storage constraints.

## Code availability statement

The template-generation, run-control and post-processing scripts are included in the reduced reproducibility package under `scripts/`, with representative DEM input files under `simulations/`. Compiler details and build flags should be recorded in the repository metadata before final upload.

![Supplementary visualization | ParaView-rendered single-pebble fragment morphology](/Users/wangjian-macbook13/Documents/颗粒破碎统计研究/figures/sp002/single_pebble_fragment_morphology_paraview.png)

**Supplementary visualization | ParaView-rendered single-pebble fragment morphology.** Final morphology of the true x-normal 0.05 m s-1 single-pebble rerun at 0.30 mm displacement, rendered directly from the particle and intact-bond dumps. The 500 subparticles are coloured by final intact-bond connected component: largest fragment, second-largest fragment and smaller fragments. Semi-transparent tubes show the remaining intact internal bonds. The final graph contains 5335 intact bonds and 40 fragments, with the two largest fragments containing 236 and 226 subparticles.

![Extended Data Fig. 1 | Single-pebble force-displacement overlay](/Users/wangjian-macbook13/Documents/颗粒破碎统计研究/figures/sp002/sp002_force_displacement_overlay.png)

**Extended Data Fig. 1 | Single-pebble force-displacement overlay.** The x-normal reference run, true 0.05 m s-1 rerun and a short 0.03 m s-1 onset check are compared against the provisional 1 mm load target window and a near-size literature displacement/load anchor. The 0.10 and 0.05 m s-1 traces first lose internal bonds at 0.1025 mm, while the 0.03 m s-1 short run first breaks at 0.10245 mm and is not used for peak-load comparison because it stops at 0.18 mm. The panel supports template-level calibration screening but not a final Li4SiO4 material law.

## Acknowledgements

This work was supported by the Anhui Provincial Natural Science Foundation (2408085QA030), the Science Foundation of the Institute of Plasma Physics, Chinese Academy of Sciences (DSJJ-2025-08), the Anhui Intelligent Mine Technology and Equipment Engineering Research Center (AIMTEERC202307), the China Post-doctoral Science Foundation under Grant Number 2024M753266, the Excellent Research and Innovation Team of Anhui Province, China (2022AH010052), the Scientific Research Foundation for High-level Talents of Anhui University of Science and Technology, China (2021yjrc51), and the Collaborative Innovation Program of Hefei Science Center, CAS, China (2019HSC-CIP006).

## Author contributions

Jian Wang: Validation, Supervision, Project administration, Methodology, Investigation, Conceptualization. Siyu Wang: Writing - original draft, Formal analysis, Data curation, Visualization. Hang Zhang: Writing - original draft, Formal analysis, Data curation, Visualization. Ming-Zhun Lei: Writing - review and editing, Validation, Project administration, Formal analysis. Wei Wen: Writing - review and editing, Supervision, Project administration, Methodology, Conceptualization. Qi-Gang Wu: Validation, Resources, Data curation. Gang Shen: Writing - review and editing, Supervision, Project administration. Haishun Deng: Supervision, Project administration.

## Conflict of interest

The authors declare no competing interests.

## References

References are maintained in `manuscript/references.bib`. DOI, year and publisher-title metadata were checked against Crossref on 2026-05-31; the audit table is stored as `tables/reference_crossref_audit_20260531.csv`.
