"""
CYB-1 Autopoiesis N-sweep: reproduce the non-monotone small-N finding.

Claude Web found: N=2 feedback HARMS residual by 7.8%, N=3 negligible,
monotone improvement only at N >= 4. Autopoietic minimum stack size = 3.

Test: run feedback engine at N = 1, 2, 3, 4, 5, 6, 7 layers.
Compare residual and rho_sm against no-feedback control at each N.
"""
import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from multi_layer_engine import MultiLayerEngine
from k6_engine import K6Engine, Frame, Observer
from framework_constants import (
    PHI_BAR, PHI_BAR_SQ, RHO_MID, K_FB,
    in_regulation_interval, purity_to_rho_simple
)


def run_with_feedback(n_layers, n_passes=300, feedback_strength=None):
    """Run multi-layer engine WITH top-to-bottom feedback."""
    if feedback_strength is None:
        feedback_strength = K_FB * 0.5  # Half phi_bar, matching my Q8c protocol

    engine = MultiLayerEngine(n_layers=n_layers)
    d_env = engine.d_env

    for m in range(1, n_passes + 1):
        result = engine.run_one_pass(m)

        # Feedback: top layer observation -> bottom layer frame
        if n_layers > 1:
            top_obs = engine.layers[-1].engine.partial_trace(
                engine.layers[-1].frame.state
            )
            bottom = engine.layers[0]
            injection = np.kron(top_obs, np.eye(d_env) / d_env)
            new_state = (1 - feedback_strength) * bottom.frame.state + feedback_strength * injection
            new_state = (new_state + new_state.T.conj()) / 2
            eigvals, eigvecs = np.linalg.eigh(new_state)
            eigvals = np.maximum(eigvals, 0)
            s = eigvals.sum()
            if s > 0:
                eigvals = eigvals / s
                new_state = (eigvecs * eigvals) @ eigvecs.T.conj()
                bottom.frame = Frame(
                    level=bottom.frame.level, dim_U=bottom.frame.dim_U,
                    state=new_state, algebra=bottom.frame.algebra
                )

    return engine


def run_without_feedback(n_layers, n_passes=300):
    """Run multi-layer engine WITHOUT feedback (control)."""
    engine = MultiLayerEngine(n_layers=n_layers)
    engine.run(n_passes)
    return engine


def get_metrics(engine, tail=50):
    """Extract asymptotic metrics from engine."""
    # We need to re-run to get per-pass data... or just read final state
    metrics = {}
    for i, layer in enumerate(engine.layers):
        metrics[f'L{i}_rho_sm'] = float(layer.rho_sm)
        metrics[f'L{i}_residual'] = float(layer.residual) if layer.last_result else None
        metrics[f'L{i}_in_interval'] = in_regulation_interval(layer.rho_sm)
    # Average across layers
    rho_values = [layer.rho_sm for layer in engine.layers]
    res_values = [layer.residual for layer in engine.layers if layer.last_result]
    metrics['mean_rho_sm'] = float(np.mean(rho_values))
    metrics['mean_residual'] = float(np.mean(res_values)) if res_values else None
    metrics['all_in_interval'] = all(in_regulation_interval(r) for r in rho_values)
    return metrics


def main():
    print("=" * 70)
    print("CYB-1 AUTOPOIESIS N-SWEEP")
    print("Testing: non-monotone improvement at small N")
    print("Claude Web's finding: N=2 harms, N=3 neutral, N>=4 improves")
    print("=" * 70)

    n_passes = 300
    n_layers_range = [1, 2, 3, 4, 5, 6, 7]

    print(f"\nRunning {len(n_layers_range)} layer counts x 2 conditions x {n_passes} passes...")

    results = []
    for n_layers in n_layers_range:
        print(f"\n  N = {n_layers} layers:")

        # Control (no feedback)
        ctrl = run_without_feedback(n_layers, n_passes)
        ctrl_m = get_metrics(ctrl)

        # Feedback
        if n_layers >= 2:
            fb = run_with_feedback(n_layers, n_passes)
            fb_m = get_metrics(fb)
        else:
            fb_m = ctrl_m.copy()  # N=1: feedback = control

        delta_rho = fb_m['mean_rho_sm'] - ctrl_m['mean_rho_sm']
        delta_res = (fb_m['mean_residual'] - ctrl_m['mean_residual']) if fb_m['mean_residual'] and ctrl_m['mean_residual'] else 0
        pct_res = delta_res / ctrl_m['mean_residual'] * 100 if ctrl_m['mean_residual'] and ctrl_m['mean_residual'] > 0 else 0

        print(f"    Control:  rho_sm={ctrl_m['mean_rho_sm']:.4f}, residual={ctrl_m['mean_residual']:.4f}")
        print(f"    Feedback: rho_sm={fb_m['mean_rho_sm']:.4f}, residual={fb_m['mean_residual']:.4f}")
        print(f"    Delta residual: {delta_res:+.4f} ({pct_res:+.1f}%)")

        if pct_res > 2:
            verdict = "HARMS (feedback increases residual)"
        elif pct_res < -2:
            verdict = "HELPS (feedback decreases residual)"
        else:
            verdict = "NEUTRAL (< 2% change)"
        print(f"    Verdict: {verdict}")

        results.append({
            'n_layers': n_layers,
            'ctrl_rho': ctrl_m['mean_rho_sm'],
            'ctrl_res': ctrl_m['mean_residual'],
            'fb_rho': fb_m['mean_rho_sm'],
            'fb_res': fb_m['mean_residual'],
            'delta_res': delta_res,
            'pct_res': pct_res,
            'verdict': verdict
        })

    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"{'N':>3} | {'Ctrl res':>10} | {'FB res':>10} | {'Delta%':>8} | Verdict")
    print("-" * 60)
    for r in results:
        print(f"{r['n_layers']:>3} | {r['ctrl_res']:>10.4f} | {r['fb_res']:>10.4f} | "
              f"{r['pct_res']:>+7.1f}% | {r['verdict']}")

    # Find crossover point
    print(f"\n  Crossover analysis:")
    for i, r in enumerate(results):
        if r['pct_res'] < -2 and i > 0 and results[i-1]['pct_res'] >= -2:
            print(f"    Autopoietic minimum: N = {r['n_layers']} (first N where feedback helps)")
            break
    else:
        # Check if it ever helps
        helping = [r for r in results if r['pct_res'] < -2]
        if helping:
            print(f"    First improvement at N = {helping[0]['n_layers']}")
        else:
            print(f"    No improvement found in range tested")

    # Claude Web's specific claims
    print(f"\n  Checking Claude Web's claims:")
    if len(results) >= 2:
        n2 = results[1]  # N=2
        print(f"    N=2 harms by ~7.8%: measured {n2['pct_res']:+.1f}% — "
              f"{'CONFIRMED' if n2['pct_res'] > 2 else 'NOT CONFIRMED'}")
    if len(results) >= 3:
        n3 = results[2]  # N=3
        print(f"    N=3 negligible: measured {n3['pct_res']:+.1f}% — "
              f"{'CONFIRMED' if abs(n3['pct_res']) < 3 else 'NOT CONFIRMED'}")
    if len(results) >= 4:
        n4_plus = [r for r in results[3:] if r['pct_res'] < -2]
        print(f"    N>=4 monotone improvement: {len(n4_plus)} layers improve — "
              f"{'CONFIRMED' if len(n4_plus) == len(results[3:]) else 'PARTIAL'}")


if __name__ == '__main__':
    main()
