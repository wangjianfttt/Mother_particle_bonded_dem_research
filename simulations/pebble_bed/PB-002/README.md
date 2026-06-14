# PB-002 densification concept

PB-002 will test a safer bed-initialization workflow:

1. Insert bonded pebble templates with enough spacing to avoid cross-pebble bond creation.
2. Create internal bonds only at `tsCreateBond = 1`.
3. Continue compression or settling after step 1; because `createBondAlways off`, later close contacts should not create new cohesive bonds between different pebbles.
4. Use side walls and a bottom plate to form a supported confined bed.

The purpose is to build a physically interpretable bed before production-scale simulations.

## First densification test

PB-002 used an initial spacing of 1.30 mm to avoid cross-pebble bonds, then compressed the bed with a low top plate.

Result:

- initial bonds: 80676, equal to 12 x 6723;
- no later new cohesive bonds were created between pebbles;
- final top displacement: 0.80 mm;
- peak top force: 121.97 N;
- peak bottom force: 0 N;
- final broken bonds: 8419;
- first break displacement: 0.02 mm.

Conclusion: the one-step top compression workflow successfully prevents cross-pebble bond creation, but still does not produce a meaningful bottom-supported bed response. The bed must be initialized by settling or denser random packing before compression.
