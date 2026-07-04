# CPM material-response summary

Date: 2026-07-04

Input: `tables/pb007_material_parameter_response.csv`.

## Source-backed findings

- **completed_endpoint_rows**: 11 completed endpoints; 8 cracking endpoints; 3 zero-loss endpoints
  Boundary: Finite 100-particle endpoint set.
- **strength_matrix_scope**: 6 strength-reduction rows across early_cracking and synchronous_cracking geometries
  Boundary: Strength multipliers 0.75x, 0.50x and 0.25x for two cracking geometries.
- **intact_geometry_controls**: intact_geometry remains at 0 broken bonds for strength multipliers 1x, 0.5x, 0.25x; final force-sum range 0.253-0.253 N
  Boundary: Zero-loss controls in the 60 micrometre displacement window.
- **early_cracking_response**: first localized bond loss remains at 19 micrometres; endpoint bond loss is 10-15 bonds; force-sum range 0.575-1.328 N
  Boundary: Geometry-specific response; onset does not advance in this geometry.
- **synchronous_cracking_response**: first localized bond loss advances from 39 to 19 micrometres (20 micrometres, 51.3%); endpoint bond loss is 10-15 bonds; force-sum range 0.747-1.18 N
  Boundary: Geometry-specific response; onset advances under strength reduction in this geometry.
- **force_path_endpoint_separation**: minimum cracking force sum 0.575 N / maximum zero-loss force sum 0.253 N = 2.28
  Boundary: Endpoint separator for current finite windows, not a universal threshold.
- **spanning_graph_retention**: all 11 material-response endpoints retain a spanning final native force graph
  Boundary: Local bond loss occurs within connected load-bearing networks.

## Geometry-level endpoint table

| Case | Endpoint broken bonds | First localized bond loss (micrometres) | Final force sum (N) | Top reachable | Bottom reachable from top |
| --- | ---: | ---: | ---: | ---: | ---: |
| early_cracking at 1x | 10 | 19 | 0.575 | 46 | 10 |
| early_cracking at 0.75x | 10 | 19 | 1.328 | 53 | 12 |
| early_cracking at 0.5x | 10 | 19 | 1.196 | 62 | 13 |
| early_cracking at 0.25x | 15 | 19 | 0.871 | 56 | 13 |
| intact_geometry at 1x | 0 | none | 0.253 | 67 | 18 |
| intact_geometry at 0.5x | 0 | none | 0.253 | 67 | 18 |
| intact_geometry at 0.25x | 0 | none | 0.253 | 67 | 18 |
| synchronous_cracking at 1x | 10 | 39 | 0.945 | 72 | 12 |
| synchronous_cracking at 0.75x | 10 | 29 | 1.180 | 79 | 14 |
| synchronous_cracking at 0.5x | 10 | 19 | 0.853 | 73 | 14 |
| synchronous_cracking at 0.25x | 15 | 19 | 0.747 | 76 | 10 |

## Manuscript use

Use these values to support the finite-window claim that local force-path topology and bonded-particle strength jointly control early fracture. Do not use them as a converged stochastic fracture-probability estimate or as a universal Li4SiO4 material law.
