# emden-gravity-cosmic — synthesis

Practical-first synthesis of the 151 claims in this bucket. Every assertion
is pinned to SC-* ids. This file organizes
the art, it does not adjudicate it.

Bucket composition: AR05 (46), AR02 (29), BR01 (16), WO04 (16), WO05 (9),
AR03 (6), PM01 (5), WO03 (5), TC01 (4), SI01 (4), SI03 (4), SI02 (3),
DI01 (2), SI06 (2). Roughly 25 claims carry practical facets
(geometry / measurement / experiment / phenomenology); the rest is the
Emden–self-consistent-gravity model family that generates the sizing formulas
below. A gravitational-spinner sub-family (PM01, TC01, WO05, WO03) rides in
this bucket because its claims tie wheel self-rotation to the gravitational
field; its sibling claims live in the `general` bucket (PM01-001…009,
WO05-001/003/004/006/016/020…).

## The art (practical layer)

- **Sizing recipe for a hollow "gas bubble" held by a self-consistent
  gravitational field** (the bucket's most reusable engineering content).
  Inputs: particle mass m, temperature T, concentration/density on the
  zero-pressure sphere (n₀ / ρ₀), state parameter β. Steps: compute spatial
  scale l = sqrt(kT/(2πGmρ₀)) [SC-AR02-019, SC-AR05-017]; set the
  zero-pressure sphere radius R = β·l [SC-AR02-024, SC-AR05-022]; cut the
  density distribution at a chosen floor to get cavity radius r₁ and outer
  radius r₂; mass = ⟨ρ⟩ × shell volume. Two cut conventions appear:
  r₁ = 0.6R, r₂ = 1.6R with cutoff at n = 0.2n₀ [SC-AR02-034, SC-AR02-035]
  vs r₁ = 0.24R, r₂ = 2.24R with cutoff at n = 0.01n₀ [SC-BR01-018,
  SC-BR01-019, SC-BR01-020]. The two conventions are not reconciled in the
  sources (see Open questions).
- **Worked sizing cases** (all values as stated):
  - Oxygen gas: ρ₀ = 1.33 kg/m³, T = 293 K, m = 5.32·10⁻²⁶ kg →
    l = 1.2·10⁷ m; β = 3 → R = 3.6·10⁷ m (~5 Earth radii), r₁ = 2.16·10⁷ m,
    r₂ = 5.76·10⁷ m, ⟨ρ⟩ = 0.133 kg/m³ → mass 10²³ kg ("somewhat exceeding
    the mass of the Moon") [SC-AR02-034]. Second oxygen case at
    n₀ = 1e25 m⁻³, 300 K: p₀ = 4.14e4 Pa, ρ₀ = 0.532 kg/m³, R = 3l =
    5.6e7 m, M = 9.6e23 kg, interaction energy W = 7.0e28 J; β = 10 →
    M = 8.6e24 kg, W = 4.3e29 J [SC-BR01-018].
  - Icy nanoparticles of diameter 40 nm: m = 3·10⁻²⁰ kg, ρ₀ = 80 kg/m³,
    T = 250 K, n₀ = 2.7e21 m⁻³ → l = 1.85·10³ m; β = 3 → R = 5.6e3 m,
    r₁ = 3.3e3 m, r₂ = 8.9e3 m; ⟨ρ⟩ = 8 kg/m³ → mass "22 billion tons"
    [SC-AR02-035]. This is the Tunguska object in [SC-BR01-025]: p₀ = 9.3 Pa,
    R = 3l = 5.55e3 m, cavity r₁ = 1.33e3 m, r₂ = 12.4e3 m,
    N = 4.7e30 particles, M = 1.41e11 kg (141 million tons), W = 1.53e13 J;
    at 40 km/s, Ek = 1.13e20 J = "24.6 billion tons of TNT"
    (1 t TNT = 4.6e9 J); β = 10 variant: M = 1.3e15 kg, "226 trillion tons
    of TNT" [SC-BR01-025].
  - Water vapor: n₀ = 1e25 m⁻³, 300 K, β = 3 → R = 1.0e8 m,
    M = 3.0e24 kg, W = 4.0e29 J; β = 10 → M = 2.8e25 kg [SC-BR01-019].
  - Neutron gas: n₀ = 1e25 m⁻³, 300 K, β = 3 → R = 1.8e9 m, r₁ = 0.43e9 m,
    r₂ = 4.0e9 m, M = 9.9e26 kg, W = 2.32e33 J; β = 10 → M = 8.9e27 kg
    [SC-BR01-020].
  - Predicted exotic "water-gas bubble": water molecule mass 3.0e-26 kg,
    n₀ = 3.33e28 m⁻³, T = 293 K, β = 3 → R = 1.7e6 m, cavity 0.4e6 m,
    r₂ = 3.8e6 m ("1.7 times smaller than Earth radius"),
    M = 5.0e22 kg; with near order of water molecules accounted the mass
    drops "5-7 orders" — offered as a possible delivery mechanism of Earth's
    water [SC-BR01-027].
- **Design similarity laws** for field traps of equal particle mass:
  l = C·(T/n₀)^(1/2); trap mass scale M* = F·T^(3/2)/n₀^(3/2); at fixed T,
  l = E·M*/T with E = G/(2k) [SC-AR05-047]. Capacity: potential-well traps
  hold 1–2 orders of magnitude more mass than the mass scale for
  3 ≤ α ≤ 10 (Table 1) [SC-AR05-049]; first-kind traps always out-mass
  second-kind traps at equal parameters, the difference growing with α
  (Table 3); increasing n₀ at constant α decreases trap mass and size, and
  conversely [SC-AR05-056]. Neutron traps at T = 10¹¹ K across
  n₀ = 2.0·10²⁰…2.0·10²⁶ cm⁻³: M* = 0.599·10⁴¹…0.599·10³⁸ g,
  l = 0.242·10¹⁵…0.242·10¹² cm (Table 2) [SC-AR05-054].
- **Numerical solver protocol** behind every estimate above: integrate
  φ″ + 2φ′/r = 4πGmn₀·exp(−mφ/kT) (6.1) with special fourth-order
  Runge–Kutta formulas, step 10⁻⁴, boundary conditions φ(R) = φ₀ = 0,
  φ′(R) = 0; the zero-sum of pressure gradients is then satisfied
  automatically [SC-AR05-036, SC-AR02-024]. The β² ≫ 1 closed-form
  approximation p = 1 − α²[exp(2η) − 1] is stated valid for α ≥ 3 and
  claimed exactly correct in cylindrical symmetry [SC-AR05-027,
  SC-AR05-033].
- **Handy closed forms** (checkable without simulation): plane well
  φ = φ₀ + (2kT/m)·ln ch(x/l), ρ/ρ₀ = n/n₀ = p/p₀ = ch⁻²(x/l),
  gx = −g₀·th(x/l) with g₀ = 2kT/ml = 8πGp₀; field pressure
  D = D₀·th²(x/l), D₀ = p₀ = g₀²/(8πG); characteristic sizes −3l…3l
  [SC-BR01-010, SC-AR05-017, SC-AR05-018, SC-AR05-019, SC-AR02-021].
  Second-kind (logarithmic) trap: φ = φ₀ + φ*·ln(r/l), gr/g₀ = l/r,
  ρ/ρ₀ = l²/r², with ~r⁻¹ field and ~r⁻² density singularities at zero;
  the full pressure is no longer an integral there [SC-AR05-039,
  SC-AR05-041, SC-AR05-042, SC-AR05-044]. Exact cylindrical-symmetry
  solutions come in three branches (H > 0 sh², H = 0 ln², H < 0 sin² in
  ln(x₀/x)) [SC-AR03-004, SC-AR03-007].
- **Inverse Tunguska protocol**: measuring the ellipse occupied by the
  "mast forest" is stated to allow computing the fallen body's mass, impact
  angle and geometric dimensions via the theory; cavity estimable at ~1 km
  diameter; source-spread of body parameters: gas-ball diameters 2.7–50 km,
  masses from 3 thousand tons to 1.3 trillion tons [SC-BR01-028,
  SC-BR01-024].
- **Gravitational spinner (Aldo Costa)** — the only repeatedly observed
  hardware in the bucket: wheel radius > 10 m [SC-WO05-007] (11 m per
  [SC-TC01-018]), more than 200 weights that change their distance from the
  rotation axis in two half-spaces separated by a vertical plane through
  the axis [SC-WO05-008], angular speed ~0.01 rad/s (author's estimate)
  [SC-WO05-008], rotating ~20 years with lubrication every 3 months
  [SC-WO05-007] (monthly per [SC-TC01-018]). Bench-testable equation of
  motion: I·dω/dt = M₀ − M₁ − M₂, M₂ = ηω; stationary ω* = (M₀ − M₁)/η,
  independent of I; no rotation when friction moment exceeds the asymmetric
  moment [SC-WO05-014; the ω* form is SC-WO05-016, cross-bucket `general`].
- **The canonical "kitchen"** that generates all of the above: any plane
  equation φ″ = f(φ) (Poisson of special kind Δφ = f(φ)) reduces by Kamke's
  algorithm (multiply by 2φ′; U(φ) = −∫f(φ)dφ) to the "living forces"
  integral φ′²/2 + U(φ) = P [SC-WO04-010, SC-WO04-011, SC-SI01-002]; P is
  read as the total pressure — field pressure (≈ strength²/8πG) plus
  particle pressure — and is claimed conserved in all collectively
  interacting systems (gravity, electrostatics, magnetism)
  [SC-WO04-012, SC-SI01-001, SC-WO04-013, SC-WO04-014].
- **What the theory predicts observably** (see Phenomenology map for
  thresholds): a thin-wall bubble geometry with an empty cavity and no sharp
  density boundary [SC-WO04-020, SC-AR05-018]; epicenter-spared destruction
  for hollow impactors [SC-AR02-036, SC-AR05-067]; black holes as
  solar-system-sized hot gas bubbles whose trap state is NOT determinable
  from stellar-velocity mass measurements [SC-SI01-037, SC-WO04-022,
  SC-AR05-065]; binding energy shifting the observed mass of an accumulation
  vs the additive one, in either sign [SC-WO04-023].

## Key quantities and recipes

| claim | quantity / recipe | source doc:page |
|---|---|---|
| SC-AR02-019 | l = sqrt(kT/(2πGmρ₀)); φ = (2kT/m)·ln[(1/α)·ch(αx/l)] | AR02 p.2 |
| SC-AR02-024 | β² = 2πGm²n₀R²/kT = T*/T = R²/l²; T* = 2πGm²n₀R²/k | AR02 p.3 |
| SC-AR02-021 | g* = 2kT/ml = 8πGp₀; ρ/ρ₀ = [(1/α)ch(αx/l)]⁻² | AR02 p.3 |
| SC-AR05-017 | φ = φ₀ + φ*·ln[ch(x/l)], φ* = 2kT/m | AR05 p.6 |
| SC-AR05-047 | l = C·(T/n₀)^(1/2); M* = F·T^(3/2)/n₀^(3/2); l = E·M*/T | AR05 p.18 |
| SC-AR05-049 | well-trap capacity exceeds mass scale 1–2 orders for α = 3…10 | AR05 p.18 |
| SC-AR05-054 | neutron traps, T = 1e11 K: M* = 0.599e41…0.599e38 g, l = 0.242e15…0.242e12 cm | AR05 p.19 |
| SC-AR05-036 | RK4, step 1e-4, BC φ(R) = φ₀ = 0, φ′(R) = 0 | AR05 p.14 |
| SC-AR05-027 | approximation p = 1 − α²[exp(2η) − 1], valid α ≥ 3 | AR05 p.10 |
| SC-AR02-034 | O₂ ball: l = 1.2·10⁷ m; β=3: R = 3.6·10⁷ m, r₁ = 2.16·10⁷ m, r₂ = 5.76·10⁷ m, M = 1e23 kg | AR02 p.5 |
| SC-AR02-035 | ice-NP ball (40 nm): l = 1.85·10³ m, R = 5.6e3 m, r₁ = 3.3e3 m, r₂ = 8.9e3 m, M = 22 billion tons | AR02 p.5 |
| SC-BR01-011 | A = kT/sqrt(2πG) = 3.14e-6 kg/m^(1/2) at 300 K; l = A/(m·n₀) spans 10⁶–10⁹ m | BR01 p.42 |
| SC-BR01-018 | O₂, n₀ = 1e25 m⁻³: R = 5.6e7 m, M = 9.6e23 kg, W = 7.0e28 J | BR01 p.68 |
| SC-BR01-019 | water vapor: R = 1.0e8 m, M = 3.0e24 kg, W = 4.0e29 J | BR01 p.69 |
| SC-BR01-020 | neutrons: R = 1.8e9 m, M = 9.9e26 kg, W = 2.32e33 J | BR01 p.70 |
| SC-BR01-025 | Tunguska snowball: 40 nm pellets, R = 5.55e3 m, cavity 1.33e3 m, M = 1.41e11 kg, Ek = 1.13e20 J | BR01 p.92 |
| SC-BR01-027 | water-gas bubble: R = 1.7e6 m, r₂ = 3.8e6 m, M = 5.0e22 kg | BR01 p.94 |
| SC-BR01-028 | inverse problem: mast-forest ellipse → mass, impact angle, dimensions | BR01 p.95 |
| SC-AR05-041 | second-kind trap: gr/g₀ = l/r (~r⁻¹ singularity) | AR05 p.16 |
| SC-AR05-042 | second-kind trap: ρ/ρ₀ = l²/r² (~r⁻² singularity) | AR05 p.16 |
| SC-AR05-044 | second-kind: P = 2p₀l²/r² ≠ const; gradients ~r⁻³ | AR05 p.16 |
| SC-AR03-007 | three exact cylindrical branches in ln(x₀/x) | AR03 p.2 |
| SC-WO05-007 | Costa wheel: radius > 10 m, ~20 years rotation, lubrication every 3 months | WO05 p.2 |
| SC-WO05-008 | >200 movable weights; angular speed ~0.01 rad/s | WO05 p.2 |
| SC-WO05-016 (cross-bucket: `general`) | ω* = (M₀ − M₁)/η; independent of I; no rotation if M₁ > M₀ | WO05 p.4 |
| SC-WO05-014 | I·dω/dt = M₀ − M₁ − M₂; M₂ = ηω | WO05 p.3 |
| SC-WO04-011 | Kamke reduction: φ′²/2 + U(φ) = P, U(φ) = −∫f(φ)dφ | WO04 p.3 |
| SC-WO04-020 | bubble radii from 1 km to solar-system sizes and above | WO04 p.5 |
| SC-SI01-037 | SMBH as gas bubbles: 1e6…1e9 solar masses, T = 1e11…1e12 K, solar-system size | SI01 § Каноническая форма… |

## Testable protocols

- **Hollow-ball sizing + solver reproduction** [SC-AR05-036, SC-AR02-024,
  SC-BR01-018, SC-AR02-034]. (1) Implement eq. (6.1)
  φ″ + 2φ′/r = 4πGmn₀exp(−mφ/kT). (2) Integrate with fourth-order
  Runge–Kutta, step 10⁻⁴, BC φ(R) = φ₀ = 0, φ′(R) = 0 [SC-AR05-036].
  (3) Reproduce the integral-curve family and the special Emden point
  [SC-AR02-027, SC-AR05-026]. (4) For a chosen gas/particle set, compute l,
  R = βl, cut at n = 0.2n₀ [SC-AR02-034] and at n = 0.01n₀
  [SC-BR01-018], and compare M, r₁, r₂ against the published tables.
  [GAP]: the sources do not state which cutoff convention is the faithful
  one — both appear.
- **Plane-solution bench check** [SC-BR01-010, SC-AR05-017, SC-AR05-018,
  SC-AR05-019]. Verify φ = φ₀ + (2kT/m)ln ch(x/l), ch⁻² density profile,
  th(x/l) field profile, and the constant total pressure P = p₀ by pure
  numerics (substitution back into (2.1)–(2.5)); also verify the claimed
  exactness of the α² ≫ 1 solution in cylindrical symmetry
  [SC-AR05-033]. [GAP]: no laboratory analogue of a plane self-consistent
  gravitating layer is extractable from this bucket (the like-charge
  analogue lives in DI01/DI02, see `general`).
- **Costa spinner replication + ω\* law** [SC-WO05-007, SC-WO05-008,
  SC-WO05-014; ω* consequence SC-WO05-016 cross-bucket `general`].
  (1) Build a wheel of radius > 10 m.
  (2) Arrange > 200 movable weights whose distance from the axis can change
  in two half-spaces separated by a vertical plane through the axis
  [SC-WO05-008]. (3) Launch with initial angular velocity ω₀.
  (4) Measure stationary ω and test ω* = (M₀ − M₁)/η and its independence
  of I [SC-WO05-016, cross-bucket `general`]. (5) Watch for stoppage when
  the asymmetric moment
  disappears [SC-WO05-015]. [GAP]: weight masses, weight travel, and the
  mechanism producing M₀ are not extracted anywhere in the corpus.
- **Inverse Tunguska reconstruction** [SC-BR01-028, SC-BR01-024].
  (1) Digitize the ellipse of the standing "mast forest" and the fallen-taiga
  boundary. (2) Feed ellipse dimensions into the hollow-snowball model with
  40 nm ice pellets, n₀ = 2.7e21 m⁻³, T = 250 K, β = 3 [SC-BR01-025].
  (3) Output mass, impact angle, r₁/r₂. [GAP]: the actual inversion formulas
  (ellipse → angle/mass) are asserted, not extracted; descent speed 40 km/s
  is taken from observation lists [SC-BR01-024].
- **Water-gas bubble ocean test** (prediction with a number attached)
  [SC-BR01-027]: an impact of the quoted bubble would raise the ocean level
  by "97 km" without near-order correction, or "hundreds of meters" with it
  — a paleogeological signature the sources themselves propose to look for.
  [GAP]: no extracted procedure for the geological search.

## Phenomenology map

- **What the theory predicts observably (practical-first).** (i) Field
  traps exist as hollow shells: a cavity free of matter inside r₁, a shell,
  and no matter beyond r₂, with NO sharp density boundary anywhere — the
  profile is smooth (ch⁻² or (ch)⁻²-family), so "bubble walls" are gradual
  [SC-AR02-021, SC-AR05-018, SC-AR05-045, SC-WO04-020]. (ii) Hollow
  impactors spare the epicenter: particle flux density at the center of
  impact is substantially smaller than in adjacent layers → minimal
  epicenter destruction, matching Kulik's expedition and the standing
  "mast forest" [SC-AR02-036, SC-AR05-067, SC-SI01-036, SC-SI03-004,
  SC-BR01-024]. (iii) Galactic black holes are non-radiating hot neutron/
  hydrogen/helium bubbles; their masses are measurable from stellar
  velocities but the trap state is not determinable that way [SC-SI01-037,
  SC-WO04-022, SC-AR05-064, SC-AR05-065]. (iv) Binding energy of particles
  with the field can raise or lower the observed mass of an accumulation
  relative to the additive count [SC-WO04-023]. (v) Passive states of
  galactic nuclei can host non-radiating high-temperature neutrons
  [SC-AR05-064].
- **Thresholds and state parameters.** The well/gap character is governed
  by the single state parameter α (or β): 0 < α ≤ 1 gives non-negative well
  minimum with gentle walls; α > 1 gives negative minimum with steeper
  walls [SC-AR02-020]; β² ≪ 1 pushes the special Emden point far out,
  β² ≫ 1 brings it near the origin and licenses the closed-form
  approximation (satisfactory already at α = 3) [SC-AR05-026, SC-AR05-027].
  Well traps out-retain gap traps at equal conditions [SC-AR05-062]; the
  capacity excess is 1–2 orders for α = 3…10 [SC-AR05-049]. Second-kind
  traps come in three state types (negative potential energy / positive
  with large cavity / intermediate), with M₂ = M*·χ for dense packing
  [SC-AR05-050, SC-AR05-052].
- **Retention mechanism (claimed).** The self-consistent field holds matter
  by static field-origin forces: the Bernoulli force coincides with the
  field-pressure gradient and compensates Newtonian attraction volume by
  volume; total pressure is conserved in plane symmetry [SC-AR02-015,
  SC-AR02-016, SC-AR05-020, SC-BR01-006, SC-BR01-009]. The same five
  postulates are claimed to cover gravitating and like-charge systems
  [SC-BR01-001, SC-DI01-019, SC-DI01-020], and the first integral is stated
  to explain why static gravitating systems do not collapse [SC-SI03-003].
  Pressure gradient is repulsive for gravitating particles, attractive in
  like-charge systems [SC-SI06-003].
- **Spinner phenomenology.** Long self-rotation of asymmetric wheels:
  in-bucket historical anchor — Villard de Honnecourt 1240 and Mariano di
  Jacopo 1438 [SC-WO05-005]; further historical exemplars catalogued in the
  `general` bucket (Bhaskara's half-filled tubes SC-WO05-004, Bessler/
  Orffyreus checks at 2 weeks, 40 days, 2 months SC-WO05-003, Howard
  Johnson's magnetic motor 1979 SC-WO05-006) and
  current (Aldo Costa, parameters above [SC-WO05-007, SC-WO05-008,
  SC-TC01-018]). Claimed regimes: constant ω with three competing torques
  [SC-PM01-005, SC-TC01-011], power of driving moment always equal to total
  friction power while the wheel "draws energy from the gravitational fuel
  tank" [SC-PM01-008, SC-TC01-013], half-period draw / half-period return
  cycle [SC-PM01-010].
- **Energy-infrastructure forecasts attached to the path** (WO03):
  counter-rotating-acrylic-disk generation (Testatica) is claimed as the
  seed of "Divine Fire" technology that would multiply ecological
  electricity production "hundreds of times" within 10 years
  [SC-WO03-002, SC-WO03-029]; solar/wind are characterized as seed-energy-
  dependent sources with land and noise penalties [SC-WO03-010] (storage
  costs and 10-year modernization: SC-WO03-011, cross-bucket `general`);
  civilization's waste heat is claimed
  a contributor to observed warming [SC-WO03-006], with a long-phase cosmic
  warming alternative [SC-WO03-005] (companion claims in `general`:
  SC-WO03-003/004).

## Theory aside (secondary)

NOT load-bearing for the practical layer; linked into
`clusters/debt-candidates.md`. What the models assume about measurable
reality: (1) isothermal Boltzmann equilibrium holds at astrophysical scales
(ρ = ρ₀exp(−m(φ−φ₀)/kT)) with purely Newtonian pair interaction
[SC-AR05-009, SC-AR02-012, SC-BR01-007]; (2) the field quantity g²/8πG is a
mechanical pressure that can balance gas pressure term by term — this is
the assumption every sizing number above rests on [SC-WO04-012,
SC-AR05-019]; (3) boundary conditions are fixed not arbitrarily but by the
plane total-pressure first integral, and the resulting solution is claimed
to describe real astrophysical density distributions [SC-AR02-002,
SC-SI02-029, SC-SI03-001]; (4) polytropic generalizations with the n < 0
case "not considered before" [SC-BR01-008]. The claim that the retention
property is "previously unknown" and the naming of "Emden-Laue-Frenkel
forces" are theory-position statements, not measurement [SC-AR02-017,
SC-AR05-016, SC-WO04-018]. Historical attributions (Emden 1907, Laue 1914,
Frenkel 1948/1953, Baryakhtar's 2003 evaluation) frame provenance, not
evidence [SC-AR02-003, SC-AR02-004, SC-WO04-015, SC-WO04-017, SC-SI06-001,
SC-WO04-007]. Debt-candidate claims in this bucket (per
`clusters/debt-candidates.md`): SC-AR02-017, SC-AR02-036, SC-AR05-016,
SC-AR05-064, SC-AR05-067, SC-BR01-027, SC-WO04-018, SC-WO04-022,
SC-WO04-023, SC-PM01-002, SC-PM01-005, SC-PM01-008, SC-PM01-010,
SC-TC01-011, SC-TC01-013, SC-TC01-018, SC-WO03-002, SC-WO03-005,
SC-WO03-029, SC-WO05-007, SC-WO05-011, SC-WO05-013. The bucket's internal
tension on spinners: the circulation theorem says zero work over a cycle in
a uniform field — acknowledged as "a correct mathematical result" for a
single mass [SC-PM01-003, SC-TC01-010] — vs the four-force rebuttal
(gravity, support reaction, sliding friction, viscous friction) claiming the
work transfer happens through the support-reaction force [SC-WO05-009,
SC-WO05-012, SC-WO05-013, SC-WO05-014].

Residual model-family claims (accounted, not separately load-bearing): the
base equation system and its plane/spherical reductions are restated in
parallel across AR02 and AR05 [SC-AR02-001, SC-AR02-006, SC-AR02-007,
SC-AR02-008, SC-AR02-009, SC-AR02-010, SC-AR02-011, SC-AR02-013,
SC-AR02-014, SC-AR02-018, SC-AR02-023, SC-AR05-002, SC-AR05-006,
SC-AR05-007, SC-AR05-008, SC-AR05-010, SC-AR05-011, SC-AR05-012,
SC-AR05-013, SC-AR05-014, SC-AR05-015, SC-AR05-021, SC-AR05-060,
SC-AR05-061, SC-BR01-004]; the order-reduction/η(ξ) machinery and
approximation validity [SC-AR02-026, SC-AR02-028, SC-AR05-025,
SC-AR05-032, SC-AR05-029]; generalized-Emden classification and exact-
solution search context [SC-AR03-001, SC-AR03-002, SC-AR03-003,
SC-AR03-005, SC-AR05-003, SC-AR05-005, SC-AR05-023, SC-AR05-040,
SC-SI02-002, SC-SI02-028, SC-SI03-002]; figure/curve inventories
[SC-AR02-022]; the charge-bubble-on-a-sphere twin of SI01-012
[SC-WO04-025]; Tunguska literature-state context (expeditions, comet
mainstream, comet-nucleus parameters) [SC-BR01-030]; canonical-methods
framing and recognition history [SC-WO04-001, SC-WO04-002, SC-WO04-009].

## Open questions

1. Which cavity cutoff is the faithful reading of the theory — r₁ = 0.6R at
   n = 0.2n₀ [SC-AR02-034] or r₁ = 0.24R at n = 0.01n₀ [SC-BR01-018]? The
   choice changes every published mass by large factors.
2. Internal consistency of SC-BR01-019: "M = 3.0e24 kg, which the author
   states exceeds the Earth mass" — recompute against the actual Earth mass
   and against the bucket's own neutron case (SC-BR01-020, "three orders
   above Earth mass").
3. BR01-025's own numbers: Ek = 1.13e20 J exceeds the claimed interaction
   energy W = 1.53e13 J by seven orders — what, in the model, holds the
   snowball together during a 40 km/s descent [SC-BR01-025, SC-AR02-036]?
4. Reproduce the β² ≫ 1 approximate solution and test its claimed exactness
   in cylindrical symmetry [SC-AR05-027, SC-AR05-033]; pin down the special
   Emden point numerically [SC-AR02-027, SC-AR05-026].
5. Can the plane total-pressure integral (4.2) uniquely select boundary
   conditions in the spherical problem, as asserted [SC-AR02-002,
   SC-SI02-029, SC-SI03-001]? What breaks if classical Emden center
   conditions are used instead?
6. What observable distinguishes a first-kind trap from a second-kind trap
   at astronomical distance, given that velocity-based mass measurements
   cannot [SC-AR05-065, SC-AR05-050]?
7. Spinner bench test: measure M₀, M₁, η for a documented Costa-type wheel
   and check ω* = (M₀ − M₁)/η and its I-independence [SC-WO05-008,
   SC-WO05-014, SC-WO05-016 (cross-bucket `general`)]; the corpus lacks the
   weight/drive parameters
   needed to predict ω* from first principles.
8. Mass budget of the Tunguska object across documents spans
   10⁶–10⁹ t [SC-SI01-036], 1e8–1e10 tons [SC-WO04-022], 141 million tons
   to 1.3 trillion tons [SC-BR01-025, SC-BR01-028] — which estimate flows
   from which input assumptions, and can the mast-forest inversion
   [SC-BR01-028] discriminate?
9. The charge-system twin of the theory (DI01/DI02) claims short-lived
   like-charge accumulations in vacuum are explained for the first time
   [SC-DI01-022]; do the plane charge-atmosphere solutions
   [SC-DI01-020] quantitatively match any extracted laboratory measurement
   (see `general` bucket, SC-DI02-005, SC-MO02-008)?
10. Do the "hundreds of times in 10 years" scaling claims
    [SC-WO03-002, SC-WO03-029] trace to any computed energy balance in the
    corpus, or are they programmatic assertions only?
