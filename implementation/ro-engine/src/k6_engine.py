"""
K6' Engine — The cybernetic loop implementation.

Implements the minimal self-growing algorithm (MIN-1 §1.2):
  Step 1: P1 Productive Act (R-flow on K-subsystem)
  Step 2: P2 Mediating Act (exp(h)-flow transport)
  Step 3: P3 Observer Act (partial trace = quotient)
  Step 4: K6' Closure Check (self-model vs observation)
  Step 4a: Self-Model Refinement (gain φ̄, RES-4)
  Step 4b: Frame Regulation (endogenous ρ-correction)
  Step 5: Commitment increment (on closure)
  Step 6: Tower lift (on milestone) — Phase 1.5
  Step 7: Recursive Disclosure (kernel accounting)

All branch points resolved to framework-canonical values.
"""
import numpy as np
from scipy.linalg import expm
from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple, List
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from framework_constants import (
    R, N, h, J, I2, exp_h, PHI, PHI_BAR, PHI_BAR_SQ,
    K_FB, L, RHO_MIN, RHO_MAX, RHO_MID,
    threshold_at_pass, purity_to_rho_simple, in_regulation_interval,
    cross_channel_content
)


@dataclass
class Frame:
    """Typed data object representing the framework at a tower level.
    Not just a Hilbert space — annotated content the observer can examine."""
    level: int
    dim_U: int
    state: np.ndarray           # ρ_U (density matrix of universe)
    algebra: Dict[str, np.ndarray] = field(default_factory=dict)

    def __post_init__(self):
        if not self.algebra:
            d = self.dim_U // 2  # d_K for the split
            self.algebra = {
                'R': np.kron(R, np.eye(d)),
                'N': np.kron(N, np.eye(d)),
                'h': np.kron(h, np.eye(d)),
                'I': np.eye(self.dim_U),
            }


@dataclass
class Observer:
    """Observer triple K = (d_K, Δ_K, σ_K) with explicit self-model.
    Self-model is K's internal representation of its own state in H_K."""
    d_K: int
    self_model: np.ndarray      # d_K × d_K density matrix
    delta_K: float = 1.0        # Feasibility window
    sigma_K: np.ndarray = None  # Computational signature

    def __post_init__(self):
        if self.sigma_K is None:
            self.sigma_K = np.array([0.5, PHI_BAR/2, PHI_BAR_SQ/2])  # Self-signature

    @property
    def rho_pd(self):
        """Phase-Dist parameter of self-model."""
        return purity_to_rho_simple(self.self_model)


@dataclass
class AccessibleUniverse:
    """U(K) — what the observer can access after quotient."""
    reduced_state: np.ndarray   # q_K(ρ_U) = tr_env(ρ_U)
    rho_pd: float               # Phase-Dist of reduced state
    ker_dim: int                # Dimension of kernel


@dataclass
class K6Result:
    """Result of one K6' pass."""
    closed: bool
    residual: float
    threshold: float
    observer: Observer
    frame: Frame
    accessible: AccessibleUniverse
    pass_number: int
    bits_extracted: float
    commitment_total: float


class K6Engine:
    """The K6' cybernetic loop engine.

    Implements MIN-1 algorithm at arbitrary d_K and tower level.
    Flow strength ε controls discretization (ε → 0 = continuous limit).
    """

    def __init__(self, d_K: int, d_env: int = None, eps_p1: float = 0.1,
                 eps_p2: float = 0.1, eps_p3: float = 0.0, level: int = 1):
        """
        Args:
            d_K: Observer disclosure dimension (2, 4, 8, ...)
            d_env: Environment dimension (default = d_K)
            eps_p1: P1 flow strength (R-conjugation)
            eps_p2: P2 flow strength (h-transport)
            eps_p3: P3 flow strength (N-rotation)
            level: Tower level
        """
        self.d_K = d_K
        self.d_env = d_env or d_K
        self.d_U = d_K * self.d_env
        self.eps_p1 = eps_p1
        self.eps_p2 = eps_p2
        self.eps_p3 = eps_p3
        self.level = level

        # Build generators at this dimension
        self._build_generators()

    def _build_generators(self):
        """Construct generators via tensor products at the current tower level."""
        d = self.d_K
        d_env = self.d_env

        # For d_K = 2^n, use tensor power of base generators
        # For d_K = 2: direct R, N, h
        # For d_K = 4: R⊗I₂ + I₂⊗R (summed insertion), etc.
        # For general: build from the base 2×2 generators

        n_K = int(np.log2(d))
        if 2**n_K != d:
            raise ValueError(f"d_K must be power of 2, got {d}")

        # Production generator on K-subsystem (summed insertion for d_K > 2)
        if n_K == 1:
            R_K = R
            N_K = N
            h_K = h
        else:
            # Summed insertions: R_K = Σ_s (I⊗...⊗R_s⊗...⊗I)
            R_K = np.zeros((d, d))
            N_K = np.zeros((d, d))
            h_K = np.zeros((d, d))
            for s in range(n_K):
                factors_R = [np.eye(2)] * n_K
                factors_R[s] = R
                factors_N = [np.eye(2)] * n_K
                factors_N[s] = N
                factors_h = [np.eye(2)] * n_K
                factors_h[s] = h
                term_R = factors_R[0]
                term_N = factors_N[0]
                term_h = factors_h[0]
                for i in range(1, n_K):
                    term_R = np.kron(term_R, factors_R[i])
                    term_N = np.kron(term_N, factors_N[i])
                    term_h = np.kron(term_h, factors_h[i])
                R_K += term_R
                N_K += term_N
                h_K += term_h

        # Lift to full universe: generator ⊗ I_env
        I_env = np.eye(d_env)
        self.R_U = np.kron(R_K, I_env)
        self.N_U = np.kron(N_K, I_env)
        self.h_U = np.kron(h_K, I_env)
        self.I_U = np.eye(self.d_U)

        # Pre-compute flow operators for current ε values
        self._update_flow_operators()

    def _update_flow_operators(self):
        """Compute exp(ε·generator) for P1, P2, P3 flows."""
        if self.eps_p1 != 0:
            self.flow_p1 = expm(self.eps_p1 * self.R_U)
        else:
            self.flow_p1 = self.I_U.copy()

        if self.eps_p2 != 0:
            self.flow_p2 = expm(self.eps_p2 * self.h_U)
        else:
            self.flow_p2 = self.I_U.copy()

        if self.eps_p3 != 0:
            self.flow_p3 = expm(self.eps_p3 * self.N_U)
        else:
            self.flow_p3 = self.I_U.copy()

    def make_bell_state(self) -> np.ndarray:
        """|Ψ⁺⟩⟨Ψ⁺| — maximally entangled (gauge orbit, pre-naming I/2)."""
        d = min(self.d_K, self.d_env)
        psi = np.zeros(self.d_U)
        for i in range(d):
            psi[i * self.d_env + i] = 1.0 / np.sqrt(d)
        return np.outer(psi, psi)

    def make_max_mixed(self) -> np.ndarray:
        """I/d_U — maximally mixed universe state."""
        return self.I_U / self.d_U

    def make_product_state(self) -> np.ndarray:
        """Product state |0⟩⟨0| ⊗ I_env/d_env."""
        rho_K = np.zeros((self.d_K, self.d_K))
        rho_K[0, 0] = 1.0
        rho_env = np.eye(self.d_env) / self.d_env
        return np.kron(rho_K, rho_env)

    def init_frame(self, state: np.ndarray = None) -> Frame:
        """Initialize FRAME with a universe state."""
        if state is None:
            state = self.make_bell_state()
        return Frame(level=self.level, dim_U=self.d_U, state=state)

    def init_observer(self, rho_pd_init: float = None) -> Observer:
        """Initialize observer with self-model at regulation midpoint."""
        if rho_pd_init is None:
            rho_pd_init = RHO_MID
        # Construct density matrix with target ρ_PD
        # For d_K=2: ρ = (I + r⃗·σ⃗)/2 with |r⃗|² = 1 - 2*ρ_PD
        r_sq = max(0, 1 - 2 * rho_pd_init)
        r = np.sqrt(r_sq)
        # Point along z-axis for simplicity
        self_model = np.array([[0.5 + r/2, 0], [0, 0.5 - r/2]])
        if self.d_K > 2:
            # For larger d_K: embed in top-left 2×2, rest maximally mixed
            sm = np.eye(self.d_K) / self.d_K
            # Mix: target purity = 1 - ρ_PD (simplified for d_K > 2)
            target_purity = 1 - rho_pd_init
            # Pure component
            pure = np.zeros((self.d_K, self.d_K))
            pure[0, 0] = 1.0
            mixed = np.eye(self.d_K) / self.d_K
            # Interpolate: ρ = α|0⟩⟨0| + (1-α)I/d
            # purity = α² + (1-α)²/d + cross terms... approximate:
            # For large d: purity ≈ α² + (1-α)²/d
            # Solve for α given target_purity
            alpha = np.sqrt(max(0, (target_purity - 1/self.d_K) / (1 - 1/self.d_K)))
            alpha = min(alpha, 1.0)
            self_model = alpha * pure + (1 - alpha) * mixed
        return Observer(d_K=self.d_K, self_model=self_model)

    def partial_trace(self, rho_U: np.ndarray) -> np.ndarray:
        """q_K = tr_env: trace out environment, return reduced state on K."""
        reshaped = rho_U.reshape(self.d_K, self.d_env, self.d_K, self.d_env)
        return np.trace(reshaped, axis1=1, axis2=3)

    def observe(self, K: Observer, F: Frame) -> AccessibleUniverse:
        """Arrow K → F → U(K). Observer quotients the frame."""
        reduced = self.partial_trace(F.state)
        rho_pd = purity_to_rho_simple(reduced)
        ker_dim = self.d_U**2 - self.d_K**2  # dim(ker(q_K))
        return AccessibleUniverse(
            reduced_state=reduced,
            rho_pd=rho_pd,
            ker_dim=ker_dim
        )

    def apply_dynamics(self, F: Frame) -> Frame:
        """Apply P1 + P2 + P3 flows to the frame state.
        Step 1 (P1): exp(ε₁·R⊗I) conjugation
        Step 2 (P2): exp(ε₂·h⊗I) conjugation
        Step 3 (P3): exp(ε₃·N⊗I) conjugation (rotation)
        """
        state = F.state.copy()

        # P1: Production (R-flow)
        if self.eps_p1 != 0:
            state = self.flow_p1 @ state @ self.flow_p1.T
            state = state / np.trace(state)  # Renormalize (non-unitary R)

        # P2: Mediation (h-flow)
        if self.eps_p2 != 0:
            state = self.flow_p2 @ state @ self.flow_p2.T
            state = state / np.trace(state)

        # P3: Observation (N-rotation, unitary)
        if self.eps_p3 != 0:
            state = self.flow_p3 @ state @ self.flow_p3.T
            # No renormalization needed (unitary)

        return Frame(level=F.level, dim_U=F.dim_U, state=state, algebra=F.algebra)

    def refine_self_model(self, K: Observer, U_K: AccessibleUniverse) -> Observer:
        """Step 4a: Update self-model toward observation at gain φ̄ (RES-4).
        Then regulate to keep self-model in [φ̄², 1/2]."""
        # Fibonacci-gain update: new = (1-φ̄)·old + φ̄·observed
        new_sm = (1 - K_FB) * K.self_model + K_FB * U_K.reduced_state

        # Ensure valid density matrix
        new_sm = (new_sm + new_sm.T.conj()) / 2  # Hermitianize
        # Eigenvalue clamp (keep positive semidefinite)
        eigvals, eigvecs = np.linalg.eigh(new_sm)
        eigvals = np.maximum(eigvals, 0)
        eigvals = eigvals / eigvals.sum()  # Normalize trace = 1
        new_sm = (eigvecs * eigvals) @ eigvecs.T.conj()

        # ρ-regulation: if outside [φ̄², 1/2], correct
        rho_pd = purity_to_rho_simple(new_sm)
        if rho_pd < RHO_MIN:
            # Too pure — mix toward maximally mixed
            target_rho = RHO_MIN
            correction = K_FB * (target_rho - rho_pd) / (0.5 - rho_pd + 1e-10)
            correction = min(correction, 1.0)
            mixed = np.eye(self.d_K) / self.d_K
            new_sm = (1 - correction) * new_sm + correction * mixed
        elif rho_pd > RHO_MAX:
            # Too mixed — purify toward dominant eigenvector
            target_rho = RHO_MAX
            eigvals, eigvecs = np.linalg.eigh(new_sm)
            pure = np.outer(eigvecs[:, -1], eigvecs[:, -1].conj())
            correction = K_FB * (rho_pd - target_rho) / (rho_pd + 1e-10)
            correction = min(correction, 1.0)
            new_sm = (1 - correction) * new_sm + correction * pure

        return Observer(d_K=K.d_K, self_model=new_sm, delta_K=K.delta_K, sigma_K=K.sigma_K)

    def regulate_frame(self, F: Frame, K: Observer) -> Frame:
        """Step 4b: Endogenous frame regulation.
        K perturbs F toward consistency with self-model (weak correction)."""
        # Weak endogenous correction: nudge reduced state toward self-model
        reduced = self.partial_trace(F.state)
        diff = K.self_model - reduced
        # Apply correction as a small perturbation to the K-subsystem
        correction_strength = PHI_BAR_SQ * 0.1  # Very weak
        # Construct correction operator on full space
        correction = np.kron(diff, np.eye(self.d_env) / self.d_env)
        new_state = F.state + correction_strength * correction
        # Ensure valid density matrix
        new_state = (new_state + new_state.T.conj()) / 2
        eigvals, eigvecs = np.linalg.eigh(new_state)
        eigvals = np.maximum(eigvals, 0)
        if eigvals.sum() > 0:
            eigvals = eigvals / eigvals.sum()
        else:
            return F  # Don't break the state
        new_state = (eigvecs * eigvals) @ eigvecs.T.conj()
        return Frame(level=F.level, dim_U=F.dim_U, state=new_state, algebra=F.algebra)

    def k6_pass(self, K: Observer, F: Frame, m: int) -> K6Result:
        """Execute one complete K6' pass.

        Returns K6Result with closure status, updated observer and frame.
        """
        # Step 3 (P3): Observe
        U_K = self.observe(K, F)

        # Step 4: Closure check
        residual = np.linalg.norm(K.self_model - U_K.reduced_state, 'fro')
        thresh = threshold_at_pass(m)
        closed = residual < thresh

        # Step 4a: Refine self-model
        K_new = self.refine_self_model(K, U_K)

        # Step 4b: Regulate frame (endogenous)
        F_reg = self.regulate_frame(F, K_new)

        # Steps 1-2: Apply dynamics (P1 + P2 + P3 flow)
        F_new = self.apply_dynamics(F_reg)

        # Step 5: Commitment accounting
        bits = 2 * L if closed else 0

        return K6Result(
            closed=closed,
            residual=residual,
            threshold=thresh,
            observer=K_new,
            frame=F_new,
            accessible=U_K,
            pass_number=m,
            bits_extracted=bits,
            commitment_total=0  # Accumulated by caller
        )

    def run(self, n_passes: int, initial_state: np.ndarray = None,
            initial_rho_pd: float = None) -> List[K6Result]:
        """Run the K6' loop for n_passes iterations.

        Returns list of K6Result for each pass.
        """
        F = self.init_frame(initial_state)
        K = self.init_observer(initial_rho_pd)

        results = []
        total_bits = 0.0

        for m in range(1, n_passes + 1):
            result = self.k6_pass(K, F, m)
            total_bits += result.bits_extracted
            result.commitment_total = total_bits

            results.append(result)

            # Update state for next pass
            K = result.observer
            F = result.frame

        return results


def tower_lift(engine: K6Engine, K: Observer, F: Frame) -> Tuple[K6Engine, Observer, Frame]:
    """Step 6: Tower lift via monoidal functor F: S_n → S_n ⊗ S_n.

    Doubles the system dimension. K6' diagonal map: P3 at level n → P1 at level n+1.
    """
    new_d_K = engine.d_K * 2
    new_d_env = engine.d_env * 2
    new_level = engine.level + 1

    # State lift: ρ_U → ρ_U ⊗ ρ_U (tensor product, then normalize)
    new_state = np.kron(F.state, F.state)
    new_state = new_state / np.trace(new_state)

    # Observer lift: self-model tensored with itself
    new_sm = np.kron(K.self_model, K.self_model)
    new_sm = new_sm / np.trace(new_sm)

    # Create new engine at higher level
    new_engine = K6Engine(
        d_K=new_d_K, d_env=new_d_env,
        eps_p1=engine.eps_p1, eps_p2=engine.eps_p2, eps_p3=engine.eps_p3,
        level=new_level
    )

    new_F = Frame(level=new_level, dim_U=new_d_K * new_d_env, state=new_state)
    new_K = Observer(d_K=new_d_K, self_model=new_sm)

    return new_engine, new_K, new_F
