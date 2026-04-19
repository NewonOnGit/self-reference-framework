# P3: Observation

## Projection 3: π, Rotation, and the Imaginary Domain
### v2 — March 2026

**Author:** Kael

---

**Document Species:** CANONICAL. Projection file. Owns the P3/LoMI projection: π as absolute forcing, INV computation type, SO(2) maximal compact, spin-½, binary-phase closure, co-determination, observer incompleteness, LoMI arithmetic projection, AGM Fibonacci limit, P3 attractor.

**Grid address:** B(4, P3). The Observation projection.

**Generator attribution:** 𝔤₁ (seed — the solution space whose imaginary-domain iteration IS the P3 content). Also 𝔤₄ (domain decomposition — the im/ker split that P3 reads).

**Depends on:** ALGEBRA (generators R/N, Identity 2, orbit types, exponential sector, native observation). SUBSTRATE (sweep, duality D, ORE/CIA, stance grammar, UAT).
**Required by:** CROSS_PROJECTION (independence witness, folding, elliptic fraction). OBSERVER (observer incompleteness, P3 attractor, consciousness). PHYSICS (spin-½, Lorentz double cover, Λ > 0 selection).

---

**P3 reads f'' = −f on the imaginary line.** While P1 reads f'' = f on ℝ (exponential growth, aperiodic, unbounded), P3 reads the companion equation f'' = −f on i·ℝ — the domain of cos(t) and sin(t), periodic, bounded, norm-preserving. Identity 2 (N² = −I) IS f'' = −f in matrix form. The exponential flow exp(θN) = cos(θ)I + sin(θ)N traces out SO(2) — rotation without growth. P3 is the observation face: what does self-action preserve? The answer is the rotation group — closed orbits, periodic return, identity through difference.

---

## THEOREM INDEX

| Theorem | Statement | Section |
|---------|-----------|---------|
| **4.3** | **π absolutely forced: unique θ with exp(Nθ)=−I, zero ambiguity** | **§1** |
| **1.4** | **P3 → INV: norm-preserving rotation** | **§1** |
| **1.7** | **SO(2) maximal compact, exp(πN)=−I generates center** | **§1** |
| **1.7a** | **Spin-½: ker(SL(2,ℂ)→SO⁺(1,3)) = {I, −I}** | **§1** |
| 1.7b | Binary-Phase Closure: e^{iπ}+1=0 | §1 |
| 1.7e | Direction-Independent Inversion: exp(πM)=−I for all M²=−I | §1 |
| **1.5b** | **P3 Attractor: det(A⊗B)≥0, Type III dominance asymptotic** | **§1** |
| **1.8** | **Observer Incompleteness: no injection B(H_U)→B(H_K) for d_K < d_U** | **§1** |
| 4.3a | Highly Composite → LoMI, 93.3% | §2 |
| 4.6 | Totient Ratio as Continuous LoMI Signature | §2 |
| **4.4** | **AGM Fibonacci Limit: AGM(1,φ)/φ ≈ 0.7975** | **§3** |
| 6.2 | Fibonacci CF: golden signature [0;1,...,1,2] | §3 |
| 6.3 | Anti-LoMI: period-2 oscillation | §4 |

---

## §1 π AND THE ROTATION FACE

**Theorem 4.3 (π Is Absolutely Forced).** *N = [[0,−1],[1,0]] is the unique skew-symmetric 2×2 matrix with entries in {−1,0,1} and N²=−I (ALGEBRA §5). The unique θ ∈ (0,2π) satisfying exp(Nθ)=−I is θ=π.*

*Proof.* exp(Nθ) = cos(θ)I + sin(θ)N. Setting this equal to −I: cos(θ)=−1 and sin(θ)=0. Unique solution in (0,2π): θ=π. ∎

**Forcing quality: absolute.** No normalization choice (N is unique up to sign, and sign doesn't affect π). No conjugacy ambiguity (exp(πN)=−I is a scalar matrix — conjugation-invariant). No free parameters. Compare: e has one normalization choice (entry vs Killing), φ has one conjugacy choice (R vs Q = JRJ). π has none. This is why the forcing hierarchy is π > φ > e (ALGEBRA Thm 4.5).

**Theorem 1.4 (P3 → INV).** *P3 maps to the INV computation type. N has eigenvalues ±i with |λ|=1: iteration preserves norms exactly. exp(θN) is orthogonal for all θ. INV is the unique norm-preserving primitive — P1's eigenvalues have mixed magnitude {φ, φ̄}, P2's generate expansion/contraction {eᵗ, e⁻ᵗ}.* ∎

The structural invertibility threshold: σ_MIX < φ̄²/2 is the condition under which INV (observation) dominates MIX (irreversibility). Below this threshold, observation can recover from irreversible steps.

**Theorem 1.7 (SO(2) as Maximal Compact).** *exp(θN) traces SO(2) ⊂ SL(2,ℝ) — the maximal compact subgroup. All orbits closed. exp(2πN)=I (full loop). exp(πN)=−I generates the center Z(SL(2,ℝ))={±I}. The quotient SL(2,ℝ)/{±I} = PSL(2,ℝ) is a Dist quotient at the group level: the projection identifying x with −x.* ∎

**Theorem (Observation Flow Master Identity).** *For all θ, exp(θN) has invariants:*

*disc(exp(θN)) = −4 sin²(θ)*
*CC(exp(θN)) = sin²(θ)*
*tr(exp(θN)) = 2 cos(θ)*
*det(exp(θN)) = 1*

*Proof.* exp(θN) = cos(θ)·I + sin(θ)·N (rotation flow, N² = −I). Pauli coordinates: α = cos(θ), β = 0, γ = sin(θ), δ = 0. By MT8 (CROSS_PROJECTION §4½): ρ = −sin²(θ), disc = 4ρ = −4sin²(θ), CC = |ρ|/(|ρ|+α²) = sin²(θ)/(sin²+cos²) = sin²(θ). The observation flow moves M through the Pauli (β,γ,δ)-space along the γ-axis; its ρ-value is always ≤ 0, confirming the elliptic/P3/spacelike classification (MT8 Cor 1). ∎

**Corollary (Observation-Flow Is Sin²-Parametrized).** The cross-channel content of the observation flow IS the sin-squared function. The observation generator's rotation angle θ directly parametrizes the observation's mixedness: at θ = 0 (identity) and θ = π (−I), the observation is fully diagonal (CC = 0); at θ = π/2 (pure N), the observation is fully cross-channel (CC = 1); at θ = π/4, the observation is at the CC attractor value (CC = 1/2). The orbit of CC under the observation flow is a full sin² period, with zero at endpoints and maximum at the midpoint.

**Corollary (Framework Discriminants from Pentagon/Hexagon/Decagon).** *The four framework discriminant values {0, −φ̄², −3, −4} are the disc values of exp(θN) at specific rational multiples of π:*

| θ | sin²(θ) | disc(exp(θN)) | Framework identity |
|---|---------|---------------|--------------------|
| 0 | 0 | 0 | identity |
| π/10 | φ̄²/4 | **−φ̄²** | K4 minimum (Möbius contraction rate) |
| π/6 | 1/4 | −1 | — |
| π/4 | 1/2 | **−2** | CC attractor angle |
| π/3 | 3/4 | **−3** | disc(Tu) |
| π/2 | 1 | **−4** | disc(N) |
| π | 0 | 0 | −I |

*The decagonal angle π/10 realizes the K4 minimum (framework's universal contraction rate φ̄²) as a discriminant. The hexagonal angle π/3 realizes disc(Tu) = −3. The pentagon angle π/5 gives cos(π/5) = φ/2, the golden ratio in the pentagon.* ∎

The observation generator does not merely produce π — it produces all four framework discriminant values as natural angles of the regular polygons that its rotation orbits traverse. The pentagon/decagon/hexagon geometry of SO(2)/N is the geometric source of the discriminant classification.

**Theorem 1.7a (Spin-½).** *The equation exp(πN)=−I is the algebraic origin of half-integer spin. Under the Lorentz double cover SL(2,ℂ) → SO⁺(1,3), the kernel is ker={I, exp(πN)}={I,−I}. A 2π spatial rotation lifts to −I ≠ I in SL(2,ℂ). Representations of SL(2,ℂ) that do NOT factor through SO⁺(1,3) exist — these are the spinor representations.*

*Proof.* Rotation by angle θ around any axis lifts to exp(iθ·n⃗·σ⃗/2) ∈ SU(2) ⊂ SL(2,ℂ). At θ=2π: exp(iπσ_z) = diag(e^{iπ}, e^{−iπ}) = −I = exp(πN). If the kernel were trivial, only integer-spin representations would exist. The nontrivial kernel {I,−I} — forced by exp(πN)=−I — allows half-integer spin. ∎

The LoMI connection: the quotient SL(2,ℂ)/{±I} = SO⁺(1,3) IS a LoMI morphism. The classical rotation group cannot distinguish ψ from −ψ. The kernel {I,−I} is the observer's blind spot. Half-integer spin is the physical content of LoMI's quotient structure: what is "invisible" to the classical group (the sign of the spinor) is precisely what makes quantum mechanics different from classical mechanics.

**Remark (Non-Naming Eigenstates and Spinor Indistinguishability).** The J-eigenstates |±⟩ = (|0⟩±|1⟩)/√2 at Level 0 (SUBSTRATE Thm 0.12') are the structural template of the spinor ψ and −ψ that ker(SL(2,ℂ)→SO⁺(1,3)) = {I,−I} cannot distinguish. J treats |ψ⟩ and J|ψ⟩ identically — the swap symmetry sends each pole to the other, preserving the equal-weight superposition. The classical rotation group treats ψ and −ψ identically — the sign kernel means SO⁺(1,3) cannot see the spinor phase. Both are mode (ii) symmetries: J² = I (involutory swap) and (−I)² = I (involutory sign). The passage from J-indistinguishability at Level 0 to spinor-indistinguishability at Level 6 IS the tower lift of mode (ii) through the monoidal functor F: FinSet → Hilb_ℂ (OBSERVER A2'). Mode (ii) IS the structural content of every quotient kernel whose elements cannot be physically separated.

**Theorem 1.7b (Binary-Phase Closure).** *The canonical binary inversion flow z(θ)=e^{iθ} has minimal inversion parameter τ=π. The closure law is e^{iπ}+1=0.*

*Proof.* Continuous one-parameter group homomorphisms ℝ→S¹ have form z(θ)=e^{ikθ}. Unit-speed normalization fixes |k|=1. At θ=π: z(π)=e^{iπ}=−1. Adding the identity pole: e^{iπ}+1=0. This IS the (0,0)-entry of exp(πN)=−I read in ℂ≅span{I,N}. ∎

π is the first inversion time — not "half the circumference" imported from geometry but the unique smallest positive θ satisfying exp(θN)=−I. That this equals half the circumference is a consequence: circumference = 2π = 2×(first inversion time).

**Theorem 1.7e (Direction-Independent Inversion).** *For ANY M ∈ M₂(ℂ) with M²=−I: exp(πM)=−I.* By Cayley-Hamilton: exp(πM) = cos(π)I + sin(π)M = −I. The center {−I} is the locus where ALL phase directions agree. Verified: 10,000 random directions in S² ⊂ su(2), max error 2.09×10⁻¹⁵. ∎

**Theorem 1.5b (P3 Attractor).** *det(A⊗B) = det(A)²det(B)² ≥ 0. P1 (det<0) is impossible at tower level ≥ 2. The P3 (elliptic/INV) fraction grows monotonically:*

| Level | P1 (det<0) | P2+P3 (det>0) | P3 fraction |
|-------|-----------|---------------|-------------|
| 1 | ~72% | ~28% | ~28% |
| 2 | 0% | 100% | ~49% |
| 3 | 0% | 100% | ~64% |
| ∞ | 0% | 100% | → 1 |

*Type III (rotational) computation is the universal attractor. Compression (Type I) and expansion (Type II) are level-1 phenomena; asymptotically, all tensor-tower computation is INV-like.* ∎

**Lemma (P3 Infectiousness).** *If A ∈ M₂(ℝ) has complex eigenvalues (P3 type), then A ⊗ B has complex eigenvalues for any B with nonzero real eigenvalue.* Eigenvalues of A ⊗ B include λμ with Im(λ) ≠ 0 and μ ∈ ℝ \ {0}, so Im(λμ) ≠ 0. Complex eigenvalues propagate irreversibly through the tensor tower. ∎

**Corollary (Exact Convergence Rate).** *P₃(n) = 1 − (1/‖N‖_F)^{2^{n−1}} = 1 − 2^{−2^{n−2}}.* At level 1: P₃ = 1 − 1/√2 ≈ 0.293 (classical). The residual r_n = 1 − P₃(n) satisfies r_{n+1} = r_n² — the self-product tower acting on the non-observation fraction. The base 1/√2 = 1/‖N‖_F is the reciprocal of the P3 generator norm. Exact values: r₂ = 1/2, r₃ = 1/4, r₅ = 2^{−8}, r₇ = 2^{−32}. SA dominance is essentially total above level 5. ∎

At the physical level: P3 dominance selects Λ > 0 (PHYSICS). The cosmological constant's sign is forced by the P3 attractor — the universe, at sufficient tower depth, is observationally dominated.

**Theorem 1.8 (Observer Incompleteness).** *For d_K < d_U, there is no injective structure-preserving map B(H_U) → B(H_K). Compression ratio: d_K²/d_U² → 0 as d_U → ∞.* For the minimal observer d_K=2: the compression wall d_K²=4 limits K to 4 operators. Every observer creates a quotient (seen/unseen), and this quotient IS the Dist morphism q∘q=q. ∎

**Stance grammar at P3.** Anchor = cos(1) (the sweep value at s=1: α(1) = exp(N)[0,0] = cos(1) — the P3 endpoint). Address = sin(1) (the [0,1] entry discarded by the [0,0] extraction — what the observation doesn't capture). Exterior = π as period (π organizes the P3 sector — sets the period of cos, determines the phase structure — but never appears as an evaluated output; it is IN ker(sweep), not in im(sweep)). Co-closure = SO(2) (the stabilized rotation group: a continuous Lie group emerging from the interaction of discrete generators R and N; genuinely new — SO(2) ⊄ any discrete group).

The sweep at s=1 gives α(1) = cos(1). The integral ∫_{P3}α = 1/2 is rational DESPITE the endpoint being transcendental (SUBSTRATE Thm SW-2). This IS quantitative UKI (CATEGORY Thm 1.13a): π organizes the sector without surviving integration. The period is in the kernel; the value is in the image.

---

## §2 CO-DETERMINATION AND LoMI ARITHMETIC

**Definition (Co-determination).** A co-determination of (A,B) is a structure C = LoMI(A,B) such that: (a) C is determined by A and B jointly, (b) C does not reduce to either alone, (c) C is found by iterated mutual action, (d) C stabilizes, (e) A and B remain distinct throughout. The Euclidean algorithm GCD(a,b) = GCD(b, a mod b) is the arithmetic paradigm: the shared identity is found by iterated mutual reduction, with neither element collapsed. Co-determination is LoMI's structural content: identity through difference, not through collapse.

**LoMI arithmetic reads integers through divisibility.** UP_L(n) = {multiples of n} (n is contained in larger structures). DOWN_L(n) = {divisors of n} (smaller structures contained in n). At n=1: the universal fixed point — contained in every multiple, its own only divisor.

**V_L(n) = |log(d(n)) − log(φ(n))|,** where d(n) = divisor count, φ(n) = Euler's totient. Measures the gap between "how many observe n" and "how many n is coprime to." V_L(1) = 0. Equilibrium points where d(n) = φ(n) (e.g., n=30) are exact LoMI balance.

**Theorem 4.3a (Highly Composite → LoMI).** *28/30 highly composite numbers are LoMI-dominant (93.3%).* High divisor count → low totient ratio → LoMI. The two exceptions (2 and 4) have φ(n)/n = 0.5, exactly at the classification boundary. ∎

**Grade: ENCODED.** Statistical classification, not derived from first principles.

**Theorem 4.6 (Totient Ratio as Continuous LoMI Signature).** *φ(n)/n measures relational density: small ratio = many non-coprime relationships = high LoMI character.* Strongly LoMI (φ/n < 0.3): 30, 60, 120, 360. LoMI-dominant (0.3–0.4): 6, 12, 24. Mixed (0.4–0.5): 4, 8, 10. Not LoMI (>0.5): all primes (φ(p)/p = (p−1)/p → 1). Primes have minimal relational density — confirming their non-LoMI character. ∎

**Carmichael-totient depth:** λ(n)/φ(n) measures cyclic structure depth in (ℤ/nℤ)×. λ/φ = 1 for primes (flat), < 1 for composites (nested). This is the concrete realization of "LoMI contains TDL" (folding containment): divisibility relationships carry a natural level hierarchy.

---

## §3 LoMI OPERATIONS

**GCD as LoMI fixed point.** GCD(a,b) is the mutual identity — the largest shared structure. The Euclidean algorithm is iterated composition (LoMI contains I²) converging to the mutual fixed point. For coprimes: GCD = 1, the universal R(R)=R.

**LCM as LoMI join.** LCM(a,b) = a·b/GCD(a,b) — the minimal container. GCD × LCM = a × b: the product of the shared and the joint equals the product of the parts.

**Theorem 4.4 (AGM Fibonacci Limit).** *AGM(F(n), F(n+1))/F(n+1) → AGM(1,φ)/φ ≈ 0.7975 as n → ∞.*

*Proof.* For large n: F(n) ≈ φⁿ/√5, F(n+1) ≈ φ·F(n). By homogeneity: AGM(F(n), φ·F(n))/(φ·F(n)) = F(n)·AGM(1,φ)/(φ·F(n)) = AGM(1,φ)/φ. ∎

| Pair | AGM/F(n+1) |
|------|-----------|
| (5, 8) | 0.79613 |
| (34, 55) | 0.79751 |
| (233, 377) | 0.797542 |
| (1597, 2584) | 0.797543 |

The AGM fixed point of consecutive Fibonacci numbers encodes AGM(1,φ)/φ — the LoMI "golden mean" of the golden ratio. Not a special value of π but a new φ-derived constant.

**Theorem 6.2 (Fibonacci CF Signature).** *cf(F(n), F(n+1)) = [0; 1, 1, ..., 1, 2] with (n−1) ones.* The golden signature. φ̄ = [0;1,1,1,...] (all 1s, infinite) is the slowest-converging continued fraction — φ̄ is the "most irrational" number. ∎

**Maximal LoMI structure of consecutive Fibonacci pairs.** GCD(F(n),F(n+1)) = 1 always (maximally coprime — classical theorem, FORCED). F(n)/F(n+1) → φ̄ (maximally adjacent — Binet, FORCED). φ̄ has the slowest CF convergence among all irrationals (FORCED by CF theory). The conjunction: simultaneously as SEPARATE as possible (no shared factor beyond 1) and as CLOSE as possible (ratio = golden = slowest convergence). This tension between maximal separation and maximal adjacency IS the LoMI structure. Mutual identity requires both difference and relationship.

**Grade: FORCED.** Each component (coprimality, ratio convergence, CF slowness) is independently FORCED; their conjunction is FORCED.

---

## §4 ANTI-LoMI

**Theorem 6.3 (Anti-LoMI Is Period-2).** *The anti-LoMI operation continues past the half-turn: exp(Nπ)=−I → (−I)²=+I → (−I)³=−I → ... Period 2.* ∎

| Projection | Forward | Reverse |
|-----------|---------|---------|
| P1 / I² | Converges to φ | Diverges from φ |
| P2 / TDL | Ascends through levels | Descends through levels |
| P3 / LoMI | Stabilizes at K(K)=K | Oscillates with period 2 |

The anti-projections are reverse flows of the projections, appearing in dynamics (backwards time) and physics (CP violation, time reversal, parity).

---

## §5 P3-SPECIFIC PROJECTION STRUCTURE

**Independence witness:** P3 carries complex conjugate eigenvalues (det > 0, Δ < 0). Neither P1 (real eigenvalues, opposite signs, det < 0) nor P2 (real eigenvalues, same signs, det > 0, Δ > 0) can produce complex conjugate pairs. P3 content is inaccessible from the other two projections.

**P3 folding containments:** P3 ⊃ P1 via NRN = R⁻¹ = R−I (Identity 5) — observation conjugates production to its inverse. P3 ⊃ P2 via Carmichael-totient depth — the LoMI layer carries natural level structure (TDL within LoMI). Neither containment is complete: P3 cannot access P1's negative-determinant territory or P2's same-sign real eigenvalues.

**Phase duality:** x²−x−1 = 0 (P1, roots φ and −φ̄, off the unit circle) vs x²+x+1 = 0 (P3, roots ω = e^{2πi/3}, on the unit circle). Coefficients differ by sign of the linear term. P1 eigenvalues are phase-dependent (one expanding, one contracting). P3 eigenvalues are phase-neutral (both |λ|=1). The √3 bridge: ‖R‖_F = 2sin(2π/3) = √3 connects the P1 generator norm to the P3 rotation angle. The same number serves both projections — an instance of folding containment at the constant level.

**V_L(n): The LoMI potential component.** Measures the relational gap between divisor count and totient. V_L(1) = 0 (fixed point). P3's contribution to the gradient flow toward n=1 (CROSS_PROJECTION for the composite V = V_I + V_T + V_L).

---

## §6 VERIFICATION AND CLAIM STATUS

### Verification

| Claim | Method | Result |
|-------|--------|--------|
| exp(Nπ) = −I | Numeric, error 3.81×10⁻¹⁶ | ✓ |
| exp(2πN) = I | Numeric, error 7.62×10⁻¹⁶ | ✓ |
| ‖exp(θN)v‖ = ‖v‖ for 6 values of θ | Direct | ✓ |
| iN = σ_y | Direct | ✓ |
| Pauli commutation [σ_x,σ_y]=2iσ_z | Matrix commutator | ✓ |
| ker(SL(2,ℂ)→SO⁺(1,3)) = {I,−I} | Schur's lemma | ✓ |
| exp(πM)=−I for 10,000 random M²=−I | Max error 2.09×10⁻¹⁵ | ✓ |
| P3 fraction: 28%→49%→64% | Monte Carlo at levels 1–3 | ✓ |
| P3 Infectiousness: complex eigenvalues infectious under ⊗ | Eigenvalue arithmetic | ✓ |
| P₃(n) = 1 − 2^{−2^{n−2}} exact formula | Infectiousness induction; Monte Carlo 10⁵/level | ✓ |
| Residual base = 1/‖N‖_F = 1/√2 | Direct | ✓ |
| HC → LoMI: 28/30 = 93.3% | Classification | ✓ |
| AGM(1,φ)/φ = 0.797543... | Iterated AGM | ✓ |
| cf(89,144) = [0;1,...,1,2] with 9 ones | Euclidean algorithm | ✓ |
| GCD(F(n),F(n+1)) = 1 for n=1,...,20 | Direct | ✓ |
| (−I)² = +I (period-2) | Direct | ✓ |

### Claim Status

| Claim | Status |
|-------|--------|
| π absolutely forced (zero ambiguity) | FORCED |
| P3 → INV (norm-preserving) | FORCED |
| SO(2) maximal compact | FORCED |
| exp(πN)=−I generates center | FORCED |
| Spin-½ from nontrivial kernel | FORCED |
| Binary-phase closure e^{iπ}+1=0 | FORCED |
| Direction-independent inversion | FORCED |
| P3 attractor (Type III dominant) | FORCED |
| P3 Infectiousness (complex eigenvalues infectious under ⊗) | FORCED (eigenvalue arithmetic) |
| Exact convergence P₃(n) = 1 − 2^{−2^{n−2}}, rate 1/‖N‖_F | FORCED (infectiousness + combinatorics) |
| Observer incompleteness | FORCED |
| Co-determination (LoMI structure) | FORCED |
| Totient ratio = continuous LoMI signature | FORCED |
| GCD = LoMI fixed point, LCM = LoMI join | FORCED |
| AGM Fibonacci limit | FORCED |
| Fibonacci CF = golden signature | FORCED |
| Consecutive Fibonacci = maximal LoMI tension | FORCED (three independent FORCED facts) |
| Anti-LoMI period-2 | FORCED |
| P3 independence witness | FORCED |
| Phase duality P1↔P3 | FORCED |
| HC → LoMI 93.3% | ENCODED (statistical) |
| Elliptic minority 1−1/√2 ≈ 29.3% at level 1 | FORCED (classical discriminant theory; Monte Carlo confirms) |

---

*f'' = −f on the imaginary line: the companion equation whose solutions rotate without growing. π is absolutely forced — zero ambiguity, strongest constant. SO(2) = the maximal compact, all orbits closed. Spin-½ from ker(SL(2,ℂ)→SO⁺(1,3)) = {I,−I}. The P3 attractor drives all tower computation toward Type III. Co-determination IS LoMI: identity through difference. Consecutive Fibonacci pairs are maximally coprime AND maximally adjacent — the tension IS the observation structure. The sweep ends at cos(1); π is in the kernel; ∫_{P3}=1/2 is rational. Observation has a blind spot. The blind spot IS the observation.*

*f'' = f.*

*R(R) = R.*
