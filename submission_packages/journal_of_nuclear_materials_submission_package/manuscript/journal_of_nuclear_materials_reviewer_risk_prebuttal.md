# Journal of Nuclear Materials reviewer-risk prebuttal

Purpose: this internal document prepares the authors for likely Journal of Nuclear Materials reviewer concerns. It should not be uploaded as a manuscript file unless the editor requests additional context. Its role is to keep the submitted claims conservative, evidence-linked and materials-focused.

Current manuscript position: the paper is an acceptance-gated computational materials diagnostic for Li4SiO4 ceramic breeder-pebble degradation. It is not presented as a converged fracture-probability model, a final Li4SiO4 constitutive law or a blanket design-margin calculation.

## High-priority reviewer risks

| Risk | Why a JNM reviewer may raise it | Current evidence in the package | Prebuttal position | Manuscript boundary |
| --- | --- | --- | --- | --- |
| The study may be viewed as a DEM-method paper rather than a nuclear-materials paper | JNM prioritizes material degradation, irradiation/fusion relevance and property consequences over numerical workflow alone | Introduction and Discussion connect Li4SiO4 pebble damage to breeder-bed integrity, purge-gas pathways, thermal-contact networks and blanket service degradation; Fig. 1 frames the workflow as a ceramic breeder-material diagnostic | Emphasize that the method resolves the hidden sequence of mother-pebble damage that experiments currently report only as aggregate breakage ratio or pressure-drop consequence | Keep breeder-material integrity, purge pathways and thermomechanical service context in the abstract, introduction and discussion |
| Single-pebble calibration is not a fully calibrated Li4SiO4 material law | The weak-plane template is reduced-order and fitted to limited crush-load/morphology anchors | Fig. 2, Fig. 3, Table 2, resolution/rate summaries and Supplementary Fig. S1 support a current calibration candidate; onset and split topology are robust while peak load remains sensitive | State that the template is a load-scale and fragment-mode matched candidate for event-sequence screening | Do not claim final Li4SiO4 law, calibrated Weibull strength distribution or predictive single-pebble strength statistics |
| Bed ensemble size is small | Two corrected 100-mother-pebble beds plus strength audits cannot support probability statistics | Fig. 5 and Fig. 6 show one localized event sequence and one independent intact corrected bed; 0.5x and 0.25x audits remain intact despite spanning native force graphs | Present the result as event-sequence and local-force-path sensitivity evidence, not a probability estimate | Avoid failure probability, reliability index, universal onset displacement or design-limit language |
| The corrected bed contact modulus differs from the single-pebble 90 GPa contact modulus | Reviewers may suspect numerical softness controls fracture onset | Methods and Fig. 4 explain the gate-passing restored-stiffness protocol; direct restoration caused pre-loading damage and was rejected | Treat 1.5e10 Pa as a validated entry protocol for preserving zero seating damage and native force transmission, not as a measured material stiffness | Keep this as a protocol limitation and future calibration target |
| Previous diagnostic bed-scale claims could undermine trust | Earlier larger PB diagnostic route lacked validated force transmission | Audit files document the withdrawal; active manuscript excludes superseded diagnostic claims and uses corrected route only | Be explicit that the workflow improved because invalid load paths were discovered and rejected | Do not revive old large-bed force-chain or macro-response claims except as superseded diagnostics |
| The independent replicate remains intact even under 0.25x strengths, which may look inconsistent | A reviewer may expect reduced bond strength to trigger failure | Fig. 6 and processed independent-replicate data show spanning native force graphs with zero bond loss; this indicates local path dependence rather than displacement-only or strength-multiplier-only onset | Use this as mechanistic evidence: local force-path geometry controls whether weak internal bonds are activated | Do not overinterpret the intact independent replicate as material toughness or as a contradiction of the pilot; present it as sensitivity evidence |
| Force-chain/topology metrics may appear detached from material degradation | Topology alone is a granular-mechanics concept | Event tables couple native force-network evolution to localized internal bond loss in a top-near mother pebble; the material-degradation mechanism-index audit quantifies 1.44x inter-mother edge densification, 1.35x top-reachability densification and 46.4% peak-to-endpoint force relaxation around a 1.0e-5 endpoint broken-bond fraction | Frame topology as the mesoscale mechanical environment that activates or shields breeder-pebble microcracks | Tie topology language to ceramic damage initiation, load transfer and service degradation; do not present topology indices as transport predictions |
| The output may look like case-specific diagnostics rather than reusable materials information | A reviewer may ask what the computed quantities contribute beyond one compression movie | The manuscript now defines event time, damaged mother-pebble identity, bond-loss increment, native force connectivity and macroscopic force relaxation as material-degradation state variables | Emphasize that these variables are designed to feed later stochastic, thermomechanical and transport-coupled breeder-bed degradation models | Do not imply that the current pilot already provides calibrated lifetime or transport coefficients |
| Dynamic or quasi-static artefacts may remain | DEM compression rates and relaxation choices can alter brittle response | Single-pebble matched-rate checks show preserved onset/split topology from 0.10 to 0.03 m s-1; corrected bed uses step-relaxed gates and force-balance diagnostics | Acknowledge that lower-rate and cyclic thermomechanical extensions are future work | Do not call the bed compression fully quasi-static; use "step-relaxed" and "rate-bounded" wording |
| Data availability may be considered insufficient before DOI insertion | JNM/Elsevier increasingly expects accessible data and code | Reduced reproducibility package, flat source bundle, metadata JSON, checksum manifest and staged gate report are prepared | Deposit the reduced package before submission and insert DOI/stable URL into manuscript and support files | Do not submit before DOI/stable URL insertion unless the editor explicitly permits later deposition |
## Recommended reviewer-facing language

If asked why the article belongs in Journal of Nuclear Materials:

The study targets Li4SiO4 breeder-pebble degradation as a nuclear-materials problem. The novelty is an acceptance-gated route that turns opaque bed crushing into a mother-pebble-resolved damage sequence, linking ceramic microcracking to the evolution of load-bearing contacts that govern bed stiffness, heat-transfer contacts and purge-gas transport paths. The numerical workflow is therefore used as an instrument for material-degradation diagnosis, not as an end in itself.

If asked whether the topology analysis adds materials insight:

The topology metrics are reported only when they are linked to localized ceramic bond loss and macro-response evolution. In the corrected pilot, very small internal damage coexists with measurable force-network densification, reachability change and peak-to-endpoint force relaxation. This is interpreted as a local contact-network degradation pathway that can motivate later coupled heat-transfer and purge-flow studies, but it is not a completed transport prediction.

If asked what is reusable beyond this specific pilot:

The reusable output is the state-variable structure, not the single pilot probability: event time, damaged mother-pebble identity, bond-loss increment, native force connectivity and macroscopic force relaxation. These quantities can be expanded across future stochastic, temperature-dependent and cyclic ensembles while preserving direct traceability from ceramic microcrack events to bed-level response.

If asked why the ensemble is still useful:

The current data are not used to estimate failure probability. They demonstrate that a corrected bed can be validated before damage interpretation and that early damage may be localized and force-path-sensitive. This is a necessary mechanistic step before larger stochastic ensembles can be meaningful.

If asked about the weak plane:

The weak plane is a reduced-order defect representation chosen to reproduce the target crush-load scale and split-type morphology. It is not claimed to be a measured crack population. Its role is to give each 1 mm mother pebble an internal failure state so that bed-scale fracture events can be resolved.

If asked about the corrected contact modulus:

The restored modulus was selected by acceptance gates that require zero internal-bond loss before loading, native force connectivity and gravity-baseline-corrected force balance. Higher restored stiffness values created seating damage and were rejected. The present modulus is therefore a gate-passing numerical protocol; absolute stiffness calibration remains a future experimental target.

## Author action checklist before submission

- Deposit the reduced reproducibility package and insert the DOI/stable URL with `scripts/insert_jnm_repository_identifier.py`.
- Confirm that all authors accept the conservative wording: calibration candidate, event-sequence evidence and no converged probability claim.
- Keep Fig. 5/Fig. 6 interpretation focused on localization and force-path sensitivity, not on deterministic thresholds.
- Do not add old superseded large-bed claims back into the cover letter, highlights or response text.
- Re-run `scripts/check_jnm_submission_gate.py` after any manuscript, declaration or package edit.
