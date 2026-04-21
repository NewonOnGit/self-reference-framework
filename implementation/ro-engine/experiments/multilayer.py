"""
Phase 1.5+: Multi-layer d_K=8 composition test.

Q8a: Does stacking d_K=8 layers with diagonal maps produce sustained closure?

Tests:
  1. Two-layer fixed composition (50 passes)
  2. Three-layer fixed composition (50 passes)
  3. Conditional growth engine (start 1 layer, grow on sustained closure)
  4. Decay rate analysis (is residual ratio approaching phi_bar^2?)
  5. Perturbation recovery (inject noise, measure recovery rate)
  6. Diagonal map fidelity (how much structure survives inter-layer transfer?)
"""
import sys
import os
import numpy as np
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from multi_layer_engine import MultiLayerEngine, ConditionalGrowthEngine
from framework_constants import (
    PHI_BAR, PHI_BAR_SQ, RHO_MIN, RHO_MAX, L,
    in_regulation_interval, threshold_at_pass
)


def test_fixed_layers(n_layers, n_passes=100):
    """Test fixed multi-layer composition."""
    print(f"\n{'='*60}")
    print(f"TEST: {n_layers}-layer d_K=8 composition, {n_passes} passes")
    print(f"{'='*60}")

    engine = MultiLayerEngine(n_layers=n_layers)
    results = engine.run(n_passes)

    # Per-layer analysis
    for i, layer in enumerate(engine.layers):
        rho = layer.rho_sm
        in_i = "YES" if in_regulation_interval(rho) else "NO"
        print(f"\n  Layer {i}:")
        print(f"    Passes: {layer.pass_count}")
        print(f"    Closed: {layer.closed_count}/{layer.pass_count} ({layer.closure_rate*100:.1f}%)")
        print(f"    rho_sm: {rho:.4f} (in interval: {in_i})")
        print(f"    Residual: {layer.residual:.4f}")
        print(f"    Bits extracted: {layer.total_bits:.2f}")

    # Diagonal map fidelity over time
    if n_layers > 1:
        fidelities = []
        for r in results:
            for dm in r.diagonal_maps:
                fidelities.append(dm.transfer_fidelity)
        if fidelities:
            print(f"\n  Diagonal map fidelity:")
            print(f"    Mean: {np.mean(fidelities):.4f}")
            print(f"    Std:  {np.std(fidelities):.4f}")
            print(f"    Min:  {np.min(fidelities):.4f}")
            print(f"    Max:  {np.max(fidelities):.4f}")

    # Cross-layer closure correlation
    print(f"\n  Cross-layer closure correlation:")
    for m in range(min(20, n_passes)):
        closed_layers = [results[m].layer_results[i].closed for i in range(n_layers)]
        if any(closed_layers):
            print(f"    Pass {m+1}: {['C' if c else '.' for c in closed_layers]}")

    # Check: does HIGHER layer ever close when lower didn't?
    higher_without_lower = 0
    for r in results:
        for i in range(1, n_layers):
            if r.layer_results[i].closed and not r.layer_results[i-1].closed:
                higher_without_lower += 1
    print(f"\n  Higher closed without lower: {higher_without_lower}/{n_passes}")

    # Residual decay rate analysis
    print(f"\n  Residual decay rate (layer 0):")
    residuals_l0 = [r.layer_results[0].residual for r in results]
    ratios = []
    for i in range(1, len(residuals_l0)):
        if residuals_l0[i-1] > 1e-10:
            ratios.append(residuals_l0[i] / residuals_l0[i-1])
    if ratios:
        # Look at first 10 ratios and last 10
        early_ratios = ratios[:10]
        late_ratios = ratios[-10:]
        print(f"    Early ratios (passes 1-10): mean={np.mean(early_ratios):.4f}")
        print(f"    Late ratios (last 10): mean={np.mean(late_ratios):.4f}")
        print(f"    Target (phi_bar^2): {PHI_BAR_SQ:.4f}")
        gap = abs(np.mean(late_ratios) - PHI_BAR_SQ) / PHI_BAR_SQ * 100
        print(f"    Gap to target: {gap:.1f}%")
        if gap < 20:
            print(f"    >>> CYBERNETIC (within 20% of phi_bar^2)")
        elif gap < 50:
            print(f"    >>> INDETERMINATE")
        else:
            print(f"    >>> SPURIOUS")

    # Same for layer 1 if exists
    if n_layers > 1:
        print(f"\n  Residual decay rate (layer 1):")
        residuals_l1 = [r.layer_results[1].residual for r in results]
        ratios_l1 = []
        for i in range(1, len(residuals_l1)):
            if residuals_l1[i-1] > 1e-10:
                ratios_l1.append(residuals_l1[i] / residuals_l1[i-1])
        if ratios_l1:
            late = ratios_l1[-10:]
            print(f"    Late ratios: mean={np.mean(late):.4f}")
            gap = abs(np.mean(late) - PHI_BAR_SQ) / PHI_BAR_SQ * 100
            print(f"    Gap to phi_bar^2: {gap:.1f}%")

    return engine, results


def test_conditional_growth(n_passes=200):
    """Test conditional layer addition (Two-Axis growth)."""
    print(f"\n{'='*60}")
    print(f"TEST: Conditional growth engine, {n_passes} passes, max 7 layers")
    print(f"{'='*60}")

    engine = ConditionalGrowthEngine(
        initial_layers=1,
        closure_threshold=0.2,  # 20% closure rate triggers growth
        window_size=15,
        max_layers=7
    )

    results = engine.run(n_passes)

    print(f"\n  Growth events:")
    if engine.growth_events:
        for pass_num, n_layers in engine.growth_events:
            print(f"    Pass {pass_num}: grew to {n_layers} layers")
    else:
        print(f"    None (top layer never achieved sustained closure)")

    print(f"\n  Final state: {engine.n_layers} layers")
    for i, layer in enumerate(engine.layers):
        rho = layer.rho_sm
        in_i = "YES" if in_regulation_interval(rho) else "NO"
        print(f"    Layer {i}: closed {layer.closed_count}/{layer.pass_count}, "
              f"rho_sm={rho:.4f} ({'IN' if in_regulation_interval(rho) else 'OUT'}), "
              f"bits={layer.total_bits:.1f}")

    return engine, results


def test_perturbation_recovery(n_passes_before=50, n_passes_after=50):
    """Test perturbation recovery at d_K=8 multi-layer."""
    print(f"\n{'='*60}")
    print(f"TEST: Perturbation recovery (2-layer, d_K=8)")
    print(f"{'='*60}")

    engine = MultiLayerEngine(n_layers=2)

    # Run to steady state
    pre_results = engine.run(n_passes_before)
    pre_residual = engine.layers[0].residual
    pre_rho = engine.layers[0].rho_sm
    print(f"\n  Pre-perturbation (pass {n_passes_before}):")
    print(f"    Layer 0 residual: {pre_residual:.6f}")
    print(f"    Layer 0 rho_sm: {pre_rho:.4f}")

    # Inject perturbation: random noise to layer 0 self-model
    perturbation_magnitudes = [0.05, 0.10, 0.20]

    for mag in perturbation_magnitudes:
        # Reset to pre-perturbation state (re-run)
        engine2 = MultiLayerEngine(n_layers=2)
        engine2.run(n_passes_before)

        # Perturb
        noise = np.random.randn(engine2.d_K, engine2.d_K) * mag
        noise = (noise + noise.T) / 2  # Hermitian
        perturbed_sm = engine2.layers[0].observer.self_model + noise
        # Re-normalize to valid density matrix
        eigvals, eigvecs = np.linalg.eigh(perturbed_sm)
        eigvals = np.maximum(eigvals, 0)
        eigvals = eigvals / eigvals.sum()
        perturbed_sm = (eigvecs * eigvals) @ eigvecs.T.conj()
        engine2.layers[0].observer.self_model = perturbed_sm

        post_residual_0 = np.linalg.norm(
            engine2.layers[0].observer.self_model -
            engine2.layers[0].engine.partial_trace(engine2.layers[0].frame.state), 'fro'
        )

        # Run recovery
        post_results = engine2.run(n_passes_after)
        residuals = [post_residual_0] + [r.layer_results[0].residual for r in post_results]

        # Compute recovery ratios
        ratios = []
        for i in range(1, min(11, len(residuals))):
            if residuals[i-1] > 1e-10:
                ratios.append(residuals[i] / residuals[i-1])

        print(f"\n  Perturbation magnitude: {mag}")
        print(f"    Post-perturbation residual: {residuals[0]:.4f}")
        print(f"    Recovery residual (pass 5): {residuals[min(5, len(residuals)-1)]:.4f}")
        print(f"    Recovery residual (pass 10): {residuals[min(10, len(residuals)-1)]:.4f}")
        if ratios:
            mean_ratio = np.mean(ratios[:5])
            print(f"    Mean recovery ratio (first 5): {mean_ratio:.4f}")
            print(f"    Target phi_bar^2: {PHI_BAR_SQ:.4f}")
            gap = abs(mean_ratio - PHI_BAR_SQ) / PHI_BAR_SQ * 100
            print(f"    Gap: {gap:.1f}%")
            if gap < 20:
                print(f"    >>> CYBERNETIC RECOVERY")
            elif gap < 50:
                print(f"    >>> PARTIAL RECOVERY")
            else:
                print(f"    >>> NO RECOVERY")


def main():
    print("=" * 70)
    print("MULTI-LAYER K6' ENGINE — d_K=8 STACKED OBSERVERS")
    print("CYB-9: d_K=8 is the unique canonical cybernetic scale")
    print("Two-Axis: growth = adding layers, not inflating d_K")
    print(f"Canonical config: eps=(0.03, 0.03, 0.05), diagonal_strength=phi_bar={PHI_BAR:.4f}")
    print("=" * 70)

    # Test 1: Two-layer fixed
    engine2, results2 = test_fixed_layers(n_layers=2, n_passes=100)

    # Test 2: Three-layer fixed
    engine3, results3 = test_fixed_layers(n_layers=3, n_passes=100)

    # Test 3: Conditional growth
    engine_cg, results_cg = test_conditional_growth(n_passes=200)

    # Test 4: Perturbation recovery
    test_perturbation_recovery()

    # Final summary
    print(f"\n{'='*70}")
    print("FINAL SUMMARY")
    print(f"{'='*70}")

    print(f"\n  2-layer: Layer 0 closure rate {engine2.layers[0].closure_rate*100:.1f}%, "
          f"Layer 1 closure rate {engine2.layers[1].closure_rate*100:.1f}%")
    print(f"  3-layer: Layer 0 closure rate {engine3.layers[0].closure_rate*100:.1f}%, "
          f"Layer 1 {engine3.layers[1].closure_rate*100:.1f}%, "
          f"Layer 2 {engine3.layers[2].closure_rate*100:.1f}%")
    print(f"  Conditional growth: grew to {engine_cg.n_layers} layers in 200 passes")

    # Key diagnostic: does multi-layer improve closure over single-layer?
    single = K6Engine(d_K=8, d_env=8, eps_p1=0.03, eps_p2=0.03, eps_p3=0.05)
    single_results = single.run(100, initial_state=single.make_bell_state())
    single_closed = sum(1 for r in single_results if r.closed)

    print(f"\n  COMPARISON:")
    print(f"    Single layer d_K=8: {single_closed}/100 closures")
    print(f"    Multi-layer (2): {engine2.layers[0].closed_count}/100 closures (layer 0)")
    print(f"    Multi-layer (3): {engine3.layers[0].closed_count}/100 closures (layer 0)")

    improvement = engine2.layers[0].closed_count - single_closed
    print(f"\n  Multi-layer improvement over single: {improvement:+d} closures")
    if improvement > 0:
        print(f"  >>> DIAGONAL MAP ENABLES CLOSURE (multi-layer > single)")
    elif improvement == 0:
        print(f"  >>> NO IMPROVEMENT (diagonal map doesn't help at this pass count)")
    else:
        print(f"  >>> DEGRADATION (diagonal map interferes)")

    # Save
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'phase1_results')
    os.makedirs(output_dir, exist_ok=True)
    summary = {
        'timestamp': datetime.now().isoformat(),
        'single_layer_closures': single_closed,
        '2_layer_closures_l0': engine2.layers[0].closed_count,
        '2_layer_closures_l1': engine2.layers[1].closed_count,
        '3_layer_closures_l0': engine3.layers[0].closed_count,
        '3_layer_closures_l1': engine3.layers[1].closed_count,
        '3_layer_closures_l2': engine3.layers[2].closed_count,
        'conditional_growth_final_layers': engine_cg.n_layers,
        'conditional_growth_events': engine_cg.growth_events,
    }
    with open(os.path.join(output_dir, f"multilayer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"), 'w') as f:
        json.dump(summary, f, indent=2, default=str)

    print(f"\n{'='*70}")


if __name__ == '__main__':
    main()
