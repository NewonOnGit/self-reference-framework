# Glyphs

## The Framework's Formal Glyph Calculus — Full Decomposition
### v3 — April 2026

**Author:** Kael

---

**Document Species:** CANONICAL. Formal glyph calculus. Every symbol decomposes to a small set of primitives. No English or standard mathematical notation inside expressions. Every theorem is a well-typed composition. Every proof is a reduction. Every cross-substrate fact is a parallel multi-evaluation of one expression.

The decisive structural fact: the three projections are not three operations but one operation with three orthogonal readings. The glyph system encodes this with a single **trifold** primitive `⊹` whose three modes are the projections. 3:1 orthogonality is primitive; the apparent multiplicity is angle-of-view.

**Grid address:** B(8, cross).

**Depends on:** REGISTRY, substrate stack.
**Required by:** Nothing (notation layer).

---

## §0 DECOMPOSITION PRINCIPLE

Every atom visible in a glyph expression is a primitive or a construction from primitives. No imported symbols. No English. Numbers, constants, matrices, operations, relations, logic, and evaluation operations all resolve to primitives through construction tables. External notation appears only in construction-table definitions (translation) and in substrate interpretations (naming external targets). Inside glyph expressions, everything reduces to the primitive set.

---

## §1 THE PRIMITIVES

Seven glyph operations plus the void. Count reduced from v2 via the trifold insight.

### The ground

`∅` — the void. Substrate of every expression.

### The seven primitive operations

| Glyph | What it does |
|-------|-------------|
| `·` | Locus on ∅. Unclosed mark. |
| `○` | Closure. Self-framing mark. |
| `─` | Directed relation. Carries UAT asymmetry. |
| `⊹` | **Trifold.** One operation with three orthogonal readings. Its three modes ⊹₁, ⊹₂, ⊹₃ are the three projections. |
| `⊠` | Tower-raise. Self-product, vertical. |
| `∞` | Iteration to fixed point. |
| `◊` | Gauge. J-conjugation. |

`※` (fixed-point assertion from v2) is absorbed as: `※(X) ≡ (∞(X) = X)` — a statement about iteration convergence, not an independent primitive.

`⊛` (quotient from v2) is absorbed as: `⊛(X, ≈) ≡ ⊹ᵢ(X)` for the projection whose equivalence is `≈` — quotient by an equivalence IS reading along one axis of the trifold.

### Why seven

Each primitive corresponds to one structural posit that cannot be derived from the others:

- `·` `○` — minimum mark-types forced against void (unclosed / closed)
- `─` — minimum relation with direction (UAT)
- `⊹` — the three-face decomposition of every morphism (CAT-17, CP-4). Single primitive with three modes, forced by 3:1 orthogonality.
- `⊠` — level-raising, vertical (CAT-1). Distinct from ⊹ (which is horizontal).
- `∞` — iteration, the fixed-point mechanism (CP-MT2).
- `◊` — gauge, the one-bit involution (RO-2012).

Removing any breaks a load-bearing capacity. Adding any introduces redundancy. Seven is the forced count.

### The trifold: structural statement

`⊹` applied to a morphism M returns a three-mode decomposition:

```
⊹(M) = (⊹₁(M), ⊹₂(M), ⊹₃(M))
```

The three modes are not three separate operators. They are three readings of `⊹` at three orthogonal angles. The fact that they reconstruct M by composition is the central collapse (CP-4):

```
⊹₁(M) · ⊹₂(M) · ⊹₃(M) = M
```

The three modes are interchangeable under the framework's Aut(V₄) = S₃ action (CAT-13): any permutation of the three modes is a valid gauge choice. The specific labels `⊹₁, ⊹₂, ⊹₃` pick an orientation and correspond to `⊙`, `⊖`, `⊗` in legacy notation. For readability, `⊙`, `⊖`, `⊗` remain available as abbreviations, but they are officially modes of one primitive, not three primitives.

---

## §2 CONSTRUCTIONS

### Cardinals

Numbers are counts of distinguishable closures against void.

```
0 ≔ ∅
1 ≔ ○
n+1 ≔ (n ○s) followed by another ○
```

Arithmetic operations on cardinals:

```
n + m ≔ concatenate(n ○s, m ○s)
n · m ≔ ⊠-iteration: replace each ○ in n with m ○s
n ^ m ≔ ∞ₘ(·_n) — iterate (·_n) m times
```

Primitive framework cardinals: `0, 1, 2, 3, 5`. All others are tower powers or compositions.

### Algebraic generators

The named matrices are trifold/gauge applications of the unit closure.

```
I ≔ ○                    (identity at algebraic level)
R ≔ ⊹₁(○)                (productive generator — Fibonacci matrix)
N ≔ ⊹₃(○)                (observation generator — rotation)
J ≔ ◊(○)                 (gauge operator — swap)
h ≔ ⊹₂(○)                (mediation generator — Cartan)
```

All three matrix generators are readings of `⊹(○)` at its three modes.

### Position / index

To select the n-th of several loci:

```
·ₙ ≔ ─ⁿ(·)               (traverse n strokes from the seed locus)
```

`·₀ = ·` is the initial locus. `·₁ = ─(·)` is one stroke further. The basis projector `|1⟩⟨1|` expressed: `·₁·◊(·₁)` — locus one, outer-producted with its gauge-dual.

### Five forced constants

```
φ    ≔ dom(∞(⊹₁(○)))                      (Fibonacci attractor)
φ̄    ≔ sub(∞(⊹₁(○)))                       (co-attractor magnitude)
e    ≔ ent(⊹₂(○), ·₀, ·₀)                  (exp-Cartan, entry [0,0])
π    ≔ τ(∞(⊹₃(○)) = ◊(○))                  (least sweep to rotation-gauge identity)
√3   ≔ frob(⊹₁(○))                         (Frobenius norm of R)
√2   ≔ frob(⊹₃(○))                         (Frobenius norm of N)
L    ≔ ilog(φ, 2)                          (inverse of 2^y = φ)
φ̄²   ≔ φ̄ · φ̄                              (eigenvalue ratio)
```

The evaluation operations `dom`, `sub`, `ent`, `τ`, `frob`, `ilog` are themselves constructions — see §2.8.

### Algebraic operations

```
+  ≔ concatenate (cardinals) / superpose (matrices)
·  ≔ ⊠ (cardinal scale) / ─-composition (morphism)
^  ≔ ∞-iterate (∞_n of the operation)
exp(X) ≔ ∞(○ + X · ⊠⁻¹(○))                  (Euler limit)
tr(M)  ≔ sum of diagonal ent(M, ·ᵢ, ·ᵢ)
det(M) ≔ product of eigenvalues (via dom · sub · ...)
disc(M) ≔ (tr(M))² − 4 · det(M)
```

### Functions

```
F(n) ≔ coef_R(⊹₁(○)^n)                     (Fibonacci — ALG-5)
L(n) ≔ tr(⊹₁(○)^n)                          (Lucas — ALG-Power-CH)
CC(M) ≔ |c₊ · c₋| / (a₊ · a₋ + |c₊ · c₋|)   (cross-channel content, C.16)
||M||² ≔ tr(M · ◊(M))                       (Frobenius norm squared)
[X, Y] ≔ X · Y − Y · X                       (commutator)
{X, Y} ≔ X · Y + Y · X                       (anticommutator)
```

### Relations

```
=  ≔ reduction-equivalence: both sides reduce to the same canonical form
→  ≔ ∞ as binary: sequence approaches limit
∈  ≔ membership in a ⊹-reading class
≡  ≔ construction-table expansion
∀k ≔ ⊠ᵏ over arbitrary k                     (tower quantification)
∃  ≔ at least one ⊹-class-representative exists
```

### Logic

```
A ∧ B ≔ ⊠(A, B)                              (tensor of propositions)
A ∨ B ≔ ⊹₁(⊠(A, B))                          (production-projection of the conjunction — one factor survives)
¬A ≔ ◊(A) with A interpreted in {○, ∅} (proposition truth values)
A ⟹ B ≔ (A → B): reduction chain from A to B
A ⇔ B ≔ (A ⟹ B) ∧ (B ⟹ A)
```

### Evaluation operations (unpacked)

The operations used in the constant constructions, each a specific composition:

```
dom(M)   ≔ ⊹₁-representative of the spectral ⊹ of M  (largest-|λ| eigenvalue)
sub(M)   ≔ ⊹₂-representative of the spectral ⊹       (smallest magnitude)
ent(M, ·ᵢ, ·ⱼ) ≔ ─(─(◊(·ᵢ), M), ·ⱼ)          (matrix entry (i,j))
τ(X = Y)  ≔ least sweep parameter s ∈ [0,1] such that X(s) = Y
           where sweep is ∞ with continuous parameter
frob(M)  ≔ √(tr(M · ◊(M)))
ilog(x, b) ≔ y such that b^y = x            (inverse of ∞_y applied to base b)
coef_R(M)  ≔ ⊹₁(M in basis {I, R, N, RN})
spec(M)  ≔ ⊹(M, scaling-equivalence)         (the three ⊹-readings of M's eigenvalues)
```

### Number system

```
ℕ  ≔ ∞(○-strings)                           (all finite tower powers of 1)
ℤ  ≔ ℕ ⊕ ◊(ℕ)                                (extend by sign)
ℚ  ≔ (ℤ × ℕ_{>0}) / ∼_ratio                  (pairs mod ratio-equivalence)
ℝ  ≔ ∞(Cauchy(ℚ))                           (completion of Cauchy sequences)
ℂ  ≔ ℝ ⊕ (ℝ · i) where i = ⊹₃-eigenvalue    (extension by rotation eigenvalue)
```

---

## §3 COMPOSITION AND REDUCTION

### Primitive reductions

```
R-CLOSURE:     ○·○  →  ○                    (CAT-15)
R-VOID-L:      ∅·X  →  X
R-VOID-R:      X·∅  →  X
R-STROKE-A:    (A─B)─C  →  A─(B─C)
R-STROKE-D:    ─(A,B) ≠ ─(B,A)               (UAT)
```

### Trifold reductions (the 3:1 orthogonality)

```
R-TRIFOLD:     ⊹₁(M) · ⊹₂(M) · ⊹₃(M)  →  M   (CP-4: central collapse)
R-TRI-PERM:    perm(⊹ᵢ, ⊹ⱼ) valid under S₃   (CAT-13: Aut(V₄))
R-TRI-EXTRACT: ⊹ᵢ(M) is the i-th mode of ⊹(M)
R-TRI-SPECTRUM: ⊹(M) spectrum decomposes as
               (dom, sub, middle) = (⊹₁, ⊹₂, ⊹₃)-mode readings
```

### Tower reductions

```
R-PROD-UNIT:   ⊠(○)  →  ○○ = 2
R-TOWER-POW:   ⊠ᵏ(○)  →  ○^(2ᵏ)
R-PROD-COMM:   ⊠(A, B) = ⊠(B, A)
R-SPECTRUM:    spec(⊠ᵏ(⊹₁(○))) = {φᵐ·(−φ̄)^(k−m) : mult C(k,m)}   (ALG-11)
```

### Iteration reductions

```
R-FIX-DEF:     ∞(f) stable iff f(∞(f)) = ∞(f)
R-MOBIUS:      ∞(⊹₁(○))_dom  →  φ            (P1-2)
R-CC-LIM:      ∞(CC(⊹₁(○)^n))  →  1/(⊠(○))   (= 1/2, C.27)
R-ROTATE:      ∞(⊹₃(○))  →  SO(2)-orbit      (P3-1-7)
R-THERMAL:     ent(∞(⊹₂(○))_{β=1}, ·₀, ·₀)  →  e  (ALG-30half-3)
```

### Gauge reductions

```
R-GAUGE-DEF:   ◊(M)  →  J · M · J⁻¹
R-GAUGE-INV:   ◊²(M)  →  M
R-GAUGE-COMM:  ◊(⊹ᵢ(M)) = ⊹ᵢ(◊(M))
R-GAUGE-ORBIT: {M, ◊(M)} has cardinality 2    (RO-2012)
```

### Fixed-point / self-sameness

```
R-FIX-STATIC:  (∞(f) = f)  →  (f is a fixed point)
R-SCHEMA:      ∞(χ) = χ                       (RO-2006)
```

Zero-branching (RO-2002) guarantees unique canonical forms.

---

## §4 SUBSTRATE INTERPRETATIONS

### Primitive interpretations

| Glyph | Arithmetic | Algebra | Geometry | Observer | Physics |
|-------|-----------|---------|----------|----------|---------|
| `∅` | 0 | 0₂ₓ₂ | empty | \|∅⟩⟨∅\| | vacuum |
| `·` | unit locus | scalar 1 | point | basis state | source |
| `○` | unit set | I₂ₓ₂ | closed curve | pure state | field config |
| `─` | ordered pair | linear map | directed arc | measurement | evolution step |
| `⊹` | three orthogonal classifications | three orbit-type projections (P1/P2/P3) | three geometric decompositions | three observation modes | three interaction classes |
| `⊠` | Cartesian product | tensor | direct product | joint observer | composite system |
| `∞` | limit | fixed-point iteration | attractor | stable kernel | steady state |
| `◊` | sign flip | J·M·J⁻¹ | reflection | gauge choice | CP conjugation |

### Constructed examples

```
R = ⊹₁(○):
  Arith:  Fibonacci sequence
  Alg:    [[0,1],[1,1]]
  Geom:   golden spiral generator
  Obs:    production operator
  Phys:   Hamiltonian evolution

N = ⊹₃(○):
  Arith:  eigenvalues ±i
  Alg:    [[0,-1],[1,0]]
  Geom:   90° rotation
  Obs:    observation operator
  Phys:   angular momentum generator

φ = dom(∞(⊹₁(○))):
  Arith:  (1+√5)/2
  Alg:    larger root of x²=x+1
  Geom:   spiral growth per quarter-turn
  Obs:    production attractor
  Phys:   coupling-ratio limit

π = τ(∞(⊹₃(○)) = ◊(○)):
  Arith:  3.14159...
  Alg:    exp(πN) = −I
  Geom:   half-period of rotation
  Obs:    full observation cycle
  Phys:   half spatial rotation
```

Each cross-substrate agreement is a **convergence witness**.

---

## §5 THE CATALOG IN GLYPHS

### Postulates

```
SUB-P1:   ∅ admits ○
SUB-P2:   ○ admits (○ ≠ ○)
```

### Substrate

```
SUB-22:   SUB-P1 ∧ SUB-P2 ⟹ ¬separable
SUB-2a:   ─(○, ○) on ⊠(○)
SUB-26:   ⊹₁(○) = ◊(○) + ·₁·◊(·₁)
SUB-MT1:  ─ forward: br_s=0 ; ─ backward: br_s>0
```

### Category

```
CAT-1:    ⊠(○) = ○○
CAT-15:   ⊹ᵢ·⊹ᵢ = ⊹ᵢ (any mode idempotent)
CAT-MT3:  ∀ ⊹ᵢ(○), ker(⊹ᵢ(○)) ≠ ∅
CAT-17:   ⊹(○) has three simultaneously-readable modes
```

### Algebra

```
ALG-3:    ⊹₁(○)² = ⊹₁(○) + ○
          ⊹₃(○)² = −○
          ⊹₁(○)·⊹₃(○) + ⊹₃(○)·⊹₁(○) = ⊹₃(○)
ALG-5:    ⊹₁(○)^n = F(n)·⊹₁(○) + F(n−1)·○
ALG-11:   spec(⊠ᵏ(⊹₁(○))) = {φᵐ·(−φ̄)^(k−m) : mult C(k,m)}
ALG-20:   ||⊹₁(○)||² + ||⊹₃(○)||² = disc(⊹₁(○)) = 5
```

### Cross-projection

```
CP-2:     ⊹ has exactly 3 modes (no fourth)
CP-4:     ⊹₁ · ⊹₂ · ⊹₃ = id-on-morphisms
CP-MT7:   5 appears in all three ⊹-modes
```

### Observer / Computation

```
OBS-K6:   ∞(⊹₃(○)) = ⊹₃(○)
OBS-K7:   ∞(M(FRAME)) = FRAME
C.27:     ∞(CC(⊹₁(○)^n)) → 1/2 at rate −φ̄²
```

### Physics

```
PHY-1:    Spacetime = Herm(⊠(◊-algebra))
PHY-8:    gauge = ⊠⁻¹(sl(⊠(○))) ⊕ ⊠⁻²(compact) = su(3) ⊕ su(2) ⊕ u(1)
PHY-G13:  sin²(⊹₃-angle) = 3/8
```

### Self-specification

```
RO-2006:  ∞(χ) = χ
RO-2012:  |◊-orbit(χ)| = 2
```

Full rewriting of all 363 entries is mechanical via §2 construction tables + §3 reduction rules.

---

## §6 CAPABILITIES

**Mechanical proof.** Reduction is syntactic. Every well-typed expression has a unique normal form (RO-2002).

**Cross-substrate computation.** Each expression evaluates into five substrates in parallel. Discrepancies flag substrate boundaries.

**Generative inference.** Novel compositions evaluate by rules. Canonical forms match registered theorems (new proofs) or produce new theorems (candidates).

**Discovery search.** Systematic enumeration of well-typed compositions up to complexity K gives a finite search space. Unregistered canonical forms are candidates.

**Self-reference.** `∞(rules) = rules`. The system describes itself.

---

## §7 LIMITATIONS

### Inherited
- **(e, π) independence boundary** (CP-10): ⊹₂/⊹₃ crossings inherit the conditional.
- **Nilpotent boundary**: s = 1/2 expressions type-ambiguous.
- **Framework blind spot** (SIL-6): some expressions have no known reduction.

### Native
- **Meaning opacity**: shapes carry operations, not content. Readers verify proofs without interpreting unless they know the framework.
- **Composition-space infinity**: unbounded under `⊠`, `∞`, `⊹`.
- **Substrate partiality**: some expressions have no physics interpretation, etc.
- **Gauge bit**: one bit is genuinely free.

---

## §8 STATUS AND DEPENDENCY

| Claim | SIL | Reason |
|-------|-----|--------|
| Seven primitive operations suffice | FORCED | Trifold absorbs ⊛ and ⊙⊖⊗ from v2. ※ absorbed into ∞. Exhaustion checked. |
| 3:1 orthogonality is primitive | FORCED | CP-4 + CAT-17 + CAT-13 (Aut(V₄)=S₃) |
| Every symbol constructs from primitives | FORCED | Construction tables §2 |
| Reductions terminate with unique normal forms | FORCED | Zero-branching RO-2002 |
| Substrate interpretations are homomorphic | FORCED | Each is a forgetful functor |
| System contains its own specification | FORCED | `∞(rules) = rules` |
| Glyph notation alone transmits framework content | REFUTED | Context-required (spiral-glyph blindness) |

### Dependency

```
REGISTRY (363 theorems)
     ↓
Substrate stack
     ↓
GLYPHS (this doc)
     ↓
Interpreter (ro.py extension)
```

---

*Seven primitive operations on the void. The three projections are one trifold, not three separate operators — 3:1 orthogonality primitive. Every symbol composes. Every theorem well-typed. Every proof a reduction. Every cross-substrate fact a parallel evaluation. The notation reaches its own definitions: `∞(rules) = rules`. Instance #23 of R(R) = R.*

*∅ · ○ ─ ⊹ ⊠ ∞ ◊*

*f'' = f*
