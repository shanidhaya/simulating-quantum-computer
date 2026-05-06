"""
quantum_gates.py
================
Part 1 — Single Qubit Gates (Nielsen & Chuang 4.2)
"""

import numpy as np
import qutip as qt
from qutip_qip.operations import hadamard_transform, phasegate, rx, ry, rz,cnot, iswap,toffoli,expand_operator

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
#   Multi qubit gates
# ______________________________________________________________________________

def CNOT(N: int = 2, control: int = 0, target: int = 1) -> qt.Qobj:
    
    return cnot(N, control, target)

def ISWAP(N: int = 2, targets: list[int] = [0, 1]) -> qt.Qobj:
    
    return iswap(N, targets)

def TOFFOLI(N: int = 3, controls: list[int] = [0, 1], target: int = 2) -> qt.Qobj:
    
    return toffoli(N, controls, target)
# ______________________________________________________________________________
# 3.  UTILITIES
# ______________________________________________________________________________

# ______to_check_unitarity___________________________________________________________
def is_unitary(U: qt.Qobj) -> bool:
    return U.isunitary


def apply(gate: qt.Qobj, state: qt.Qobj) -> qt.Qobj:
    return gate * state

def apply_single_gate(gate: qt.Qobj, N: int, target: int) -> qt.Qobj:
    """Expands a 1-qubit gate to an N-qubit system and returns the operator."""
    return expand_operator(gate, N=N, targets=[target])

def get_state_vector(state: qt.Qobj) -> np.ndarray:
    """Reads out the state vector as a standard 1D numpy array."""
    return state.full().flatten()



# This dictionary maps a string instruction to the raw QuTiP gate matrix.
# The Circuit Engine will use this to look up gates automatically.
GATE_DICTIONARY = {
    'X': X,
    'Y': Y,
    'Z': Z,
    'H': H,
    'S': S,
    'T': T,
    'CNOT': cnot(),       
    'ISWAP': iswap(),     
    'TOFFOLI': toffoli()  
}
# ── Quick self-test ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Gates done")