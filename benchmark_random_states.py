"""
benchmark_random_states.py
==========================
Benchmarks the physical circuit simulation method vs the mathematical 
NumPy method for generating Hilbert-Schmidt random mixed states.
"""

import time
import numpy as np
import matplotlib.pyplot as plt
import qutip as qt

# Import from your upgraded modules
from generator import generate_random_circuit
from random_states import hilbert_schmidt_random_state

def generate_hs_circuit(num_qubits: int, num_layers: int = 50) -> qt.Qobj:
    """
    Method A: The Physics Way
    Simulates an Environment, scrambles it with the System, and traces it out.
    """
    total_qubits = num_qubits * 2
    state = qt.tensor([qt.basis(2, 0)] * total_qubits)
    
    ops, _, _ = generate_random_circuit(total_qubits, num_layers)
    for op in ops:
        state = op * state
        
    system_indices = list(range(num_qubits))
    return state.ptrace(system_indices)

def generate_hs_math(num_qubits: int) -> qt.Qobj:
    """
    Method B: The Math Way
    Uses Ginibre matrices based on arXiv:1010.3570.
    """
    dim = 2 ** num_qubits
    return hilbert_schmidt_random_state(dim)

def run_benchmark():
    qubit_counts = [1, 2, 3, 4]  
    num_layers = 50
    
    circuit_times = []
    math_times = []
    
    print(f"{'System Qubits':<15} | {'Circuit Time (s)':<20} | {'Math Time (s)':<15}")
    print("-" * 55)
    
    for q in qubit_counts:
        # --- 1. Benchmark Circuit Method ---
        # FIXED: Using high-resolution performance counter
        start = time.perf_counter()
        generate_hs_circuit(q, num_layers)
        t_circ = time.perf_counter() - start
        circuit_times.append(t_circ)
        
        # --- 2. Benchmark Math Method ---
        start = time.perf_counter()
        generate_hs_math(q)
        t_math = time.perf_counter() - start
        
        # FIXED: Ensure time is never exactly 0.0 to prevent Log-Scale crashes
        t_math = max(t_math, 1e-7) 
        math_times.append(t_math)
        
        print(f"{q:<15} | {t_circ:<20.4f} | {t_math:<15.6f}")

    # ==========================================
    # Plotting the Results
    # ==========================================
    plt.figure(figsize=(10, 6))
    
    plt.plot(qubit_counts, circuit_times, marker='o', linestyle='-', color='#d62728', label='Circuit Method (Physics)')
    plt.plot(qubit_counts, math_times, marker='s', linestyle='-', color='#1f77b4', label='Math Method (NumPy)')
    
    plt.title('Performance: Quantum Circuits vs. Mathematical Formalism', fontsize=14)
    plt.xlabel('Number of System Qubits (N)', fontsize=12)
    plt.ylabel('Execution Time (seconds) - Log Scale', fontsize=12)
    
    plt.yscale('log')
    plt.xticks(qubit_counts)
    
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(fontsize=12)
    plt.tight_layout()
    
    print("\nBenchmark complete! Rendering plot...")
    plt.show()

if __name__ == "__main__":
    run_benchmark()