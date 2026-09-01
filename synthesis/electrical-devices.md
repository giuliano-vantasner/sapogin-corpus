# electrical-devices — synthesis

Practical-first synthesis of the 366 claims in this bucket — the largest of
the corpus. The art falls into six device families: (1) the Mandelstam–
Papaleksi mechanical varicap + oscillating circuit and its "current
instability" regime (AR06, BR04, TC07); (2) the CODM/KODM displacement-
current converter lineage and the СПМ mains-converter program (TC02, TC03,
TC05); (3) the Testatika machine, reconstructed from drawings and community
reports (TC07, WO03, WO05, SI05, SI09, SI10); (4) thermionic/TEP and
gradient-injector hardware with the 1Ц21П storage experiment (BR02, BR03,
DI02); (5) the planar-inductance patents PA01–PA03 with the AR07 nanofilm
effect (AR07-037 here; the full eddy-current model lives in synthesis/
discharge-plasma.md); (6) nanofilm/graphene varicaps and closed energy
chains (WO02, WO07, SI11). Every assertion is pinned to SC-* ids. Verdicts
come later, in campaigns; this file organizes the art, it does not
adjudicate it.

## The art (practical layer)

- **Mandelstam–Papaleksi mechanical varicap (the reference build)**:
  cylindrical rotor–stator capacitance, 26 disks of 28.5 cm diameter, each
  divided into 16 radial sectors, 2 mm spacing; Paschen breakdown
  ~2.5 kV/mm at atmospheric pressure; working voltage approached but did
  not exceed 5 kV; a 5 kV spark gap was connected in parallel — which,
  per SC-AR06-025, is exactly why the instability regime (mode 3) was never
  seen (SC-BR04-003, SC-AR06-025). Recomputed operating point: rotor
  50 Hz, capacitance modulation 800 Hz, circuit resonance 400 Hz, C₀ =
  5.65 нФ, L = 27.7 Гн, mean current 73 мА, R = 7 кОм at Q = 10, amplitude
  energy 71 мДж, power 56 Вт (SC-BR04-004). Rotation frequency = 2× circuit
  resonance; output 400 Hz, 5000 V (SC-SI03-014, SC-WO02-017).
- **Current-instability gain figures (numerical modeling)**: at modulation
  depth 20% the circuit charge amplitude grows 6-fold in eight periods; at
  80% it grows > 10 000-fold (SC-AR06-003); the companion study reports
  4.9× at 20% for Q = 100 and the same > 10⁴ at 80%, independent of the two
  initial-condition classes checked (SC-BR04-011). Regime map at 20%
  modulation: damped oscillations for Q < 10, Mandelstam–Papaleksi beats
  for 10 < Q < 100, unbounded growth for Q ≥ 100 (SC-BR04-002). High Q is
  stated sufficient; the frequency ratio is the necessary condition
  (SC-BR04-010); varying the inductance at doubled frequency works too
  (SC-BR04-010).
- **Instability-hunting design correction**: the spark gap must go; the
  variable capacitance should be a rotor disk with radial conducting
  sectors inside П-shaped stator plates, so the radial breakdown feeds the
  circuit rather than heating air between full plates (SC-AR06-026);
  acrylic (vinyl) disks carrying radial sectors of thin aluminum or copper
  foil are the stated build (SC-BR04-015); instability cutoff is set by air
  breakdown between sector and plate at closest approach, regulated by
  plate spacing (SC-BR04-014, SC-BR04-015).
- **50 Hz design table for an instability circuit**: with Q = 100 and
  R = 5…100 Ом, L = QR/(2πν) spans 1.6…32 Гн and C₀ = (2πνQR)⁻¹ spans
  6.366…0.318 мкФ (SC-BR04-029); the three-regime conclusion and
  "certification by increment" proposal close the method (SC-BR04-030).
- **Self-rotating sector disk (Franklin-arrow principle)**: each radial
  sector is an "electric arrow"; approaching a П-plate it discharges
  through the smallest gas gap, its end charges flip, and the force jumps
  from attraction to repulsion — the wheel keeps turning, with dry
  crackling and ozone (SC-TC07-022, SC-BR04-034); three motion regimes are
  reported: damped finite oscillation, finite motion after stop, and
  uniform rotation only when air breakdown occurs (SC-BR04-017); the
  circulation period follows the dipole small-oscillation law
  T₀ = 2π√(J/(pE)) (SC-BR04-019); the 2017 experimental conclusion: the
  additional rotational energy is supplied by air breakdown between sector
  and П-electrodes (SC-BR04-016, SC-SI03-015).
- **CODM/KODM displacement-current converter (the central recipe)**: a
  "flat capacitor inside a flat capacitor" cell — inner radiating capacitor
  (mesh plates allowed, any dielectric) inside a receiving capacitor on the
  system axis; AC on terminals 1-2 swings the dipole moment in volume V;
  part of the Maxwell displacement current is taken at terminals 3-4
  (SC-TC03-018, SC-TC05-017). Design law: i_M = A·C·U·ν with A a
  dimensionless design constant (SC-TC03-012); load power
  P_вых = i_M²R = (ACUν)²R vs input P_вх = CU²ν/2, hence conversion
  coefficient k = P_вых/P_вх = 2A²RCν (SC-TC03-019, SC-TC03-020); the k vs
  R/R* plot is a straight line with R* = (2A²Cν)⁻¹ separating sub-unity
  from super-unity regions (SC-TC03-023); determine the true R* of a build
  by Legendre least squares on measured k points (SC-TC03-024).
- **Frequency rule for super-unity**: the amplitude-power ratio is
  P_M0/P_C0 = 4πνRC = ν/ν* with ν* = (4πRC)⁻¹; η = 1 at ν = ν*; sub-unity
  below; super-unity above (SC-TC02-056, SC-TC02-057, SC-TC02-058,
  SC-TC02-059). Worked estimate at η = 1/5: ν* = 250 Hz, R = 320 Ом,
  7.5 Вт on the capacitance vs 1.5 Вт on the resistance (SC-TC02-062).
- **СПМ mains-converter program (220 V / 50 Hz, 10 kW)**: requires a
  radiating capacitor C = 1 мФ holding 0.22 Кл at 220 В (SC-TC03-032);
  overall dimensions ≈ 0.6×0.6×0.2 м³ already envisioned (SC-TC03-034);
  η = 10 design point: R* = 10 Ом, load R = 100 Ом, i_M = 11 А, load drop
  1.1 кВ, load power 12.1 кВт vs 1.21 кВт mains draw (SC-TC05-031);
  looped operation via two symmetric Tesla transformers in series with the
  calorimeter — one returns 10% of excess energy to the input (then the
  circuit is disconnected from the mains), the other passes up to 90% to
  the consumer (SC-TC03-037, SC-TC05-034). Project staging: Stage 1 —
  10 мФ capacitance with 1–2 Кл effective charge; Stage 2 — converter at
  coefficient 10; Stage 3 — looped energy chain (ЗЭЦ) at 10 kW
  (SC-TC05-048).
- **Large-capacitance options, ranked**: Variant 1 — parallel electrolytic
  capacitors К43456А-400 В-1000 мкФ (uncertainty flagged: charge hiding in
  the aluminum case, SC-TC05-039); Variant 2 — multilayer thin-film
  capacitors from foil-clad getinax/textolite, section connections with
  and without jumpers (SC-TC05-040); Variant 3 — dielectric filled with
  mutually insulated metal balls (steel, brass, aluminum, copper), sweeping
  diameter/material (SC-TC05-041); Variant 4 — same with conducting rods
  oriented across the field line (SC-TC05-042); the declared shortest path
  — centimeter ДМД (dielectric–metal–dielectric) structures, effective
  charge up to 10⁵–10⁶ Кл (SC-TC05-046). Metrology: RLC meter E7-22 at low
  voltage; for effective charge above 1 Кл, Ivanov notch-filter methods
  (SC-TC05-047). Heated-filament lamps inside an air capacitor are proposed
  as a thermoelectron dipole source and КПД probe (SC-TC05-045).
- **Testatika construction (as extracted)**: Wimshurst-machine skeleton
  (1883) with the charge-removing brushes removed; a pair of acrylic disks
  carrying tens of radial electret strips (trapezoidal plates in the
  power builds); U-shaped/П-shaped capacitor plates coupled to a
  high-voltage Tesla transformer and Leyden jars (SC-WO03-013,
  SC-TC03-028); counter-rotation of the disks multiplies the number of
  rotating dipoles and the electrization frequency (SC-TC02-029); the main
  node is the oscillatory circuit whose capacitance is the fixed П-plates
  with the sector disks rotating inside (SC-TC07-007, SC-TC07-008);
  operating point ~30 кВ with the plasma gap raising geometric capacitance
  to 30 нФ (SC-TC03-028); power-raising recipe: match the number of
  removable П-plates to the number of radial electrets on one disk
  (SC-TC02-031). Reported park: 100 Вт, 300 Вт, 3 кВт, 10 кВт at Methernitha,
  Linden (SC-TC07-002, SC-BR04-031, SC-WO05-019); motor and generator on
  one axis with the circuit output looped to its input (SC-TC01-020).
- **CODM experiments actually run**: П-shaped capacitor with a charged
  ball moved periodically between points A and B — the electrometers at
  the plates charge/discharge, demonstrating the electrization effect
  (SC-TC02-026); the straight-through klystron shows the effect natively —
  the output-grid voltage always exceeds the first-grid voltage
  (SC-TC02-027); rotating dipole moment ~10 нКл·м at 0.5 Hz produces a
  kilovolt-scale swing on electrometers (Atamanchenko build: two hollow
  oppositely charged metal cylinders on a rotation axis, 2020/2021,
  Taganrog) (SC-TC02-028, SC-TC03-030, SC-SI09-004); Zhuravkov's
  "subcritical" discharge ignites at point-to-plate ≈ 1 mm, hundreds of
  volts, breakdown field 250 В/мм — usable instead of electrodes 1-2 to
  raise converter efficiency (SC-TC02-044; breakdown field SC-TC02-045 —
  discharge-plasma bucket); a PCB "reactor"
  with variable R/C and an L playing the Tesla inductance is laid out for
  element-level study (SC-TC02-047).
- **Gradient electron injector and the 1Ц21П storage experiment**: a plane
  system cannot inject (zero pressure gradient; skewing causes surface
  breakdown) (SC-BR02-012); the working configuration is the vacuum diode
  1Ц21П with an additional ceramic-insulated anode, where the field-
  pressure gradient at the cathode end throws the electron coat to the
  anode (SC-BR02-014); the angular-aperture injector geometry (cathode at
  φ = 0, anode rotated by aperture angle θ, E_φ ~ 1/r) places the drift/
  accumulator space opposite the gradient (SC-BR02-015); reported storage
  result: Q = 90 Кл accumulated, U = 25 кВ, capacitance 3.6 мФ against
  3.0 пФ initial (SC-BR02-022) (debt-candidate); cm/mm asymmetric injectors
  have valve (rectifying) properties — the electron cushion tears off only
  on the negative cathode half-wave (SC-BR02-030).
- **Spindt-cathode hardware**: parameters tabulated — tip radius 50 нм,
  I = 50–150 мкА, J = 2–8 А/см², pulling field 70–200 В/мкм, technical
  vacuum 10⁻⁹ mm Hg (SC-BR02-005); highest emission when the tip is level
  with the Mo control-electrode diaphragm (SC-BR02-004); counter-facing
  Spindt cathode pairs at d = 1–10 мкм without anode give thermoelectron
  concentrations up to 10¹⁷ м⁻³ at j₀ = 8 А/см², tunable by the control
  electrode — the proposed core of precision ΔT sensors and millivolt
  sources (SC-BR03-027, SC-BR03-028).
- **TEP (thermoelectron converter) numbers**: fundamental law k·φ/e + T =
  const gives EMF ε₀ = (k/e)·ΔT — 1.72 мВ at ΔT = 20 K up to 258.6 мВ at
  ΔT = 3000 K (SC-BR03-017); Bulyga's tungsten converters: 200–1000 мВ,
  internal resistance 3–15 кОм, gaps 100–200 мкм (SC-BR03-014); foreign
  TEP at 6 мкм gap: 1 Вт/см², efficiency ≈ 4%; 1–2 В requires gap ≤ 10 мкм
  (SC-BR03-030); limiting design point: W electrodes, d = 100 мкм, cathode
  3500 K / anode 500 K → EMF 0.26 В, l = 29 мкм, n = 2.8·10¹⁵ м⁻³
  (SC-BR03-022); thermoelectron layer thickness ~45.5 мкм at
  T₀ = 3.5·10³ K (SC-BR03-023); an oscillating thermoelectron layer under
  AC field is proposed as a DC-free microwave generator (SC-BR03-007).
- **Planar inductance patents (verbatim legal-technical claims)**: RU
  2 622 894 C2 claim 1 — planar inductance with a non-inverting current
  follower (low input, high output impedance) inserted, its output on the
  first film section, input through a correcting capacitor on the follower
  output (SC-PA01-001); claim 3 extends to N film sections with matched
  follower/capacitor chains (SC-PA01-003); own resonance rises 2–4× by
  choosing the correcting-capacitor ratio (SC-PA01-005). RU 2 623 100 C1
  claim 1 — same idea with the current amplifier input on the conducting
  shield element under the coil (SC-PA02-001); SiGe process f_α = 200–300
  ГГц keeps f_α >> f_в (SC-PA02-005). PA03 claim 1 — an additional thin
  film h₂ << h₁, no galvanic contact, inserted into the coil's inner
  region (SC-PA03-001); construction detail: film radius R < R₁ (inner
  turn radius), thickness h₂ << h₁ (SC-AR07-037). Patent technical results:
  wider working-frequency range without a petal screen, fewer deposited
  layers (SC-SI07-001, SC-SI07-002).
- **Nanofilm varicap (double electric layer)**: five-layer stacks —
  metal plate / dielectric / metal *or* semiconducting film / dielectric /
  metal plate (SC-WO07-006); 4 nm film at n = 10²⁵ м⁻³ breaks down
  (polarizes) at 0.4 В, 40 nm film at ~4 В; capacitance is largest at the
  breakdown voltage and falls ~1/U above it (SC-WO07-009); the Chinese
  4 nm-gap capacitor showed jump-then-1/U behavior (SC-WO07-002) and the
  SFU 10 nm film showed negative-capacitance domain-wall behavior with the
  same 1/U falloff (SC-WO07-003).
- **Graphene fluctuation source and the stationary closed chain**:
  Thibado's freestanding graphene under a transverse DC field develops a
  plasma instability; two dipole regimes — electric energy ≈ thermal
  (chaotic, bending, fluctuation current) vs electric >> thermal (oriented,
  static) (SC-WO07-004, SC-WO02-003, SC-WO02-004); connected to diode
  structures only the chaotic case yields a rectified current
  (SC-WO02-011); the proposed stationary generator is two mutually
  perpendicular capacitors — graphene capacitor 1-2 inside an LCR circuit
  driven to current instability, part of the AC returned to plain-plate
  capacitor 3-4, with pulse-periodic startup (SC-WO02-023); longitudinal
  coaxial arrangement variant with max displacement-current density on the
  axis (SC-WO02-024); power caveat: ~10⁻¹⁸ Вт at 100 Ом as drawn, ×10²⁰
  with cm-size macro plates (SC-WO02-025).
- **Self-charging capacitor & thermoelectricAttraction (TC01 family)**:
  plate contact separates charge in microseconds (Pustovoit–Beletsky
  force); discharge-after-separation multiplies charge ~order of magnitude;
  discharge/recharge cycles repeat against an ohmic load; ΔT across the
  plates strengthens it (SC-TC01-029 through SC-TC01-034).
- **BTG Archimedes generator**: dome-shaped floats traverse a closed path
  in a 10–20 м water tower; mechano-electric converter on the axis
  (SC-TC01-019).
- **Measurement instrumentation for this whole layer**: mechanical school
  electrometer modeled as Q = Q*·sin^{3/2}(α/2) with charge scale
  Q* = √(8l·mg/k) — Q* = 10.86…121.4 нКл over needle L = 50…250 мм,
  M = 250…1250 мг; linear 30–120° (SC-TE06-003, SC-TE06-004, SC-TE06-006,
  SC-TE06-007); upgraded electrometer with 5°-step scale calibrated
  1.0–6.0 кВ ↔ 10–60°, capacitance 17.7 пФ (SC-TE11-003, SC-TE11-005,
  SC-TE11-006); E7-22 RLC meter + notch filters for q > 1 Кл
  (SC-TC05-047).
- **Cross-bucket note**: the planar-inductance physics (eddy currents,
  negative inductance, film thickness windows) is synthesized in
  synthesis/discharge-plasma.md (AR07, MO01); the devices here consume it
  (SC-AR07-037, SC-PA03-001, SC-TC05-035: the planar current-vortex
  inductance would shrink Tesla-transformer inductances an order of
  magnitude in volume).

## Key quantities and recipes

| claim | quantity / recipe | source doc:page |
|---|---|---|
| SC-AR06-003 | 20% modulation → 6× charge growth in 8 periods; 80% → >10⁴× | AR06 p.1 |
| SC-BR04-011 | Q = 100: 4.9× (20%) / >10 000× (80%) per 8 periods | BR04 p.14 |
| SC-BR04-003 | M–P capacitor: 26 disks, ⌀28.5 см, 16 sectors, 2 mm gap; ~2.5 кВ/мм; 5 кВ spark gap | BR04 p.8 |
| SC-BR04-004 | rotor 50 Гц; C-mod 800 Гц; resonance 400 Гц; C₀ = 5.65 нФ; L = 27.7 Гн; 73 мА; R = 7 кОм; 71 мДж; 56 Вт | BR04 p.9 |
| SC-BR04-029 | 50 Гц, Q = 100, R = 5…100 Ом: L = 1.6…32 Гн; C₀ = 6.366…0.318 мкФ | BR04 p.44 |
| SC-TC03-012 | displacement-current law: i_M = A·C·U·ν | TC03 p.3 |
| SC-TC03-020 | conversion coefficient k = P_вых/P_вх = 2A²RCν | TC03 p.5 |
| SC-TC03-023 | R* = (2A²Cν)⁻¹; k vs R/R* straight line | TC03 p.6 |
| SC-TC02-056 | P_M0/P_C0 = 4πνRC = ν/ν*; ν* = (4πRC)⁻¹ | TC02 p.16 |
| SC-TC02-028 | CODM: p = 10 нКл·м at 0.5 Гц → kilovolt electrometer swing | TC02 p.10 |
| SC-TC02-044 | Zhuravkov discharge ignition: point-to-plate ≈ 1 mm at hundreds of volts | TC02 p.13 |
| SC-TC03-028 | Testatika CODM: ~30 кВ; geometric C = 30 нФ | TC03 p.7 |
| SC-TC02-031 | power-up recipe: № П-plates = № radial electrets per disk | TC02 p.11 |
| SC-TC03-032 | СПМ 10 кВт: C = 1 мФ, q = 0.22 Кл @220 В, 50 Гц | TC03 p.7 |
| SC-TC05-031 | η = 10 point: R* = 10 Ом, R = 100 Ом, i_M = 11 А, 1.1 кВ, 12.1 кВт vs 1.21 кВт | TC05 p.10 |
| SC-TC03-037 | Tesla pair: 10% return / 90% to consumer | TC03 p.8 |
| SC-TC05-046 | ДМД structures: cm-scale; effective charge up to 10⁵–10⁶ Кл | TC05 p.14 |
| SC-TC05-047 | E7-22 RLC meter; notch-filter methods above q = 1 Кл | TC05 p.15 |
| SC-TC05-048 | stages: C = 10 мФ / 1–2 Кл → converter k = 10 → ЗЭЦ 10 кВт | TC05 p.16 |
| SC-BR02-005 | Spindt: R = 50 нм; 50–150 мкА; 2–8 А/см²; 70–200 В/мкм; 10⁻⁹ mm Hg | BR02 p.8 |
| SC-BR02-022 | storage: Q = 90 Кл, U = 25 кВ, C = 3.6 мФ (initial 3.0 пФ) | BR02 p.32 |
| SC-BR03-017 | ε₀ = (k/e)·ΔT: 1.72 мВ @20 K … 258.6 мВ @3000 K | BR03 p.30 |
| SC-BR03-014 | Bulyga TEP: 200–1000 мВ; 3–15 кОм; gap 100–200 мкм | BR03 p.28 |
| SC-BR03-030 | foreign TEP: 6 мкм gap, 1 Вт/см², КПД ≈ 4% | BR03 p.27 |
| SC-BR03-028 | counter-Spindt: d = 1–10 мкм; n up to 10¹⁷ м⁻³; l ≈ 4 мкм | BR03 p.39 |
| SC-WO07-009 | 4 nm film: breakdown 0.4 В; 40 nm: ~4 В; C ~ 1/U above breakdown | WO07 p.2 |
| SC-WO02-025 | graphene device ~10⁻¹⁸ Вт @100 Ом; cm plates ×10²⁰ | WO02 p.7 |
| SC-WO02-018 | Dzhanibekov–Sapogin: ~10 В rectified; 16 radial slots/plate | WO02 p.5 |
| SC-TC01-029 | plate contact charges in µs (Pustovoit–Beletsky separation) | TC01 p.13 |

## Testable protocols

- **Mode-3 hunt on the Mandelstam–Papaleksi bench** (SC-BR04-003,
  SC-BR04-004, SC-AR06-021, SC-AR06-025, SC-AR06-026, SC-BR04-014,
  SC-BR04-015, SC-BR04-029):
  - Materials: variable air capacitance as rotor disk with radial
    conducting sectors + П-shaped stator plates (SC-AR06-026, SC-BR04-015);
    series L, R, C circuit; **no spark gap** (SC-AR06-025 identifies it as
    the mode-3 suppressor).
  - Geometry: reference M–P build 26 disks, ⌀28.5 см, 16 radial sectors,
    2 mm spacing (SC-BR04-003); 50 Hz design point from the L/C table
    (SC-BR04-029).
  - Procedure: 1) drive the rotor at ω = 2ω₀ (SC-AR06-017); 2) run the
    stated initial-condition classes y(0)=0, y′(0)=1 and y(0)=1, y′(0)=0
    (SC-AR06-021); 3) sweep modulation ε = 0.2 → 0.8 and Q through the
    10/100 boundaries (SC-BR04-002, SC-BR04-011); 4) let instability
    charge the capacitance and cut it by air breakdown at set plate spacing
    (SC-BR04-014); 5) certify by growth increment (SC-BR04-030).
    [GAP] no extracted circuit-wiring schematic beyond Рис. 1/Рис. 4
    references.
- **CODM conversion-coefficient measurement** (SC-TC02-026, SC-TC02-028,
  SC-TC03-018, SC-TC03-019, SC-TC03-020, SC-TC03-023, SC-TC03-024):
  - Materials: inner radiating capacitor (mesh plates + dielectric
    allowed), receiving capacitor, ohmic load, electrometers, rotating
    dipole (two hollow oppositely charged cylinders worked — SC-TC03-030).
  - Geometry: receiving capacitor on the system axis; "flat capacitor
    inside a flat capacitor" (SC-TC03-018).
  - Procedure: 1) apply AC U at frequency ν to terminals 1-2
    (SC-TC03-018); 2) record i_M amplitude and load power on R
    (SC-TC03-019); 3) compute k = 2A²RCν pointwise (SC-TC03-020); 4) fit
    k vs R/R* and extract R* by Legendre least squares (SC-TC03-023,
    SC-TC03-024); 5) cross-check the ν* = (4πRC)⁻¹ frequency law
    (SC-TC02-056). Reference anchor: 10 нКл·м at 0.5 Гц → kV swing
    (SC-TC02-028).
- **СПМ staged build** (SC-TC05-048, SC-TC05-039–SC-TC05-042,
  SC-TC05-046, SC-TC05-047, SC-TC05-031, SC-TC05-034, SC-TC03-037):
  - Stage 1: realize ≥10 мФ with 1–2 Кл effective charge via ДМД
    centimeter structures (or variants 1–4: electrolytics / foil-clad
    getinax multilayer / ball-filled / rod-filled dielectric)
    (SC-TC05-048, SC-TC05-046, SC-TC05-039–SC-TC05-042); verify with E7-22
    below 1 Кл and Ivanov notch-filter methods above (SC-TC05-047).
  - Stage 2: mains converter at k = 10 per the η = 10 design point
    (SC-TC05-031).
  - Stage 3: close the loop — two symmetric Tesla transformers in series
    with the calorimeter, 10% feedback to input, mains off, 90% to load
    (SC-TC05-034, SC-TC03-037). [GAP] A-value and dielectric loss data for
    any ДМД build; transformer ratings unstated.
- **Testatika-style self-rotating sector disk** (SC-TC07-007, SC-TC07-008,
  SC-BR04-015, SC-BR04-016, SC-BR04-017, SC-TC07-022, SC-TC07-025,
  SC-BR04-034):
  - Materials: acrylic (vinyl) disk(s); radial sectors of thin aluminum or
    copper foil; П-shaped capacitor plates; HV source; (full machine:)
    electret strips, Tesla transformer, Leyden jars (SC-WO03-013).
  - Geometry: sectors radial on the disk; disk rotating inside the П-plates
    (SC-TC07-007, SC-TC07-008).
  - Procedure: 1) spin the disk inside the П-plates at constant angular
    velocity (SC-BR04-015); 2) classify motion into the three regimes and
    confirm uniform rotation co-occurs with air breakdown
    (SC-BR04-017, SC-BR04-016); 3) observe ms-scale dipole reversal at each
    sector discharge and the current pulse it produces in the circuit
    inductance (SC-TC07-025, SC-TC07-026); 4) log ozone/crackling as the
    process signature (SC-BR04-034). [GAP] no extracted plate dimensions,
    gap values, or voltage for the replication builds.
- **Nanofilm varicap stack** (SC-WO07-006, SC-WO07-009, SC-WO07-002):
  - Materials: metal plates; dielectric layers; central metal or
    semiconducting film (two stack variants) (SC-WO07-006).
  - Geometry: film thickness nanometres — 4 nm and 40 nm reference points
    (SC-WO07-009).
  - Procedure: 1) fabricate the five-layer stack (SC-WO07-006); 2) ramp
    static voltage to the plasma-instability breakdown (0.4 В @4 nm;
    ~4 В @40 nm) (SC-WO07-009); 3) record C(U): expect largest C at
    breakdown, ~1/U decay above (SC-WO07-009, SC-WO07-002). [GAP] no
    extracted dielectric constants, areas, or deposition process.

## Phenomenology map

- **Charge accumulation under capacitance rotation**: mechanical capacitance
  change in a source-free circuit always accumulated excess charge on the
  plates, up to air breakdown (SC-AR06-006, SC-TC07-010); the Dzhanibekov–
  Sapogin slotted-duralumin build rectified ~10 В at any rotation frequency
  (SC-WO02-018); gain figures scale with modulation depth (SC-AR06-003,
  SC-BR04-011).
- **Spark-gap shadowing**: the M–P 5 kV spark gap forced operation into
  beat mode, hiding the instability regime (SC-AR06-025, SC-BR04-003,
  SC-BR04-012).
- **Electrization by moving dipoles**: charged ball between П-plates moves
  electrometer charge (SC-TC02-026); rotating 10 нКл·м dipole at 0.5 Hz →
  kV swings (SC-TC02-028, SC-SI09-004); klystron output-grid voltage
  exceeds input-grid voltage (SC-TC02-027); 50 years of two-electrode
  anomalous-energy experiments in gaseous/liquid/solid media are claimed
  into the same circuit family, some releasing heat, some not (SC-TC02-001,
  SC-TC03-006, SC-SI10-005) — the k < 1 vs k > 1 branch is offered as the
  reason (SC-TC03-022, SC-TC05-020).
- **Katorgin–Marin calorimetry and the radiation tax**: more power on the
  calorimeter than drawn from the socket in some regimes (SC-TC02-063);
  the 30 kW plasma insert radiated lethally and unshieldably
  (SC-TC03-027 — discharge-plasma bucket, SC-TC02-041); the stationary СПМ
  is claimed free of this defect (SC-TC03-035; stationary-plates advantage
  SC-TC03-036 — discharge-plasma bucket).
- **Testatika phenomenology**: autonomous AC output 100 Вт…10 кВт, ozone
  and crackling at the U-plates, no takers of the replication challenge
  despite 15–20 years of posted drawings (SC-TC07-002, SC-BR04-034,
  SC-WO03-017, SC-TC07-006, SC-WO03-019); Marinov's 1989 study registered
  the anomaly (SC-TC07-003, SC-TC02-049).
- **Storage anomalies**: 1Ц21П-based accumulator — 90 Кл at 25 кВ,
  capacitance 3.6 мФ from 3.0 пФ (SC-BR02-022); self-charging capacitor
  cycling against ohmic loads with µs-scale recharge onset
  (SC-TC01-029, SC-TC01-032).
- **Nanoscale capacitors**: 4 nm gap — capacitance jump then 1/U decay
  (SC-WO07-002); SFU 10 nm film — negative capacitance via domain wall
  (SC-WO07-003); graphene — chaotic vs locked dipole regimes with and
  without rectifiable current (SC-WO07-004, SC-WO02-011).
- **Kholoshenko vacuum-capacitor pulse conversion (2021, Marseille)**:
  charge/discharge of a vacuum capacitor by a plasmoid source reported as
  over-unity (SC-SI05-015); the pulsed conversion coefficient depends on
  the charge/discharge period ratio (SC-SI05-009).
- **Cross-bucket**: bubble-synthesis energy release between electrodes
  (SC-SI01-018, in synthesis/transmutation-nuclear.md) is the mechanism
  claimed behind the two-electrode heat experiments; the eddy-current
  negative-inductance states that bound L in these circuits are in
  synthesis/discharge-plasma.md.

## Theory aside (secondary)

The modeling spine is the source-free series circuit with harmonic
reactive-parameter modulation, y″ + y′/Q + y/(1 + ε·cos nx) = 0, reducible
to a Hill equation with pumping ~1/(1+ε·cos) against dissipation ~1/4Q²
(SC-AR06-012, SC-AR06-013, SC-AR06-016, SC-AR06-017); its three solution
classes (SC-AR06-002, SC-BR04-009) and the parametric-resonance optimum
n = 2 (SC-AR06-017) are the quantitative claims a campaign can check
symbolically/numerically first. On top of it sits the "law of
electrodynamic induction" — i_M = dΦ_D/dt, D = P + ε₀E — asserted as the
displacement-current counterpart of Faraday's law (SC-WO02-008, SC-TC05-010,
SC-TC05-011), with the k = 2A²RCν and ν* = (4πRC)⁻¹ conversion rules as its
engineering face (SC-TC03-020, SC-TC02-056). Interpretive claims that the
usual energy bookkeeping fails in these regimes (SC-TC02-049, SC-TC02-059,
SC-TC02-065, SC-TC03-021, SC-TC05-019, SC-TC07-027, SC-WO03-022,
SC-BR04-013, SC-BR04-026, SC-BR04-035) are debt-candidates and are NOT
load-bearing for running any protocol above — the protocols only consume
i_M, k, ν*, R*. Alternative-emission theory (excess-charge atmosphere
replacing Fowler–Nordheim tunneling, SC-BR02-031; Richardson–Dushman
declared inapplicable, SC-BR03-001, SC-BR03-003; three-halves-law
critique, SC-BR03-004, SC-BR03-008; Casimir formula called erroneous,
SC-TC01-023; graphene Hamiltonian called unrelated to the effect,
SC-WO02-005) is likewise quarantined here. The bisil two-force extension
f₁ = ρE, f₂ = E·div E/4π (SC-TC07-020, SC-TC07-021) is shared with the
transmutation bucket's gasostatics. Debt-candidate registry:
clusters/debt-candidates.md (AR06, BR02, BR03, BR04, TC01, TC02, TC03,
TC05, TC07, WO02, WO03, WO05, WO07, PM01 entries).

## Open questions for campaigns

1. Numerically reproduce the growth factors 6× / 4.9× / >10⁴× of
   SC-AR06-003 and SC-BR04-011 by RK4 on eq. (7) (SC-AR06-021): do the
   stated Q, n = 2, ε suffice, and is growth truly initial-condition
   independent (SC-BR04-011)?
2. Audit the Mandelstam–Papaleksi recomputation (SC-BR04-004): the source
   itself says its 71 мДж / 56 Вт are "more than twice" the original
   figures — locate and quantify the discrepancy.
3. Does the ν* = (4πRC)⁻¹ rule (SC-TC02-056) follow from network theory on
   the two-channel circuit (SC-TC02-008), or does it smuggle in the EDI
   premise (SC-WO02-008)?
4. The constant A in i_M = ACUν (SC-TC03-012) is undetermined for any real
   geometry [GAP] — derive or measure it for the SC-TC02-026 ball-and-plates
   and SC-TC02-028 rotating-dipole builds before any СПМ power claim
   (SC-TC05-031) can be checked.
5. Storage anomaly triage: is the 3.0 пФ → 3.6 мФ capacitance jump
   (SC-BR02-022) a measurement artifact, an electret effect, or real —
   what instrumentation was used [GAP]?
6. Valve/rectifier asymmetry of cm injectors (SC-BR02-030): extract the
   geometry threshold between valve and non-valve behavior; nano-scale
   injectors are claimed to lose it.
7. Testatika replication record: 15–20 years of posted drawings and zero
   independent replications (SC-TC07-006, SC-WO03-019, SC-SI10-016) — what
   minimal parameter set from SC-TC03-028 (30 кВ, 30 нФ, electret count)
   would a falsifiable replication need?
8. Kholoshenko pulsed conversion (SC-SI05-015, SC-SI05-009): is the claimed
   over-unity a bookkeeping of charge/discharge period asymmetry? Rebuild
   the energy ledger per period.
9. Cross-check the M–P gain claims against standard parametric-amplifier
   theory: Manley–Rowe constraints on SC-AR06-003/SC-BR04-011 growth
   without a pump-energy source term.
10. Do the planar-inductance patents' resonance-boost claims (SC-PA01-005,
    2–4×) survive SPICE-level simulation with realistic follower bandwidths
    (SC-PA02-005)?
