"""
test_deutsch_jozsa.py
=====================
Automated unit tests to rigorously verify the Deutsch-Jozsa quantum algorithm.
Checks that Constant oracles return strictly zeros, and Balanced oracles return non-zeros.
"""

import unittest
import qutip as qt
from circuit_engine import apply_instruction, measure_qubit
from deutsch_jozsa import create_dj_oracle

def execute_dj_algorithm(num_qubits: int, oracle_type: str) -> list[int]:
    """
    Executes the Deutsch-Jozsa algorithm and returns the measurement results.
    """
    # 1. Start with |00...0>
    state = qt.tensor([qt.basis(2, 0)] * num_qubits)
    
    # 2. Initial Superposition (Hadamards)
    for q in range(num_qubits):
        state = apply_instruction(state, ['H', [q]])
        
    # 3. Apply the Oracle
    U_f = create_dj_oracle(num_qubits, oracle_type)
    state = U_f * state
    
    # 4. Final Interference (Hadamards)
    for q in range(num_qubits):
        state = apply_instruction(state, ['H', [q]])
        
    # 5. Measure all qubits
    measurements = []
    for q in range(num_qubits):
        result, state = measure_qubit(state, target_qubit=q)
        measurements.append(result)
        
    return measurements


class TestDeutschJozsa(unittest.TestCase):
    
    def setUp(self):
        # We will test using a 3-qubit system
        self.N = 3

    def test_constant_0(self):
        """Constant 0 MUST return exactly [0, 0, 0]."""
        results = execute_dj_algorithm(self.N, "constant_0")
        
        # If the sum of the list is 0, it means every element is 0.
        self.assertEqual(sum(results), 0, f"Expected [0, 0, 0] but got {results}")

    def test_constant_1(self):
        """Constant 1 MUST return exactly [0, 0, 0]."""
        results = execute_dj_algorithm(self.N, "constant_1")
        
        self.assertEqual(sum(results), 0, f"Expected [0, 0, 0] but got {results}")

    def test_balanced_parity(self):
        """Balanced parity MUST return at least one '1' (e.g., [1, 1, 1])."""
        results = execute_dj_algorithm(self.N, "balanced")
        
        # If the sum is greater than 0, there is at least one '1' in the list.
        self.assertGreater(sum(results), 0, f"Expected a non-zero state, but got {results}")

    def test_balanced_first_qubit(self):
        """Balanced first-qubit MUST return at least one '1' (e.g., [1, 0, 0])."""
        results = execute_dj_algorithm(self.N, "balanced_first_qubit")
        
        self.assertGreater(sum(results), 0, f"Expected a non-zero state, but got {results}")


if __name__ == '__main__':
    unittest.main(verbosity=2)