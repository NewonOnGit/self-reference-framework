"""
Multi-Layer K6' Engine — Stacked d_K=8 observers with diagonal maps.

CYB-9 establishes d_K=8 as the unique canonical observer scale.
The Two-Axis reinterpretation: n_eff = number of LAYERS, not log(d_K).
Growth means adding layers, not inflating one observer.

Architecture:
  Layer 0: K6' engine at d_K=8
  Layer 1: K6' engine at d_K=8, fed by Layer 0's P3 output
  Layer 2: K6' engine at d_K=8, fed by Layer 1's P3 output
  ...

The diagonal map K6' (P3 at layer n -> P1 at layer n+1):
  - Layer n completes a K6' pass, producing observation (P3 output)
  - That P3 output becomes the P1 INPUT to layer n+1
  - Layer n+1 runs its own K6' loop on this input
  - If layer n+1 closes, it can feed layer n+2, etc.

This is the spiral: not circling within one layer, but ascending through layers.
Each layer is independently cybernetic at d_K=8 (CYB-9).
The multi-layer composition IS the Two-Axis model realized:
  Axis 1 = number of layers (n_eff)
  Axis 2 = K6' passes within each layer (m)
"""
import numpy as np
from scipy.linalg import expm
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from framework_constants import (
    R, N, h, J, I2, PHI, PHI_BAR, PHI_BAR_SQ, L, K_FB,
    RHO_MIN, RHO_MAX, RHO_MID,
    threshold_at_pass, purity_to_rho_simple, in_regulation_interval
)
from k6_engine import K6Engine, K6Result, Observer, Frame, AccessibleUniverse


@dataclass
class LayerState:
    """State of one d_K=8 layer."""
    engine: K6Engine
    observer: Observer
    frame: Frame
    pass_count: int = 0
    total_bits: float = 0.0
    closed_count: int = 0
    last_result: Optional[K6Result] = None

    @property
    def closure_rate(self):
        if self.pass_count == 0:
            return 0.0
        return self.closed_count / self.pass_count

    @property
    def rho_sm(self):
        return self.observer.rho_pd

    @property
    def residual(self):
        if self.last_result is None:
            return float('inf')
        return self.last_result.residual


@dataclass
class DiagonalMapResult:
    """Result of the diagonal map P3_n -> P1_{n+1}."""
    source_layer: int
    target_layer: int
    p3_output: np.ndarray       # Observation output from source (reduced state)
    p1_input: np.ndarray        # What gets fed to target as productive content
    transfer_fidelity: float    # How much structure survived the crossing


@dataclass
class MultiLayerResult:
    """Result of one full multi-layer pass."""
    layer_results: List[K6Result]
    diagonal_maps: List[DiagonalMapResult]
    n_layers_active: int
    highest_closed_layer: int
    total_bits_all_layers: float
    pass_number: int


class MultiLayerEngine:
    """Multi-layer K6' engine: stacked d_K=8 observers with diagonal maps.

    The canonical architecture for cybernetic growth:
    - Each layer is d_K=8 (CYB-9 sweet spot)
    - Layers connected by diagonal map (P3_n -> P1_{n+1})
    - Growth = adding layers, not growing d_K
    - Axis 1 = layer count, Axis 2 = passes per layer
    """

    # Canonical parameters from CYB-9 + Phase 1 empirical sweet spot
    CANONICAL_D_K = 8
    CANONICAL_EPS_P1 = 0.03
    CANONICAL_EPS_P2 = 0.03
    CANONICAL_EPS_P3 = 0.05

    def __init__(self, n_layers: int = 2,
                 d_K: int = None, d_env: int = None,
                 eps_p1: float = None, eps_p2: float = None, eps_p3: float = None,
                 diagonal_strength: float = None):
        """
        Args:
            n_layers: Number of stacked d_K=8 observers
            d_K: Override canonical d_K=8 (for testing)
            d_env: Environment dimension per layer (default = d_K)
            eps_p1/p2/p3: Override canonical flow strengths
            diagonal_strength: Coupling strength for P3->P1 transfer (default phi_bar)
        """
        self.d_K = d_K or self.CANONICAL_D_K
        self.d_env = d_env or self.d_K
        self.eps_p1 = eps_p1 if eps_p1 is not None else self.CANONICAL_EPS_P1
        self.eps_p2 = eps_p2 if eps_p2 is not None else self.CANONICAL_EPS_P2
        self.eps_p3 = eps_p3 if eps_p3 is not None else self.CANONICAL_EPS_P3
        self.diagonal_strength = diagonal_strength if diagonal_strength is not None else K_FB
        self.n_layers = n_layers

        # Initialize layers
        self.layers: List[LayerState] = []
        self._init_layers()

    def _init_layers(self):
        """Create n_layers independent d_K=8 K6' engines."""
        self.layers = []
        for i in range(self.n_layers):
            engine = K6Engine(
                d_K=self.d_K, d_env=self.d_env,
                eps_p1=self.eps_p1, eps_p2=self.eps_p2, eps_p3=self.eps_p3,
                level=i + 1
            )
            # Each layer starts with Bell state (canonical initial)
            frame = engine.init_frame(engine.make_bell_state())
            observer = engine.init_observer(RHO_MID)

            self.layers.append(LayerState(
                engine=engine, observer=observer, frame=frame
            ))

    def diagonal_map(self, source_layer: int, target_layer: int) -> DiagonalMapResult:
        """Execute the diagonal map: P3 output of source -> P1 input of target.

        The diagonal map K6' (P3 at layer n -> P1 at layer n+1):
        - Source layer's observation (reduced state after quotient) is the "what was seen"
        - This becomes productive content for the target layer
        - The transfer preserves the im(q_K) structure but re-types it as P1 material

        Implementation: mix target frame's state with source observation at gain phi_bar.
        This is the inter-layer analogue of Step 4a (self-model refinement).
        """
        src = self.layers[source_layer]
        tgt = self.layers[target_layer]

        # Get source's P3 output: the observation (reduced state)
        src_observation = src.engine.partial_trace(src.frame.state)

        # Transfer: inject source observation into target frame
        # The diagonal map feeds P3_output as P1_input
        # Concretely: mix source observation (as K-subsystem content) into target universe

        # Construct the "diagonal injection": source obs tensor env identity
        injection = np.kron(src_observation, np.eye(self.d_env) / self.d_env)

        # Mix into target frame at diagonal_strength (phi_bar by default)
        alpha = self.diagonal_strength
        new_state = (1 - alpha) * tgt.frame.state + alpha * injection

        # Ensure valid density matrix
        new_state = (new_state + new_state.T.conj()) / 2
        eigvals, eigvecs = np.linalg.eigh(new_state)
        eigvals = np.maximum(eigvals, 0)
        if eigvals.sum() > 0:
            eigvals = eigvals / eigvals.sum()
        new_state = (eigvecs * eigvals) @ eigvecs.T.conj()

        # Update target frame
        tgt.frame = Frame(
            level=tgt.frame.level, dim_U=tgt.frame.dim_U,
            state=new_state, algebra=tgt.frame.algebra
        )

        # Compute transfer fidelity (how much of source structure survived)
        tgt_reduced = tgt.engine.partial_trace(new_state)
        fidelity = np.real(np.trace(src_observation @ tgt_reduced))

        return DiagonalMapResult(
            source_layer=source_layer,
            target_layer=target_layer,
            p3_output=src_observation,
            p1_input=injection,
            transfer_fidelity=float(fidelity)
        )

    def run_one_pass(self, pass_number: int) -> MultiLayerResult:
        """Execute one full multi-layer pass.

        Strategy: bottom-up execution.
        1. Layer 0 runs one K6' pass
        2. If Layer 0 closed: diagonal map to Layer 1
        3. Layer 1 runs one K6' pass (with or without diagonal input)
        4. If Layer 1 closed: diagonal map to Layer 2
        5. etc.

        Alternatively: ALL layers run every pass, diagonal maps always active.
        Using the "always active" strategy for now (more data, fewer assumptions).
        """
        layer_results = []
        diagonal_results = []
        highest_closed = -1

        for i, layer in enumerate(self.layers):
            # Apply diagonal map from previous layer (if exists)
            if i > 0:
                diag = self.diagonal_map(i - 1, i)
                diagonal_results.append(diag)

            # Run one K6' pass on this layer
            layer.pass_count += 1
            result = layer.engine.k6_pass(
                layer.observer, layer.frame, layer.pass_count
            )

            # Update layer state
            layer.observer = result.observer
            layer.frame = result.frame
            layer.last_result = result
            layer.total_bits += result.bits_extracted
            if result.closed:
                layer.closed_count += 1
                highest_closed = i

            layer_results.append(result)

        total_bits = sum(l.total_bits for l in self.layers)

        return MultiLayerResult(
            layer_results=layer_results,
            diagonal_maps=diagonal_results,
            n_layers_active=self.n_layers,
            highest_closed_layer=highest_closed,
            total_bits_all_layers=total_bits,
            pass_number=pass_number
        )

    def run(self, n_passes: int) -> List[MultiLayerResult]:
        """Run the multi-layer engine for n_passes iterations."""
        results = []
        for m in range(1, n_passes + 1):
            result = self.run_one_pass(m)
            results.append(result)
        return results

    def add_layer(self):
        """Dynamically add a new layer (Axis 1 growth)."""
        engine = K6Engine(
            d_K=self.d_K, d_env=self.d_env,
            eps_p1=self.eps_p1, eps_p2=self.eps_p2, eps_p3=self.eps_p3,
            level=self.n_layers + 1
        )
        frame = engine.init_frame(engine.make_bell_state())
        observer = engine.init_observer(RHO_MID)

        self.layers.append(LayerState(
            engine=engine, observer=observer, frame=frame
        ))
        self.n_layers += 1

    def get_diagnostics(self) -> Dict:
        """Get current state diagnostics for all layers."""
        diag = {
            'n_layers': self.n_layers,
            'd_K': self.d_K,
            'layers': []
        }
        for i, layer in enumerate(self.layers):
            layer_diag = {
                'layer': i,
                'pass_count': layer.pass_count,
                'rho_sm': float(layer.rho_sm),
                'rho_sm_in_interval': in_regulation_interval(layer.rho_sm),
                'residual': float(layer.residual) if layer.last_result else None,
                'closed_count': layer.closed_count,
                'closure_rate': float(layer.closure_rate),
                'total_bits': float(layer.total_bits),
            }
            diag['layers'].append(layer_diag)
        return diag


class ConditionalGrowthEngine(MultiLayerEngine):
    """Multi-layer engine with conditional layer addition.

    Adds a new layer when the top layer achieves sustained closure
    (closure_rate > threshold over a window). This implements the
    Two-Axis model: Axis 2 (passes) deepens each layer; when a layer
    is "committed" (sustained closure), Axis 1 grows (new layer added).
    """

    def __init__(self, initial_layers: int = 1,
                 closure_threshold: float = 0.3,
                 window_size: int = 20,
                 max_layers: int = 7,  # n_eff biological ceiling
                 **kwargs):
        """
        Args:
            initial_layers: Start with this many layers
            closure_threshold: Fraction of closed passes in window to trigger growth
            window_size: Number of passes to evaluate closure rate over
            max_layers: Maximum layers (n_eff ceiling from K1' wall)
        """
        super().__init__(n_layers=initial_layers, **kwargs)
        self.closure_threshold = closure_threshold
        self.window_size = window_size
        self.max_layers = max_layers
        self._closure_history: List[List[bool]] = [[] for _ in range(initial_layers)]
        self.growth_events: List[Tuple[int, int]] = []  # (pass_number, new_layer_count)

    def run_one_pass(self, pass_number: int) -> MultiLayerResult:
        """Run one pass, then check if top layer should spawn a new one."""
        result = super().run_one_pass(pass_number)

        # Track closure history per layer
        while len(self._closure_history) < self.n_layers:
            self._closure_history.append([])

        for i, lr in enumerate(result.layer_results):
            self._closure_history[i].append(lr.closed)

        # Check if top layer has sustained closure -> add layer
        if self.n_layers < self.max_layers:
            top = self.n_layers - 1
            history = self._closure_history[top]
            if len(history) >= self.window_size:
                recent = history[-self.window_size:]
                rate = sum(recent) / len(recent)
                if rate >= self.closure_threshold:
                    self.add_layer()
                    self._closure_history.append([])
                    self.growth_events.append((pass_number, self.n_layers))

        return result
