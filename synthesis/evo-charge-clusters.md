# evo-charge-clusters — synthesis

Practical-first synthesis of the 629 claims in this bucket (352 theory / 277 practical-layer,
per `claims/claims.jsonl`; membership concatenated from `clusters/clusters.json` bucket
"evo-charge-clusters", 41 sub-clusters). Heaviest contributors: TC08 (125), WO01 (76), TC06 (58),
WO06 (33), AR10 (31), AR09 (28), AR08 (27), MO03 (25), BR02 (22), AR05 (19). Every assertion is
pinned to SC-* ids. This file organizes the art, it does not
adjudicate it.

## The art (practical layer)

**Reference phenomenon — Shoulders charge clusters (EV / "зарядовый кластер").**
- Discovered 1987 (USA, Bodega) on a tip cathode in vacuum; hollow spherical clusters "flowing" in
  rings from the cathode point at 10 kV impulse voltage (SC-TC08-030, SC-SI02-021, SC-SI11-002).
- Generation field 2–10 kV between cathode and anode; sizes fractions–tens of µm; charge
  10⁸–10¹¹ electrons; lifetime/glow-out 30–100 ps, exceeding the Coulomb dispersal time
  (SC-DI01-001, SC-SI04-006, SC-MO02-004, SC-SI02-022).
- Shoulders resolved the picosecond current structure between tip cathode and planar anode at
  ~10 kV impulse; current fragments into portions ≤10 µm (SC-TC03-001, SC-TC05-001, SC-SI10-009).
- Cluster diameters 5–15 µm, hollow; radiate EM energy, hence short life; estimated ~2000 K
  (SC-WO01-022).
- Mean electron concentration in an EV 6.6·10²³ cm⁻³; EV rings ~20 µm; residual charge after
  collision of a 3 µm EV with an electrode 2·10¹⁰ electrons; a 10 µm EV loses 3.5·10¹⁴ electrons
  per mm of path (SC-MO02-004, SC-MO02-022).
- Concentration can exceed the metal mean by an order of magnitude; lacking a lattice, clusters
  show solid-like mechanical properties (SC-SI04-007).

**Crater forensics (the calibration experiment).**
- An EV striking flat titanium at an angle leaves a ring-shaped melted crater with a rim — read as
  a hollow, soap-bubble-like shell (SC-BR02-007, SC-WO01-062, SC-TC06-006, SC-MO03-014).
- Enlarged crater image: inner melt radius ρ₁ = 12.7 µm, outer ρ₂ = 14.5 µm, melt thickness
  Δ = 1.80 µm; assumption "5–15 % of kinetic energy at 10 kV went into melt heating" gives
  N = 6.2·10⁹–1.9·10¹⁰ cluster electrons, melt energy Q ≈ 1.5·10⁻⁶ J (SC-DI01-017, SC-DI02-010).
- Three impact classes predicted by energy release (large/medium/small) (SC-SI04-011, SC-BR01-003).

**Gradient electron injector and vacuum charge storage (BR02).**
- Shoulders triode: tip-cathode-to-control-electrode gap of order 1 µm → strongly inhomogeneous
  transverse field that compresses the electron "coat" (SC-BR02-003).
- Observed autoemission fields only 20–70 V/µm (not the Fowler–Nordheim (3–5)·10⁷ V/cm) with
  current densities 10⁴–10⁸ A/cm² (SC-BR02-001, SC-BR02-032).
- Two extraction regimes computed for a cm-scale injector (R1 = 10 mm, R2 = 30 mm, layer
  20×20 mm × 10 µm thick): regime 1 j* = 2·10⁵ A/cm², v* = 5·10³ m/s, 90 C in 1.5 s; regime 2
  (viscous) j* = 2·10³ A/cm², 90 C in 67.2 s; cluster-formation time τ₃ₖ = 4 µs (SC-BR02-021,
  SC-BR02-023, SC-BR02-024, SC-BR02-016).
- Injector design rule: aperture angle ≲ 0.1 rad for large pressure gradients; hollow channel
  outlet sizes the cluster; conical small-aperture variant for wear resistance (SC-BR02-020).
- Storage: preliminary experiments show a spherical cluster's capacitance can rise ~10⁹× over the
  UE-K interelectrode capacitance; with electrization coefficient β = 1.2·10⁹ from 1Ts21P-lamp
  experiments the accumulated cluster radius is R = 2.7 cm (SC-BR02-019, SC-BR02-025).
- Functional chain: HV pulses to cathode + control electrode → gradient tears electron layer off
  cathode → drift space → merge in main accumulator (SC-BR02-018, SC-BR02-017).
- Proposed experimental program: cm-scale copper prototypes; map breakdown vs geometry
  (tip/planar/cylindrical) and distance; 15 kW AC toroidal-coil pump; Paschen 25 kV/cm (DC), AC
  breakdown an order lower (SC-BR02-029).
- Applications claimed: bombarding radioactive targets to reduce radioactivity, surface treatment,
  non-lethal weapons, over-unity plasma chains, charge 1–100 C at 30 kW (SC-BR02-034, debt-flagged).

**Vacuum varicap with electron cluster (the electrical-path flagship).**
- Kholoshchenko–Kovalenko patent WO 2011031189A1 ("Vacuum capacitor", 2011): vacuum diode with the
  anode moved outside the glass; capacitance shows anomalously large values at tens of kV
  (SC-AR08-003, SC-AR08-004, SC-TC05-044).
- Sapogin's elementary theory introduces the electrization parameter ε = E'/E₀ = C/C₀ > 1 and
  computes Table 1 for a 1Ts21P tube (V = 15 cm³): C from 0.96 mF at 25 kV to 24 F at 1 V,
  response charge q' = 24 C constant; agrees with the patent by order of magnitude (SC-AR08-015,
  SC-AR08-021, SC-AR08-022, SC-AR08-024, SC-AR08-028).
- Two varicap modes: direct thermal→electric conversion; capacitive tuning of vacuum capacitance
  by 10³–10⁶× (SC-SI11-004, SC-SI11-005).
- A stationary electron cluster of centimeter sizes inside a diode with removed anode is reported
  as independent confirmation (SC-AR08-027, debt-flagged).
- Replication guidance: the French kenotrons studied recently produced no clusters because their
  cathodes lacked sharp points/roughness; the Petersburg diodes did show large capacitance changes
  (SC-WO06-012, SC-WO06-014). Measured electron-gas mean potential ~1 mV at 1000 K cathode via
  blocking voltage on a lockable diode (SC-WO06-006).

**Dzhanibekov–Sapogin / Novocherkassk mechano-electric line.**
- Mandelstam–Papaleksi (1950s): motor-rotated varicap in a series RLC circuit develops ~5 kV AC
  without a DC source; discharger rated just above 5 kV protected it (SC-TC08-003, SC-TC08-004,
  SC-TC08-016, SC-TC06-025). Measured conversion coefficient ≈ 1 — the authors' own null result for
  over-unity in that circuit (SC-TC06-026). The key electric/mechanical power ratio was never
  measured (SC-TC08-006).
- Dzhanibekov–Sapogin (unpublished, ~2008): two dural plates, ~500 pF, 16 radial slits each, one
  rotating → rectified ~10 V (SC-TC06-027).
- Novocherkassk 2019 converter: metal bearing with friction coefficient 0.01, pointed radial
  sectors; produced AC whose amplitude depended on rotation frequency even without an oscillatory
  circuit; could not reach self-rotation due to bearing friction (SC-TC08-026, SC-TC08-027,
  SC-TC08-029).
- Testatika (P. Bauman, Linden): Wimshurst-based self-rotating capacitance with radial sectors and
  П-shaped takeoff plates; claimed devices 100 W–10 kW, volume power density ≈ 1.2 kW/m³; Sapogin's
  own revision lowers the claim to 30–100 W (SC-TC06-029, SC-TC06-030, SC-TC08-017, SC-TC08-025).
  The over-unity cell is located in the two symmetric spark dischargers (SC-TC06-031); П-plate
  voltage reached 12–15 kV → high-voltage air breakdown (SC-TC08-015). Counter-rotating acrylic
  disks with tens of radial plates (SC-TC08-076). Improvements proposed: low-friction metal
  bearings, takeoff-plate count scaled with sector count, sector shape borrowed from flagellar
  bacterial motors (~100 nm, 2018) (SC-TC08-020, SC-TC08-021, SC-TC08-022, SC-TC08-023,
  SC-TC08-009).

**Displacement-current / КОДМ measurement chain (TC08/TC06).**
- Atamanchenko 2021: a 1 nC charge moving at 1 cm/s between П-plates electrizes them to ~800 V
  (SC-TC08-073); a mechanical dipole p = 10 nC·m rotated at 0.5 Hz swings electrometers by
  kilovolts (SC-TC08-075, with TMSL lab); klystron velocity modulation as the historical first
  observation (SC-TC08-074); Gandurin (St. Petersburg, 2017) verified the electric-origin moment on
  a П-capacitor (SC-TC08-014).
- Sambuk transformer: toroidal primary, one-turn copper-pipe secondary → kiloampere displacement
  currents, dynamic heating (SC-TC08-069).
- Mains recipe: switch an electric kettle through an electrolytic capacitor (conduction→displacement
  conversion); at 400 Hz ship frequency heating efficiency claimed ×10; optional diode bridge + series
  capacitor doubles frequency (SC-TC08-071, SC-TC08-141).
- Worked design estimate: η = 5 at 50 Hz, 220 V amplitude, C = 1 µF → R = 7.9 kΩ, charge amplitude
  2.2·10⁻⁴ C, displacement current 69 mA, power on R 37.6 W (SC-TC08-085, SC-TC08-086).
- Stationary point-varicap: two electrodes in П-plates, gap > 5 mm, U > 10 kV; air breakdown
  2 kV/mm raises the seed displacement current by ~an order; heat the points to 1000 K for bigger
  bubbles; procedure: sweep input voltage to approach the critical Maxwell-current density, then
  switch off the seed source (SC-TC08-093, SC-TC08-094, SC-TC08-095, SC-TC08-096, SC-TC08-097,
  SC-TC08-099).
- Solid-plasma varicap: nickel point cathode, tungsten (or substitute) anode, DC heater — Fig. 19
  (SC-TC08-100).
- Graphene cell: emitting capacitor 1-2 (graphene film) in series LCR with current instability;
  return path through capacitor 3-4; impulse/AC start-up, then sources switched off; two
  orientations (mutually perpendicular; longitudinal surround), air-operable plane-point diode at
  ~100 µm electrode distance; gap breakdown ≈ 1 V/µm (SC-TC06-056, SC-TC06-057, SC-TC06-058,
  SC-TC06-059, SC-TC06-061, SC-TC06-062, SC-TC06-021, SC-TC06-022).
- Safety note: the unclosed part of the displacement current is broadband, unshieldable radiation;
  harm threshold quoted at P > hundreds of watts; the Katorgin insert at 30 kW radiates lethally
  (SC-TC06-064, SC-TC05-025).
- Related capacitor tech: Sleptsov superdielectric (ε up to 10⁸): 1000 F in 100×50×20 mm³ at 3 V,
  q = 3000 C; recipe: 50/50 metal + dielectric nanopowder, sinter, cool, plate (SC-TC05-038,
  SC-TC05-043). Beletsky butterfly capacitor: 20×20 cm plexiglas plates glued with 8 µm Al film,
  lower gap 1–2 mm, ~90° opening → discharge ≈ 2 kV/mm; pressing forms an 8 µm conducting charged
  layer (SC-TC08-043, SC-TC08-044, SC-TC01-028). Carbon-paper (nm graphite film) on a charged plate
  collapses the electrometer potential at constant charge → millifarads at 1 V claimed (SC-WO06-028).

**Hydrogen plasma (Katorgin–Marin, NPO Energomash, Khimki).**
- 2000/2005/2009 setups: hydrogen plasma between two thin-walled coaxial brass cylinders ~12 cm
  apart, ~40 kV applied, 30–35 kW pump, ~1 A DC background carrying chaotic microsecond surges up to
  60 A; luminous tubular currents ~2000 K (SC-BR02-027, SC-MO03-016, SC-MO03-017, SC-WO01-083,
  SC-WO01-084, SC-TC08-077).
- Interpretation: each ~60 A µs spike carries ~30 µC ≈ 10¹⁴ particles; conversion coefficient
  (excess heat / grid energy) 2–5, tunable by hydrogen pressure, pumping speed, electrode geometry
  (SC-MO03-017, SC-TC08-077).
- Cluster birth rate in hot hydrogen plasma ×10⁴ over Shoulders' vacuum rate; charge per current
  filament cluster ≈ 1 µC; filament length 12 cm (SC-TC06-033, SC-TC02-039, SC-TC02-046).

**Water and atmospheric plasmoids.**
- Golubnichiy group: long-lived glowing objects (LLO/DSO) of mm radii in purified water under
  powerful short pulses; Shabanov: surface discharge in tap water forms cm-size glowing air films
  (SC-AR09-001, SC-SI02-017, SC-SI02-018).
- Objects form fast (apparent µs) then radiate stored energy over ms–s; can be electrically
  neutral, positive, or negative (SC-SI02-019, SC-AR09-002, SC-AR09-003, SC-SI02-020).
- Shabanov (Gatchina, 2000): an electron-cluster film floating above the water–air boundary with a
  radial current (SC-SI05-014). Vachaev–Ivanov "Energoniva": stationary glowing cm ball lightning
  maintained by external electric sources (SC-WO01-086).
- Wimshurst demo: two balls charged to ~25 kV glow in darkness with a µm–tens-of-µm layer at the
  negative electrode; charge transfer prefers the thin-walled sphere's outer surface (SC-MO03-002,
  SC-WO01-011, SC-WO01-017); a pointed conductor slides the charge film off into air/vacuum — the
  claimed EV-birth picture (SC-WO01-020).

**Metal films and nanowires (Marakhtanov; skin-effect route).**
- Films of several hundred atomic layers at fixed 180 °C: explosions above critical current
  densities j_crit(W) = 1.43·10⁹ A/m² and j_crit(Al) = 8.04·10⁹ A/m², explosion time µs
  (SC-SI01-028).
- Conductors ≤ 20 nm diameter at GHz: skin effect expels current into a thin shell leaving a
  charge-free internal cavity; the outer shell is described as a thin-walled charge cluster; a
  resistivity jump at a p-n junction ends the equilibrium in an explosion (SC-SI01-025, SC-SI01-026,
  SC-SI01-027, SC-SI10-002, SC-SI10-003).

**Rossi-Focardi chips heater (bridge to the catalysis bucket).**
- 2011 source: cylindrical conducting tube filled with Ni-Li chips, hydrogen at 55 bar, MW-class
  thermal output; tube temperature Tp = 200–500 °C depending on hydrogen pressure (SC-TC08-108,
  SC-TC08-109).
- Sapogin's re-analysis (60 g Ni chips, L = 0.2 m, r = 10 mm, wall 1 mm): C ≈ 10⁻¹⁰ F, charge
  0.8 mC, energy amplitude 3.2 kJ, P = 1 MW at 50 Hz, displacement current 250 mA ≈ 20 A/m²; volume
  power density 16 GW/m³ (SC-TC08-123, SC-TC08-124, SC-TC08-125, SC-TC01-047).
- Recipe claims: reactors work on any metal chips in vacuum (no hydrogen needed); heating method
  indifferent (gas/flame/DC/AC) but must be geometrically symmetric; chips beat powder/foil because
  their points nucleate bubbles as on Shoulders' cathode; heat by DC and watch the chaotic current
  component appear near Tp, then switch the DC off (boiling-plasma self-heating); an unnoticed AC
  source is present — register it with an inductance/capacitance sensor (SC-TC08-117, SC-TC08-118,
  SC-TC08-119, SC-TC08-120, SC-TC08-121, SC-TC08-126, SC-TC08-101).
- Discriminating experiment: run the same chip heating in vacuum without hydrogen vs with hydrogen
  as in Rossi's setup to see which releases more energy (SC-TC08-115).

**Diagnostics and procedures (cross-device).**
- Cluster-charge diagnostic: record the chaotic current component accompanying heating; the area of
  a statistical ejection on the current–time diagram gives the mean charge of the synthesized
  cluster; reference oscillogram: Katorgin's (SC-TC06-048, SC-TC02-015).
- Zhuravkov subcritical discharge: point-plane in air, breakdown 1.5× below classical; 2022 claim
  of a stationary self-reproducing plasma reactor, transmitted by e-mail, unpublished (SC-TC08-078,
  SC-TC08-080).
- Centrifugal charge separation: 1 m rod at 40 Hz → 253 electrons at the rod end, dipole moment
  0.4 µC·m; disk generator recipe: 40–60 conducting rods radially on a dielectric disk, П-shaped
  take-off plates with tip screws, suspension friction < 0.05, into a high-voltage series LCR
  circuit (SC-MO03-027, SC-TC08-052, SC-MO03-028, SC-MO03-029).
- Dipole-plasmoid harvester: long conductor along a plane capacitor's field lines, low-frequency AC
  supply, harvest dipole-bubble decay energy in the circuit; thermocouple EMF (µV→mV) cited as
  macroscopic charge separation in solid-state plasma (SC-MO03-021, SC-MO03-025).
- Thermoelectron converter recipe: conical cathode, wide part heated 200–3000 K, narrow tip cold
  (SC-MO03-026); atmospheric variant: tungsten cone, base Ø 1–2 cm, tip micron, 30°, heater
  1000–2000 K, Faraday-cage anode Ø 2–4 cm at 2 mm–5 cm (SC-WO06-017).

## Key quantities and recipes

| claim | quantity / recipe | source doc:page |
|---|---|---|
| SC-SI01-028 | j_crit(W) = 1.43·10⁹ A/m²; j_crit(Al) = 8.04·10⁹ A/m²; films of several hundred atomic layers; 180 °C fixed; explosion µs | SI01 §Каноническая форма… |
| SC-DI01-001 | Formation field 2–10 kV; size fractions–tens µm; charge 10⁸–10¹¹ electrons; lifetime 30–100 ps | DI01 p.3 |
| SC-WO01-022 | Hollow cluster diameter 5–15 µm; 10⁸–10¹¹ electrons; ~2000 K | WO01 p.6 |
| SC-BR02-001 | Autoemission field 20–70 V/µm; current density 10⁴–10⁸ A/cm² | BR02 p.7 |
| SC-MO02-004 | Mean electron concentration in EV 6.6·10²³ cm⁻³; EV rings ~20 µm | MO02 p.7 |
| SC-MO02-022 | 3 µm EV residual charge 2·10¹⁰ e; 10 µm EV loses 3.5·10¹⁴ e per mm; lifetime estimate 3·10⁻¹¹ s; j 6·10¹¹ А/см³ | MO02 p.237 |
| SC-DI01-017 | Crater melt radii 12.7/14.5 µm, Δ = 1.80 µm → N = 6.2·10⁹–1.9·10¹⁰; melt Q ≈ 1.5·10⁻⁶ Дж | DI01 p.26 |
| SC-BR02-020 | Injector: aperture angle ≤ 0.1 рад; hollow channel sizes the cluster; conical wear variant | BR02 p.30 |
| SC-BR02-021 | Injector geometry R1 = 10 мм, R2 = 30 мм, layer 20×20 мм × 10 мкм; q = 1,6 мКл; θ = 1 рад (57,3°) | BR02 p.32 |
| SC-BR02-023 | Regime 1: v* = 5·10³ м/с, j* = 2·10⁵ А/см², τ* = 12·10⁻⁶ с; 90 Кл за 1,5 с | BR02 p.32 |
| SC-BR02-024 | Regime 2 (viscous): v* = 50 м/с, j* = 2·10³ А/см²; 90 Кл за 67,2 с; τ3к = 4 мкс | BR02 p.33 |
| SC-BR02-025 | Electrization coefficient β = 1,2·10⁹ → cluster R = 2,7 см (объём 82,5 см³) | BR02 p.33 |
| SC-BR02-019 | Spherical-cluster capacitance ↑ to ~10⁹× vs UE-K gap | BR02 p.28 |
| SC-AR08-022 | Varicap (1Ts21P volume 15 cm³): C = 0.96 mF @ 25 kV … 24 F @ 1 V; q' = 24 C constant; W up to 30e3 J | AR08 p.7 |
| SC-SI11-005 | Varicap capacitance tuning 10³–10⁶× | SI11 §Физические основы… |
| SC-AR08-003 | Vacuum diode with isolated anode: anomalous capacitance at tens of kV (patent WO 2011031189A1) | AR08 p.1 |
| SC-WO06-017 | W-cone cathode: base Ø 1–2 cm, tip micron, 30°, heater 1000–2000 K, anode Ø 2–4 cm at 2 mm–5 cm | WO06 p.4 |
| SC-WO06-019 | Bubble onset ~10 kV; check voltages up to 30 kV; 10 cm wire as series ohmic probe | WO06 p.5 |
| SC-WO06-006 | Electron-gas mean potential ~1 mV at 1000 K cathode (blocking-voltage method) | WO06 p.2 |
| SC-TC08-004 | Mandelstam–Papaleksi varicap: ~5 kV AC in series RLC, no DC source | TC08 p.1 |
| SC-TC06-026 | Same circuit: measured conversion coefficient k ≈ 1 | TC06 p.6 |
| SC-TC06-027 | Dzhanibekov–Sapogin: 2 dural plates, C ≈ 500 пФ, 16 radial slits, rectified U ≈ 10 В | TC06 p.7 |
| SC-TC08-026 | Novocherkassk 2019: bearing friction coefficient 0,01; pointed radial sectors | TC08 p.7 |
| SC-TC06-030 | Testatika: 1,2 кВт/м³ volume density; up to 10 кВт output (cf. SC-TC08-025 revision: 30–100 W) | TC06 p.7 |
| SC-TC08-015 | П-plate voltage 12–15 кВ → high-voltage air breakdown in Testatika | TC08 p.4 |
| SC-MO03-017 | Katorgin: 60 А µs spike ≈ 30 мкКл ≈ 10¹⁴ частиц; conversion coefficient 2–5 | MO03 p.31 |
| SC-BR02-027 | H₂ plasma: 1 А DC background, spikes to 60 А; 30 кВт pump; brass coaxial electrodes ~12 см | BR02 p.34 |
| SC-TC06-033 | Hot hydrogen plasma: cluster appearance rate ×10⁴ vs Shoulders | TC06 p.8 |
| SC-TC08-108 | Rossi 2011: Ni-Li chips, H₂ 55 бар, cylindrical conducting tube, MW-class thermal | TC08 p.39 |
| SC-TC08-109 | Rossi tube temperature Tp = 200–500 °C, depends on hydrogen pressure | TC08 p.40 |
| SC-TC08-123 | 60 г Ni chips; L = 0,2 м; r = 10 мм; wall 1 мм → P = 1 МВт; 16 ГВт/м³ | TC08 p.45 |
| SC-TC08-124 | Same: C ≈ 10⁻¹⁰ Ф; q = 0,8 мКл; W = 3,2 кДж; I(смещения) = 250 мА; f = 50 Гц | TC08 p.45 |
| SC-TC08-095 | Stationary point-varicap in air: breakdown 2 кВ/мм; d = 5–10 мм; seed current ×10 | TC08 p.35 |
| SC-TC08-085 | η = 5 design: C = 1 мкФ, R = 7,9 кОм, i₀ = 69 мА, P_R = 37,6 Вт (50 Гц, 220 В) | TC08 p.30 |
| SC-TC05-038 | Sleptsov superdielectric: ε до 10⁸; 1000 Ф in 100×50×20 мм³ at 3 В; q = 3000 Кл | TC05 p.12 |
| SC-TC08-043 | Beletsky: 20×20 см plates, 8 мкм Al film, gap 1–2 мм, discharge ≈ 2 кВ/мм at ~90° | TC08 p.13 |
| SC-MO03-027 | 1 m rod at 40 Hz → 253 electrons at rod end (cf. SC-TC08-052: dipole 0,4 мкКл·м) | MO03 p.46 |
| SC-MO03-029 | Disk-generator test: suspension friction < 0,05; match П-plate count to rod count; series LCR | MO03 p.49 |
| SC-MO03-026 | Thermoelectron injector: conical cathode, wide part 200–3000 К, cold narrow tip | MO03 p.43 |
| SC-TC06-062 | Air-breakdown field ≈ 1 В/мкм for the plasma-discharger gaps; power × thousands ∝ conductor volume | TC06 p.14 |
| SC-TC06-048 | Diagnostic: area of statistical ejection on I–t diagram = mean cluster charge | TC06 p.10 |

## Testable protocols

**1. Vacuum-diode cluster generator with diagnostics (WO06 recipe — the most step-complete).**
- Make a tungsten cone cathode (withstands 3000 K): large base Ø 1–2 cm, tip polished to micron
  size, cone angle 30°; attach a heater to the large base, operating 1000–2000 K; place a
  Faraday-cage cylindrical anode with lid, Ø 2–4 cm, coaxially at 2 mm–5 cm; assemble on a vacuum
  stand (SC-WO06-017). [GAP: required vacuum pressure, cathode-stem feedthrough spec]
- Connect an ohmic insert in series with the diode (a 10 cm wire into the oscilloscope input
  suffices) and observe current vs time; sweep voltage up to 30 kV; look for chaotic
  large-amplitude pulses above the ~10 kV bubble-onset threshold (SC-WO06-019, SC-WO06-006).
- Optimize: vary cathode–anode distance, cone heating temperature, and voltage for the most
  powerful cluster generation; only then try operation in air and look for a single luminous
  current cord (SC-WO06-020).
- Follow-up modes: Direction 1 — thermal→electric conversion (heat cathode, measure cathode-anode
  voltage vs temperature) (SC-WO06-023); Direction 2 — insulate the anode with a dielectric and
  study capacitance increase from the inter-electrode cluster (SC-WO06-024, SC-AR08-025).
- Reference baselines: Shoulders' 10 kV impulse, 5–15 µm, 10⁸–10¹¹ e, 30–100 ps (SC-TC03-001,
  SC-WO01-022, SC-DI01-001); electron-gas potential check via blocking voltage (SC-WO06-006).

**2. Aperture injector + charge storage (BR02 program).**
- Fabricate cm-scale prototypes from copper: R1 = 10 mm, R2 = 30 mm, emitting layer 20×20 mm,
  10 µm thick; aperture angle ≤ 0.1 rad; hollow-channel outlet sizes the cluster (SC-BR02-020,
  SC-BR02-021, SC-BR02-029). [GAP: acceptance metric for "cluster produced" other than capacitance]
- Drive: equal HV pulses to cathode and control electrode; injector gradient tears the electron
  layer off the cathode; clusters cross the drift space and merge in the main accumulator
  (SC-BR02-018).
- Expected regimes: regime 1 j* = 2·10⁵ А/см², 90 Кл за 1,5 с; regime 2 j* = 2·10³ А/см², 90 Кл за
  67,2 с (SC-BR02-023, SC-BR02-024).
- Map air breakdown vs electrode geometry (tip/planar/cylindrical) and distance; drive the 15 kW
  AC toroidal-coil pump; compare DC Paschen 25 кВ/см against AC breakdown (an order lower)
  (SC-BR02-029).
- Storage check: capacitance rise of the accumulator vs the UE-K gap (claimed up to ~10⁹×;
  predicted cluster R = 2.7 cm at β = 1,2·10⁹) (SC-BR02-019, SC-BR02-025).

**3. Chips heater with two-class discrimination (Rossi-style, TC08).**
- Fill a cylindrical conducting tube with metal chips (Ni for the reference; any chips claimed to
  work in vacuum), e.g. 60 g, L = 0,2 м, r = 10 мм, wall 1 мм (SC-TC08-117, SC-TC08-123).
- Heat by direct current, geometrically symmetric; monitor current vs time: near the Rossi
  temperature Tp (200–500 °C class, hydrogen-pressure dependent in the original) a powerful chaotic
  current component should appear on the DC background; register Tp with an inductance or
  capacitance sensor next to the cylinder (SC-TC08-118, SC-TC08-119, SC-TC08-109).
- At boiling-plasma state switch the DC off and monitor continued heating of the cooling medium
  (SC-TC08-121); check for the unnoticed AC source with an inductance/capacitance sensor
  (SC-TC08-126).
- Discrimination run (Sapogin's own proposal): first class — chip heating in vacuum WITHOUT
  hydrogen; second class — with hydrogen as in Rossi's experiments; compare released energy
  (SC-TC08-115, SC-TC08-101, SC-TC08-108). [GAP: vessel sealing and hydrogen-handling procedure]
- Instrument the capacitor: C ≈ 10⁻¹⁰ Ф, expected q = 0,8 мКл, displacement current 250 мА at
  50 Гц per the source's re-analysis (SC-TC08-124, SC-TC08-125).

**4. Hydrogen-plasma reactor with oscillographic cluster counting (Katorgin replication).**
- Two thin-walled coaxial brass cylindrical electrodes ~12 см apart; pump hydrogen through; apply
  ~40 кВ; ignite the glow discharge with a 30–35 кВт pump (SC-MO03-016, SC-BR02-027, SC-WO01-083).
- Record anode and cathode current oscillograms: ~1 А DC background with chaotic µs surges to
  60 А; luminous tubular currents ~2000 К (SC-WO01-084, SC-MO03-016).
- Apply the cluster-charge diagnostic: measure the area of a statistical ejection on the I–t
  diagram to get the mean cluster charge (source estimate ~30 мкКл ≈ 10¹⁴ частиц per 60 А spike)
  (SC-TC06-048, SC-MO03-017).
- Calorimetry: input 30–35 кВт vs thermal output; the source claims conversion coefficient 2–5,
  tunable by hydrogen pressure, pumping speed, electrode geometry (SC-MO03-017, SC-TC08-077).
- Radiation safety: unclosed displacement current is broadband and unshieldable; harm threshold
  quoted P > hundreds of watts (SC-TC06-064, SC-TC05-025).

**5. Mechano-electric varicap (Novocherkassk/Testatika line, room-temperature entry experiment).**
- Mount 40–60 conducting rods radially at equal azimuthal angles on a dielectric disk; П-shaped
  take-off plates with tip screws at tunable distance, not touching the disk; spin at constant
  angular velocity (SC-MO03-028).
- Acceptance gate: suspension friction coefficient < 0,05 (above it friction beats the
  electric-origin moment and the system will not rotate); match П-plate count to rod count for
  maximal torque; connect the variable capacitance into a high-voltage series LCR circuit
  (SC-MO03-029, SC-MO03-027, SC-TC08-052).
- Replication anchor points: Mandelstam–Papaleksi ~5 кВ AC in the RLC (SC-TC08-004); their
  measured conversion coefficient k ≈ 1 as the null reference (SC-TC06-026); Novocherkassk 2019:
  friction 0,01 metal bearing, AC output without a resonant circuit, no self-rotation (SC-TC08-026,
  SC-TC08-027, SC-TC08-029).
- Improvement levers: metal low-friction bearings; takeoff-plate count × sector count; sector
  profile from flagellar bacterial motors (SC-TC08-022, SC-TC08-023, SC-TC08-009, SC-TC08-021).

## Phenomenology map

- **Thresholds.** Cluster formation fields 2–10 kV (SC-DI01-001, SC-SI04-006); picosecond current
  fragmentation at ~10 kV impulse in vacuum (SC-TC03-001, SC-SI10-009); WO06 protocol expects
  bubble onset ~10 kV and sweeps to 30 kV (SC-WO06-019); air breakdown rules: 25 кВ/см DC Paschen
  vs an order lower on AC (SC-BR02-029), 2 кВ/мм point-plane (SC-TC08-095), ≈1 В/мкм designed gaps
  (SC-TC06-062), point-plane subcritical discharge 1.5× below classical breakdown (SC-TC08-078);
  film explosions at j_crit = 1,43·10⁹ А/м² (W) / 8,04·10⁹ А/м² (Al) at 180 °C (SC-SI01-028);
  self-rotation needs friction < 0,05 (SC-MO03-029) and was not reached at 0,01-bearing without
  further reduction (SC-TC08-029).
- **Timescales.** EV glow-out 30–100 ps (SC-DI01-001, SC-MO02-004: 3·10⁻¹¹ s); bubble formation
  compression ≈ 70 пс then stationary ≈ 70 пс (SC-TC08-031, SC-TC08-032); cluster-formation
  τ3к = 4 мкс in the injector (SC-BR02-024); µs current surges in hydrogen plasma (SC-WO01-084);
  µs explosions above j_crit in nanofilms (SC-SI01-028); water plasmoids form in apparent µs and
  radiate ms–s (SC-SI02-019, SC-AR09-002); plasmoids ("tracers") can reside in metal for months,
  releasing energy at surface defects (SC-MO03-015, SC-WO01-064).
- **States and classes.** Plasmoids occur electrically neutral, positive, negative (SC-AR09-003,
  SC-SI02-020); radiating (> 1 Å radius) vs non-radiating (< 1 Å) plasmoid classes — only the
  former decay spontaneously at equal plasma temperature (SC-TC08-102); compression vs expansion
  EDP set by the sign of the temperature gradient (cold centre → compressing) (SC-SI10-020,
  SC-TC01-003); cyclic three-step synthesis → stationary → decay with re-synthesis (SC-TC01-042,
  SC-TC01-005, SC-TC08-103); claimed synthesis:decay energy asymmetry 1:10²–10³ (SC-TC06-002,
  SC-TC02-066, SC-SI06-011, SC-TC06-038).
- **Where clusters are claimed to arise.** Vacuum diode gaps at tip cathodes (SC-TC02-033,
  SC-TC03-001); hydrogen plasma between coaxial electrodes (SC-BR02-027, SC-MO03-016); discharge
  films in purified/tap water (SC-AR09-001, SC-SI02-017/018); metal films and ≤20 nm wires at GHz
  (SC-SI01-028, SC-SI01-025); solid-state plasma of heated chips/powder — the Rossi line
  (SC-TC08-120, SC-TC06-050); spark dischargers of the Testatika (SC-TC06-031); air gap of a
  Wimshurst machine (SC-MO03-002, SC-WO01-011); LED/gas-discharge lamp currents (claimed chaotic
  component) (SC-TC06-053).
- **Crater impact morphology.** Ring-shaped melted crater with central ridge on titanium; melt
  radii 12,7/14,5 мкм, Δ = 1,80 мкм → incident N = 6,2·10⁹–1,9·10¹⁰ electrons; three impact classes
  by energy release (SC-BR02-007, SC-WO01-062, SC-DI01-017, SC-DI02-010, SC-SI04-011).
- **Stated replication caveats (from the sources themselves).** Not all excess-energy experiments
  were repeatable elsewhere (SC-WO01-088); modern French kenotrons do not produce clusters for
  lack of cathode points (SC-WO06-012, SC-WO06-014); Testatika conversion data were not published
  (SC-TC06-030); Zhuravkov's self-reproducing reactor claim is unpublished e-mail material
  (SC-TC08-080); Dzhanibekov–Sapogin 10 V result is unpublished (SC-TC06-027).

## Theory aside (secondary)

NOT load-bearing for the practical layer; the models are self-consistent-field "electric
hydrostatics" descending from Emden, Laue (1912–1914 thermoelectron equilibria), Vlasov and
Frenkel (1948): a total-pressure integral yields "forces of field origin" that hold like charges
against Coulomb dispersal, giving hollow, thin-walled bubble equilibria with a charge-free cavity
(SC-WO01-038, SC-WO01-041, SC-WO01-044, SC-BR01-005, SC-DI01-004, SC-MO03-012, SC-SI01-005). On
top of it stand: the electrization parameter ε = C/C₀ varicap theory (SC-AR08-002, SC-AR08-013,
SC-AR08-015); the Pustovoit-type explosive-instability model of plasmoid birth in two-component
plasma, reduced to a Burgers-like equation with slow/fast-wave instability classes (SC-AR09-010,
SC-AR09-020, SC-AR10-010, SC-TC08-042); and the "law of electrodynamic induction" +
parametric-power-resonance displacement-current energetics, including explicit claims that energy
conservation fails in bubble synthesis/decay and at certain AC frequencies (SC-TC06-016,
SC-TC08-081, SC-TC08-083, SC-TC06-002). The same machinery is extended speculatively to neutron
supermassive clusters at 10¹¹–10¹² K, Tunguska, lunar craters and the solar corona (SC-AR05-063,
SC-PM02-003, SC-BR01-022, SC-BR01-026, SC-PM02-020, SC-TC06-052) — astrophysics, not lab art.
Debt-candidate-tagged claims in this bucket (99 of 629; registry: `clusters/debt-candidates.md`)
cluster exactly on these load-bearing-for-theory points, e.g. AR08 SC-AR08-005/007/012/026/027,
AR09 SC-AR09-007/021/025, AR10 SC-AR10-005/022/028/030/031, TC06 SC-TC06-002/007/008/012/023/
037/038/040/044/046/047/052/053/064, TC08 SC-TC08-002/005/007/018/025/027/028/034/039/041/046/
048/063/070/078/080/081/083/105/111/113/127/129/130/131/133/135/137, WO01 SC-WO01-009/013/018/
019/023/025–031/046/050–053/056/057/061/063–065/068/072/076–081/085/086/087/089, plus the BR01/
BR02/MO02/MO03/PM01/PM02/AR05 lists in the registry. The conflict line runs straight through the
art: Earnshaw-type prohibition vs "field-origin forces" (SC-WO01-008 vs SC-BR02-008), and
energy-conservation vs the 1:1000 synthesis/decay asymmetry and the 160 µJ vs 154 mJ cluster
energy-balance claim (SC-TC06-002 vs SC-TC02-066; SC-WO01-051).

## Open questions

1. Are Shoulders' EVs, Mesyats' ectons and the hydrogen-plasma current portions one object class?
   Compare parameters: 30–100 ps lifetime vs µs ecton/η spikes; 10⁸–10¹¹ e vs ~30 мкКл portions
   (SC-DI01-001, SC-MO02-022, SC-DI02-001, SC-BR02-002, SC-MO03-017, SC-TC06-033).
2. Verify or bound the claimed synthesis/decay energy asymmetry 1:10²–10³ and the cluster
   energy-balance figure 160 µJ (source work) vs 154 mJ (layer energy) — this is the direct
   energy-conservation conflict (SC-TC06-002, SC-TC02-066, SC-SI06-011, SC-WO01-051).
3. Reconcile the varicap numbers: measured patent anomaly (SC-AR08-003), model table
   C = 0,96 мФ…24 Ф (SC-AR08-022), tuning 10³–10⁶× (SC-SI11-005), storage claim ~10⁹×
   (SC-BR02-019), and the k ≈ 1 null measurement of the same circuit family (SC-TC06-026).
4. Replication determinants: which cathode-surface parameters (tip radius, roughness, work
   function) decide cluster production, given kenotron failures and Petersburg successes
   (SC-WO06-012, SC-WO06-014, SC-TC08-120)?
5. Does the "critical displacement current density" mode exist (SC-TC08-063, SC-TC08-064,
   SC-TC08-096)? Check the Rossi re-analysis consistency: C ≈ 10⁻¹⁰ Ф with 250 мА at 50 Гц vs
   1 МВт/16 ГВт/м³ calorimetry (SC-TC08-123, SC-TC08-124, SC-TC08-125, SC-TC01-047).
6. Hydrogen's role: run the two-class chips experiment (vacuum vs H₂) of SC-TC08-115; is the
   55 бар Ni-Li configuration thermally distinct from vacuum-only chips (SC-TC08-108, SC-TC08-101)?
7. Audit Katorgin calorimetry: conversion coefficient 2–5 claim vs measured input 30–35 кВт and
   the ×10⁴ cluster-birth-rate estimate (SC-MO03-017, SC-TC08-077, SC-TC06-033, SC-TC06-039).
8. Reproduce Marakhtanov's film j_crit values (1,43·10⁹ / 8,04·10⁹ А/м² at 180 °C) and the µs
   explosion signature (SC-SI01-028).
9. Test Zhuravkov's two claims: breakdown 1.5× below classical in subcritical point-plane
   discharge; the unpublished self-reproducing reactor (SC-TC08-078, SC-TC08-080).
10. Establish the electric/mechanical power ratio Mandelstam–Papaleksi never measured and audit
    Testatika power claims 10 кВт vs the 30–100 W revision (SC-TC08-006, SC-TC06-030,
    SC-TC08-025, SC-TC08-017).
11. Verify the Wimshurst glow-layer thickness (µm–tens of µm at ~25 кВ) as a room-temperature
    cluster-formation datum (SC-MO03-002, SC-WO01-011).
12. Decide the mechanical-varicap autonomous-source claim (AC without a resonant circuit,
    Novocherkassk 2019) against circuit-theory expectations (SC-TC08-027, SC-TC08-028).
