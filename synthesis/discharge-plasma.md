# discharge-plasma — synthesis

Practical-first synthesis of the 97 claims in this bucket. The bulk is the
eddy-current (Foucault) inductance program: AR07's cylindrical-film theory
(46 claims) with its negative-inductance states, film-thickness windows,
and chip-inductor design tables, plus MO01's macroscopic brass-rod and
microsolenoid experiments and the current-cord phenomenology. The second
strand is conductor explosion at critical current density in
sub-5-nm/few-hundred-atomic-layer films (TC04, SI10, SI01) with the
Marakhtanov thresholds. The remainder is discharge device support
(Zhuravkov subcritical discharge, Katorgin–Marin plasma insert), the
Maxwell–Ohm solution census behind skin effect vs current crowding
(SI01, WO04), and a peripheral astrophysical tail (PM02 invisible
bubbles). Cross-bucket: the devices that consume these inductances and
discharges are synthesized in synthesis/electrical-devices.md (notably
SC-AR07-037 and PA01–PA03 there); the charge-bubble phenomenology these
forces are meant to explain is in synthesis/transmutation-nuclear.md.
Every assertion is pinned to SC-* ids. Verdicts come later, in campaigns;
this file organizes the art, it does not adjudicate it.

## The art (practical layer)

- **Wire-explosion thresholds (Marakhtanov experiment — the hard numbers of
  this bucket)**: current passed through metal films of several hundred
  atomic layers with cooled-metal temperature fixed at 180 °C; at current
  densities above 1.43·10⁹ А/м² in tungsten and 8.04·10⁹ А/м² in aluminum
  the conductors exploded within microseconds (SC-TC04-014). Generalization:
  nanometer-diameter conductors always explode — the lattice is torn by
  electric-field-pressure-gradient forces — and lowering the current density
  only stretches the time to "Armageddon" (SC-TC04-015, SC-SI01-029)
  (debt-candidate). Industrial symptom: sub-5-nm transistors in Chinese
  fabs began exploding (SC-SI10-001, SC-TC04-001).
- **Hollow-current-cavity regime**: straight current in a cylindrical
  conductor of diameter ≤ 20 nm at gigahertz frequencies is squeezed out by
  the skin effect so strongly that a charge-free cylindrical cavity forms
  inside the current (SC-TC04-002, SC-TC04-011) (debt-candidate).
- **CFICR chip inductor design (conducting film inside current ring)** —
  the constructive payoff of the eddy-current program: an additional thin
  film h₂ << h₁, radius R < R₁, no galvanic contact, placed inside a
  single-turn film ring (SC-AR07-037 — full recipe in the electrical-devices
  bucket; patents SC-PA03-001 there). Working numbers from this bucket:
  - Fixed inductance 10 нГн: h = 50, 100, 150, 200, 250, 300, 350, 400,
    450, 500 нм ↔ R = 16, 23, 28, 32, 36, 39, 42, 45, 48, 50 мкм; above
    500 nm the single elementary current vortex may destabilize into the
    dynamic state (SC-AR07-034).
  - Flux-inductance table at R = 50 мкм: h₂ = 50…350 нм →
    L_Φ = 100, 50, 33.3, 25, 20, 16.7, 14.3 нГн (SC-AR07-039); total
    inductance L = L_к + L_Φ (SC-AR07-038, electrical-devices bucket).
  - Material choice shifts the frequency window at fixed geometry:
    f* scales with resistivity — copper 15.5·10⁻⁹ Ом·м → 3.14·10⁶ Гц;
    aluminum 25.0·10⁻⁹ → 5.0·10⁶; tungsten 48.9·10⁻⁹ → 10.0·10⁶; nickel
    61.4·10⁻⁹ → 12.4·10⁶; nichrome 1.0·10⁻⁶ → 203·10⁶; electronic silicon
    КЭФ 1.0·10⁻³ → 203·10⁹ Гц (SC-AR07-040); resistivity does not change
    the inductance value, only the window (SC-AR07-040).
  - Recipe: Al film R = 50 мкм, h₂ = 100 нм gives 50 нГн over 0.5–50 МГц;
    nichrome same geometry 20 МГц–2 ГГц; copper 0.3–30 МГц; tungsten
    1–100 МГц; nickel 1.2–120 МГц; silicon 20 ГГц–2 ТГц (SC-AR07-041).
  - Payoff claim: 100→14 нГн usable, 7–50× the best single-layer CMOS
    inductance; working range 0.1f* < f < 10f*; surface inductance density
    up to ~10 Гн/м² (SC-AR07-042, SC-AR07-035); baseline single-turn
    rings give only 0.5–3.5 нГн at 20–100 мкм sizes (SC-AR07-036).
- **Three eddy-current inductance states (the state-selection map)**:
  - Frequency-dependent dynamic inductance with two zeros F₁ < F₂
    (macroscopic cylinders): L/L* = (1 + β²/3 − 2πβ)/β², zeros at
    F₁/f* ≈ 0.1605 and F₂/f* ≈ 18.69, minimum L_min ≈ −9.536 L* at
    0.3183 f*, high-frequency limit L* /3 (SC-AR07-019, SC-AR07-020)
    (debt-candidate); scales L* = μ₀πR²/h and f* = 2ρ/(μ₀πR²)
    (SC-AR07-017, SC-AR07-019).
  - Frequency-independent negative flux inductance in conducting cylinders
    (h > 1 мкм, h > R regime, orientation σ = +1): response field opposes
    B₀ over the half-period, giving a negative half-period-averaged flux
    (SC-AR07-033, SC-AR07-028); value L_Φ = μ₀πR²/2h, geometry-only
    (SC-AR07-031).
  - Frequency-independent positive flux inductance in ultra-thin films:
    orientation σ = −1 appears only in films tens-to-hundreds of nm thick —
    the extracted window is 10 to 500 nm — showing "weak ferromagnetism"
    (SC-AR07-027, SC-AR07-032) (debt-candidate).
- **Multilayer-film experiments to hit**: Al/Cu double layers of 200 nm per
  double layer — from six layers up, L(f) develops negative segments;
  two double layers give positive, practically frequency-independent L
  (SC-AR07-007, SC-AR07-008); zero counts: two zeros on six layers, one on
  ten, none on thirty (SC-AR07-021); earlier planar data: NGS/PGS quality
  factor peaks near 2 GHz and falls to zero near 7–8 GHz; RPGS cylindrical
  build confirmed both and showed inductance reaching zero then negative at
  GHz (SC-AR07-004, SC-AR07-005) (debt-candidate).
- **Macroscopic bench replication (cheap)**: brass cylinder 192 ± 1 mm long,
  7.0 ± 0.5 mm diameter inside a 23.0 ± 0.5 mm measuring solenoid of 98
  turns of 0.23 mm wire, L₀ = 21.0 мкГн, resonance method over 9 kHz–1.1
  МГц (SC-MO01-014); result: negative frequency-independent flux
  inductance, 0.1–100 МГц, volume density 11.5 Гн/м³, diamagnetic
  susceptibility −0.5, elementary current layer ≈ 100 нГн with layer width
  equal to the wire diameter (SC-MO01-016).
- **Current cord (anti-skin phenomenology to watch for)**: Kuhn & Ibrahim
  (2001) found AC at GHz forming a spatially localized current cord that
  shrinks with frequency — ohmic resistance and inductance rise, Ohm's law
  fails (SC-MO01-003); ribbon microsolenoids show inductance rising with
  frequency up to a cutoff where the cord collapses, then inductive
  properties vanish (SC-MO01-002; jitter/cutoff detail SC-MO01-004 —
  electrical-devices bucket); single planar inductors cut
  off near 1 ГГц, with cord cross-section ~order below conductor
  cross-section (SC-MO01-009); two-layer opposite-direction currents give
  the largest inductance; cylindrical symmetry avoids cord-kinking losses
  (SC-MO01-011, SC-MO01-009).
- **Zhuravkov subcritical discharge**: breakdown field 250 В/мм, realizable
  at mains voltage; ignited at point-to-plate distance ≈ 1 mm at hundreds
  of volts — proposed as the low-voltage plasma source inside displacement-
  current "reactors" (SC-TC02-045; ignition geometry SC-TC02-044 —
  electrical-devices bucket; recipe consumer there too).
- **Katorgin–Marin plasma insert (the discharge cautionary tale)**: 30 kW
  hydrogen-plasma insert; most of the displacement current exits as harmful
  unshieldable radiation (SC-TC03-027); the F–P cell's missed plasma layer
  at the palladium electrode is the liquid-phase cousin (SC-TC01-045 —
  electrical-devices bucket).
- **Cathode-beam reference table (beam devices)**: eight cathode types
  tabulated at 100 eV — e.g. tantalum 0.5 А/см², 2300 K → beam ⌀350 мкм,
  480 мкА; tungsten 7.3 А/см², 2700 K → 100 мкм, 570 мкА; lanthanum
  hexaboride 20.4 А/см², 2100 K → 53 мкм, 450 мкА; monocrystalline tungsten
  10⁶ А/см², 300 K → 0.09 мкм, 64 мкА (SC-DI02-008).
- **Design dichotomy to respect**: film vs cylinder is set by h < R (film),
  h << R (thin film), h > R (cylinder) (SC-AR07-011); σ = −1 lives in
  10–500 nm films, σ = +1 in macroscopic cylinders with h >> 1 мкм
  (SC-AR07-027, SC-AR07-028); above 500 nm thickness a film's single
  elementary vortex can jump to the dynamic state (SC-AR07-034).
- **Peripheral but extracted**: indicator experiments showing EM field
  weakening with distance from an AC cord and partial absorption by plaster
  (SC-TE07-006, SC-TE07-007); PM02's invisible-bubble tail (momenta
  2.5·10⁸…2.5·10⁵ кг·м/с for solar-ejected liquid-wall bubbles) is
  astrophysical speculation inside this bucket, not device-relevant
  (SC-PM02-017, SC-PM02-018, SC-PM02-019) (debt-candidate).

## Key quantities and recipes

| claim | quantity / recipe | source doc:page |
|---|---|---|
| SC-TC04-014 | explosion thresholds @180 °C: W > 1.43·10⁹ А/м²; Al > 8.04·10⁹ А/м²; films of several hundred atomic layers; µs | TC04 p.3 |
| SC-TC04-002 | d ≤ 20 nm at GHz → charge-free hollow current cavity | TC04 p.1 |
| SC-SI10-001 | sub-5-nm transistors explode in production | SI10 § |
| SC-AR07-019 | L/L* = (1 + β²/3 − 2πβ)/β²; L* = μ₀πR²/h | AR07 p.7 |
| SC-AR07-017 | β = μ₀πR²f/2ρ = f/f*; f* = 2ρ/(μ₀πR²) | AR07 p.6 |
| SC-AR07-014 | eddy current density scale j* = πfB₀R/ρ | AR07 p.5 |
| SC-AR07-015 | volume heat-power scale p* = π²f²B₀²R²/ρ | AR07 p.5 |
| SC-AR07-020 | F₁/f* ≈ 0.1605; F₂/f* ≈ 18.69; L_min ≈ −9.536 L* @0.3183 f*; L∞ = L*/3 | AR07 p.8 |
| SC-AR07-031 | flux inductance L_Φ = μ₀πR²/2h (frequency-independent) | AR07 p.15 |
| SC-AR07-027 | σ = −1 window: film thickness 10–500 nm → positive frequency-independent L | AR07 p.15 |
| SC-AR07-028 | σ = +1: cylinders h > R, >> 1 µm → strong diamagnetism | AR07 p.12 |
| SC-AR07-007 | Al/Cu double layers 200 nm; negative-L segments from 6 layers | AR07 p.3 |
| SC-AR07-008 | two double layers: positive, frequency-independent L | AR07 p.2 |
| SC-AR07-021 | L zeros: 2 (6 layers), 1 (10 layers), 0 (30 layers) | AR07 p.8 |
| SC-AR07-004 | NGS/PGS: Q max near 2 GHz, zero near 7–8 GHz | AR07 p.2 |
| SC-AR07-034 | 10 нГн fixed: h = 50…500 нм ↔ R = 16…50 мкм; >500 nm unstable | AR07 p.16 |
| SC-AR07-039 | R = 50 µm: h₂ = 50…350 нм → L_Φ = 100…14.3 нГн | AR07 p.17 |
| SC-AR07-040 | f* by material: Cu 3.14 МГц; Al 5.0; W 10.0; Ni 12.4; нихром 203 МГц; Si 203 ГГц | AR07 p.16 |
| SC-AR07-041 | recipe: Al 50 нГн @0.5–50 МГц; нихром 20 МГц–2 ГГц; Cu 0.3–30 МГц; W 1–100 МГц; Ni 1.2–120 МГц; Si 20 ГГц–2 ТГц | AR07 p.19 |
| SC-AR07-042 | 7–50× CMOS single-layer inductance (100→14 нГн) | AR07 p.19 |
| SC-AR07-035 | working range 0.1f* < f < 10f*; up to ~10 Гн/м² surface density | AR07 p.17 |
| SC-AR07-036 | single-turn baseline: 0.5–3.5 нГн at 20–100 µm | AR07 p.17 |
| SC-MO01-014 | brass rod 192±1 mm × 7.0±0.5 mm; solenoid 23.0±0.5 mm, 98 turns, 0.23 mm wire, L₀ = 21.0 µH; 9 kHz–1.1 MHz | MO01 p.219 |
| SC-MO01-016 | negative flux L: 11.5 Гн/м³; χ = −0.5; layer ≈ 100 нГн; width = wire diameter | MO01 p.227 |
| SC-MO01-003 | Kuhn–Ibrahim 2001 current cord at GHz | MO01 p.9 |
| SC-MO01-009 | single planar inductor cutoff ~1 ГГц | MO01 p.173 |
| SC-TC02-045 | Zhuravkov subcritical discharge: E_breakdown = 250 В/мм | TC02 p.14 |
| SC-TC03-027 | Katorgin–Marin insert 30 кВт; harmful radiation | TC03 p.7 |
| SC-DI02-008 | cathode table: LaB₆ 20.4 А/см² → 53 µm/450 µA; mono-W 10⁶ А/см², 300 K → 0.09 µm/64 µA | DI02 p.261 |

## Testable protocols

- **Brass-rod negative flux-inductance replication** (SC-MO01-014,
  SC-MO01-016):
  - Materials: brass cylinder; copper magnet wire.
  - Geometry: rod 192 ± 1 mm × ⌀7.0 ± 0.5 mm; measuring solenoid 23.0 ±
    0.5 mm long, 98 turns of 0.23 mm wire, pre-measured L₀ = 21.0 мкГн
    (V7-80 inductance mode) (SC-MO01-014).
  - Procedure: 1) pre-measure the empty solenoid (SC-MO01-014); 2) insert
    the rod and take the resonance-method L(f) curve at five points over
    9 kHz–1.1 МГц (SC-MO01-014); 3) extend to 0.1–100 МГц and fit the
    negative frequency-independent flux inductance (SC-MO01-016); 4) check
    the reported signatures: 11.5 Гн/м³ volume density, χ = −0.5,
    elementary layer ≈ 100 нГн with width equal to wire diameter
    (SC-MO01-016). [GAP] no extracted bridge circuit diagram for the
    resonance readings.
- **Multilayer Al/Cu negative-inductance sweep** (SC-AR07-007, SC-AR07-008,
  SC-AR07-021):
  - Materials: alternating aluminium/copper layers; substrates as in the
    Ohio work.
  - Geometry: double layers (Al + Cu) of 200 nm each; stack counts 2, 6,
    10, 30 (SC-AR07-007, SC-AR07-021).
  - Procedure: 1) deposit the stack; 2) measure L(f) per stack count;
    3) count inductance zeros — expected 2 (6 layers), 1 (10 layers),
    0 (30 layers), negative segments from six layers up (SC-AR07-021,
    SC-AR07-007); 4) two-layer control must show positive
    frequency-independent L (SC-AR07-008). [GAP] no extracted lithography,
    contact, or fixture details.
- **CFICR 50 нГн film-in-ring inductor** (SC-AR07-039, SC-AR07-040,
  SC-AR07-041, SC-AR07-034; construction claim SC-AR07-037 and patent
  SC-PA03-001 live in the electrical-devices bucket):
  - Materials: aluminum film (or Cu/W/Ni/nichrome/Si per the frequency
    band wanted) (SC-AR07-041).
  - Geometry: current ring + inner film R = 50 µm, h₂ = 100 nm, h₂ << h₁,
    R < R₁ (SC-AR07-037, SC-AR07-039).
  - Procedure: 1) pattern the single-turn ring; 2) deposit the electrically
    isolated inner film (SC-AR07-037); 3) verify L between terminals
    against the table (50 нГн expected for Al @100 nm) (SC-AR07-039);
    4) confirm the frequency-independence window (0.5–50 МГц for Al)
    (SC-AR07-041); 5) keep h₂ ≤ 500 nm to stay in the single-vortex state
    (SC-AR07-034).
- **Marakhtanov film-explosion threshold test** (SC-TC04-014):
  - Materials: tungsten and aluminum films of several hundred atomic
    layers.
  - Geometry/conditions: cooled-metal temperature fixed at 180 °C
    (SC-TC04-014).
  - Procedure: 1) prepare W and Al films; 2) hold 180 °C; 3) ramp current
    density; 4) record explosion threshold and time — claimed:
    > 1.43·10⁹ А/м² (W), > 8.04·10⁹ А/м² (Al), explosion within µs
    (SC-TC04-014). [GAP] no extracted substrate, atmosphere, or film-area
    details; oscillography method unstated.
- **Zhuravkov subcritical discharge ignition** (SC-TC02-045; ignition
  geometry SC-TC02-044 — electrical-devices bucket):
  - Materials: point electrode facing a capacitor plate; mains-derived HV
    supply.
  - Geometry: point-to-plate ≈ 1 mm in air (SC-TC02-044, electrical-devices
    bucket).
  - Procedure: 1) apply rising voltage at hundreds of volts; 2) confirm
    ignition below the ~2.5 kV/mm-scale ordinary breakdown, consistent
    with the quoted 250 В/мм subcritical field (SC-TC02-045);
    3) (per the consuming recipe) substitute these electrodes for the
    reactor's planar electrodes and compare converter efficiency
    (SC-TC02-044 — electrical-devices bucket). [GAP] no extracted electrode
    material or tip radius.

## Phenomenology map

- **Inductance states vs scale** — the bucket's organizing observation
  ladder: ultra-thin films (10–500 nm) show positive frequency-independent
  L ("weak ferromagnetism") (SC-AR07-027, SC-AR07-032); thin multilayers
  (≥6 double layers of 200 nm) develop negative L(f) segments with
  countable zeros (SC-AR07-007, SC-AR07-021); macroscopic rods show
  negative frequency-independent flux inductance with χ = −0.5
  (SC-MO01-016); solid cylinders show the two-zero dynamic curve with
  L_min ≈ −9.536 L* (SC-AR07-020); integrated planar structures show Q(f)
  peaking near 2 GHz and collapsing near 7–8 GHz (SC-AR07-004).
- **Current localization**: GHz currents cord (Kuhn–Ibrahim), shrinking
  cross-section, defeating Ohm's law (SC-MO01-003); ribbon microsolenoid
  inductance rises then dies at cutoff (~1 ГГц single inductors)
  (SC-MO01-002, SC-MO01-009; SC-MO01-004 — electrical-devices bucket);
  sub-20-nm wires at GHz hollow
  out entirely (SC-TC04-002, SC-TC04-011).
- **Explosive endgame**: same field-pressure-gradient forces claimed to
  tear nanofilms/nanowires apart above material-dependent thresholds
  (W 1.43·10⁹ А/м², Al 8.04·10⁹ А/м² at 180 °C, µs) (SC-TC04-014,
  SC-TC04-015, SC-SI01-029); industrially visible as exploding sub-5-nm
  transistors (SC-SI10-001, SC-TC04-001).
- **Discharge phenomenology**: subcritical 250 В/мм point discharge
  (SC-TC02-045); hydrogen-plasma insert at 30 kW radiating most of its
  displacement current harmfully (SC-TC03-027, SC-TC01-046); thin plasma
  layer at the F–P palladium electrode (SC-TC01-045); Mesyats ectons and
  Katorgin's current-discreteness as the discharge-face of the same
  cluster picture (SC-SI10-011).
- **Astrophysical tail (not device-relevant)**: Sun as a thin-wall plasma
  bubble at 10⁷ K (SC-SI01-035, SC-WO04-021); invisible liquid-wall
  bubbles with train-like momenta as a claimed spacecraft hazard
  (SC-PM02-017–SC-PM02-019) (debt-candidates).

## Theory aside (secondary)

The AR07 model assumes a uniform axial B₀cos(ωt), azimuthal-only vortex
field (betatron orientation), linear radial profiles E₀(r) = E*·r/R with
E* = πfB₀R, Ohmic closure j = E/ρ, and a response field B₁ with B₁* = βB₀;
the energy balance ⟨W⟩ = W_q + L⟨i²⟩/2 then yields L/L* = (1 + β²/3 −
2πβ)/β² (SC-AR07-013–SC-AR07-019). Admitted limitations: an unremovable
1/f² singularity at ultra-low frequency (dynamic L never limits to static
L), restricting validity to ≳100 МГц (SC-AR07-022, SC-AR07-023); neglecting
the radial response component B₁r is repaired by the second parameter α,
which shifts the zeros (β₁, β₂ table for α = 0…27) and kills negative L
beyond α₀ = 3π² − 1 ≈ 28.6, with solid films measured near α ≈ 0
(SC-AR07-024, SC-AR07-025). The σ = ±1 orientation dichotomy that selects
film vs cylinder states is stated but not mechanized (SC-AR07-027,
SC-AR07-028, SC-AR07-032 — debt-candidates). The interpretive frame claims
one universal field-pressure force explains skin effect, current crowding,
hollow current tubes, and nanowire explosions alike (SC-SI01-006,
SC-WO04-019, SC-SI01-022, SC-BR04-033 — shared with the transmutation
bucket's gasostatics; debt-candidates). None of this interpretive layer is
load-bearing for the design tables above: L_Φ = μ₀πR²/2h, the h↔R tables,
and the material frequency scales (SC-AR07-031, SC-AR07-034, SC-AR07-039,
SC-AR07-040) are checkable geometry arithmetic. Debt-candidate registry:
clusters/debt-candidates.md (AR07, TC04, WO04, SI01, PM02 entries).

## Open questions for campaigns

1. Symbolic/numeric re-derivation of the dynamic-inductance curve: are
   F₁/f* = 0.1605, F₂/f* = 18.69, L_min = −9.536 L*, L∞ = L*/3
   (SC-AR07-020) exact consequences of L/L* = (1 + β²/3 − 2πβ)/β²
   (SC-AR07-019)?
2. Bound the model: design the ultra-low-frequency experiment the source
   itself calls for to locate the cutoff below which L(f) ~ 1/f² diverges
   from experiment (SC-AR07-022, SC-AR07-023).
3. Fit the Ohio multilayer data (200 nm Al/Cu, 6/10/30 layers): does
   β = μ₀πR²f/2ρ with the real stack geometry reproduce the observed
   zero-count pattern 2/1/0 (SC-AR07-007, SC-AR07-021)?
4. What physical mechanism selects σ = −1 in 10–500 nm films vs σ = +1 in
   cylinders (SC-AR07-027, SC-AR07-028, SC-AR07-032)? No mechanism is
   extracted — [GAP] blocking first-principles design beyond the tables.
5. Threshold ratio puzzle: W:Al explosion thresholds are 1.43 vs
   8.04·10⁹ А/м² (~1:5.6) while their resistivities (~48.9 vs
   ~25.0·10⁻⁹ Ом·м per SC-AR07-040's material table) differ ~1:2 — what
   sets the threshold (SC-TC04-014, SC-TC04-015)?
6. Reproduce the brass-rod signatures (11.5 Гн/м³, χ = −0.5, layer width =
   wire diameter, SC-MO01-016) and reconcile with the film flux-inductance
   law L_Φ = μ₀πR²/2h (SC-AR07-031) at rod aspect ratio h >> R — does the
   film formula even apply?
7. Are the CFICR gains (7–50× over CMOS single-layer, SC-AR07-042) and the
   ~10 Гн/м² density ceiling (SC-AR07-035) consistent with the claimed
   vortex instability above 500 nm (SC-AR07-034)? Where exactly does the
   state jump occur?
8. Do sub-5-nm transistor explosions (SC-SI10-001, SC-TC04-001) occur at
   current densities compatible with the Marakhtanov thresholds
   (SC-TC04-014) once interconnect cross-sections are scaled — i.e. is the
   industrial symptom the same phenomenon?
9. Katorgin–Marin radiation fraction: quantify the claimed "most of the
   displacement current" lost to radiation at 30 kW (SC-TC03-027,
   SC-TC01-046) from available calorimetry — bounds the entire
   plasma-insert device family.
