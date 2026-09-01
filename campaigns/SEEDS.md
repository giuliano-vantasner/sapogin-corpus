# Campaign seeds (PROPOSAL — requires Dan's acceptance of the split)

Derived from `clusters/cluster-report.md` (145 clusters, 8 topic buckets) and
`claims/coverage.yaml` (1,641 claims, 65 documents). Ordering is FIXED by
AGENTS.md: practical/phenomenology layer FIRST; mathematical models and
physical theory AFTER. Analysis lens: CQED per policy.yaml — **designation
still pending user confirmation**; default until designated: substrate QED
module family (`effective_actions`, `coherent_states`, `bosonic_fock`,
`dirac_vacuum_polarization`).

Campaign anatomy per AGENTS.md: claims list → frozen preregistered gate →
routed verdicts (established / refuted / bound / blocked) → executed
verification only → one commissioned review → issue-first PR (`Advances #N`).

## P1 — EVO generation: varicap electron clusters & displacement current [CORE]

- Why first: the electrical-path keystone (Tiziano: "KEY to understand the
  next steps for the electrical path").
- Claims: evo-charge-clusters clusters on varicap technology (WO06 33, WO07
  12, AR08 28), CODM displacement-current math (TC02/TC05/TC06, ~75+64 claim
  docs), AR09/AR10 two-component plasma clusters.
- Practical targets: tungsten-cone diode recipe (WO06), flat-varicap geometry
  (AR08), device critical current densities (TC04 W/Al films).
- Gate: reproduce Sapogin's cluster-formation thresholds from stated device
  geometry; executed numeric check of displacement-current densities vs
  measured explosion thresholds.

## P2 — Catalysis via charge clusters [CORE — Tiziano's KEY question]

- Why: the explicit goal question ("why charge clusters help catalysis and
  possibly EVO generation").
- Claims: catalysis bucket is THIN (6 claims: Patterson nickel-bubble
  super-unity heating, Potapov cavitation heat, plasmoid/metalized-grid
  effects) — campaign STARTS with a relation-mining pass over evo-charge-
  clusters and transmutation buckets (claims.jsonl `relations` + gitnexus
  graph) before any gate is frozen.
- Deliverable: mechanism map (cluster → surface → catalysis) with each link
  pinned to source claims or explicitly marked Sapogin-asserted-only.

## P3 — Isotope transmutation: proton clusters of nuclear size [CORE]

- Claims: transmutation-nuclear bucket (131 claims; AR04 37 claims, 28 core —
  proton-cluster tables; TC08 bubble synthesis/decay energy asymmetry; AR03).
- Practical targets: nuclear signatures, isotope shifts, input power, energy
  balances, electrode materials/geometry from AR04 tables.
- Gate: energy-balance recomputation from stated inputs/outputs; executed
  arithmetic, no prose verdicts.

## P4 — Device catalog: recipes, schematics, procedures

- Claims: electrical-devices bucket (366 claims): Testatika, self-charging
  Beletsky capacitor, Zhuravkov subcritical discharge, gradient electron
  injectors (WO02-adjacent, AR07 film geometry), thermoelectron-gas EMF
  sources (BR03), patents PA01–PA03 verbatim claims + figures.
- Deliverable: per-device structured recipe card (materials, geometry,
  procedure_steps, measurements, schematic_refs already extracted) + CQED-lens
  feasibility annotation.

## P5 — Current-crowding, wire explosion, skin-effect phenomenology

- Claims: discharge-plasma bucket (97 claims): Marakhtanov thresholds (W
  1.43e9 A/m², Al 8.04e9 A/m² @180C), AR06 circuit current instability
  (Runge-Kutta procedure extracted), AR07 planar eddy-current inductance.
- Gate: recompute instability growth rates; executed integration.

## T1 — Theory AFTER practical: Emden/canonical foundations

- Claims: emden-gravity-cosmic (151) + foundations-canonical (100) +
  general (161) buckets — Emden solutions, biwave least action, canonical
  total-pressure integral, cosmology (black holes, Tunguska).
- Job: reconstruct the mathematical model family, test internal consistency,
  bind what the practical campaigns actually require; CQED battle-testing
  concentrated here. Everything not load-bearing for P1–P5 → `wontfix(user)`
  candidates rather than open-ended theory review.

## D1 — Debt resolution via substrate workflow

- Input: governance/debt.yaml (33 open entries, 308 claims) — already seeded
  from extractor tags. Campaigns P1–P5 and T1 absorb their own doc entries as
  they run; D1 closes the residue with routed verdicts.

## Open question for Dan (non-blocking)

1. CQED designation: confirm default (substrate QED module family) or name
   the codebase to designate as the analysis lens.
