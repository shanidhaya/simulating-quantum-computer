import numpy as np
import qutip as qt
from circuit_engine import apply_instruction
from deutsch_jozsa import create_dj_oracle

def run_noisy_dj(num_qubits: int, oracle_type: str, noise_channel=None, noise_prob=0.0, noise_loc="after"):
    """
    Executes the DJ algorithm using Density Matrices, injecting noise 
    either 'before' or 'after' the Oracle. Returns the Accuracy Rate.
    """
    # 1. Initialize as a Density Matrix: |0...0><0...0|
    ket0 = qt.tensor([qt.basis(2, 0)] * num_qubits)
    rho = ket0 * ket0.dag()
    
    # 2. Initial Superposition
    for q in range(num_qubits):
        rho = apply_instruction(rho, ['H', [q]])
        
    # --- NOISE INJECTION (BEFORE ORACLE) ---
    if noise_channel and noise_loc == "before":
        for q in range(num_qubits):
            rho = noise_channel(rho, noise_prob, target=q)
            
    # 3. The Oracle (Density Matrix Evolution: U * rho * U_dag)
    U_f = create_dj_oracle(num_qubits, oracle_type)
    rho = U_f * rho * U_f.dag()
    
    # --- NOISE INJECTION (AFTER ORACLE) ---
    if noise_channel and noise_loc == "after":
        for q in range(num_qubits):
            rho = noise_channel(rho, noise_prob, target=q)
            
    # 4. Final Interference
    for q in range(num_qubits):
        rho = apply_instruction(rho, ['H', [q]])
        
    # 5. Calculate Accuracy (No need to simulate random measurements!)
    # The probability of measuring |00...0> is literally the first 
    # diagonal element of our final density matrix.
    prob_000 = rho.diag()[0].real
    
    if "constant" in oracle_type:
        # A constant function SHOULD return |00...0>. 
        return prob_000
    else:
        # A balanced function SHOULD return anything EXCEPT |00...0>.
        return 1.0 - prob_000