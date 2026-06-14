# Literature-to-claim support for the main manuscript

This note records how the key literature supports the main PB-006 manuscript argument. It separates claims that can be supported by prior work from claims that must remain project-owned simulation results.

## Literature-supported background claims

| Manuscript claim | Supporting literature | How it should be used |
| --- | --- | --- |
| Li4SiO4 ceramic breeder pebble beds are relevant to HCPB blanket design and require thermo-mechanical characterization. | Piazza et al., 2002, `10.1016/S0022-3115(02)00983-2`; Reimann et al., 2000, `10.1016/S0920-3796(00)00357-4` | Use in the opening paragraph to justify why compression, wall interaction and bed mechanics matter for fusion blankets. |
| Macroscopic compression tests provide bed-scale force-displacement or stress-strain benchmarks but cannot resolve individual pebble fracture sequences inside an opaque bed. | Zaccari/Lo Frano et al., 2009, `10.1016/j.jnucmat.2008.12.288` | Use to motivate why DEM event tracking adds information beyond experiments. |
| DEM is an established method for linking ceramic breeder bed compression to contact networks, packing descriptors and force distributions. | An et al., 2007, `10.1016/j.fusengdes.2007.02.004`; Gan and Kamlah, 2010, `10.1016/j.jmps.2009.10.009` | Use to position PB-006 as an extension of DEM bed mechanics toward explicit internal breakage events. |
| Ceramic breeder pebble crushing should be treated statistically because crush strength is scattered and contact force distributions are heterogeneous. | Gan et al., 2011, `10.1016/j.jnucmat.2010.12.131`; Annabattula et al., 2014, `10.13182/FST13-737` | Use to justify multi-seed beds, stochastic template orientations and future Weibull-style calibration. |
| Single Li4SiO4 pebble crush strength depends on contact geometry/material and pebble-pebble contact strength is more relevant to in-bed failure than ideal plate tests alone. | Zhao et al., 2013, `10.1016/j.engfracmech.2012.05.011` | Use in calibration limitations and to explain why single-pebble plate calibration is necessary but not sufficient. |
| Failure initiation and propagation in Li4SiO4 pebbles can alter the bed stress-strain response and should be tracked explicitly. | Zhao et al., 2013, `10.1016/j.fusengdes.2012.09.008`; Wang et al., 2021, `10.1016/j.fusengdes.2021.112606` | Use to motivate the focus on event sequence, localization and post-breakage bed evolution. |
| Bonded-particle DEM is a standard way to represent brittle bodies, crack initiation, bond loss, post-peak softening and fragments. | Potyondy and Cundall, 2004, `10.1016/j.ijrmms.2004.09.011` | Use in Methods/Introduction to justify the bonded-subparticle model class. |
| Li4SiO4 sub-ball/bonded DEM can reproduce size-dependent single-pebble fracture modes. | Kuang et al., 2024, `10.1016/j.fusengdes.2023.114105` | Use as the closest methodological precedent for bonded Li4SiO4 pebbles. |

## Project-owned claims that must not be outsourced to literature

| Claim | Required project evidence |
| --- | --- |
| A 500-subparticle 1 mm template is adequate. | Single-pebble force-displacement calibration, fragment morphology, and ideally subparticle-count sensitivity at 250/500/1000. |
| The lock-then-compress insertion workflow does not bias the bed. | Packing fraction, bed height, coordination/fabric descriptors and zero broken internal bonds before compression. |
| The PB-006 fracture-event sequence is physically meaningful. | Mother-pebble-resolved bond-loss events, event timing, top-bin localization, multi-seed repeatability and contact/force-path diagnostics. |
| Later 1000-pebble propagation beyond 0.10 mm has occurred. | Completed restartable 0.15 mm seed01, orient02 and seed02 cases with interpretable thermo output and local bond dumps. Current evidence supports robust top-layer onset and orientation-/packing-sensitive post-onset propagation, but not full bed-scale probability. |
| Bond parameters represent Li4SiO4 rather than a generic brittle template. | Parameter calibration against crush load, elastic slope, size effect and failure morphology, with uncertainty stated. |
