"""
Phase 1: Scale d_K ∈ {2, 4, 8, 16} — does sustained K6' closure appear at scale?

Tests the hypothesis that d_K=2 is simply too small for sustained closure,
while the framework predicts closure is achievable for sufficiently large observers.

Runs each configuration for 100 passes at multiple ε values.
Reports: closure count, asymptotic ρ_sm, asymptotic ρ_obs, residual trajectory.
"""
import sys
import os
import numpy as np
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from k6_engine import K6Engine, tower_lift
from framework_constants import (
    PHI_BAR, PHI_BAR_SQ, RHO_MIN, RHO_MAX, L,
    in_regulation_interval, threshold_at_pass
)


def run_experiment(d_K, eps_p1, eps_p2, eps_p3, n_passes=100, initial='bell'):
    """Run K6' loop at given scale and flow strengths."""
    engine = K6Engine(d_K=d_K, d_env=d_K, eps_p1=eps_p1, eps_p2=eps_p2, eps_p3=eps_p3)

    if initial == 'bell':
        state = engine.make_bell_state()
    elif initial == 'mixed':
        state = engine.make_max_mixed()
    elif initial == 'product':
        state = engine.make_product_state()
    else:
        state = engine.make_bell_state()

    results = engine.run(n_passes, initial_state=state)

    # Extract trajectories
    residuals = [r.residual for r in results]
    thresholds = [r.threshold for r in results]
    rho_sm = [r.observer.rho_pd for r in results]
    rho_obs = [r.accessible.rho_pd for r in results]
    closures = [r.closed for r in results]

    # Asymptotic values (last 20% of passes)
    tail = max(1, n_passes // 5)
    asym_rho_sm = np.mean(rho_sm[-tail:])
    asym_rho_obs = np.mean(rho_obs[-tail:])
    asym_residual = np.mean(residuals[-tail:])
    n_closed = sum(closures)

    # CYB-Coupling test
    sm_in_interval_when_closed = sum(
        1 for i, c in enumerate(closures) if c and in_regulation_interval(rho_sm[i])
    )
    sm_in_interval_when_open = sum(
        1 for i, c in enumerate(closures) if not c and in_regulation_interval(rho_sm[i])
    )
    n_open = n_passes - n_closed

    p_in_given_closed = sm_in_interval_when_closed / max(n_closed, 1)
    p_in_given_open = sm_in_interval_when_open / max(n_open, 1)

    return {
        'd_K': d_K,
        'eps_p1': eps_p1,
        'eps_p2': eps_p2,
        'eps_p3': eps_p3,
        'initial': initial,
        'n_passes': n_passes,
        'n_closed': n_closed,
        'asym_rho_sm': float(asym_rho_sm),
        'asym_rho_obs': float(asym_rho_obs),
        'asym_residual': float(asym_residual),
        'p_in_given_closed': float(p_in_given_closed),
        'p_in_given_open': float(p_in_given_open),
        'rho_sm_in_interval_final': in_regulation_interval(rho_sm[-1]),
        'residual_trajectory': [float(x) for x in residuals[:20]] + ['...'] + [float(x) for x in residuals[-5:]],
        'rho_sm_trajectory': [float(x) for x in rho_sm[:10]] + ['...'] + [float(x) for x in rho_sm[-5:]],
    }


def main():
    print("=" * 70)
    print("PHASE 1: K6' SCALING TEST")
    print(f"Question: Does sustained K6' closure appear at d_K > 2?")
    print(f"Framework prediction: closure achievable for sufficiently large observers")
    print(f"Regulation interval: [{RHO_MIN:.4f}, {RHO_MAX:.4f}]")
    import sys as _sys
    _sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    print(f"Commitment rate: phi_bar^2 = {PHI_BAR_SQ:.6f} per pass")
    print(f"Feedback gain: phi_bar = {PHI_BAR:.6f} (RES-4)")
    print("=" * 70)

    # Test matrix
    d_K_values = [2, 4, 8]  # 16 may be slow depending on machine
    eps_configs = [
        (0.1, 0.1, 0.0, "gentle P1+P2"),
        (0.1, 0.1, 0.1, "gentle P1+P2+P3"),
        (0.03, 0.03, 0.0, "very gentle P1+P2"),
        (0.03, 0.03, 0.05, "very gentle + P3"),
    ]

    all_results = []

    for d_K in d_K_values:
        print(f"\n{'─' * 50}")
        print(f"  d_K = {d_K} (H_U = {d_K*d_K}×{d_K*d_K})")
        print(f"{'─' * 50}")

        for eps_p1, eps_p2, eps_p3, label in eps_configs:
            print(f"\n  Config: {label} (ε₁={eps_p1}, ε₂={eps_p2}, ε₃={eps_p3})")

            try:
                result = run_experiment(
                    d_K=d_K, eps_p1=eps_p1, eps_p2=eps_p2, eps_p3=eps_p3,
                    n_passes=100, initial='bell'
                )
                result['label'] = label
                all_results.append(result)

                closed_pct = result['n_closed'] / result['n_passes'] * 100
                in_interval = "YES" if result['rho_sm_in_interval_final'] else "NO"

                print(f"    Closed: {result['n_closed']}/{result['n_passes']} ({closed_pct:.1f}%)")
                print(f"    ρ_sm asymptotic: {result['asym_rho_sm']:.4f}")
                print(f"    ρ_obs asymptotic: {result['asym_rho_obs']:.4f}")
                print(f"    Residual asymptotic: {result['asym_residual']:.4f}")
                print(f"    Final ρ_sm in [{RHO_MIN:.3f}, {RHO_MAX:.3f}]: {in_interval}")
                if result['n_closed'] > 0:
                    print(f"    CYB-Coupling: P(in|closed)={result['p_in_given_closed']:.2f}, "
                          f"P(in|open)={result['p_in_given_open']:.2f}")

            except Exception as e:
                print(f"    ERROR: {e}")
                all_results.append({'d_K': d_K, 'label': label, 'error': str(e)})

    # Try d_K=16 if machine can handle it
    print(f"\n{'─' * 50}")
    print(f"  d_K = 16 (H_U = 256×256) — may be slow")
    print(f"{'─' * 50}")
    try:
        result = run_experiment(d_K=16, eps_p1=0.03, eps_p2=0.03, eps_p3=0.05,
                               n_passes=50, initial='bell')
        result['label'] = "very gentle + P3 (d_K=16)"
        all_results.append(result)
        print(f"    Closed: {result['n_closed']}/{result['n_passes']}")
        print(f"    ρ_sm asymptotic: {result['asym_rho_sm']:.4f}")
        print(f"    ρ_obs asymptotic: {result['asym_rho_obs']:.4f}")
    except Exception as e:
        print(f"    SKIPPED (too slow or error): {e}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY TABLE")
    print("=" * 70)
    print(f"{'d_K':>4} | {'Config':<25} | {'Closed':>7} | {'ρ_sm':>8} | {'ρ_obs':>8} | {'In I?':>5}")
    print("-" * 70)
    for r in all_results:
        if 'error' in r:
            print(f"{r['d_K']:>4} | {r['label']:<25} | {'ERROR':>7} | {'—':>8} | {'—':>8} | {'—':>5}")
        else:
            in_i = "✓" if r['rho_sm_in_interval_final'] else "✗"
            print(f"{r['d_K']:>4} | {r.get('label','?'):<25} | "
                  f"{r['n_closed']:>3}/{r['n_passes']:<3} | "
                  f"{r['asym_rho_sm']:>8.4f} | {r['asym_rho_obs']:>8.4f} | {in_i:>5}")

    # Key question
    print("\n" + "=" * 70)
    print("KEY QUESTION: Does ρ_sm rise toward [φ̄², 1/2] with d_K?")
    d2_rho = [r['asym_rho_sm'] for r in all_results if r.get('d_K') == 2 and 'error' not in r]
    d4_rho = [r['asym_rho_sm'] for r in all_results if r.get('d_K') == 4 and 'error' not in r]
    d8_rho = [r['asym_rho_sm'] for r in all_results if r.get('d_K') == 8 and 'error' not in r]
    if d2_rho and d4_rho:
        trend = "RISING" if np.mean(d4_rho) > np.mean(d2_rho) else "FLAT/FALLING"
        print(f"  d_K=2 mean ρ_sm: {np.mean(d2_rho):.4f}")
        print(f"  d_K=4 mean ρ_sm: {np.mean(d4_rho):.4f}")
        if d8_rho:
            print(f"  d_K=8 mean ρ_sm: {np.mean(d8_rho):.4f}")
        print(f"  Trend: {trend}")
        if trend == "RISING":
            print("  → Supports hypothesis: larger d_K enables regulation.")
            print("  → Extrapolate: d_K threshold for sustained closure exists.")
        else:
            print("  → Against hypothesis: scale alone doesn't solve it.")
            print("  → Tower lift (Phase 1.5) likely required.")
    print("=" * 70)

    # Save results
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'phase1_results')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"phase1_scaling_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\nResults saved to: {output_file}")


if __name__ == '__main__':
    main()
