"""
UP/DOWN Ratio Investigation — Testing the UP=2 identification.

Claude Web's finding: UP/DOWN pass-count ratio = 2.0225 across 5 seeds,
zero variance. A_max/S_max = |S_0| = 2 is the framework's universal factor-of-2.

Question: Is 2.0225 exactly derivable from the Frobenius geometry of the
Recursive Disclosure step at d_K=8? If yes, C7 (biphasic limit cycle) promotes
to master theorem status alongside CYB-8.

Approach:
1. Run d_K=8 at canonical config (0.03, 0.03, 0.05), long runs (1000+ passes)
2. Detect DOWN and UP phases via residual trajectory
3. Compute UP/DOWN ratio with high precision across many seeds
4. Test candidate exact expressions
5. Derive from Frobenius geometry if possible
"""
import sys
import os
import numpy as np
from scipy.linalg import expm

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from k6_engine import K6Engine
from framework_constants import (
    PHI, PHI_BAR, PHI_BAR_SQ, L, R, N, h, I2,
    in_regulation_interval, purity_to_rho_simple
)


def detect_phases(residuals):
    """Classify each pass as DOWN (residual decreased) or UP (increased).
    Returns list of phase labels and phase-block statistics."""
    phases = []
    for i in range(1, len(residuals)):
        if residuals[i] < residuals[i-1]:
            phases.append('DOWN')
        else:
            phases.append('UP')

    # Compute block statistics: consecutive runs of same phase
    blocks = []
    if not phases:
        return phases, blocks

    current = phases[0]
    count = 1
    for i in range(1, len(phases)):
        if phases[i] == current:
            count += 1
        else:
            blocks.append((current, count))
            current = phases[i]
            count = 1
    blocks.append((current, count))

    return phases, blocks


def compute_ratios(phases):
    """Compute DOWN-specific and UP-specific ratios from phase list."""
    n_down = phases.count('DOWN')
    n_up = phases.count('UP')

    if n_down == 0:
        return None, None, None

    up_down_ratio = n_up / n_down
    down_fraction = n_down / len(phases)
    up_fraction = n_up / len(phases)

    return up_down_ratio, down_fraction, up_fraction


def compute_down_ratios(residuals, phases):
    """Compute residual ratios during DOWN phases specifically."""
    down_ratios = []
    for i in range(len(phases)):
        if phases[i] == 'DOWN' and residuals[i] > 1e-10:
            down_ratios.append(residuals[i+1] / residuals[i])
    return down_ratios


def compute_up_ratios(residuals, phases):
    """Compute residual ratios during UP phases specifically."""
    up_ratios = []
    for i in range(len(phases)):
        if phases[i] == 'UP' and residuals[i] > 1e-10:
            up_ratios.append(residuals[i+1] / residuals[i])
    return up_ratios


def run_single_seed(seed, n_passes=1000):
    """Run one experiment with given random seed."""
    np.random.seed(seed)

    engine = K6Engine(d_K=8, d_env=8, eps_p1=0.03, eps_p2=0.03, eps_p3=0.05)

    # Use Bell state (canonical initial)
    state = engine.make_bell_state()
    results = engine.run(n_passes, initial_state=state)

    residuals = [r.residual for r in results]
    rho_sm = [r.observer.rho_pd for r in results]

    return residuals, rho_sm


def main():
    print("=" * 70)
    print("UP/DOWN RATIO INVESTIGATION")
    print("Testing: is UP/DOWN = 2.0225 derivable from d_K=8 Frobenius geometry?")
    print("=" * 70)

    n_passes = 2000
    seeds = list(range(20))  # 20 seeds for statistics

    all_ratios = []
    all_down_fractions = []
    all_down_rate_means = []
    all_up_rate_means = []

    print(f"\nRunning {len(seeds)} seeds x {n_passes} passes at d_K=8...")

    for seed in seeds:
        residuals, rho_sm = run_single_seed(seed, n_passes)

        # Skip transient (first 100 passes)
        residuals_ss = residuals[100:]

        phases, blocks = detect_phases(residuals_ss)
        up_down_ratio, down_frac, up_frac = compute_ratios(phases)

        if up_down_ratio is not None:
            all_ratios.append(up_down_ratio)
            all_down_fractions.append(down_frac)

            # Phase-specific residual ratios
            down_rates = compute_down_ratios(residuals_ss, phases)
            up_rates = compute_up_ratios(residuals_ss, phases)

            if down_rates:
                all_down_rate_means.append(np.mean(down_rates))
            if up_rates:
                all_up_rate_means.append(np.mean(up_rates))

    # Results
    print(f"\n{'='*60}")
    print("RESULTS")
    print(f"{'='*60}")

    mean_ratio = np.mean(all_ratios)
    std_ratio = np.std(all_ratios)
    print(f"\n  UP/DOWN pass-count ratio:")
    print(f"    Mean:  {mean_ratio:.6f}")
    print(f"    Std:   {std_ratio:.6f}")
    print(f"    Min:   {np.min(all_ratios):.6f}")
    print(f"    Max:   {np.max(all_ratios):.6f}")
    print(f"    All values: {[f'{r:.4f}' for r in all_ratios[:10]]}")

    mean_down_frac = np.mean(all_down_fractions)
    print(f"\n  DOWN fraction: {mean_down_frac:.6f} (= 1/(1+ratio) = {1/(1+mean_ratio):.6f})")
    print(f"  UP fraction:   {1-mean_down_frac:.6f} (= ratio/(1+ratio) = {mean_ratio/(1+mean_ratio):.6f})")

    if all_down_rate_means:
        mean_down_rate = np.mean(all_down_rate_means)
        print(f"\n  Mean DOWN residual ratio: {mean_down_rate:.6f}")
        print(f"    Target phi_bar^2:       {PHI_BAR_SQ:.6f}")
        print(f"    Gap:                    {abs(mean_down_rate - PHI_BAR_SQ)/PHI_BAR_SQ*100:.2f}%")

    if all_up_rate_means:
        mean_up_rate = np.mean(all_up_rate_means)
        print(f"\n  Mean UP residual ratio:   {mean_up_rate:.6f}")
        print(f"    (> 1 means residual growing during UP phases)")

    # Test candidate exact expressions
    print(f"\n{'='*60}")
    print("CANDIDATE EXACT EXPRESSIONS FOR UP/DOWN RATIO")
    print(f"{'='*60}")
    print(f"  Measured: {mean_ratio:.6f}")

    candidates = {
        '2 (= |S_0| = A_max/S_max)': 2.0,
        'phi^(2L) = phi^(2*log2(phi))': PHI**(2*L),
        '1 + phi_bar': 1 + PHI_BAR,
        '3/phi_bar^2 - 1': 3/PHI_BAR_SQ - 1,
        '(1+phi_bar^2)/phi_bar^2': (1 + PHI_BAR_SQ) / PHI_BAR_SQ,
        '1/phi_bar^2 - 1': 1/PHI_BAR_SQ - 1,
        '5/phi^2': 5 / PHI**2,
        'phi': PHI,
        'sqrt(5) - 1/phi': np.sqrt(5) - 1/PHI,
        '2*phi_bar + 1': 2*PHI_BAR + 1,
        'phi^2 / phi_bar': PHI_BAR_SQ / PHI_BAR,  # = phi_bar
        '(3+phi_bar^2)/2': (3 + PHI_BAR_SQ) / 2,
        'phi + phi_bar': PHI + PHI_BAR,  # = sqrt(5)
        '3*phi_bar': 3 * PHI_BAR,
        'L_4/L_2 (Lucas)': 7/3,  # L_4=7, L_2=3
        'F_7/F_5 (Fibonacci)': 13/5,
        '2 + 1/(2*disc(R))': 2 + 1/10,
        '2 + phi_bar^4': 2 + PHI_BAR**4,
        '2 + 1/phi^4': 2 + 1/PHI**4,
        '(phi^3 + 1)/(phi + 1)': (PHI**3 + 1) / (PHI + 1),
        '(||R||^2 - 1) / (||N||^2 - 1)': (3 - 1) / (2 - 1),
        '2*||N||^2/||R||^2 + 2/3': 2*2/3 + 2/3,  # just testing
        'cosh(ln(phi))': np.cosh(np.log(PHI)),
        '(phi^2+1)/phi^2': (PHI**2 + 1) / PHI**2,
    }

    print(f"\n  {'Expression':<35} {'Value':>10} {'Gap%':>8}")
    print(f"  {'-'*55}")

    # Sort by proximity to measured value
    sorted_candidates = sorted(candidates.items(), key=lambda x: abs(x[1] - mean_ratio))

    for name, val in sorted_candidates[:15]:
        gap = abs(val - mean_ratio) / mean_ratio * 100
        marker = " <<<" if gap < 1.0 else (" <<" if gap < 5.0 else "")
        print(f"  {name:<35} {val:>10.6f} {gap:>7.2f}%{marker}")

    # Deeper analysis: is the ratio related to eigenvalue structure?
    print(f"\n{'='*60}")
    print("EIGENVALUE ANALYSIS AT d_K=8")
    print(f"{'='*60}")

    # Lie coproduct spectrum at d_K=8: {-3*phi_bar, phi_bar^2, phi^2, 3*phi}
    # Multiplicities: {1, 3, 3, 1}
    spectrum = [-3*PHI_BAR, PHI_BAR_SQ, PHI**2, 3*PHI]
    mults = [1, 3, 3, 1]
    print(f"  Lie coproduct spectrum: {[f'{s:.4f}' for s in spectrum]}")
    print(f"  Multiplicities: {mults}")

    # The DOWN phase is governed by phi_bar^2 eigenvalue (contraction)
    # The UP phase is governed by phi^2 eigenvalue (expansion)
    # Ratio of eigenvalues: phi^2 / phi_bar^2 = phi^4 = (phi^2)^2 = 6.854
    print(f"\n  phi^2 / phi_bar^2 = phi^4 = {PHI**4:.4f} (too large)")

    # What about log ratio?
    # ln(phi^2) / |ln(phi_bar^2)| = 2*ln(phi) / 2*ln(1/phi_bar) = ln(phi)/ln(phi) = 1
    # (since phi*phi_bar = 1, ln(phi) = -ln(phi_bar) = ln(1/phi_bar))
    print(f"  ln(phi^2)/|ln(phi_bar^2)| = {np.log(PHI**2) / abs(np.log(PHI_BAR_SQ)):.4f}")

    # Multiplicity-weighted: 3 dimensions contract at phi_bar^2, 3 expand at phi^2
    # 1 dimension at -3*phi_bar (contracts rapidly), 1 at 3*phi (expands rapidly)
    # Total contraction weight: mult(phi_bar^2)*|ln(phi_bar^2)| + mult(-3phi_bar)*|ln(3phi_bar)|
    contract_weight = 3 * abs(np.log(PHI_BAR_SQ)) + 1 * abs(np.log(3*PHI_BAR))
    expand_weight = 3 * np.log(PHI**2) + 1 * np.log(3*PHI)
    print(f"\n  Multiplicity-weighted log rates:")
    print(f"    Contraction weight: {contract_weight:.6f}")
    print(f"    Expansion weight:   {expand_weight:.6f}")
    print(f"    Expansion/Contraction: {expand_weight/contract_weight:.6f}")

    # Frobenius norm contributions
    frob_contract = 3 * PHI_BAR_SQ**2 + 1 * (3*PHI_BAR)**2
    frob_expand = 3 * PHI**4 + 1 * (3*PHI)**2
    print(f"\n  Frobenius squared contributions:")
    print(f"    Contracting: {frob_contract:.4f}")
    print(f"    Expanding:   {frob_expand:.4f}")
    print(f"    Ratio:       {frob_expand/frob_contract:.4f}")

    # The time spent in UP vs DOWN should relate to how much the
    # system needs to "undo" each DOWN step during UP
    # If DOWN contracts by phi_bar^2 and system is at steady-state plateau,
    # then UP must expand by 1/phi_bar^2 = phi^2 to restore.
    # But UP rate < phi^2 per pass (dynamics slower).
    # If UP rate = r_up per pass, and DOWN rate = phi_bar^2 per pass:
    # Steady state: (phi_bar^2)^n_down * r_up^n_up = 1 (net zero)
    # => n_up/n_down = |ln(phi_bar^2)| / ln(r_up)
    # If ratio = 2.0225, then ln(r_up) = |ln(phi_bar^2)| / 2.0225
    # r_up = exp(0.9627/2.0225) = exp(0.4761) = 1.6097
    if all_up_rate_means:
        predicted_up_rate = np.exp(abs(np.log(PHI_BAR_SQ)) / mean_ratio)
        print(f"\n  Steady-state balance prediction:")
        print(f"    If UP/DOWN = {mean_ratio:.4f} and DOWN rate = phi_bar^2 = {PHI_BAR_SQ:.4f}")
        print(f"    Then UP rate should be: exp(|ln(phi_bar^2)|/ratio) = {predicted_up_rate:.6f}")
        print(f"    Measured UP rate: {mean_up_rate:.6f}")
        print(f"    Match: {abs(predicted_up_rate - mean_up_rate)/mean_up_rate*100:.2f}% gap")

    # Final: test if the ratio is exactly derivable from specific combination
    # What if ratio = |ln(phi_bar^2)| / ln(measured_up_rate)?
    if all_up_rate_means:
        derived_ratio = abs(np.log(PHI_BAR_SQ)) / np.log(mean_up_rate)
        print(f"\n  Derived ratio from measured rates: {derived_ratio:.6f}")
        print(f"  Measured ratio from pass counts:   {mean_ratio:.6f}")
        print(f"  Agreement: {abs(derived_ratio - mean_ratio)/mean_ratio*100:.2f}%")

    print(f"\n{'='*60}")
    print("VERDICT")
    print(f"{'='*60}")
    best_name, best_val = sorted_candidates[0]
    best_gap = abs(best_val - mean_ratio) / mean_ratio * 100
    print(f"  Best candidate: {best_name} = {best_val:.6f} (gap {best_gap:.2f}%)")
    if best_gap < 1.0:
        print(f"  >>> MATCH within 1%. Candidate expression IS the ratio.")
        print(f"  >>> If derivable from d_K=8 geometry: C7 FORCED.")
    elif best_gap < 5.0:
        print(f"  >>> CLOSE (within 5%). May need correction term or different expression.")
    else:
        print(f"  >>> NO MATCH. Ratio may be implementation-dependent, not framework-canonical.")


if __name__ == '__main__':
    main()
