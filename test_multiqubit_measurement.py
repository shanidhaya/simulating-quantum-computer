import qutip as qt
import numpy as np
from circuit_engine import measure_qubit

def test_bell_state_entanglement():
    print("Testing 2-Qubit Bell State Measurement...")
    
    psi_00 = qt.tensor(qt.basis(2, 0), qt.basis(2, 0))
    psi_11 = qt.tensor(qt.basis(2, 1), qt.basis(2, 1))
    bell_state = (psi_00 + psi_11).unit()
    
    result, collapsed_state = measure_qubit(bell_state, target_qubit=0)
    
    assert result in [0, 1], f"Measurement result {result} is invalid."
    assert len(collapsed_state.dims[0]) == 2, "State dimensions changed! Should still be 2 qubits."
    
    if result == 0:
        expected_state = psi_00
    else:
        expected_state = psi_11
        
    fidelity = qt.fidelity(collapsed_state, expected_state)
    assert np.isclose(fidelity, 1.0), "Entangled qubit did not collapse correctly!"
    
    print(f"✓ Bell state test passed. Qubit 0 measured as {result}. Entire state collapsed to |{result}{result}>.")

def test_independent_qubit_isolation():
    print("\nTesting 3-Qubit Independent Measurement...")
    
    q0 = qt.basis(2, 0)
    q1_plus = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
    q2 = qt.basis(2, 1)
    
    psi_init = qt.tensor(q0, q1_plus, q2)
    
    result, collapsed_state = measure_qubit(psi_init, target_qubit=1)
    
    assert result in [0, 1], f"Measurement result {result} is invalid."
    assert len(collapsed_state.dims[0]) == 3, "State dimensions changed! Should still be 3 qubits."
    
    if result == 0:
        expected_state = qt.tensor(q0, qt.basis(2, 0), q2)
    else:
        expected_state = qt.tensor(q0, qt.basis(2, 1), q2)
        
    fidelity = qt.fidelity(collapsed_state, expected_state)
    assert np.isclose(fidelity, 1.0), "Measurement improperly affected adjacent unentangled qubits!"
    
    print(f"✓ 3-Qubit isolation test passed. Qubit 1 collapsed to {result}, adjacent qubits remained intact.")

def test_4qubit_ghz_state():
    print("\nTesting 4-Qubit GHZ State Measurement...")
    
    # 1. Manually construct the 4-qubit GHZ state: (|0000> + |1111>) / sqrt(2)
    q0 = qt.basis(2, 0)
    q1 = qt.basis(2, 1)
    
    psi_0000 = qt.tensor(q0, q0, q0, q0)
    psi_1111 = qt.tensor(q1, q1, q1, q1)
    ghz_state = (psi_0000 + psi_1111).unit()
    
    # 2. Measure Qubit 2 (the third qubit)
    result, collapsed_state = measure_qubit(ghz_state, target_qubit=2)
    
    # 3. Assertions
    assert result in [0, 1], f"Measurement result {result} is invalid."
    assert len(collapsed_state.dims[0]) == 4, "State dimensions changed! Should still be 4 qubits."
    
    # Because it is a maximally entangled GHZ state, measuring Qubit 2 
    # dictates the state of Qubits 0, 1, and 3 instantly.
    if result == 0:
        expected_state = psi_0000
    else:
        expected_state = psi_1111
        
    fidelity = qt.fidelity(collapsed_state, expected_state)
    assert np.isclose(fidelity, 1.0), "4-Qubit GHZ state did not collapse correctly!"
    
    print(f"✓ 4-Qubit GHZ test passed. Qubit 2 measured as {result}. Entire state instantly collapsed to |{result}{result}{result}{result}>.")

if __name__ == "__main__":
    test_bell_state_entanglement()
    test_independent_qubit_isolation()
    test_4qubit_ghz_state()
    print("\nAll multi-qubit measurement tests passed successfully!")