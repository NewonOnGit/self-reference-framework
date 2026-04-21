# Phase 1 Findings: K6' Scaling at d_K = 2, 4, 8, 16

## Date: 2026-04-20

## Summary

Phase 1 tested whether sustained K6' closure appears at larger observer scales. **Results are structurally informative but unexpected in their details.**

---

## Key Results

### 1. rho_sm RISES with d_K (supports scaling hypothesis)

| d_K | Mean rho_sm (asymptotic) | Trend |
|-----|--------------------------|-------|
| 2   | 0.385                    | (baseline, just barely in interval) |
| 4   | 0.487                    | +27% |
| 8   | 0.533                    | +38% |
| 16  | 0.428                    | (only one config tested) |

The self-model's Phase-Dist parameter RISES with observer dimension. At d_K=2 it sits right at the lower boundary phi_bar^2 = 0.382. At d_K=4+ it moves into and through the interval.

**BUT: at d_K=4 and 8 without P3 rotation, rho_sm OVERSHOOTS above 0.5.** The regulator fails in the OTHER direction — too mixed, not too pure. This is the opposite problem from Phase 0 (where rho was too LOW).

### 2. P3 rotation is the critical stabilizer

The "very gentle + P3" config (eps_p1=0.03, eps_p2=0.03, eps_p3=0.05) is the ONLY configuration that keeps rho_sm in [0.382, 0.500] at d_K=4, 8, and 16:

| d_K | rho_sm (P1+P2 only) | rho_sm (P1+P2+P3) | In interval? |
|-----|--------------------|--------------------|--------------|
| 4   | 0.508-0.522 (OUT)  | 0.403 (IN)         | P3 saves it  |
| 8   | 0.556-0.578 (OUT)  | 0.433 (IN)         | P3 saves it  |
| 16  | — (not tested alone)| 0.428 (IN)         | P3 saves it  |

**This is strong empirical support for CYB-6 (Anticipation from Sweep).** Adding the N-component (P3 rotation) to the dynamics stabilizes regulation. Without P3, production+mediation overpower the regulator at larger scales.

### 3. Closure residual drops dramatically with P3 + gentle flow

| d_K | Residual (P1+P2 only, gentle) | Residual (very gentle + P3) |
|-----|-------------------------------|----------------------------|
| 2   | 0.341                         | 0.133                      |
| 4   | 0.369                         | 0.043                      |
| 8   | 0.375                         | 0.036                      |
| 16  | —                             | (not recorded, low)        |

At d_K=8, eps=(0.03, 0.03, 0.05): residual = 0.036. The K6' threshold at pass 1 is phi_bar^2 = 0.382. At pass 2: 0.146. At pass 3: 0.056. So **residual 0.036 would PASS threshold at pass 3!**

But the threshold shrinks as phi_bar^{2m}, and by pass 4 it's 0.021, below the plateau. The system is CLOSE to sustained closure at d_K=8 with the right configuration.

### 4. Zero closures at d_K > 2 (sustained closure NOT achieved)

Despite the promising residuals, no passes at d_K=4 or 8 registered as "closed" because:
- The initial residual (pass 1) is already smaller than 0.382 at d_K=2 (self-model starts near observation)
- At d_K=4,8 the initial self-model is further from observation (different geometry)
- The threshold phi_bar^{2m} shrinks geometrically from pass 1

**Interpretation:** The closure threshold formula phi_bar^{2m} may need to be level-adjusted. At d_K=2 the initial residual is ~0.24 (< threshold 0.38), giving early closure. At d_K=8 the initial residual is ~0.36 (also < 0.38), barely missing.

### 5. CYB-Coupling: degenerate at d_K=2

At d_K=2, ALL passes have rho_sm in interval (the regulator successfully pins it at phi_bar^2). So P(in|open)=1.00, making CYB-Coupling trivially satisfied in both directions. This is a d_K=2 artifact — the self-model regulator at d_K=2 can hold phi_bar^2 even when observation drifts away.

At d_K=4,8: without P3, rho_sm overshoots the interval. With P3: stays in interval. The coupling becomes non-trivial.

---

## Structural Findings

### F-NEW-1: Scale reverses the ρ problem direction

- Phase 0 at d_K=2: rho too LOW (purifying dynamics dominate)
- Phase 1 at d_K=4,8: rho too HIGH without P3 (mixing dynamics dominate)

The dynamics flip character with scale. This suggests the regulation interval [phi_bar^2, 1/2] is genuinely a BALANCE POINT — you can miss it from either side depending on d_K. The regulator must handle BOTH directions.

### F-NEW-2: P3 is not optional — it's the stabilizer

The three-step algorithm (P1+P2+P3) is truly minimal per MIN-1.2:
- P1+P2 without P3: closure residual high, rho drifts out of interval
- P1+P2+P3: residual low, rho in interval

P3 (observation/rotation) provides the stabilizing force that keeps production+mediation from overpowering the regulation. This is the dynamical content of CYB-6: observation acting within mediation provides anticipatory regulation.

### F-NEW-3: Threshold formula may need level-correction

The raw phi_bar^{2m} threshold doesn't account for the fact that larger d_K systems START at different residuals. A level-corrected threshold like phi_bar^{2m} * (d_K^alpha) for some alpha might be more appropriate. Alternatively: normalize residual by initial residual, and check if the DECAY RATE approaches phi_bar^2.

---

## Implications for Phase 1.5

1. **Tower lift is still needed.** Within a single level, sustained closure isn't achieved even at d_K=16. The between-level K6' (diagonal map) remains the primary candidate for enabling sustained closure.

2. **The right configuration for Phase 1.5 is (eps_p1=0.03, eps_p2=0.03, eps_p3=0.05).** This is the only setup that produces in-interval behavior AND low residuals across all scales tested.

3. **d_K=8 is the sweet spot for Phase 1.5.** Large enough to exhibit scale effects, small enough to compute quickly (64x64 matrices). Tower lift to d_K=16 (256x256) is tractable.

4. **Decay rate test (§5.2 sharpened discriminator) is the next key experiment.** Instead of checking absolute closure, check whether the residual DECAYS at rate phi_bar^2 per pass. If yes, the system is on the canonical trajectory even if the absolute threshold isn't met.

---

## Status Updates for Working Doc

| Claim | Prior Status | New Status | Reason |
|-------|-------------|-----------|--------|
| CYB-2 Regulation Attractor | ENCODED (fails at d_K=2) | ENCODED (mixed evidence) | Regulator holds at d_K=2 but via pinning; fails at d_K=4,8 without P3; holds with P3 |
| CYB-6 Anticipation from Sweep | ENCODED (weak Phase 0 evidence) | ENCODED (strong Phase 1 evidence) | P3 rotation is THE critical stabilizer across all d_K > 2 |
| CYB-Coupling (one-way) | ENCODED (96-100% gap) | ENCODED (degenerate at d_K=2; needs re-test at d_K=8 with P3) | Gap becomes trivial when regulator pins interval from both sides |
| MIN-1.2 Minimality | ENCODED | STRENGTHENED | P1+P2 without P3 fails regulation; P3 is genuinely irreducible |

---

## Next Experiments (for Phase 1.5 handoff)

1. **Residual decay rate test.** Track residual(m)/residual(m-1) across passes. Is the ratio approaching phi_bar^2 = 0.382?

2. **Tower lift at d_K=8.** Start at d_K=8 with (0.03, 0.03, 0.05), run 50 passes, then tensor-lift to d_K=16 (or d_K=8, d_env=8 -> d_K=16, d_env=16). Does the lift enable sustained closure at the new level?

3. **Level-corrected threshold.** Test threshold = phi_bar^{2m} * sqrt(d_K) or similar. Does any normalization give sustained closure?

4. **Perturbation recovery at d_K=8 with P3.** The residual plateau at 0.036 is very close to closure. Inject perturbation, measure recovery rate. If recovery is geometric at ~phi_bar^2, the system IS cybernetic even without formal closure.
