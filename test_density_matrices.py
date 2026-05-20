import qutip as qt
import numpy as np
from circuit_engine import apply_instruction, measure_qubit

def test_density_matrix_evolution():
    print("Testing Density Matrix Evolution...")
    
    # 1. Initialize a 1-qubit density matrix in state |0><0|
    psi_0 = qt.basis(2, 0)
    rho_0 = qt.ket2dm(psi_0)  # Converts ket to density matrix
    
    assert rho_0.isoper, "State should be an operator (density matrix)."
    
    # 2. Apply Pauli-X (Bit Flip)
    # Expected: |1><1|
    rho_1 = apply_instruction(rho_0, ['X', [0]])
    expected_rho_1 = qt.ket2dm(qt.basis(2, 1))
    
    assert np.allclose(rho_1.full(), expected_rho_1.full()), "X gate failed on density matrix."
    print("✓ X gate applied correctly. State evolved from |0><0| to |1><1|.")
    
    # 3. Apply Hadamard
    # Expected: |+><+|
    rho_plus = apply_instruction(rho_0, ['H', [0]])
    psi_plus = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
    expected_rho_plus = qt.ket2dm(psi_plus)
    
    assert np.allclose(rho_plus.full(), expected_rho_plus.full()), "H gate failed on density matrix."
    print("✓ H gate applied correctly. State evolved to superposition density matrix.")

def test_density_matrix_measurement():
    print("\nTesting Density Matrix Measurement...")
    
    # 1. Initialize a superposition state |+><+|
    psi_plus = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
    rho_plus = qt.ket2dm(psi_plus)
    
    # 2. Measure the qubit
    result, collapsed_rho = measure_qubit(rho_plus, target_qubit=0)
    
    # 3. Assertions
    assert result in [0, 1], f"Measurement result {result} is not a valid classical bit."
    assert collapsed_rho.isoper, "Collapsed state lost its density matrix structure."
    
    # Check if the collapse mathematically matches the result
    if result == 0:
        expected_rho = qt.ket2dm(qt.basis(2, 0))
    else:
        expected_rho = qt.ket2dm(qt.basis(2, 1))
        
    assert np.allclose(collapsed_rho.full(), expected_rho.full()), "Density matrix did not collapse correctly."
    print(f"✓ Measurement successful. Result: {result}. State collapsed accurately.")

if __name__ == "__main__":
    test_density_matrix_evolution()
    test_density_matrix_measurement()
    print("\nAll density matrix tests passed successfully!")