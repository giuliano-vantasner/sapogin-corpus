# catalysis — synthesis

Practical-first synthesis of the 6 claims in this bucket — the bucket is THIN, and this file
says so up front: SC-BR04-027, SC-TC06-036, SC-TC06-048, SC-TC06-050, SC-TC06-051,
SC-WO01-087 (membership from `clusters/clusters.json` bucket "catalysis"). Because 6 claims
cannot carry the mechanism question alone, this synthesis also mines the cross-bucket claims
listed under "Mechanism map" — primarily the evo-charge-clusters bucket (SC-TC08-*, SC-BR02-*,
SC-MO03-018, SC-SI05-007, SC-SI10-022, SC-TC01-006), plus tag/keyword hits in the
transmutation-adjacent and device material (SC-AR04-029, SC-TC08-113, SC-TC08-111, SC-TC08-137,
SC-PM01-011, SC-PM01-012, SC-PA03-002, SC-PA03-004). The `relations` field was checked and is
essentially unpopulated: only 39 records corpus-wide carry any relations, none touching these six
ids, and the six claims themselves have empty `relations` arrays — so the mechanism map is built
from shared tags/entities (catalysis, rossi/e-cat, patterson, mizuno, potapov, никель, керамика,
катализ), not from the relation graph. Every assertion is pinned to SC-* ids; cross-bucket pins
are marked [cross-bucket]. Verdicts come later, in campaigns; this file organizes the art, it
does not adjudicate it.

## The art (practical layer)

- **Plasmoid-assisted catalysis on tip grids.** Charge clusters and plasmoids appearing on sharp
  protrusions of metallized grids operated at high voltages — in wastewater-treatment facilities —
  are asserted to raise the catalysis rate "в десятки раз" (by tens of times). Materials:
  металлизированные сетки с острийными выступами; geometry: sharp protrusions (tips)
  (SC-BR04-027). This is the bucket's only directly catalysis-rate-quantified process claim;
  driving voltage, grid spacing, and grid material beyond "metallized" are NOT stated [GAP].
- **Nickel-powder route (Rossi E-CAT line).** In the catalytic reactions of heated nickel powder
  the solid-state plasma is heated by the temperature gradient; thermal heating + catalyst lead to
  intensive outflow of nickel's free electrons into the cold region, where they form electron
  clusters that store binding energy and, decaying, radiate it into the plasma volume, increasing
  its thermal energy (SC-TC06-050). This is the bucket's cluster→surface→catalysis mechanism
  statement.
- **Catalyst-free variant (safety + device recipe).** Thermal heating of nickel powder WITHOUT a
  catalyst reduces the growth rate of the heated-zone temperature and "the reactors stop
  exploding"; on this effect a super-unity electric-energy conversion cell is proposed: electric
  heating of nickel → temperature gradient → new electricity, resembling the thermoelectron
  converter on charge bubbles in which the point cathode is nickel and the charge-bubble
  concentration in the gap depends on the temperature gradient (SC-TC06-051).
- **Patterson / Mizuno systems (electrolytic and ceramic).** Patterson's thermal element:
  electrolysis with nickel electrodes in ordinary water; T. Mizuno, A. Samgin, A. Baraboshkin:
  conducting properties of proton ceramics; both registered anomalous heating of the conducting
  medium by current NOT fitting the classical Joule–Lenz law (SC-TC06-036).
- **Diagnostic protocol on those systems.** The anomalous heat release can be monitored for
  charge-cluster synthesis/decay: register the chaotic current component accompanying the heating;
  the area of the statistical ejection on the current–time diagram gives the mean charge of the
  synthesized electron or proton cluster; the current–time diagram should resemble B. Katorgin's.
  Electron/proton charge bubbles arise with higher efficiency in ordinary water than in heavy
  water (SC-TC06-048).
- **Cavitation/vortex heat generators (Potapov line).** Rossi's E-CAT gives excess thermal energy
  "due to catalysis"; Yu. Potapov (Kishinev, 1990) built a heat generator on a Ranque vortex-tube
  prototype; with Taganrog RESI (prof. V.I. Timoshenko, 1992), G. Sidorov and V. Kladov, heat
  generators on resonance cavitation phenomena were built with superunity conversion coefficients
  in the range 5 to 15 (SC-WO01-087, tagged debt-candidate).
- [cross-bucket] Surface preparation rule: chips/powder beat dust or foil because each chip has
  points, and on heating the points become regions where charge bubbles arise as on Shoulders'
  cathode (SC-TC08-120); reactors are claimed to run on any metal chips in vacuum, each sort having
  its own boiling/critical temperature (SC-TC08-117, SC-TC08-101).
- [cross-bucket] Electrode material palette relevant to surface catalysis: nickel, tungsten,
  copper, aluminum, nichrome, electronic silicon are the named film/electrode conductors in the
  corpus's device claims (SC-PA03-002, SC-PA03-004, SC-TC08-100 — Ni point cathode with W anode).

## Key quantities and recipes

| claim | quantity / recipe | source doc:page |
|---|---|---|
| SC-BR04-027 | Catalysis rate increase "в десятки раз" (tens of times) on metallized grids with sharp protrusions at high voltage (wastewater treatment) | BR04 p.31 |
| SC-TC06-036 | Patterson: Ni electrodes electrolysis in ordinary water; Mizuno/Samgin/Baraboshkin: proton ceramics; anomalous heating beyond Joule–Lenz | TC06 p.8 |
| SC-TC06-048 | Diagnostic: chaotic current component; ejection area on I–t diagram = mean cluster charge; ordinary water > heavy water efficiency | TC06 p.10 |
| SC-TC06-050 | Mechanism: gradient-driven electron outflow from Ni into cold region → electron clusters → decay radiates binding energy into plasma | TC06 p.11 |
| SC-TC06-051 | Catalyst-free Ni-powder heating slows heated-zone temperature growth ("reactors stop exploding"); Ni point-cathode thermoelectron cell; bubble concentration ∝ temperature gradient | TC06 p.11 |
| SC-WO01-087 | Potapov vortex-tube generator; resonance-cavitation heat generators; superunity COP range 5–15 [debt-candidate] | WO01 p.23 |
| [cross-bucket] SC-TC08-108 | Rossi 2011: Ni-Li metal chips, hydrogen 55 бар, cylindrical conducting tube, MW-class thermal output | TC08 p.39 |
| [cross-bucket] SC-TC08-109 | Tube temperature Tp = 200–500 °C, dependent on hydrogen pressure | TC08 p.40 |
| [cross-bucket] SC-TC08-123 | 60 г Ni chips; L = 0,2 м; r = 10 мм; wall 1 мм → P = 1 МВт; 16 ГВт/м³ | TC08 p.45 |
| [cross-bucket] SC-MO03-017 | Katorgin H₂ plasma: 60 А µs spike ≈ 30 мкКл ≈ 10¹⁴ частиц; conversion coefficient 2–5 | MO03 p.31 |
| [cross-bucket] SC-TC06-002 | E_decay / E_synthesis = 10²–10³ (bubble synthesis cheap, decay energy-rich) | TC06 p.1 |
| [cross-bucket] SC-BR02-027 | H₂ plasma between brass coaxial electrodes ~12 см: 1 А DC background, chaotic surges to 60 А; 30 кВт pump | BR02 p.34 |
| [cross-bucket] SC-AR04-029 | Proton-cluster Table 1: N = 2…58 protons, r2 = 2,7…14,3 fermi (Ni nucleus ≈ 5 fermi); n0 = 2·10³⁰…14·10³⁰ см⁻³; T = 500…2000 K | AR04 p.10 |

(The first six rows are the bucket's entire quantitative patrimony; the cross-bucket rows are the
numbers any surface→catalysis campaign must reckon with.)

## Testable protocols

**1. Tip-grid catalysis reactor (directly from the bucket; the art's cleanest entry).**
- Mount metallized grids with sharp protrusions (tips) as the working surface (SC-BR04-027).
- Operate at high voltage so that charge clusters/plasmoids appear on the protrusions
  (SC-BR04-027). [GAP: no voltage, gap, or grid-material values extracted — the source gives
  material class and geometry class only]
- Measure the reaction rate on/off the cluster-generating voltage; the claim to test is "×tens"
  rate increase (SC-BR04-027).
- Monitor cluster activity independently via the chaotic current component (diagnostic of
  SC-TC06-048).

**2. Ni-powder heating, catalyst vs no-catalyst A/B, with cluster diagnostics.**
- Charge a reactor with nickel powder; heat it — first with catalyst, then without (the
  no-catalyst run should show a lower heated-zone temperature growth rate; this is the stated
  explosion-safety handle) (SC-TC06-051, SC-TC06-050).
- Record current vs time throughout: look for the chaotic component; measure the area of a
  statistical ejection on the I–t diagram to estimate the mean charge of synthesized clusters;
  compare oscillograms against Katorgin's reference (SC-TC06-048).
- [cross-bucket procedure details] Heat by DC, watch for the chaotic component near the material's
  characteristic temperature, register temperature with an inductance/capacitance sensor, and run
  the vacuum-vs-hydrogen two-class discrimination (SC-TC08-119, SC-TC08-115, SC-TC08-109).

**3. Patterson-style electrolysis with proton-ceramics arm.**
- Reproduce Patterson's configuration: nickel electrodes, electrolysis in ordinary water
  (SC-TC06-036).
- In parallel, a Mizuno/Samgin/Baraboshkin-style proton-ceramics cell; in both, calorimetry against
  the Joule–Lenz expectation is the anomaly metric (SC-TC06-036).
- Apply the I–t cluster-charge diagnostic (SC-TC06-048); test the ordinary-vs-heavy-water
  efficiency claim by repeating in heavy water (SC-TC06-048).

## Phenomenology map

- **What is claimed to happen.** On high-voltage tip surfaces, clusters/plasmoids form and
  accelerate catalysis ×tens (SC-BR04-027). In heated Ni powder + catalyst, the temperature
  gradient drives free electrons into the cold region; electron clusters form, store binding
  energy, and decay-radiate it into the plasma volume — observed as excess heat (SC-TC06-050).
  In Patterson/Mizuno systems the medium heats anomalously, beyond Joule–Lenz (SC-TC06-036),
  with electron/proton bubbles arising more efficiently in ordinary than heavy water
  (SC-TC06-048). Cavitation/vortex generators (Potapov, Taganrog) are claimed at COP 5–15
  (SC-WO01-087).
- **Thresholds and knobs stated in the bucket.** The only controllable knobs named: high voltage
  on tip grids (SC-BR04-027); heating + catalyst vs heating without catalyst, which slows the
  heated-zone temperature growth (SC-TC06-051); ordinary vs heavy water (SC-TC06-048);
  temperature gradient, which sets charge-bubble concentration at a Ni point cathode
  (SC-TC06-051).
- **Mechanism map — cluster → surface → catalysis (Tiziano's key question, assembled from the
  bucket plus the mined cross-bucket claims):**
  1. SURFACE: rough/pointed surfaces are the cluster birth sites — Shoulders' tip cathode
     [cross-bucket: SC-TC03-001], Mesyats' ectons on cathode roughnesses [cross-bucket:
     SC-BR02-002], chips' points in the Rossi heater [cross-bucket: SC-TC08-120], and the
     bucket's own metallized grids with sharp protrusions (SC-BR04-027).
  2. FIELD: high voltage on those protrusions concentrates the field; autoemission is claimed at
     only 20–70 V/µm with 10⁴–10⁸ A/cm² [cross-bucket: SC-BR02-001]; formation fields 2–10 kV
     [cross-bucket: SC-DI01-001].
  3. GRADIENT: a temperature gradient pushes free electrons from hot toward cold regions — stated
     for Ni powder (SC-TC06-050) and generalized to thermoelectric separation
     [cross-bucket: SC-MO03-023]; bubble concentration in the gap follows the gradient
     (SC-TC06-051).
  4. CLUSTER: electron (or proton) clusters/bubbles form in the volume adjacent to the surface,
     store binding energy (SC-TC06-050); in the universal-mechanism framing the same
     synthesis/decay object is claimed behind Fleischmann–Pons, Mesyats' ectons, Rossi E-CAT, and
     solar-corona heating [cross-bucket: SC-MO03-018, SC-SI05-007, SC-SI10-022, SC-TC01-006].
  5. CATALYSIS EFFECT: the decay radiates stored energy into the reacting/plasma volume
     (SC-TC06-050); on grids this is asserted as catalysis-rate ×tens (SC-BR04-027); in
     electrolytic/ceramic cells as anomalous heating (SC-TC06-036); in the transmutation-adjacent
     line as Ni→Cu, Be→B, La→Ce Δz = +1 shifts [cross-bucket: SC-TC08-113] with proton clusters of
     nuclear size whose radii bracket the Ni nucleus (~5 fermi) [cross-bucket: SC-AR04-029].
  6. CONTROL/Safety: catalyst removal slows the temperature run-away (SC-TC06-051); the chaotic
     current component is the in-line signature of cluster activity at every stage
     (SC-TC06-048) [cross-bucket: SC-TC02-015].
- **Cross-bucket discipline note.** Katorgin's calorimetry (coefficient 2–5, [cross-bucket:
  SC-MO03-017]) and the Rossi numbers ([cross-bucket: SC-TC08-108/109/123]) belong to the
  evo-charge-clusters campaigns; catalysis campaigns should treat them as boundary conditions, not
  re-litigate them.
- **Replication caveats carried by the sources.** Not all excess-energy experiments repeated
  elsewhere [cross-bucket: SC-WO01-088]; the Potapov/cavitation COP 5–15 claim carries the
  debt-candidate tag in its own claim record (SC-WO01-087).

## Theory aside (secondary)

NOT load-bearing for the practical layer. The bucket's mechanism statements (SC-TC06-048,
SC-TC06-050, SC-TC06-051) rest on the "charge-bubble synthesis/decay" model: bubbles of electron
or proton charge with thin walls, whose synthesis takes little energy while decay returns
10²–10³ times more, with energy conservation explicitly asserted to fail in the process
(SC-TC06-002 [cross-bucket, debt-candidate], SC-TC06-048). The universal-mechanism claim — one
synthesis/decay object behind cold fusion, ectons, E-CAT, and the solar corona — is
[cross-bucket: SC-MO03-018, debt-candidate]; the Rossi four-way mechanism dispute (cold
synthesis vs ХТЯ transmutation vs K-capture/cold decay vs displacement-current electrophysics) is
[cross-bucket: SC-TC08-137, SC-TC08-111, SC-TC08-113, SC-TC08-136, SC-PM01-012], and Sapogin's
own two-class discriminating measurement (vacuum vs hydrogen) is the theory-adjacent experiment
that would separate them [cross-bucket: SC-TC08-115]. The proton-cluster-of-nuclear-size model
that would connect catalysis surfaces to transmutation signatures is pure theory: α = 3,
β = 10⁻⁷, N = 2…58 retained protons, r2 = 2,7…14,3 fermi [cross-bucket: SC-AR04-029,
debt-candidate]. Debt-candidate linkage: SC-WO01-087 is in-bucket tagged (see
`clusters/debt-candidates.md`, WO01 and TC06 lists); of the cross-bucket ids cited in this
aside, SC-TC06-002, SC-MO03-018, SC-TC08-111, SC-TC08-113, SC-TC08-137, SC-PM01-012 and
SC-AR04-029 carry the debt-candidate tag in that registry under their docs, while SC-TC08-115
and SC-TC08-136 are extractor-unflagged. None of these models is
needed to run the three testable protocols above; all of them are what the protocols would
adjudicate.

## Open questions for campaigns

1. Quantify the tip-grid effect: what voltage, grid geometry, and chemistry produce the "×tens"
   catalysis-rate increase, and is the effect thermal (local heating) or non-thermal? Only
   SC-BR04-027 speaks to it, with no numbers beyond "десятки раз" [GAP in the corpus itself].
2. Does the chaotic-current diagnostic (SC-TC06-048) correlate quantitatively with catalysis rate
   or excess power — i.e., can ejection-area cluster charge serve as the process-control variable
   the art implies?
3. Patterson replication: Ni electrodes in ordinary water, calorimetry vs Joule–Lenz, and the
   ordinary-vs-heavy-water efficiency ordering (SC-TC06-036, SC-TC06-048).
4. Catalyst A/B: verify that removing the catalyst from heated Ni powder genuinely slows the
   temperature run-away (the "reactors stop exploding" claim, SC-TC06-051) — this is a cheap,
   high-information experiment.
5. Surface preparation law: how do protrusion radius/roughness/chip-point density scale cluster
   production — grid tips (SC-BR04-027) vs Shoulders tip cathode vs Rossi chips [cross-bucket:
   SC-TC03-001, SC-TC08-120]?
6. Which mechanism branch does the surface effect feed: electron-cluster decay heating
   (SC-TC06-050), transmutation Δz = +1 [cross-bucket: SC-TC08-113, SC-AR04-029], or plain
   displacement-current electrophysics [cross-bucket: SC-TC08-115, SC-PM01-012]? The vacuum-vs-H₂
   A/B [cross-bucket: SC-TC08-115] discriminates the first pair.
7. Proton clusters in proton ceramics: Mizuno/Samgin/Baraboshkin's proton-conducting cells
   (SC-TC06-036) are the natural host for the proton-cluster model [cross-bucket: SC-AR04-029] —
   can proton-cluster charge be measured by the I–t diagnostic of SC-TC06-048?
8. The cavitation/vortex line (Potapov, Taganrog, COP 5–15) is a debt-candidate claim with no
   in-corpus calorimetry: acquire or run the calorimetry or scope it out (SC-WO01-087).
