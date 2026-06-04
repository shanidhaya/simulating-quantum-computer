"""
run_noise_demo.py
=================
Demonstrates how quantum noise channels from Nielsen & Chuang 
degrade a pure quantum state into a mixed state.
"""

import qutip as qt
import numpy as np

# Import your noise channels
from noise_channels import bitflip_channel, amplitude_damping_channel, depolarizing_channel


def analyze_state(name: str, rho: qt.Qobj):
    """Helper function to print state metrics."""
    purity = (rho * rho).tr().real

    # Calculate Bloch sphere coordinates (Expectation values of Pauli matrices)
    x = qt.expect(qt.sigmax(), rho)
    y = qt.expect(qt.sigmay(), rho)
    z = qt.expect(qt.sigmaz(), rho)

    print(f"--- {name} ---")
    print(f"Purity: {purity:.4f} " +
          ("(Pure)" if purity > 0.99 else "(Mixed)"))
    print(f"Bloch Coords: X={x:.3f}, Y={y:.3f}, Z={z:.3f}\n")


if __name__ == "__main__":
    print("=== Quantum Noise Channel Demonstration ===\n")

    # 1. Create a Pure State |+> (Points exactly at X=1 on the equator)
    # We must use density matrices for noise, so we do |+><+|
    psi_plus = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
    rho_initial = psi_plus * psi_plus.dag()

    analyze_state("Initial Pure State |+>", rho_initial)

    # 2. Apply a 30% Bitflip Error
    rho_bitflip = bitflip_channel(rho_initial, p=0.3, target=0)
    analyze_state("After 30% Bitflip Noise", rho_bitflip)

    # 3. Apply 40% Amplitude Damping (Losing energy to the environment)
    rho_damped = amplitude_damping_channel(rho_initial, gamma=0.4, target=0)
    analyze_state("After 40% Amplitude Damping", rho_damped)

    # 4. Apply 50% Depolarizing Noise (Complete hardware scrambling)
    rho_depol = depolarizing_channel(rho_initial, p=0.5)
    analyze_state("After 50% Depolarizing Noise", rho_depol)
