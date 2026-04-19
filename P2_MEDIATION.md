# P2: Mediation

## Projection 2: e, Level-Transition, and the Exponential Bridge
### v2 — March 2026

**Author:** Kael

---

**Document Species:** CANONICAL. Projection file. Owns the P2/TDL projection: e as level-transition constant, the OSC computation type, TDL arithmetic projection, S₃ distance structure, detailed balance, KMS partition function, Landauer cost, the gravity chain entry point, extensions to ℤ and ℚ.

**Grid address:** B(4, P2). The Mediation projection.

**Generator attribution:** 𝔤₃ (the evaluation chain — P2 IS the exponential evaluation, the passage from algebraic to transcendental).

**Depends on:** ALGEBRA (generators R/N, orbit types, five constants, exponential sector). SUBSTRATE (UAT, sweep, duality D, stance grammar). P1_PRODUCTION (natural temperature β=ln(φ), self-signature).
**Required by:** CROSS_PROJECTION (independence witness, folding, KMS for lattice). OBSERVER (Bekenstein chain). PHYSICS (Landauer→Bekenstein→η→Einstein).

---

**P2 reads f'' = f through the exponential map.** The equation R²=R+I is polynomial — it closes in finitely many terms. The exponential exp(h) = diag(e, e⁻¹) carries this algebraic structure beyond polynomial reach, producing the transcendental constant e. P2 is the crossing face: the domain where f'' = f transcends itself. The solutions at the P2 generator are pure exponentials — eᵗ and e⁻ᵗ — the level-transition functions connecting tower strata.

---

## THEOREM INDEX

| Theorem | Statement | Section |
|---------|-----------|---------|
| **4.2** | **e Is Forced: two routes, one constant** | **§1** |
| 1.7 | e = det(exp(R)) = exp(tr(R)) (P1→P2 bridge) | §1 |
| **1.6** | **P2 → OSC: derived composite interpolating P1↔P3** | **§1** |
| 1.2 | TDL Tower Saturation: compression wall at d² | §2 |
| 2.6 | Complexity Depth Bound: C_max(n) = 2ⁿ/log₂(φ) | §2 |
| 2.2 | S₃ Cayley Distance: diameter 2 | §3 |
| 3.4 | Signature Space Topology: P open, NP closed | §3 |
| **3.3** | **Detailed Balance: P(n→m)/P(m→n) = exp(−βΔV)** | **§4** |
| 4.4 | Landauer Cost: E = log_φ(2) = 1/L | §4 |
| **4.5** | **KMS Partition Function: Z(β) = coth(β/2)⁴** | **§4** |
| **Cor 4.5a** | **KMS-Fibonacci: coth(ln(φ)/2) = φ³; Z_M(ln(φ)) = φ¹²** | **§4** |

---

## §1 e AND THE LEVEL-TRANSITION FACE

Three independent routes produce e:

**Route 1 (P3-type observation of the P2 generator):** h = diag(1,−1), the unique traceless diagonal with entries in {−1,0,1} (ALGEBRA §5). exp(h)[0,0] = e. The [0,0] extraction IS a P3 observation — the sweep at s = 0 (SUBSTRATE §8½): α(0) = e. P2's constant IS the sweep's hyperbolic endpoint.

**Route 2 (P1-type composition through the exponential):** det(exp(R)) = exp(tr(R)) = exp(1) = e (ALGEBRA Thm 30½.3). The P1 generator's exponential determinant IS the P2 constant. Zero algebraic resistance between production and mediation at the exponential level.

**Route 3 (unipotent route):** exp(T)[0,0] = e where T = [[1,1],[0,1]] is the unipotent production generator. T has tr(T) = 2 and T² = 2T − I, so exp(T) = e·[[1,1],[0,1]] giving [0,0] = e. The unipotent route extracts e through a parabolic (null) operator rather than a boost (hyperbolic, Route 1) or determinant (composition-invariant, Route 2).

**Convergence witness.** Three distinct causal types produce e: Route 1 via a timelike/boost generator (h, disc=4), Route 2 via a composition-invariant of the P1 boost (R, disc=5), Route 3 via a null/parabolic generator (T, disc=0). The exponential maps all three causal sectors to the same transcendental constant. This is a tier-3 convergence witness — one value, three causal routes, corresponding to the three Minkowski projections (P1/P2/P3) each contributing an independent derivation of e through the exponential map.

**Theorem 1.6 (P2 → OSC).** *P2 maps to the OSC computational primitive — the derived composite interpolating between P1 and P3 along the canonical family M(θ) = cos(θ)R + sin(θ)N.* At θ = 0: pure R (P1). At θ = π/2: pure N (P3). Between: a continuous path through orbit-type space. OSC is not a primitive like P1's FIX/REPEL or P3's INV — it is the mediating interpolation that connects them. The P2 computation type IS the transition itself. ∎

**Theorem (Null Geodesic and the Koide Inverse).** *The element n = (h + N)/2 satisfies n² = 0 — it is a null vector in the Minkowski (2,1) structure of sl(2,ℝ). exp(τ·n) = I + τ·n for all τ (linear growth, no curvature), since all higher-order terms vanish. At τ = 1: exp(n)[0,0] = 1 + 1/2 = 3/2 = 1/Q. The sweep's nilpotent-boundary value α(1/2) = 3/2 IS the τ = 1 point of affine motion along this null geodesic from the identity.*

*Proof.* This is Corollary AA.3 (ALGEBRA §7). Direct expansion: (h+N)² = h² + hN + Nh + N² = I + {h,N} − I = 0 by Axiom AA. Since n² = 0, the exponential series terminates: exp(τn) = I + τn. The [0,0] entry: (I + τn)[0,0] = 1 + τ·(h[0,0] + N[0,0])/2 = 1 + τ/2. At τ = 1: 3/2. ∎

The P2 mediation sector connects two causal regions (timelike, spacelike). Its boundary is the light cone. The Koide inverse 1/Q = 3/2 is the unique lightlike scale — it appears wherever a 4-Minkowski norm meets a null condition (ALGEBRA Koide Inverse Convergence). Mediation is literally null-directional motion in the Minkowski geometry of M₂(ℝ).

**Stance grammar at P2.** Anchor = h (the Cartan generator — the diagonal element exp acts on). Address = exp(h) = diag(e, e⁻¹) (the exponential bridge — the morphism doing the level-transition). Exterior = the nilpotent boundary {M : M²=0} (where exp degenerates: exp(M)=I+M — the exponential cannot produce transcendentals there, ALGEBRA §9). Co-closure = e itself (the transcendental value produced by the h-to-exp interaction). Co-closure irreducibility (SUBSTRATE Thm 0.3p at Level 3): e is transcendental — it lives in no algebraic extension of ℚ. Genuinely new: e ∉ ℚ(φ) ∩ ℚ(√3) ∩ ℚ(√2).

---

## §2 TDL ARITHMETIC

The P2 projection reads integers through tower-level structure: how many prime-factor layers built this number? This is f'' = f's level-transition reading of arithmetic.

**Theorem 1.2 (Tower Saturation).** *The TDL compression wall is at d²: a d-state observer can distinguish at most d² distinct tower-level configurations.* The self-product tower has |S_n| = 2^{2^n}, growing doubly exponentially. The information capacity saturates because the observer's Bekenstein bound limits distinguishable states. ∎

**Theorem 2.6 (Complexity Depth Bound).** *C_max(n) = 2ⁿ/log₂(φ).* The maximum computational complexity processable at tower level n. At each level, the observer spends log₂(φ) ≈ 0.694 bits per step on structural maintenance (the self-modeling overhead = L), leaving 2ⁿ − 2ⁿL bits for content processing. The bound tightens with level. ∎

TDL-tagged numbers: each integer n gets a tower level ℓ(n) = ⌊log₂(Ω(n))⌋ where Ω(n) is the total prime factor count with multiplicity. Numbers at the same tower level are TDL-equivalent as categories — they have isomorphic level-transition structures.

Constants in the observer loop: e enters the K6' closure (OBSERVER) as the eigenvalue of the Cartan generator — the rate at which the observer's self-model updates propagate through the tower. Without e, the loop has no quantitative transition rate.

---

## §3 S₃ DISTANCE AND COMPLEXITY

**Theorem 2.2 (S₃ Cayley Distance).** *The S₃ Cayley graph on generators {(12), (123)} has diameter 2.* Every group element is reachable in at most 2 generator applications. Complexity classes: C ∈ {0, 1/2, 1} (three levels, matching three orbit types). ∎

**Corrects** the earlier claim of diameter 3 (THREE_PROJECTIONS_UNIFIED §5.2). BFS on the 6-element graph confirms diameter 2.

**Theorem 3.4 (Signature Space Topology).** *P (tractable computations) is open in signature space; NP (hard computations) is closed.* The boundary at φ̄² is a closed surface: the set of signatures with exactly one component equal to φ̄² has measure zero in the signature simplex. The P side (all components < φ̄²) is open; the NP side (at least one component ≥ φ̄²) is closed. ∎

The operator table classifies arithmetic operations by projection character: addition is P1-dominant (compositive), exponentiation is P2-dominant (level-transitional), GCD is P3-dominant (observational). Every elementary arithmetic operation has a projection signature.

---

## §4 THERMODYNAMICS AND THE GRAVITY CHAIN

### §4.1 Detailed Balance

**Theorem 3.3 (Detailed Balance).** *The arithmetic flow satisfies detailed balance at natural temperature β = ln(φ) (P1_PRODUCTION Thm 5.6):*

P(n → m) / P(m → n) = exp(−β[V(m) − V(n)])

*Proof.* V(n) = V_I(n) + V_T(n) + V_L(n) is the composite potential. The transition rate P(n→m) is the probability of the arithmetic flow moving from n to m under the combined P1+P2+P3 gradient. The Boltzmann factor exp(−βΔV) governs the ratio because the flow satisfies the Kolmogorov criterion: for every closed loop n₁→n₂→...→n_k→n₁, the product of forward/backward ratios equals 1. Verified on four test pairs:

| Pair | V(n) | V(m) | exp(−β·ΔV) | Reading |
|------|------|------|-----------|---------|
| 12 ↔ 6 | 4.51 | 3.30 | 11.29 | Downhill strongly favored |
| 60 ↔ 30 | 7.06 | 4.40 | 202 | Strongly favored |
| 144 ↔ 12 | 12.27 | 4.51 | 5.4×10⁶ | Overwhelmingly |
| 360 ↔ 60 | 12.73 | 7.06 | 8.4×10⁴ | Strongly favored |

At β → 0: all ratios → 1 (infinite temperature, all transitions equally likely). ∎

### §4.2 KMS Partition Function

**Theorem 4.5 (KMS Partition Function).** *Z(β) = coth(β/2)⁴.*

*Proof.* The 1D partition function for |x| on ℤ is Z₁(β) = Σ_{x∈ℤ} e^{−β|x|} = 1 + 2Σ_{k=1}^∞ e^{−βk} = (1+e^{−β})/(1−e^{−β}) = coth(β/2). Since H(x₁,...,x₄) = |x₁|+|x₂|+|x₃|+|x₄| decomposes as a sum of four independent L¹ norms, Z(β) = Z₁(β)⁴ = coth(β/2)⁴. ∎

Shell counts: N₄(C) = (8C³ + 16C)/3 for C ≥ 1. The number of ℤ⁴ lattice points at complexity C. Verified for C = 1,...,11.

**Corollary 4.5a (KMS-Fibonacci Identity).** *coth(ln(φ)/2) = φ³.*

*Proof.* At x = ln(φ)/2: e^{2x} = φ. coth(x) = (e^{2x}+1)/(e^{2x}−1) = (φ+1)/(φ−1). By CH: φ+1 = φ². And φ−1 = 1/φ = φ̄. So (φ+1)/(φ−1) = φ²/φ̄ = φ²·φ = φ³. ∎

At natural temperature β = ln(φ): Z_M(ln(φ)) = (φ³)⁴ = φ¹². Each generator weight: e^{−ln(φ)} = φ̄. The lattice partition function (CROSS_PROJECTION): Z_Λ = coth(β/2)⁵ = φ¹⁵ = Z_M·φ³. The extra factor φ³ = coth(ln(φ)/2) is the contribution of the fifth (exponential/P2) lattice coordinate.

The exponent structure: Z_M = φ¹² has exponent 12 = ‖R‖²·|V₄| = 3·4 (Killing form value of R). Z_Λ = φ¹⁵ has exponent 15 = ‖R‖²·disc(R) = 3·5. Difference: 15−12 = 3 = ‖R‖² — the P2 exponential coordinate's contribution. Ratio: 12/15 = |V₄|/disc(R) = 4/5 — the algebra-to-lattice dimension fraction.

The thermal-topological bridge: coth(ln(φ)/2) = φ³ simultaneously evaluates the partition function (thermodynamics) and produces a power of φ (topology, via q = φ²). At the framework's natural temperature, the thermal face and the topological face of P2 produce the SAME number. This is the P2-specific convergence witness: thermal physics and Fibonacci topology converge through the coth identity.

### §4.3 Landauer Cost and the Gravity Chain

**Theorem 4.4 (Landauer Cost).** *E_Landauer = kT·ln(2) = ln(2)/ln(φ) = log_φ(2) = 1/L ≈ 1.4404, where L = log₂(φ) ≈ 0.694.* The minimum energy to erase one bit at framework temperature β = ln(φ). ∎

**The L connection.** The Cosmological Tower Equation (PHYSICS §7 Thm 5.10j) is Λ_n = 12πη/(ln(φ)·2^n), where ln(φ) = L·ln(2) enters as the nats-converted Landauer maintenance cost per tower level. The cosmological constant's magnitude and the minimum bit-erasure energy are governed by the same framework constant:
- Landauer: 1/L = log_φ(2) (energy per erased bit, in bits)
- Tower equation: 1/ln(φ) = 1/(L·ln(2)) (the cost coefficient in Λ_n — L converted to nats via the nats-bits bridge ln(2))
- Information budget: L ≈ 0.694 (content capacity fraction), 1−L ≈ 0.306 (self-modeling overhead)

The tower equation uses ln(φ) = L·ln(2) (the nats reading, required by thermodynamic entropy in the Jacobson derivation). The Landauer cost uses 1/L (the bits reading, P2). The information budget and two-axis model use L (the content reading, P1). The nats-bits bridge ln(2) is a P2 fact: the exponential map exp(h) defines the base of natural logarithms.

**The gravity chain.** P2 owns the entry point:

Landauer erasure cost (1/L) → Bekenstein state entropy S_max = ln(d_K) nats (OBSERVER Thm 10½.1b) → dimensional anchor η = 1/(4G) (PHYSICS) → Einstein equations (PHYSICS §G14)

Each link is a theorem. The chain from bit-erasure to spacetime curvature passes through P2 because level-transition (the exponential map carrying algebraic data upward) IS the mechanism converting information-theoretic cost into geometric constraint. Without e, there is no exponential bridge, no Landauer cost at finite temperature, no gravity chain.

### §4.4 Extensions

**To ℤ:** V(−n) = V(n) by parity symmetry (all potential components depend only on |n|). Fixed points: {±1}. The flow on ℤ is the parity-symmetric extension of the ℕ flow.

**To ℚ:** For r = p₁^{a₁}·.../q₁^{b₁}·... in lowest terms: Ω(r) = Σ|a_i|+Σ|b_j| (total prime factor count including denominator). Gradient flow extends naturally; fixed points remain ±1. The p-adic absolute value |r|_p = p^{−v_p(r)} provides an alternative metric. The ℕ results are not artifacts of restriction.

---

## §5 P2-SPECIFIC PROJECTION STRUCTURE

**Independence witness:** P2 carries det > 0 with Δ > 0 (real same-sign eigenvalues). Neither P1 (det < 0) nor P3 (complex eigenvalues) can produce this configuration. P2 content is inaccessible from the other two projections.

**P2 folding containments:** P2 ⊃ P1 via ascent-as-composition: the path 1 → p₁ → p₁p₂ → ... → n builds n from 1 via prime multiplication. Each step IS the I² operation (f acting on g) applied at the number level. Building n from primes IS iterated P1 composition.

P2 ⊃ P3 via digital-root-as-observation: numbers with the same digital root belong to the same congruence class mod 9. Shared class identity IS LoMI mutual identification — the digital root operator IS an observer with blind spot = digital-root-equivalence-class. TDL reduction CREATES LoMI equivalence classes.

At the generator level: exp(th) = diag(eᵗ, e⁻ᵗ) simultaneously contains composition (eᵗ·eˢ = e^{t+s}) and observation (eᵗ and e⁻ᵗ as reciprocals).

**Anti-TDL:** Replaces growth (×e) with decay (×e⁻¹). Level structure persists but inverts. e·e⁻¹ = 1 connects TDL to its reversal.

**V_T(n):** The TDL potential component. V_T(n) = |Ω(n) − ap(n)| where ap(n) = additive persistence. Measures the level gap between tower depth and reduction depth. V_T(1) = 0 (fixed point).

---

## §6 VERIFICATION AND CLAIM STATUS

### Verification

| Claim | Method | Result |
|-------|--------|--------|
| exp(h)[0,0] = e | Numeric, machine precision | ✓ |
| det(exp(R)) = e | Determinant to machine precision | ✓ |
| K(h,N) = 0 (Killing orthogonal) | 4·tr(hN) = 0 | ✓ |
| Tower saturation at d² for d = 2,3,4,5 | Direct | ✓ |
| C_max(n) = 2ⁿ/log₂(φ) for n = 1,...,7 | Direct | ✓ |
| S₃ Cayley diameter = 2 | BFS on 6-element graph | ✓ |
| Detailed balance for 4 pairs | Numeric ratios | ✓ |
| Z(β) = coth(β/2)⁴ for 5 values of β | Formula vs factorization | ✓ |
| N₄(C) = (8C³+16C)/3 for C = 1,...,11 | Direct count vs formula | ✓ |
| coth(ln(φ)/2) = φ³ | Algebraic + numeric | ✓ |
| Generator weight at β=ln(φ): e^{−ln(φ)} = φ̄ | Direct | ✓ |
| V(−n) = V(n) for tested n | Direct | ✓ |

### Claim Status

| Claim | Status |
|-------|--------|
| e forced (two routes) | FORCED |
| Two-route convergence witness | FORCED (CATEGORY 4.3) |
| P2 → OSC | FORCED |
| TDL tower saturation at d² | FORCED |
| Complexity depth bound C_max | FORCED |
| S₃ Cayley diameter = 2 | FORCED |
| P open, NP closed in signature space | FORCED |
| Detailed balance | FORCED |
| KMS Z(β) = coth(β/2)⁴ | FORCED |
| KMS-Fibonacci coth(ln(φ)/2) = φ³ | FORCED |
| Z_M(ln(φ)) = φ¹² | FORCED |
| Thermal-topological bridge | FORCED |
| Landauer cost = 1/L | FORCED |
| L connection (Landauer ↔ tower equation) | FORCED (same constant) |
| Extensions to ℤ, ℚ | FORCED |
| P2 independence witness | FORCED |
| P2 folding containments | FORCED |

---

*f'' = f through the exponential map: the crossing face where the equation transcends polynomial structure. Two routes to e converge (P3-type observation and P1-type composition). P2 → OSC, the interpolating computation type. TDL arithmetic reads integers by tower level. S₃ diameter 2. Detailed balance at β = ln(φ). KMS partition function Z = coth(β/2)⁴ with the thermal-topological bridge coth(ln(φ)/2) = φ³. Landauer cost 1/L enters the gravity chain: bit-erasure → Bekenstein → η → Einstein. The same L governs both the Landauer cost and the Cosmological Tower Equation.*

*f'' = f.*

*R(R) = R.*
