"""
run_deutsch_jozsa.py
====================
Runs the Deutsch-Jozsa algorithm using your circuit engine to determine 
if a secret blackbox function is Constant or Balanced in a single query!
"""

import qutip as qt
from circuit_engine import apply_instruction, measure_qubit
from deutsch_jozsa import create_dj_oracle

def run_algorithm(num_qubits: int, secret_function_type: str):
    print(f"\nTesting {num_qubits}-Qubit '{secret_function_type.upper()}' Blackbox...")
    
    # Step 1: Initialize all N qubits to |0>
    state = qt.tensor([qt.basis(2, 0)] * num_qubits)
    #ancilla = qt.tensor([qt.basis(2,1)] * num_qubits)
    # Step 2: Apply Hadamard to all qubits (Superposition)
    for q in range(num_qubits):
        state = apply_instruction(state, ['H', [q]])
        
    # Step 3: Apply the Secret Oracle
    # Because our engine usually takes string instructions like ['H', [0]], 
    # and U_f is a massive N-qubit matrix, we just apply it via direct math here!
    U_f = create_dj_oracle(num_qubits, secret_function_type)
    state = U_f * state
    
    # Step 4: Apply Hadamard to all qubits again (Interference)
    for q in range(num_qubits):
        state = apply_instruction(state, ['H', [q]])
        
    # Step 5: Measure all qubits
    measurements = []
    for q in range(num_qubits):
        result, state = measure_qubit(state, target_qubit=q)
        measurements.append(result)
        
    print(f"Measurement Results: {measurements}")
    sum1=sum(measurements)
    # Analyze the result
    if sum(measurements) == 0 :
        print("-> Conclusion: The function is CONSTANT!")
    else:
        print("-> Conclusion: The function is BALANCED!")

if __name__ == "__main__":
    print("=== Running Deutsch-Jozsa Algorithm ===")
    
    # Try it with a Constant function (should measure all 0s)
    run_algorithm(num_qubits=3, secret_function_type="constant_1")
    
    # Try it with a Balanced function (should measure at least one 1)
    run_algorithm(num_qubits=3, secret_function_type="balanced")

    # NEW: Try our new first-qubit balanced function!
    run_algorithm(num_qubits=3, secret_function_type="balanced_first_qubit")