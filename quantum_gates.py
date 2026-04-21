"""
quantum_gates.py
================
Part 1 — Single Qubit Gates (Nielsen & Chuang 4.2)
"""

import numpy as np
import qutip as qt
from qutip_qip.operations import hadamard_transform, phasegate, rx, ry, rz

# ______________________________________________________________________________
# 1.  STANDARD GATES
# ______________________________________________________________________________

# Pauli-X  
X = qt.sigmax()

# Pauli-Y
Y = qt.sigmay()

# Pauli-Z  
Z = qt.sigmaz()

# Hadamard
H = hadamard_transform()

# Phase gate  S = Z^(1/2)
S = phasegate(np.pi / 2)

# π/8 gate  T = Z^(1/4)
T = phasegate(np.pi / 4)

STANDARD_GATES: dict[str, qt.Qobj] = {
    "X": X, "Y": Y, "Z": Z,
    "H": H, "S": S, "T": T,
}

# ______________________________________________________________________________
# 2.  GENERAL ROTATION GATES  (θ-parameterised)
# ______________________________________________________________________________

def Rx(theta: float) -> qt.Qobj:
    """Rotation by *theta* about the x-axis of the Bloch sphere."""
    return rx(theta)


def Ry(theta: float) -> qt.Qobj:
    """Rotation by *theta* about the y-axis of the Bloch sphere."""
    return ry(theta)


def Rz(theta: float) -> qt.Qobj:
    """Rotation by *theta* about the z-axis of the Bloch sphere."""
    return rz(theta)


# ______________________________________________________________________________
# 3.  UTILITIES
# ______________________________________________________________________________

# ______to_check_unitarity___________________________________________________________
def is_unitary(U: qt.Qobj) -> bool:
    return U.isunitary


def apply(gate: qt.Qobj, state: qt.Qobj) -> qt.Qobj:
    return gate * state


# ── Quick self-test ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    for name, G in STANDARD_GATES.items():
        print(f"  {name}: {'Unitary' if is_unitary(G) else 'Not Unitary'}")
        
    for name, fn in [("Rx(π/3)", Rx(np.pi / 3)),
                     ("Ry(π/4)", Ry(np.pi / 4)),
                     ("Rz(π/6)", Rz(np.pi / 6))]:
        print(f"  {name}: {'Unitary' if is_unitary(fn) else 'Not Unitary'}")
        
    print("\nAll gates defined successfully using QuTiP.")