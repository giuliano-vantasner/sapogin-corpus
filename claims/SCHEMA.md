# Source-claim file schema (`claims/source/*.yaml`)

One file per source document. File name: `<doc_id>-<slug>.yaml` (e.g.
`AR07-proton-clusters-nuclear-size.yaml`). IDs are durable provenance keys:
allocate only after searching the registry; never reuse.

```yaml
schema: sapogin-corpus/source-claims/1
document:
  doc_id: AR07                    # <SECTION2><NN>, matches papers/MANIFEST.yaml
  section: articles               # articles|works|monography|dissertation|brochure|
                                  # lectures|patents|teaching|technologies|perpetual_motion|site
  title_ru: "Протонные зарядовые кластеры ядерных размеров"
  title_en: "Proton charge clusters of nuclear size"
  file: papers/articles/protonnye-zaryadovye-klastery-yadernyh-razmerov.pdf
  source_url: http://146.190.233.254/docs/articles/Протонные....pdf
  md5: <from papers/MD5SUMS>
  pages_total: 12                 # when known
  retrieved: '2026-08-31'
claims:
  - id: SC-AR07-001
    type: experimental            # experimental|physical|physics|mathematical
    facet: measurement            # theory|phenomenology|experiment|measurement|
                                  # recipe|material|process|procedure|schematic|geometry
    priority: core                # core|normal  (core = transmutation/catalysis/EVO/electrical path)
    page: 4                       # page in the document; for site pages use URL anchor/path
    quote_ru: "…"
    statement_en: "…"
    quantities: []                # e.g. ["I_crit(W) = 1.43e9 A/m^2", "d = 20 nm"]
    equations: []                 # LaTeX as stated in source
    materials: []                 # facet recipe/material/process: e.g. ["W film", "Al film"]
    geometry: []                  # e.g. ["film thickness: several hundred atomic layers"]
    procedure_steps: []           # ordered steps for recipe/process/procedure facets
    measurements: []              # {quantity, value, unit, conditions}
    schematic_refs: []            # figure/table numbers in the source
    tags: []
    notes: ""                     # extractor context; never interpretation of truth
    relations: []                 # [{to: SC-AR07-002, kind: supports|contradicts|generalizes|derives}]
coverage:
  extractor: <agent id>
  extracted: '2026-08-31'
  reviewed_by: null               # filled by extraction review
  zero_claim_document: false      # true for pedagogical docs with no physics claims
```

Rules:
- `id` uniqueness across the whole corpus (validator enforces).
- `page` REQUIRED for document claims; claims without a page are extraction defects.
- `quote_ru` must appear (after whitespace normalization) in the extracted
  document text (`papers/text/<slug>.txt`) — validator spot-checks this.
- `priority: core` requires one of the core topics in tags or a clear
  transmutation/catalysis/EVO/electrical statement.
- Never state agreement/disagreement with accepted physics inside `statement_en`;
  that adjudication belongs to campaigns and `governance/debt.yaml`.
