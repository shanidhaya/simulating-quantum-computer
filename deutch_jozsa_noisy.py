import numpy as np
import qutip as qt
from circuit_engine import apply_instruction
from deutsch_jozsa import create_dj_oracle, create_dynamic_oracle

def apply_noise(rho, channels, p, num_qubits):
    """Helper function to apply either a single channel or a list of channels."""
    if not channels or p == 0.0:
        return rho
    
    # If a single channel was passed, wrap it in a list so we can loop through it
    if not isinstance(channels, list):
        channels = [channels]
        
    for channel in channels:
        if channel.__name__ == 'depolarizing_channel':
            # Depolarizing acts globally on the entire state
            rho = channel(rho, p=p)
        else:
            # Bitflip, Phaseflip, etc. act locally on each qubit
            for q in range(num_qubits):
                rho = channel(rho, p, target=q)
    return rho

def run_noisy_dj(num_qubits: int, secret_function, noise_channel=None, noise_prob=0.0, noise_loc="post_oracle"):
    """
    Executes the DJ algorithm using Density Matrices.
    noise_loc options: 'pre_H1', 'post_H1', 'post_oracle', 'post_H2'
    """
    # 1. Initialize
    ket0 = qt.tensor([qt.basis(2, 0)] * num_qubits)
    rho = ket0 * ket0.dag()
    
    # --- NOISE: PRE-H1 ---
    if noise_loc == "pre_H1":
        rho = apply_noise(rho, noise_channel, noise_prob, num_qubits)
        
    # 2. First Superposition
    for q in range(num_qubits):
        rho = apply_instruction(rho, ['H', [q]])
        
    # --- NOISE: POST-H1 ---
    if noise_loc == "post_H1":
        rho = apply_noise(rho, noise_channel, noise_prob, num_qubits)
            
    # 3. The Oracle (Hybrid Logic)
    if callable(secret_function):
        U_f = create_dynamic_oracle(num_qubits, secret_function)
    else:
        U_f = create_dj_oracle(num_qubits, secret_function)
        
    rho = U_f * rho * U_f.dag()
    
    # --- NOISE: POST-ORACLE ---
    if noise_loc == "post_oracle":
        rho = apply_noise(rho, noise_channel, noise_prob, num_qubits)
            
    # 4. Final Interference
    for q in range(num_qubits):
        rho = apply_instruction(rho, ['H', [q]])
        
    # --- NOISE: POST-H2 ---
    if noise_loc == "post_H2":
        rho = apply_noise(rho, noise_channel, noise_prob, num_qubits)
        
    # 5. Calculate Accuracy
    prob_000 = rho.diag()[0].real
    
    # Check if we are testing a constant or balanced function to determine accuracy
    is_constant = False
    if isinstance(secret_function, str) and "constant" in secret_function:
        is_constant = True
    elif callable(secret_function):
        # We assume for this benchmark that the user tracks which type it is,
        # but defaulting to measuring the constant probability is safest for benchmarking
        # Let's return the raw probability of |000> for benchmarking graphs
        return prob_000
    
    if is_constant:
        return prob_000
    else:
        return 1.0 - prob_000