"""
test_circuit_states.py
======================
Unit tests to verify that the quantum circuit engine and random 
generator correctly produce valid mathematical mixed states.
"""

import unittest
import qutip as qt
from generator import generate_random_circuit

class TestCircuitRandomStates(unittest.TestCase):
    
    def setUp(self):
        """Generates a random mixed state using the Circuit method before each test."""
        num_system = 1
        num_env = 1
        total_qubits = num_system + num_env
        
        # 1. Start in |00>
        state = qt.tensor([qt.basis(2, 0)] * total_qubits)
        
        # 2. Scramble with a deep random circuit (50 layers)
        ops, _, _ = generate_random_circuit(total_qubits, num_layers=50)
        for op in ops:
            state = op * state
            
        # 3. Trace out the environment to get the System's density matrix
        self.rho = state.ptrace(list(range(num_system)))

    def test_is_density_matrix(self):
        """Checks if QuTiP recognizes the object as an operator (matrix)."""
        self.assertTrue(self.rho.isoper, "State should be a density matrix operator.")
        self.assertEqual(self.rho.shape, (2, 2), "A 1-qubit density matrix must be 2x2.")

    def test_trace_is_one(self):
        """Checks the conservation of probability: Tr(rho) == 1."""
        trace_val = self.rho.tr().real
        self.assertAlmostEqual(trace_val, 1.0, places=5, msg="Trace must equal exactly 1.0")

    def test_is_hermitian(self):
        """Checks if the density matrix is Hermitian: rho == rho^dag."""
        # We calculate the distance between rho and its dagger
        diff = (self.rho - self.rho.dag()).norm()
        self.assertAlmostEqual(diff, 0.0, places=5, msg="Matrix is not Hermitian!")

    def test_eigenvalues_are_positive(self):
        """Checks if all eigenvalues are >= 0 (no negative probabilities)."""
        eigenvalues = self.rho.eigenenergies()
        for eig in eigenvalues:
            self.assertGreaterEqual(eig.real, -1e-10, "Found a negative eigenvalue!")

    def test_purity_is_mixed(self):
        """
        Checks if the state is physically mixed.
        Purity = Tr(rho^2). For 1 qubit, it must be between 0.5 (mixed) and 1.0 (pure).
        Since we traced out a scrambled environment, it should be strictly < 1.0.
        """
        purity = (self.rho * self.rho).tr().real
        
        # Must be physically valid bounds
        self.assertGreaterEqual(purity, 0.4999)
        self.assertLessEqual(purity, 1.0001)
        
        # Verify it actually mixed with the environment (not perfectly pure)
        self.assertLess(purity, 0.999, "State did not entangle with the environment!")

if __name__ == '__main__':
    unittest.main(verbosity=2)