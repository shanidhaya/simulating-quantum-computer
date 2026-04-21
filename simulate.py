"""
simulate.py
===========
Starting state : |1> (south pole of the Bloch sphere)
Applies every standard gate plus R_x, R_y, R_z (each at θ = π/2)
and produces three figures using custom modules.
"""

import numpy as np
import qutip as qt
from quantum_gates import (
    X, Y, Z, H, S, T,
    Rx, Ry, Rz,
    apply, STANDARD_GATES, is_unitary,
)
from bloch_sphere import (
    plot_bloch_panels, 
    plot_all_states_single_sphere, 
    get_bloch_coords
)

# ___1.Initial state |1>___________________________________________________
ket1 = qt.basis(2, 1)   # south pole: Bloch vector (0, 0, −1)

print("=" * 55)
print("  Quantum Gate Simulation  (Nielsen & Chuang 4.2)")
print("=" * 55)

bx, by, bz = get_bloch_coords(ket1)
print(f"\nInitial state |1>  →  Bloch vector: ({bx:.3f}, {by:.3f}, {bz:.3f})\n")
print(f"{'Gate':<14}  {'α (|0> amp)':<20}  {'β (|1> amp)':<20}  Bloch (x, y, z)")
print("-" * 80)

# ── 2.  Apply every gate and record results ───────────────────────────────────
THETA = np.pi / 2                   # angle used for rotation gates

gate_specs = [
    ("X  (Pauli-X)",    X,             "#e74c3c"),
    ("Y  (Pauli-Y)",    Y,             "#9b59b6"),
    ("Z  (Pauli-Z)",    Z,             "#2980b9"),
    ("H  (Hadamard)",   H,             "#27ae60"),
    ("S  (Phase)",      S,             "#f39c12"),
    ("T  (π/8)",        T,             "#16a085"),
    ("Rx(π/2)",         Rx(THETA),     "#c0392b"),
    ("Ry(π/2)",         Ry(THETA),     "#8e44ad"),
    ("Rz(π/2)",         Rz(THETA),     "#1abc9c"),
]

entries = []
for label, gate, color in gate_specs:
    out = apply(gate, ket1)
    
    alpha = out.full()[0, 0]
    beta = out.full()[1, 0]
    bx, by, bz = get_bloch_coords(out)
    
    alpha_str = f"{alpha.real:+.3f}{alpha.imag:+.3f}j"
    beta_str = f"{beta.real:+.3f}{beta.imag:+.3f}j"
    
    print(f"{label:<14}  {alpha_str:<20}  {beta_str:<20}  ({bx:+.3f}, {by:+.3f}, {bz:+.3f})")
    entries.append((label, out, color))

# ── 3.  Unitarity verification ────────────────────────────────────────────────
print("\n--- Unitarity check ---")
for label, gate, _ in gate_specs:
    mark = "True" if is_unitary(gate) else "False"
    print(f"  {label:<14} {mark}")

# ── 4.  Render Figures ────────────────────────────────────────────────────────
print("\nRendering figures …")

std_entries  = [e for e in entries if e[0] in 
                {"X  (Pauli-X)", "Y  (Pauli-Y)", "Z  (Pauli-Z)",
                 "H  (Hadamard)", "S  (Phase)", "T  (π/8)"}]
rot_entries  = [e for e in entries if "R" in e[0]]

# Call functions from bloch_sphere.py
fig_std = plot_bloch_panels(
    std_entries, ncols=3,
    suptitle="Standard Single-Qubit Gates acting on |1⟩",
    filename="bloch_standard_gates.png",
)

fig_rot = plot_bloch_panels(
    rot_entries, ncols=3,
    suptitle=r"Rotation Gates $R_x, R_y, R_z\,(\theta=\pi/2)$ acting on |1⟩",
    filename="bloch_rotation_gates.png",
)

fig_all = plot_all_states_single_sphere(
    entries, initial_state=ket1, 
    filename="bloch_all_gates.png"
)

print("\nDone. Three figures produced.")