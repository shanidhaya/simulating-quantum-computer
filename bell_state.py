"""
simulate_bell_state.py
======================
Simulates a two-qubit circuit generating the Bell state:
(|00> + |11>) / sqrt(2) from the |00> initial state.
"""

import numpy as np
import qutip as qt
from quantum_gates import (
    H, CNOT, apply, get_state_vector, apply_single_gate
)

def main():
    print("=" * 55)
    print("  Two-Qubit Circuit: Bell State Generation")
    print("=" * 55)

    # 1. Initialize |00>
    ket0 = qt.basis(2, 0)
    psi_init = qt.tensor(ket0, ket0)
    print(f"1. Input state |00> vector: \n   {get_state_vector(psi_init)}\n")

    # 2. Apply Hadamard to Qubit 0
    # Because we are in a 2-qubit system, H must be expanded to H ⊗ I
    H_expanded = apply_single_gate(H, N=2, target=0)
    psi_step1 = apply(H_expanded, psi_init)
    
    # At this point, state is (|00> + |10>) / sqrt(2)
    print(f"2. After H on Qubit 0 (State is (|00> + |10>) / sqrt(2)): \n   {np.round(get_state_vector(psi_step1), 3)}\n")

    # 3. Apply CNOT (Control=0, Target=1)
    cnot_gate = CNOT(N=2, control=0, target=1)
    psi_final = apply(cnot_gate, psi_step1)

    # 4. Read out the final state vector
    final_vec = get_state_vector(psi_final)
    print("3. Final state after CNOT (Bell State |Φ+>):")
    print(f"   {np.round(final_vec, 3)}\n")

    # Verification: check amplitude of |00> and |11>
    amp_00 = final_vec[0] # index 0 corresponds to |00>
    amp_11 = final_vec[3] # index 3 corresponds to |11>
    
    expected_amp = 1 / np.sqrt(2)
    print(f"Amplitude of |00>: {amp_00:.4f}  (Expected: {expected_amp:.4f})")
    print(f"Amplitude of |11>: {amp_11:.4f}  (Expected: {expected_amp:.4f})")

if __name__ == "__main__":
    main()