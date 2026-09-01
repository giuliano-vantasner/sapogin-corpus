# general — synthesis

Practical-first synthesis of the 161 claims in this bucket. Every assertion
is pinned to SC-* ids. Verdicts come later, in campaigns; this file organizes
the art, it does not adjudicate it.

Bucket composition: TC02 (23), TC04 (14), WO03 (12), TC01 (11), WO05 (9),
BR04 (8), PA03 (8), DI01 (7), MO01 (7), SI09 (7), PM01 (6), SI06 (6), TE07
(6), DI02 (5), TC03 (5), MO02 (4), SI02 (4), PA01 (3), PA02 (3), SI05 (3),
SI08 (3), SI10 (3), SI03 (2), SI04 (1), SI11 (1). This bucket is the
keyword-bucketing overflow: it holds five distinct practical paths
(displacement-current power conversion; ring currents/superconductivity;
planar & multilayer inductances; self-rotating stores/Stokes principle;
charge atmospheres & self-consistent charge systems) plus school-apparatus
demos. A large device-flavored fraction belongs in `electrical-devices` —
listed explicitly in the MISBUCKETED section at the end.

## The art (practical layer)

- **Displacement-current (CODM/ODDM) power conversion** — the most
  quantified path in the bucket:
  - Claimed measured effect: with a displacement current replacing the
    conduction current, thermal power on an ohmic resistance rose "2-3
    times" over the power drawn from the mains (hydrogen plasma, mains-fed)
    [SC-TC02-040]; in high-voltage two-electrode experiments across various
    conducting media, some cases showed large heat release, others none
    [SC-SI10-013].
  - Physics lever: current amplitude ∝ ν, instantaneous-power amplitude ∝
    ν² [SC-TC02-010, SC-TC02-051, SC-TC02-055]; conversion coefficient vs
    frequency is a straight line separating below-unity from super-unity
    regions in the same resistance, Fig. 12 [SC-TC02-060].
  - Design point (mains): η = 5 at 50 Hz, U0 = 220 V, ν* = 10 Hz,
    C = 1 µF, R = 7.9 kΩ, q0 = 2.2·10^-4 C, displacement-current amplitude
    69 mA, power amplitude on the ohmic resistance 37.6 W (5× the
    capacitance power) [SC-TC02-061]. Bigger claim: R* = 10 Ω, η = 10 →
    R = 100 Ω, iM = 11 A, 1.1 kV on load, 12.1 kW out vs 1.21 kW from
    mains [SC-TC03-033].
  - Safety recipe (as stated): plastic housing with twice-distilled water
    circulating inside; housing reduces harmful radiation "by no more than
    80 times" [SC-TC02-042].
  - Program claims: stationary, low-radiation CODM constructs are the main
    task [SC-TC03-031]; "reactor" converts AC-AC power up/down depending on
    frequency without DC sources [SC-TC02-048]; highest volumetric density
    of electric power, cheapest launch cost [SC-TC02-073, SC-TC02-074,
    SC-WO03-028]; introduction raises efficiency of electric-energy use
    "by an order of magnitude" [SC-TC02-075]; capacitive transformers on
    displacement current convert step-down or over-unity, with energy
    conservation "not holding" as in electromagnetic induction
    [SC-SI09-005]; Mandelstam–Papaleksi multi-plate rotating capacitance
    and Dzhanibekov–Sapogin two-plate axial rotating capacitance are the
    named experimental ancestors [SC-SI05-003, SC-BR04-005].
- **Ring currents / room-temperature superconductivity** (sibling family of
  `foundations-canonical` SC-SI01-030…034):
  - Steel-plates experiment (verified replication claimed): two steel
    plates 10×15 cm², 1 cm thick; 500 A current pulse through a conductor
    inside the plates; attraction force 15000 N, estimated pressing
    pressure ≈ 1 MPa; the plates could not be separated by hand for two
    years (Atamanchenko & Dzyuba, Taganrog, 2018–2020, replicating
    Lickkalnen's 1917-era observations) [SC-TC04-023, SC-TC04-022]; a
    blogger heated them to white heat without separation — "NO Curie
    point" [SC-TC04-024].
  - Memory/switching cell recipe: place a steel film near (or around) a
    10-nm-diameter conductor; pass a current pulse; the vortex electric
    field twists Ampère–Foucault currents in the film; read by direct or
    reverse current — binary cells claimed replaceable for p-n junctions
    [SC-TC04-026, SC-TC04-025].
  - Claimed magnetics: all permanent magnets are the superconducting state
    of ring currents at room temperature [SC-TC04-018, SC-SI09-007];
    ring-current diameters in steel orders below 0.1 nm at room temperature
    [SC-SI09-006]; resistivity 10^-15…10^-20 Ohm·m vs copper 1.6·10^-8
    Ohm·m ("16 нОмм") [SC-TC04-020]; no Curie point up to melting
    temperature [SC-TC04-021, SC-SI09-009]; lifetimes > 100 years
    [SC-TC04-019, SC-SI09-008]; nanotech "Armageddon" enables devices on
    ring currents of radii 0.1 nm and less — sub-nano computers
    [SC-TC04-004, SC-SI10-004].
- **Planar & multilayer inductances** (monograph MO01 + patents PA01–PA03 +
  site SI06):
  - State of the art recorded: late-1980s GaAs/sapphire spirals ~25 nH,
    self-resonance > 3 GHz, sizes to 500 µm; planar Si inductor 9.3 nH with
    2.47 GHz self-resonance, square 230 µm, 9 turns, 6.5 µm width,
    5.5 µm spacing, max Q = 3; early-1990s CMOS two-metal spirals of tens
    to hundreds nH at ~2 µm thickness for 800–900 MHz LNAs [SC-MO01-001].
  - Archimedes-spiral gains (Biot–Savart estimates): N = 10 turns → 30.8 nH
    (~40× a ring); n = 2 spiral, final radius 16.8 mm → 55.8 µH (~1680×);
    claimed gain range 40–1500× [SC-MO01-005]; thin-film toroid 50 µm
    thick, radii 0.4/0.1 mm → ~12 nH, beating a six-turn ribbon solenoid of
    60-fold larger volume; a nanoscale effect can raise ultrathin-film
    inductance by an order [SC-MO01-010].
  - Negative (introduced) inductance: 30-layer Al+Cu microinductor, 20 µm
    height, eddy-current radius 200 µm → L/V = 2.4e5 H/m³, diamagnetic
    susceptibility −19…−46 (frequency-dependent) [SC-MO01-013]; multilayer
    branch of 10–30 double layers → ~2.0e7 H/m³ [SC-SI06-008]; dynamic
    inductance vanishes at two characteristic frequencies and takes both
    signs [SC-SI02-014]; RPGS second zero predicted at 1.9e12 Hz (not
    reproduced by 3D EM modeling or experiments), while two-layer Al/Cu
    nanofilm inductance measured constant to ±15% over 0.1–10 MHz
    [SC-MO01-015]; classification of closed (solenoid + film) vs open
    (planar spiral) designs [SC-MO01-017, SC-MO01-006].
  - Patent recipe (PA03): additional thin film on the chip, thickness
    tens–hundreds of nm, gives 5–50× surface inductance density; material
    sets the frequency-independent band — copper 0.3–30 MHz, aluminum
    0.5–50 MHz, tungsten 1–100 MHz, nickel 1.2–120 MHz, nichrome
    20 MHz–2 GHz, electronic silicon 20 GHz–2 THz [SC-PA03-003,
    SC-PA03-004, SC-PA03-002]; worked case: Al film R = 50 µm,
    h2 = 100 nm → Lф = 50 nH, flat 0.5–50 MHz [SC-PA03-007]; film 50–350 nm
    sweeps L = 100–14 nH; limiting surface density 9.8 H/m² [SC-PA03-008];
    Ki = 0.1–0.99 raises own resonance several times [SC-PA02-004,
    SC-PA02-002]; multi-point tap of the shield [SC-PA02-003]; Ki≈1, Ky≈1
    variant [SC-PA01-002]; SiGe transistors fα = 200–300 GHz enable
    50–80 GHz operation [SC-PA01-006]; screen-free construction vs US
    6.833.603 prototype [SC-PA01-004]; nanofilm paramagnetism (σ = −1) at
    h2 < 1 µm vs macroscopic diamagnetism (σ = +1) [SC-PA03-005,
    SC-PA03-006]; integration: ~10 nH per layer ≤ 500 nm via "conducting
    film inside the current ring" [SC-SI06-007, SC-SI02-015]; 16,000
    inductors in 40 layers on 1 mm × 1 cm² → ~1 mH positive, ~10 mH
    negative [SC-SI06-009]; replication program on Al–Cu 2…30 double
    layers (Ohio 2009 technology) [SC-SI06-010]; Tesla transformers on the
    planar current-vortex inductance, an order less volume than cylindrical
    [SC-TC03-038].
- **Electric arrow / dipole plasmoid rotor (BR04)**:
  - Mock-up: arrow on a vertical axis along external field lines between
    two small-diameter cylindrical electrodes at large potential
    difference; induced end charges flip sign at each breakdown, so the
    arrow is attracted before breakdown and repelled after — continuous
    rotation [SC-BR04-018].
  - Numbers: air breakdown 25 kV/cm = 2.5 kV/mm = 2.5 V/µm (Paschen, room
    conditions); 2–5 mm gaps need 10–25 kV; rotation period 1–2 s
    [SC-BR04-022]; measured run: aluminum arrow 100 mm × 3.5 mm rotating at
    2 Hz consumes ~2.5 mW from the HV supply — mean volume power density
    ~0.7 kW/m³ [SC-BR04-025]; mini-disk rotor: 10 mm diameter, total gap
    1 µm, driven by (or generating) two 1.5 V batteries, MEMS-only
    [SC-BR04-023]; biophysical mirror: bacterial flagellar motors ~100 nm
    body, 13–17 radial sectors, torque 1300–2000 pN·nm at 5 mV/nm → ~20
    charges per membrane, 1–2 electrons per sector [SC-BR04-020];
    energetically closed Source↔Motor chain of third kind [SC-BR04-001];
    eddy-current heating of water claimed to lower boiling point to 70 °C
    at atmospheric pressure [SC-BR04-028].
- **Self-rotating stores / Stokes principle** (PM01, TC01, SI03, SI08,
  WO05, WO03, SI10, SI11):
  - Claimed law: in a medium with friction there exists a class of
    trajectories with constant linear or angular speed — the "law of
    conservation of power", attributed to Stokes' verification on a falling
    ball in a viscous medium [SC-TC01-014, SC-TC01-015, SC-PM01-009,
    SC-PM01-007]; four conservation laws at zero total torque (two vector,
    two scalar) [SC-PM01-007]; stationary spinner speed ω* = (M₀ − M₁)/η,
    independent of moment of inertia [SC-WO05-016] (equation of motion
    detailed in `emden-gravity-cosmic`, SC-WO05-014).
  - Historical hardware claims: Bessler wheel checked at 2 weeks / 40 days
    / 2 months in a closed room [SC-WO05-003]; Bhaskara half-filled tubes
    [SC-WO05-004]; Howard Johnson magnet motor 1979 [SC-WO05-006];
    Testatica: counter-rotating acrylic disks generated AC, part consumed
    by the drive, generation stops when rotation is forcibly stopped
    [SC-WO03-014, SC-WO03-015]; Bauman stopped production, museum device,
    "suffices for the needs of one small house for years" [SC-WO05-020];
    Marinov's 1985 low-power studies [SC-WO03-018, SC-WO05-021].
  - Device-class claims: over-unity mechanical→AC converters [SC-SI03-016];
    generation regime where Source exceeds Motor + losses [SC-SI03-013];
    closed-loop chain as autonomous personal source [SC-SI10-008,
    SC-SI11-008, SC-TC03-039, SC-BR04-001]; program for low-power personal
    energetics on all well-studied fields [SC-PM01-017]; operational
    drawback admitted: high-intensity noise from large-diameter counter-
    rotating disks [SC-WO05-030].
  - Related over-unity exemplars claimed in passing: levitation currents of
    100 A lifting a 2400-tonne train by 1 cm without heating (Dotsenko)
    [SC-TC01-016]; Chinese MAGLEV at 650 km/h [SC-TC01-017]; LED-like
    system with 10 W electric in / 100 W light out (Alferov heterostructure
    context) [SC-TC01-021]; thin aluminum film heated by an automobile lamp
    giving 4 V potential difference (thermoelectric, vs "microvolts" in the
    1970s literature) [SC-TC01-025]; vacuum fluctuations negligible vs
    thermoelectric forces [SC-TC01-024]; EHB synthesis/decay as competing
    explanation of Fleischmann–Pons / Katorgin–Marin / Rossi–Focardi heat
    [SC-TC01-006]; source emitting heat + AC simultaneously [SC-TC01-035].
- **Charge atmospheres & self-consistent charge systems** (DI01, DI02,
  MO02, SI02, SI04):
  - Charge "atmospheres" on conductors: internal + external, heights set by
    temperature, curvature radius and charge [SC-MO02-001]; external
    atmosphere on a conical STM tip measured (reinterpreted) at "several
    µm"; Cavendish null explained by the shell not leaving its internal
    atmosphere, whose height is "fractions of a µm"; concentration in the
    external atmosphere grows outward, internal inward; for large negative
    charges the internal atmosphere can reach metal-like concentration
    [SC-MO02-002].
  - Estimates: nonrelativistic like-charge gas l2 = 0.35 µm, T2 = 0.35 ps,
    φm = 0.3 V at 18 µm; at x = 1 cm: φ = −7.6 kV, Ex = 10 kV/cm,
    n = 2.0e9 cm⁻³, v = 5.0e9 cm/s; kinetic energy ×2.6e3 (relativistic
    refinement required) [SC-MO02-008]; relativistic case E0 = 0.5e3 kV/cm,
    φm = 6.7e2 kV at L2 = 14e-2 cm, γm = 1.8, l2 = 8e-2 cm, T2 = 610 ps,
    τ2 = 1.7 ns, n0 = 9.4e10 cm⁻³, v = 0.99c at 0.4 cm [SC-DI02-005].
  - Thermodiffusion numerics: at δ = 1/2, β = 1/2, bounded states for
    −∞ < α < 0.5; length changes ~12× across −2 ≤ α ≤ 0.5 ("stretched
    spring"); boundary T and p vanish; sharp concentration boundary with
    unlimited growth for α = −0.75…−1.0 [SC-DI01-011, SC-DI02-007];
    finite surface charge density only for positive/zero total pressure
    [SC-DI01-012]; Gauss-theorem methodology caution (surface must not
    cross the zero-pressure surface) [SC-MO02-013]; Earnshaw's theorem as
    the foil [SC-SI04-008]; Frenkel equation derived from Maxwell–Vlasov
    [SC-DI02-003]; Vlasov's two premises [SC-DI02-019]; MRTI beam→glowing
    balls observation claimed explained [SC-DI02-014]; formal facts of the
    2003 defense (420 pages, 81 figures, council D 212.208.10)
    [SC-DI01-023].
- **School apparatus (TE07)**: hidden-wiring detector (Radio 1991 №8
  p.77, LED HL1) as the EM indicator [SC-TE07-001]; accelerated ebonite
  rod lights the LED, uniform motion does not, only relative acceleration
  matters [SC-TE07-003, SC-TE07-004, SC-TE07-005]; metal cup shields a
  lamp's EM radiation [SC-TE07-009]; spring-stiffness lab work with
  k = 2mgH/x² [SC-TE07-010].
- **Infrastructure critique framing the energy path (WO03)**: two warming
  causes, one cosmic (Earth–Sun approach, solar luminosity, magma
  overheating) — "more powerful compared with the greenhouse effect"
  [SC-WO03-003, SC-WO03-004]; blackout fragility of cities [SC-WO03-007];
  decarbonization read as clean-tech replacement [SC-WO03-008]; wind/solar
  compactness vs seed-energy dependence, storage costs, 10-year
  modernization [SC-WO03-009, SC-WO03-011].

## Key quantities and recipes

| claim | quantity / recipe | source doc:page |
|---|---|---|
| SC-TC02-040 | thermal power / mains power = 2–3 (displacement current, ohmic R, hydrogen plasma) | TC02 p.13 |
| SC-TC02-061 | η=5 design: 50 Hz, 220 V, ν*=10 Hz, C=1 µF, R=7.9 kΩ, q0=2.2e-4 C, i0=69 mA, 37.6 W | TC02 p.18 |
| SC-TC03-033 | η=10 design: R*=10 Ω, R=100 Ω, iM=11 A, 1.1 kV, 12.1 kW vs 1.21 kW from mains | TC03 p.8 |
| SC-TC02-010 | i0 ∝ ν; P0 ∝ ν² | TC02 p.5 |
| SC-TC02-060 | conversion coefficient vs frequency: line splits <1 / >1 regions (Fig. 12) | TC02 p.17 |
| SC-TC02-052 | Kirchhoff holds only at ω0 = 1/RC | TC02 p.16 |
| SC-TC02-042 | shielding: plastic housing + circulating twice-distilled water; ≤80× reduction | TC02 p.13 |
| SC-TC04-023 | steel plates 10×15 cm² ×1 cm; 500 A pulse → 15000 N, ≈1 MPa, stuck ~2 years | TC04 p.4 |
| SC-TC04-026 | memory cell: steel film + 10 nm conductor + current pulse; read by direct/reverse current | TC04 p.5 |
| SC-TC04-020 | ring-current resistivity 10^-15…10^-20 Ом·м; copper 16 нОм·м | TC04 p.3 |
| SC-TC04-010 | AC anomalies concentrated at conductor diameters < 20 nm | TC04 p.2 |
| SC-SI09-006 | ring-current diameter in steel ≪ 0.1 nm at room temperature | SI09 § Преподавание |
| SC-TC01-016 | levitation: 100 A lifts 2400 t by 1 cm, no metal heating | TC01 p.10 |
| SC-TC01-017 | MAGLEV trains at 650 km/h | TC01 p.9 |
| SC-TC01-021 | LED-like: 10 W electric in, 100 W light out | TC01 p.10 |
| SC-TC01-025 | thin Al film + automobile lamp → 4 V (thermoelectric) | TC01 p.12 |
| SC-MO01-005 | Archimedes spiral: N=10 → 30.8 nH (×40); n=2, r=16.8 mm → 55.8 µH (×1680) | MO01 p.80 |
| SC-MO01-013 | negative L/V = 2.4e5 H/m³; χ = −19…−46; 30 layers Al+Cu | MO01 p.219 |
| SC-MO01-015 | RPGS second zero 1.9e12 Hz; two-layer film flat to ±15% on 0.1–10 MHz | MO01 p.226 |
| SC-SI06-009 | 16,000 inductors / 40 layers / 1 mm×1 cm² → ~1 mH (+), ~10 mH (−) | SI06 § Интегральные индуктивности |
| SC-PA03-004 | material sets flat band: Cu 0.3–30 MHz … nichrome 20 MHz–2 GHz, Si 20 GHz–2 THz | PA03 p.6 |
| SC-PA03-007 | Al film R=50 µm, h2=100 nm → Lф = 50 nH (0.5–50 MHz) | PA03 p.11 |
| SC-PA03-008 | h2 = 50–350 nm → L = 100–14 nH; up to 9.8 H/m² | PA03 p.12 |
| SC-PA02-004 | Ki = 0.1–0.99 raises own resonance several times | PA02 p.7 |
| SC-PA01-006 | SiGe fα = 200–300 GHz → 50–80 GHz compensation range | PA01 p.8 |
| SC-BR04-025 | Al arrow 100 mm × 3.5 mm, 2 Hz, ~2.5 mW → ~0.7 kW/m³ | BR04 p.30 |
| SC-BR04-022 | Paschen 25 kV/cm; 2–5 mm gaps → 10–25 kV; period 1–2 s | BR04 p.28 |
| SC-BR04-023 | mini-disk rotor: Ø 10 mm, gap 1 µm, 2 × 1.5 V batteries, MEMS | BR04 p.28 |
| SC-BR04-020 | flagellar motor: ~100 nm, 13–17 sectors, 1300–2000 pN·nm, 5 mV/nm, 1–2 e/sector | BR04 p.26 |
| SC-BR04-028 | eddy heating lowers boiling point to 70 °C at atmospheric pressure | BR04 p.31 |
| SC-MO02-008 | l2 = 0.35 µm; at 1 cm: −7.6 kV, 10 kV/cm, n = 2.0e9 cm⁻³, v = 5.0e9 cm/s | MO02 p.96 |
| SC-DI02-005 | E0 = 0.5e3 kV/cm; φm = 6.7e2 kV; γm = 1.8; 0.99c at 0.4 cm | DI02 p.171 |
| SC-DI02-007 | −2 ≤ α ≤ 0.5: system length changes ~12× | DI02 p.250 |
| SC-WO05-016 | ω* = (M₀ − M₁)/η; no rotation if M₁ > M₀ | WO05 p.4 |
| SC-WO03-014 | counter-rotating acrylic disks → sustained AC generation | WO03 p.3 |

## Testable protocols

- **Steel-plate ring-current replication** (most reproducible: full
  geometry + drive + observable extracted) [SC-TC04-023, SC-TC04-022,
  SC-TC04-024, SC-TC04-019]. (1) Take two separate steel plates of
  10×15 cm² area, 1 cm thickness. (2) Pass a 500 A current pulse through a
  conductor inside the plates [SC-TC04-023]. (3) Measure the attraction
  force (claimed 15000 N, pressing pressure ≈ 1 MPa) and attempt manual
  separation over weeks [SC-TC04-023]. (4) Heat to white heat and test
  separation (claimed no Curie-point release) [SC-TC04-024]. (5) Calorimetry
  on the plates: claimed zero heat release by the ring currents
  [SC-TC04-019]. [GAP]: pulse duration and waveform, conductor position and
  insulation, and plate alloy are not extracted.
- **CODM displacement-current conversion loop** [SC-TC02-061, SC-TC02-040,
  SC-TC03-033, SC-TC02-010]. (1) Build the mains design point: C = 1 µF,
  R = 7.9 kΩ at 50 Hz, 220 V amplitude [SC-TC02-061]. (2) Measure power on
  the ohmic resistance vs power drawn from the mains; the extracted
  precedent claims a 2–3× excess [SC-TC02-040]. (3) Sweep frequency and map
  the conversion coefficient against the claimed straight-line <1/>1 split
  (Fig. 12) and P ∝ ν² scaling [SC-TC02-060, SC-TC02-010]. (4) Test the
  claimed Kirchhoff breakdown away from ω0 = 1/RC [SC-TC02-052].
  [GAP]: the plate geometry/actuation of the CODM itself (rotating or
  vibrating capacitor) is not extracted as procedure steps in this bucket
  (only named: multi-plate Mandelstam–Papaleksi, two-plate axial
  Dzhanibekov–Sapogin [SC-SI05-003]).
- **Electric arrow rotor** [SC-BR04-018, SC-BR04-022, SC-BR04-025].
  (1) Suspend an aluminum arrow (100 mm × 3.5 mm extracted case) on a
  vertical axis aligned with the external field lines. (2) Place between
  two small-diameter cylindrical electrodes with 2–5 mm edge gaps.
  (3) Apply 10–25 kV (Paschen threshold arithmetic in [SC-BR04-022]).
  (4) Measure rotation rate (claimed 2 Hz) and HV supply draw (claimed
  ~2.5 mW → ~0.7 kW/m³) [SC-BR04-025]. (5) Scale test: MEMS mini-disk,
  Ø 10 mm, 1 µm total gap, 3 V drive [SC-BR04-023]. [GAP]: electrode
  diameters and arrow-electrode spacing beyond the gap range are not
  extracted.
- **Memory cell on ring currents** [SC-TC04-026, SC-TC04-025]. (1) Place a
  steel film near (or around) a conductor of 10 nm diameter. (2) Pass a
  current pulse; the vortex electric field twists Ampère–Foucault currents
  in the film [SC-TC04-026]. (3) Read back with direct or reverse current
  [SC-TC04-026]. (4) Check claimed endurance: currents consume no electric
  energy and wait "for centuries" [SC-TC04-026]. [GAP]: film thickness,
  pulse amplitude/duration, readout threshold currents — none extracted.
- **Al–Cu multilayer inductance replication program** [SC-SI06-010,
  SC-MO01-013, SC-MO01-015]. (1) Master multilayer film processes per the
  2009 Ohio technology. (2) Replicate on Al–Cu multilayer films from 2 to 30
  double layers [SC-SI06-010]. (3) Verify the nanoscale positive eddy
  inductance in a single film of variable thickness; check geometry and
  resistivity dependence; demonstrate dynamic eddy inductance on a thick
  single film [SC-SI06-010]. (4) Compare against the recorded 30-layer
  L/V = 2.4e5 H/m³ [SC-MO01-013] and the ±15% flatness on 0.1–10 MHz
  [SC-MO01-015].

## Phenomenology map

- **What the theory predicts observably (practical-first).** (i) Displacement
  currents heat conductors "anomalously": heating that is anomalous for the
  Joule–Lenz current is claimed natural for the Maxwell displacement current,
  with power amplitude ∝ ν² [SC-TC02-012, SC-TC02-010]; measured 2–3×
  thermal excess over mains power [SC-TC02-040]. (ii) Conversion coefficient
  crosses unity along
  a straight line in (frequency, resistance) variables — below-unity and
  super-unity regions in the same resistance [SC-TC02-060]. (iii) Ring
  currents: no heat, no Curie point, resistivity 10^-15…10^-20 Ohm·m,
  lifetimes > 100 years, diameters < 0.1 nm in steel at room temperature
  [SC-TC04-019, SC-TC04-020, SC-TC04-024, SC-TC04-021, SC-SI09-006,
  SC-SI09-008]; macroscopic signature claimed in sticking steel plates
  (15000 N for two years) [SC-TC04-023]. (iv) AC current distribution:
  four planar variants, ≥3 cylindrical variants incl. the axial cord
  (Current Crowding Effect), current thrown into the conductor interior at
  pressure equality; "biggest miracles" for diameters < 20 nm
  [SC-TC04-008, SC-TC04-009, SC-TC04-010]. (v) Nanofilm magnetism: eddy
  currents in tens–hundreds nm cylindrical films give frequency-independent
  positive flow inductance with paramagnetic properties (σ = −1); macroscopic
  cylinders give diamagnetism (σ = +1) [SC-PA03-005, SC-PA03-006]. (vi)
  Charge atmospheres on conductors: external (µm-scale on tips) and internal
  (sub-µm) atmospheres; outward-growing concentration externally,
  inward internally [SC-MO02-001, SC-MO02-002]. (vii) Charge self-
  acceleration: like-charge gas reaches 0.99c within 0.4 cm at the extracted
  field parameters [SC-DI02-005]; beam-atmosphere interaction yields
  long-lived glowing balls [SC-DI02-014]. (viii) Eddy-current heating of
  water shifts boiling to 70 °C at 1 atm [SC-BR04-028].
- **Thresholds and where effects are claimed strong**: frequency ν* = 10 Hz
  design boundary at mains voltage [SC-TC02-061]; Kirchhoff validity limited
  to ω0 = 1/RC [SC-TC02-052]; current anomalies < 20 nm conductor diameter
  [SC-TC04-010]; nanofilm paramagnetism only for h2 < 1 µm (and h2 < R)
  [SC-PA03-006]; bounded charge layers for −∞ < α < 0.5 with ~12× length
  swing over −2 ≤ α ≤ 0.5 [SC-DI01-011, SC-DI02-007]; finite surface charge
  density only at nonnegative total pressure [SC-DI01-012]; spinner rotates
  only while M₀ > M₁ [SC-WO05-016]; Testatica generation stops when disk
  rotation is forcibly stopped [SC-WO03-015].
- **Cross-references**: the ring-current and displacement-current theory
  anchors live in `foundations-canonical` (SC-SI01-020, SC-SI01-023/024,
  SC-SI01-030…034, SC-TC03-011/013); the spinner equation of motion lives in
  `emden-gravity-cosmic` (SC-WO05-014; its stationary-speed consequence
  SC-WO05-016 is pinned in this bucket's table; the circulation-theorem
  position SC-PM01-003 and the four-force rebuttal SC-WO05-009/011/013 also
  sit there, while the "trivial mathematical Lie" phrasing SC-PM01-004 stays
  in this bucket); SCW-as-bubble sequence and bead lightning: SC-SI01-015
  (`foundations-canonical`).

## Theory aside (secondary)

NOT load-bearing for the practical layer; debt ids linked per
`clusters/debt-candidates.md`. What the models assume about measurable
reality: (1) every AC in conductors/capacitances is a "true" displacement
current carried by bound electrons [SC-TC02-019, SC-TC02-003, SC-TC02-004],
and the electrodynamic-induction law (dipole-flux law) is structurally the
electromagnetic-induction law with primary/secondary roles swapped
[SC-TC02-017, SC-TC02-018, SC-TC02-020, SC-TC03-010]; from this it is
asserted that electrostatic energy
conservation does not manifest in time-dependent fields, so power
conversion both ways is expected [SC-TC02-021, SC-TC02-069, SC-SI09-005]
— the bucket's central over-unity assumption; (2) the Stokes power-
conservation narrative — zero total torque implies four conservation laws,
including a claimed "law of conservation of power" that licenses constant-
speed motion against friction [SC-PM01-007, SC-TC01-012, SC-TC01-015];
the corpus itself records the counter-position (circulation theorem,
"correct mathematical result") and calls it misapplied [SC-PM01-004;
SC-PM01-003, SC-WO05-009, SC-WO05-011 in `emden-gravity-cosmic`]; (3)
charge atmospheres as the
re-reading of tunneling-microscope current and the Cavendish null
[SC-MO02-001, SC-MO02-002]; (4) Maxwell–Vlasov derivation of the
self-consistent charge equations [SC-DI02-003, SC-DI02-019] with Earnshaw
as the stated foil [SC-SI04-008]; (5) the "Divine Fire"/Testatica
attribution of Fleischmann–Pons-type heat to displacement-current energy
release without neutrons [SC-TC02-071, SC-WO03-027, SC-TC01-006].
Debt-candidate claims in this bucket (per `clusters/debt-candidates.md`):
SC-BR04-020, SC-BR04-028, SC-PA03-005, SC-PA03-006, SC-PM01-001,
SC-PM01-004, SC-PM01-006, SC-PM01-007,
SC-TC01-001, SC-TC01-006, SC-TC01-012, SC-TC01-015, SC-TC01-021,
SC-TC01-024, SC-TC01-035, SC-TC02-010, SC-TC02-012, SC-TC02-018,
SC-TC02-019, SC-TC02-021, SC-TC02-040, SC-TC02-052, SC-TC02-069,
SC-TC02-071, SC-TC02-074, SC-TC02-075, SC-TC03-033,
SC-TC03-039, SC-TC04-008, SC-TC04-017, SC-TC04-018, SC-TC04-019,
SC-TC04-020, SC-TC04-021, SC-TC04-022, SC-TC04-024, SC-WO03-003,
SC-WO03-004, SC-WO03-014, SC-WO03-015, SC-WO03-025,
SC-WO03-027, SC-WO03-028, SC-WO05-001, SC-WO05-028.

Residual model-family claims (accounted, not separately load-bearing): the
dissertation's novelty items, defended provisions and conclusions for the
charge-system twin of the self-consistent theory [SC-DI01-005, SC-DI01-006,
SC-DI01-021, SC-DI01-022]; the site summaries of the total-pressure boundary
conditions and the bi-wave Hamilton–Jacobi complete integral [SC-SI02-001,
SC-SI02-011]; coordinate–time symmetry of conservation laws [SC-SI05-010];
planar-confinement statements with layer thickness = 2× spatial scale
[SC-SI08-002, SC-SI08-003]; the Atamanchenko "two new fundamental laws"
program claim [SC-SI09-001].

## Open questions for campaigns

1. The 2–3× thermal excess [SC-TC02-040] vs the η = 5 and η = 10 design
   points [SC-TC02-061, SC-TC03-033]: do the three figures come from the
   same measurement chain or different generations of apparatus? Reconstruct
   the claimed measurement circuit before any replication.
2. Kirchhoff-limitation claim [SC-TC02-052]: an ordinary RC network
   experiment can test "Kirchhoff holds only at ω0 = 1/RC" cheaply and
   unambiguously — first rung of the displacement-current ladder?
3. Steel-plate sticking [SC-TC04-023]: is the 15000 N / 1 MPa attraction
   reproducible with extracted geometry alone, and can residual magnetization
   vs "ring-current superconductivity" be separated by a demagnetization
   cycle [SC-TC04-022, SC-TC04-024]?
4. Memory-cell recipe [SC-TC04-026]: what minimum pulse energy writes a
   detectable state at 10 nm conductor scale, and does the claimed
   centuries-long retention [SC-TC04-019] leave any laboratory-decay signal?
5. Inductance numbers: reconcile SC-MO01-013's L/V = 2.4e5 H/m³ with
   SC-SI06-008's ~2.0e7 H/m³ (two orders apart) — different geometries,
   different definitions, or an error?
6. Does the claimed material-dependence of the flat band
   [SC-PA03-004] survive the replication program [SC-SI06-010], given the
   ±15% flatness datum [SC-MO01-015] and the unobserved 1.9e12 Hz zero?
7. Electric arrow: does the extracted 0.7 kW/m³ [SC-BR04-025] scale to the
   MEMS mini-disk [SC-BR04-023], and is the 1–2 s period [SC-BR04-022]
   consistent with the 2 Hz measured rotation?
8. Charge-atmosphere reinterpretation of STM current [SC-MO02-001]:
   what STM observable (tip-sample distance vs measured current) distinguishes
   the "µm atmosphere contact" model from standard tunneling?
9. Glowing balls from beam-atmosphere interaction [SC-DI02-014]: do the
   MRTI observations pin lifetimes/sizes that the DI01/DI02 plane and
   cylindrical solutions can be fitted against [SC-DI01-011, SC-DI02-005]?
10. Warming claims [SC-WO03-003, SC-WO03-004]: are the three cosmic causes
    (Earth–Sun approach, luminosity rise, magma overheating) developed
    quantitatively anywhere in the corpus, or asserted only?
11. Bucketing hygiene: the device claims flagged below split from their own
    document siblings (e.g. PA01-001/003/005 vs PA01-002/004/006) — should
    the clusters be re-cut so each device family is whole before campaigns
    start?

## MISBUCKETED — device claims that belong in `electrical-devices`

The bucketing put these device-flavored claims in `general` while their
siblings from the same documents landed in `electrical-devices`
(PA01-001/003/005, MO01-004/007/012/018, SI09-002, SI05-007/009/015,
TC04-016, TE07-002/008, WO05-017/031, SI03-017, TC01-007/019/020/022/023…).
Flagged for re-bucketing before campaign work:

- Planar-inductance patents: SC-PA01-002, SC-PA01-004, SC-PA01-006,
  SC-PA02-002, SC-PA02-003, SC-PA02-004, SC-PA03-002, SC-PA03-003,
  SC-PA03-004, SC-PA03-005, SC-PA03-006, SC-PA03-007, SC-PA03-008,
  SC-PA03-009.
- Inductance monograph/site: SC-MO01-001, SC-MO01-005, SC-MO01-006,
  SC-MO01-010, SC-MO01-013, SC-MO01-015, SC-MO01-017, SC-SI06-005,
  SC-SI06-006, SC-SI06-007, SC-SI06-008, SC-SI06-009, SC-SI06-010,
  SC-SI02-014, SC-SI02-015.
- Displacement-current path (CODM/electrodynamic induction):
  SC-TC02-003, SC-TC02-004, SC-TC02-006, SC-TC02-010,
  SC-TC02-012, SC-TC02-017, SC-TC02-018, SC-TC02-019, SC-TC02-020,
  SC-TC02-021, SC-TC02-040, SC-TC02-042, SC-TC02-048, SC-TC02-051,
  SC-TC02-052, SC-TC02-055, SC-TC02-060, SC-TC02-061, SC-TC02-069,
  SC-TC02-071, SC-TC02-073, SC-TC02-074, SC-TC02-075, SC-TC03-010,
  SC-TC03-031, SC-TC03-033, SC-TC03-038,
  SC-TC03-039, SC-SI05-003, SC-SI05-004.
- Ring currents / superconductivity / magnets: SC-TC04-004, SC-TC04-008,
  SC-TC04-009, SC-TC04-010, SC-TC04-017, SC-TC04-018, SC-TC04-019,
  SC-TC04-020, SC-TC04-021, SC-TC04-022, SC-TC04-023, SC-TC04-024,
  SC-TC04-025, SC-TC04-026, SC-SI09-005, SC-SI09-006, SC-SI09-007,
  SC-SI09-008, SC-SI09-009, SC-SI09-010, SC-SI10-004.
- Over-unity energy hardware (Source/Motor chains, Testatica, self-rotating
  stores): SC-BR04-001, SC-BR04-018, SC-BR04-022, SC-BR04-023, SC-BR04-025,
  SC-WO03-014, SC-WO03-015, SC-WO03-018, SC-WO03-025, SC-WO03-027,
  SC-WO03-028, SC-WO05-006, SC-WO05-020, SC-SI03-013, SC-SI03-016,
  SC-SI10-008, SC-SI10-013, SC-SI11-008.
- Electrical exemplars & EM apparatus: SC-TC01-016, SC-TC01-017,
  SC-TC01-021, SC-TC01-025, SC-TC01-035, SC-TE07-001, SC-TE07-003,
  SC-TE07-004, SC-TE07-005, SC-TE07-009.
- Charge-atmosphere/conduction measurements with device fixtures (arguable;
  recommend keeping with the charge-system path or moving as a pair):
  SC-MO02-001, SC-MO02-002, SC-DI02-014.
- Borderline, kept here deliberately: the Stokes/perpetual-motion theory
  block (SC-PM01-001…017, SC-TC01-001…015, SC-SI08-001, SC-WO05-001/028,
  SC-WO03-025 and its `emden-gravity-cosmic` siblings SC-WO03-002/005/029)
  forms one self-contained
  energy path with `emden-gravity-cosmic`; school demos SC-TE07-010 (spring
  lab) are pedagogical, not devices.
