"""
run_deutsch_jozsa.py
====================
A generalized execution engine for the Deutsch-Jozsa algorithm.
Handles both hardcoded string oracles AND dynamic Python functions.
"""

import qutip as qt
from circuit_engine import apply_instruction, measure_qubit
from deutsch_jozsa import create_dj_oracle, create_dynamic_oracle

def run_algorithm(num_qubits: int, secret_function):
    func_name = secret_function.__name__ if callable(secret_function) else secret_function
    print(f"Running {num_qubits}-Qubit DJ Algorithm on '{func_name}'...")
    
    # Step 1: Initialize |00...0>
    state = qt.tensor([qt.basis(2, 0)] * num_qubits)
    
    # Step 2: Superposition
    for q in range(num_qubits):
        state = apply_instruction(state, ['H', [q]])
        
    # Step 3: Apply the Oracle (The Smart Routing Logic)
    if callable(secret_function):
        U_f = create_dynamic_oracle(num_qubits, secret_function)
    elif isinstance(secret_function, str):
        U_f = create_dj_oracle(num_qubits, secret_function)
    else:
        raise ValueError("Input must be a string or a python function!")
        
    state = U_f * state
    
    # Step 4: Interference
    for q in range(num_qubits):
        state = apply_instruction(state, ['H', [q]])
        
    # Step 5: Measure
    measurements = []
    for q in range(num_qubits):
        result, state = measure_qubit(state, target_qubit=q)
        measurements.append(result)
        
    # Analyze
    if sum(measurements) == 0:
        print(f"-> Result: CONSTANT (Measured {measurements})")
    else:
        print(f"-> Result: BALANCED (Measured {measurements})")
        
    return state