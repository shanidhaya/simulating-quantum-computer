"""
noise_channels.py
=================
Implements quantum noise channels from Nielsen & Chuang Chapter 8.3.
"""
import numpy as np
import qutip as qt
from qutip_qip.operations import expand_operator


def apply_kraus(rho: qt.Qobj, kraus_ops: list, target: int, N: int) -> qt.Qobj:
    """Helper function to apply 1-qubit Kraus operators to an N-qubit system."""
    rho_new = qt.Qobj(np.zeros(rho.shape), dims=rho.dims)
    for E in kraus_ops:
        # Expand the 1-qubit Kraus operator to the full N-qubit Hilbert space
        E_expanded = expand_operator(E, dims=[2]*N, targets=[target])
        rho_new += E_expanded * rho * E_expanded.dag()
    return rho_new


def bitflip_channel(rho: qt.Qobj, p: float, target: int) -> qt.Qobj:
    """N&C 8.3.3: Bit flip channel with probability p."""
    N = len(rho.dims[0])
    E0 = np.sqrt(1 - p) * qt.qeye(2)
    E1 = np.sqrt(p) * qt.sigmax()
    return apply_kraus(rho, [E0, E1], target, N)


def phaseflip_channel(rho: qt.Qobj, p: float, target: int) -> qt.Qobj:
    """N&C 8.3.3: Phase flip channel with probability p."""
    N = len(rho.dims[0])
    E0 = np.sqrt(1 - p) * qt.qeye(2)
    E1 = np.sqrt(p) * qt.sigmaz()
    return apply_kraus(rho, [E0, E1], target, N)


def amplitude_damping_channel(rho: qt.Qobj, gamma: float, target: int) -> qt.Qobj:
    """N&C 8.3.5: Amplitude damping channel with damping probability gamma."""
    N = len(rho.dims[0])
    E0 = qt.Qobj([[1, 0], [0, np.sqrt(1 - gamma)]])
    E1 = qt.Qobj([[0, np.sqrt(gamma)], [0, 0]])
    return apply_kraus(rho, [E0, E1], target, N)


def depolarizing_channel(rho: qt.Qobj, p: float) -> qt.Qobj:
    """
    N&C 8.3.4 (Eq 8.100): N-qubit Depolarizing channel.
    Replaces the state with the maximally mixed state I/d with probability p.
    Does NOT use Kraus operators, generalizing easily to N qubits!
    """
    # d is the dimension of the entire Hilbert space (e.g., 2^N)
    d = rho.shape[0]
    I = qt.qeye(rho.dims[0])  # N-qubit Identity matrix

    # Eq 8.100: E(rho) = (1-p) * rho + p * (I / d)
    return (1 - p) * rho + p * (I / d)
