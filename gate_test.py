"""
test_quantum_gates.py
=====================
Automated unit tests for quantum gates and state readouts.
"""

import unittest
import numpy as np
import qutip as qt
from quantum_gates import (
    X, CNOT, ISWAP, TOFFOLI, 
    apply, get_state_vector, apply_single_gate
)

class TestQuantumSimulation(unittest.TestCase):

    def setUp(self):
        """Sets up basic basis states used across multiple tests."""
        self.ket0 = qt.basis(2, 0)
        self.ket1 = qt.basis(2, 1)
        self.ket00 = qt.tensor(self.ket0, self.ket0)
        self.ket01 = qt.tensor(self.ket0, self.ket1)
        self.ket10 = qt.tensor(self.ket1, self.ket0)
        self.ket11 = qt.tensor(self.ket1, self.ket1)

    def test_state_vector_readout(self):
        """Test if we can cleanly read out the state vector."""
        vec = get_state_vector(self.ket1)
        np.testing.assert_array_almost_equal(vec, np.array([0.+0.j, 1.+0.j]))

    def test_cnot_gate(self):
        """Test CNOT acting on |10> (Control=0, Target=1) -> |11>"""
        cnot_op = CNOT(N=2, control=0, target=1)
        output_state = apply(cnot_op, self.ket10)
        
        # Verify the output matches |11>
        vec_out = get_state_vector(output_state)
        vec_expected = get_state_vector(self.ket11)
        np.testing.assert_array_almost_equal(vec_out, vec_expected)

    def test_iswap_gate(self):
        """Test ISWAP acting on |01>. Should swap to |10> and add phase i."""
        iswap_op = ISWAP(N=2, targets=[0, 1])
        output_state = apply(iswap_op, self.ket01)
        
        # Expected is i|10>
        expected_state = 1j * self.ket10
        vec_out = get_state_vector(output_state)
        vec_expected = get_state_vector(expected_state)
        np.testing.assert_array_almost_equal(vec_out, vec_expected)

    def test_toffoli_gate(self):
        """Test Toffoli on |110> -> |111>"""
        ket110 = qt.tensor(self.ket1, self.ket1, self.ket0)
        ket111 = qt.tensor(self.ket1, self.ket1, self.ket1)
        
        toffoli_op = TOFFOLI(N=3, controls=[0, 1], target=2)
        output_state = apply(toffoli_op, ket110)
        
        vec_out = get_state_vector(output_state)
        vec_expected = get_state_vector(ket111)
        np.testing.assert_array_almost_equal(vec_out, vec_expected)

if __name__ == "__main__":
    unittest.main(verbosity=2)