# Sapogin Corpus Agent Contract

This repository extracts the complete claim inventory of Vladimir G. Sapogin's
"Canonical Physics" (https://sapogin.com/ and its hosted documents), clusters
it into coherent physics paths with GitNexus, and then works each cluster as a
substrate-framework-style campaign whose job is debt resolution: verify,
refute, bound, or precisely scope every meaningful experimental, physical,
physics, and mathematical claim.

Governance is inherited from `vantasnerdan/substrate-framework` (AGENTS.md,
memory-templates, `.agents/skills/`) and adapted here. When a rule below
differs from the substrate contract, this file wins for this repository.

## Scope amendment (Tiziano via Dan, 2026-08-31)

Beyond the four content types, extraction targets the PRACTICAL layer:
phenomenology, experiments, measurements, recipes, materials, processes,
procedures, schematics, and geometry. Every claim carries a `facet` from that
list (or `facet: theory` for pure assertions), and claims touching isotope
transmutation, catalysis, EVO/charge-cluster generation, or the electrical
experimental path are flagged `priority: core`.

The corpus must answer, from Sapogin's own sources: why do charge clusters
(EVOs) help with catalysis and (possibly) EVO generation — including the
materials, geometries, procedures, and measurements he reports. This is KEY
for the next steps of the electrical path. Transmutation-relevant content
(e.g. "Протонные зарядовые кластеры ядерных размеров") gets first-class
extraction: nuclear signatures, isotope shifts, energy balances, input power,
electrode materials and geometry.

Analysis lens: adjudicate practical-layer claims with OUR OWN CQED framework
— default base: the substrate-framework QED module family
(`effective_actions`, `coherent_states`, `bosonic_fock`,
`dirac_vacuum_polarization`) — as deliberate battle testing of that
framework. If the user designates a different CQED codebase, record it in
`governance/policy.yaml` (`analysis_lens`) and rebind before campaign work.

Campaign ordering is FIXED: practical/phenomenology clusters FIRST; their
mathematical models and physical theory are examined AFTER the practical
layer has been worked.

## Two-layer claim model

1. **Source claims** (`claims/source/*.yaml`, IDs `SC-*`): what Sapogin and his
   sources assert. Extracted verbatim-faithful, provenance-pinned (document,
   page, quote in Russian + English translation, document MD5). Source claims
   are data, not doctrine: `epistemic: extracted`, never edited after
   extraction review except by a recorded erratum. Extraction is complete only
   when every site page and every downloaded paper is covered by a reviewed
   claim file.
2. **Corpus claims** (`governance/claims.yaml`, IDs `GC-*`): claims THIS
   project has adjudicated through a campaign (verified, refuted, bounded, or
   scoped). They follow the substrate authority order:
   accepted release > accepted claim registry > adjudicated campaign >
   proposal > attempt.

Debt is a named gap in the corpus: a contradiction between source claims, a
conflict between a source claim and accepted physics, an internal
inconsistency, or an untestable-but-load-bearing assumption. Debt entries live
in `governance/debt.yaml`; campaigns resolve them. Resolved debt is marked,
never deleted.

## Anti-gate-ceremony-theater (binding)

Theorems and physics paths are built by emergence and over-determination;
excessive pre-gating starves them. Therefore, as in the substrate contract:

- Every gate must name the concrete failure mode it prevents and what it would
  have changed in a past attempt. A gate with no such pedigree is removed.
- Every attempted route terminates in exactly one route-scoped verdict:
  established as stated, refuted with the mechanism named, or blocked with the
  missing construction named. `qualified` is a waypoint, never a resting place.
- A failed route is a branch point: execute the continuation ladder (method
  repair, reformulation, materially different candidate) or show a step
  inapplicable. Single-route termination and recursive claim weakening are
  both systemic failure modes.
- After a claim survives two independent evidence passes, further narrowing
  requires new contrary evidence, not new caution. When successive reviews
  keep shrinking a claim without such evidence, the review chain — not the
  claim — is failing; escalate to the user instead of narrowing again.
- Scope reduction must change what downstream work can conclude. Reduction
  that leaves no consumer better-informed is drift, not honesty.

## Extraction rules

- Faithfulness is the extraction oracle: a source claim must be
  reconstructible from its quote + page. Never merge two assertions into one
  claim ID; never let the extractor's interpretation enter the statement
  field (interpretation belongs to `notes` or later campaign work).
- Every claim carries `type` (experimental | physical | physics |
  mathematical), `facet`, the source document's MD5, page, and the
  original-language quote.
- Numerical claims store exact values with units as stated in the source, plus
  the quoted sentence. Do not silently convert units.
- The four extraction categories:
  - `experimental`: an asserted measurement, observation, or laboratory effect.
  - `physical`: an asserted physical mechanism, phenomenon, or interpretation.
  - `physics`: theory-level assertions (models, laws, derivational claims).
  - `mathematical`: equations, identities, solutions, and pure-math claims.
- The `facet` axis (practical layer, per the scope amendment): theory |
  phenomenology | experiment | measurement | recipe | material | process |
  procedure | schematic | geometry. Practical facets additionally store
  structured fields: `materials`, `geometry` (dimensions with units),
  `procedure_steps`, `measurements` (quantity, value, unit, conditions),
  `schematic_refs`.
- `priority`: `core` (transmutation / catalysis / EVO generation / electrical
  path) | `normal`.
- Translation: English statement must preserve asserted strength ("proves",
  "explains", "suggests") — no hedging drift in either direction.
- Coverage is tracked in `claims/coverage.yaml` (document → claim file →
  reviewer). A document with zero physics claims still gets a coverage entry
  stating so (e.g. pedagogical material).

## Download and provenance rules

- Every paper lives in `papers/<section>/` with its original filename
  transliterated to ASCII; `papers/MANIFEST.yaml` pins section, source URL,
  mirror URLs, MD5, byte size, and retrieval date. `papers/MD5SUMS` is
  regenerated on every change.
- Provenance travels with the corpus: PDFs are committed. If a host forbids
  redistribution, record that in MANIFEST and keep the hash + URL instead of
  the bytes.
- Google Drive mirrors are fetched to stable archive copies; the MANIFEST maps
  original drive IDs to corpus filenames.

## Campaigns (debt resolution)

Each cluster/path from the GitNexus clustering becomes a campaign under
`campaigns/<Pxxx-name>/` following the substrate campaign anatomy:
`proposal.yaml` (frozen objective, success gates, debt targets), `attempts/`,
`evidence/`, `reviews/`, `adjudication.yaml`, `claim-draft.yaml`.

- Campaign objective: resolve named debt (verify, refute, bound, or scope the
  source claim). A campaign that merely restates sources without adjudicating
  debt has not met its objective.
- Practical/phenomenology campaigns run first; theory campaigns follow.
- Verification is executed, never narrated: cite an executed script result
  (SymPy, numerical reproduction, literature cross-check with pinned source,
  experiment data audit). Prose reading and mental arithmetic are not
  verification. Mid-oracle crashes get fixed and re-executed.
- External literature used to adjudicate a source claim is acquired under the
  paper-sourcing discipline: pinned PDF + extracted text + MD5SUMS under the
  campaign's `sources/`. URL citation without committed bytes is a grounding
  failure (learned 2026-08-31, PR #190).
- Terminal campaign-PR gates, exhaustion certificates, bounded constructive
  review, issue-first PRs, `Advances #N`/`Fixes #N`, and the no-self-merge
  default all carry over from the substrate contract unchanged.

## Review policy (user directive 2026-08-31)

- Exactly ONE commissioned independent review per PR. Reviewers are chosen by
  the user (Dan). Unsolicited drive-by reviews are not review-of-record; do
  not treat them as gates, and do not invite them.
- Review of extraction is a faithfulness check (quote ↔ claim ↔ page) plus
  coverage completeness. Review of campaigns is substrate-style bounded
  constructive review of the frozen transaction.

## Workflow

1. Extraction loop (≤3 parallel subagents): inventory → download → extract →
   validate → review → coverage. `tools/validate_corpus.py` must pass before
   any commit of claims.
2. Clustering: `gitnexus analyze`, then semantic clustering over claim
   statements; write `clusters/<name>.md` (claims, path narrative, debt
   candidates). Clusters are proposals until the user accepts the campaign
   split.
3. Campaigns: one per cluster/path; practical layer first; substrate anatomy;
   resolve debt via CQED-lens analysis; promote `GC-*` claims through
   individual review into `governance/claims.yaml`; release manifests pin
   accepted sets.
4. Memory: durable session state via the agent-memory CLI; validate after
   every write (zero warnings).

## Tooling

- `tools/validate_corpus.py` — schema, ID uniqueness, provenance (MD5 +
  MANIFEST cross-check), coverage completeness, debt lint.
- `tools/build_jsonl.py` — emit `claims/claims.jsonl` (one record per claim,
  flattened, with document metadata) for GitNexus ingestion.
- GitNexus: `gitnexus analyze` (graph + FTS + vector). Claims are ingested as
  `claim` nodes via the JSONL loader in `tools/gitnexus_ingest.py`; clustering
  queries use `gitnexus cypher`.

## Code layout (Dan, 2026-09-01)

Code in this repo follows separation of concerns: the directory tells the
architecture story at a glance, and each file owns exactly one
responsibility (the `code-structure` skill carries the pattern). The reward
is direct: mlops-kelvin and axis-marbell — or any new agent — can land,
review, and change the code without a guided tour. Known debt:
`tools/serve_web.py` (HTTP plumbing, routes, API payloads, MCP, and served
text assets in one file) and the monolithic `web/app.js`; the commissioned
cleanup pass will split them. Land new web/tools work as separate modules
from the first line and keep the split structure on every later change.

## Agent conduct

- The user's word is absolute. Dan's steering (executed verification, scope
  discipline, review policy) overrides any convention here.
- Never send email, post GitHub comments, or push public repos without
  explicit user approval for that exact action.
- Subagents: ≤3 concurrent (user directive). Each subagent task states its
  frozen slice, schema, and acceptance checks; subagents do not run repo-wide
  validators mid-flight.
- Gitops (Dan, 2026-09-01): main is home; the cycle is dev on a short-lived
  branch → push → merge to main (PR when a commissioned review is attached)
  → delete the branch (head and fork) in the same session. Stale branches
  are swept on sight. Main should always answer "what is deployed" at a
  glance.
