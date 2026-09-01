# Skills ported from substrate-framework

These skills were inherited from `vantasnerdan/substrate-framework`. Path
adaptations for THIS repository:

- `scripts/validate_repository.py` (substrate) → `tools/validate_corpus.py` here.
- Physics module paths in `physics-erdos-loop/references/oracles.md` and
  `SKILL.md` refer to the substrate-framework checkout at
  `~/substrate-framework/src/substrate_framework/` — that remains the oracle
  base for CQED-lens campaign analysis (see AGENTS.md "Scope amendment").
- Campaign anatomy examples in the skills live under `campaigns/` in both
  repos; campaign IDs here are `Pxxx` per cluster/path from `clusters/`.
- Review policy override (AGENTS.md): ONE commissioned review per PR, chosen
  by the user. Ignore any skill text suggesting otherwise.
