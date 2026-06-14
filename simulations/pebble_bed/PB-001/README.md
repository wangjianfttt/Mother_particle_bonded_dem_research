# PB-001 small crushable pebble-bed smoke test

PB-001 is the first bed-scale test using multiple bonded Li4SiO4 pebble templates.

## Geometry

- 12 bonded pebbles
- 500 subparticles per pebble
- 6000 atoms total
- Ordered 2 x 2 x 3 initial packing
- Initial centre spacing: 1.30 mm

The 1.30 mm spacing avoids cross-pebble bond creation at `tsCreateBond = 1`. The expected initial internal bond count is:

```text
12 x 6723 = 80676
```

The smoke test produced exactly 80676 intact bonds, confirming that inter-pebble bonds were suppressed.

## Current result

Short fast-loading contact test without effective bed support:

- top speed: 1.0 m/s
- final displacement: 0.10 mm
- peak top force: 36.10 N
- final broken bonds: 308
- first bond breakage: 0.055 mm
- bottom reaction: 0 N

The zero bottom reaction means the initial ordered bed has not yet established a proper bottom-supported load chain. PB-001 is therefore a workflow proof, not a physical bed-compression result.

Confined and lightly bottom-supported test:

- side walls added as four mesh walls;
- bottom plate moved into light contact with the lowest layer;
- top speed: 2.0 m/s;
- final top displacement: 0.80 mm;
- peak top force: 128.92 N;
- peak bottom force: 0.059 N;
- final broken bonds: 9536.

The bottom reaction remains much smaller than the top force. The current ordered, initially sparse bed still behaves as a local upper-layer crushing test rather than a meaningful one-dimensional bed compression.

## Next changes

1. Add gravity or a damped settling stage.
2. Generate a denser initial packing without cross-pebble cohesive bonds.
3. Add side confinement or periodic side boundaries for a more representative bed.
4. Reduce bond dump frequency for bed-scale production runs.
5. Increase pebble count after the 12-pebble workflow is stable.
