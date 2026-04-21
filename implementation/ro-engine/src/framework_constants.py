"""
Framework constants and generators.
All values derived from f'' = f on {0,1}. Zero free parameters.
"""
import numpy as np

# === FUNDAMENTAL CONSTANTS ===
PHI = (1 + np.sqrt(5)) / 2          # φ ≈ 1.618 — golden ratio, eigenvalue of R
PHI_BAR = PHI - 1                    # φ̄ ≈ 0.618 — Möbius attractor
PHI_BAR_SQ = PHI_BAR ** 2           # φ̄² ≈ 0.382 — contraction rate per pass
L = np.log2(PHI)                     # L ≈ 0.694 — information constant
DISC_R = 5                           # disc(R) — resolution quantum
ALPHA_S = PHI_BAR**3 / 2            # α_S ≈ 0.118 — strong coupling = regulation width

# === REGULATION INTERVAL ===
RHO_MIN = PHI_BAR_SQ                 # Lower bound of admissible interval
RHO_MAX = 0.5                        # Upper bound (poised symmetry)
RHO_MID = (RHO_MIN + RHO_MAX) / 2   # Midpoint ≈ 0.441

# === FEEDBACK GAIN (RES-4) ===
K_FB = PHI_BAR                       # Gain forced by 1 - φ̄² = φ̄

# === GENERATORS (2×2) ===
R = np.array([[0, 1], [1, 1]], dtype=np.float64)   # Production generator
N = np.array([[0, -1], [1, 0]], dtype=np.float64)  # Observation generator
h = np.array([[1, 0], [0, -1]], dtype=np.float64)  # Cartan element (P2)
J = np.array([[0, 1], [1, 0]], dtype=np.float64)   # Distinction (swap)
I2 = np.eye(2, dtype=np.float64)                    # Identity

# === DERIVED ===
exp_h = np.diag([np.e, 1/np.e])     # exp(h) = diag(e, e⁻¹)

# === VERIFICATION ===
assert np.allclose(R @ R, R + I2), "R² ≠ R + I"
assert np.allclose(N @ N, -I2), "N² ≠ -I"
assert np.allclose(J @ J, I2), "J² ≠ I"
assert np.allclose(h @ N + N @ h, np.zeros((2,2))), "{h,N} ≠ 0 (Axiom AA fails)"
assert abs(PHI_BAR_SQ + PHI_BAR - 1.0) < 1e-15, "φ̄² + φ̄ ≠ 1 (Fibonacci identity)"
assert abs(np.linalg.norm(R, 'fro')**2 - 3) < 1e-15, "‖R‖² ≠ 3"
assert abs(np.linalg.norm(N, 'fro')**2 - 2) < 1e-15, "‖N‖² ≠ 2"


def threshold_at_pass(m):
    """K6' closure threshold at pass m: φ̄^{2m}"""
    return PHI_BAR_SQ ** m


def bits_per_pass():
    """Information extracted per K6' pass: 2L bits"""
    return 2 * L


def purity_to_rho(rho_matrix, d_K):
    """Convert density matrix purity to Phase-Dist ρ parameter.
    ρ = 1 - tr(ρ²) for normalized states. At d_K=2: ρ ∈ [0, 0.5]."""
    purity = np.real(np.trace(rho_matrix @ rho_matrix))
    return (1 - purity) / (1 - 1/d_K) * (1 - 1/d_K)  # Normalized


def purity_to_rho_simple(rho_matrix):
    """Simple Phase-Dist: ρ = (1 - |r⃗|²)/2 for d_K=2 Bloch ball.
    Pure state: ρ=0. Maximally mixed: ρ=0.5."""
    purity = np.real(np.trace(rho_matrix @ rho_matrix))
    # For d_K=2: purity = (1+|r|²)/2, so |r|² = 2*purity - 1
    # ρ = (1-|r|²)/2 = (1-(2*purity-1))/2 = (2-2*purity)/2 = 1-purity
    return 1 - purity


def in_regulation_interval(rho_pd):
    """Check if ρ_PD is in the forced regulation interval [φ̄², 1/2]."""
    return RHO_MIN <= rho_pd <= RHO_MAX


def cross_channel_content(M):
    """CC(M) = |disc(M)| / (|disc(M)| + tr(M)²) for 2×2 matrices.
    CC(R) = 5/6. CC(N) = 1. CC(I) = 0."""
    tr = np.trace(M)
    det = np.linalg.det(M)
    disc = tr**2 - 4*det
    denom = abs(disc) + tr**2
    if denom < 1e-15:
        return 0.0
    return abs(disc) / denom
