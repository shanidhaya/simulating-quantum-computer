"""
benchmark.py
============
Benchmarks quantum circuit execution time comparing Dense vs Sparse matrices.
Increases the number of qubits until execution time hits ~2 minutes (120 seconds).
"""

import time
import numpy as np
import scipy.sparse as sp
import matplotlib.pyplot as plt
import qutip as qt

# Import your generator
from generator import generate_random_circuit

def apply_circuit_dense(circuit_operators, initial_state_vec):
    """
    Applies the circuit using standard Dense NumPy matrix multiplication.
    Warning: This scales very poorly with memory as N increases!
    """
    state = initial_state_vec
    for op in circuit_operators:
        # Convert QuTiP object to dense numpy array and multiply
        gate_dense = op.full()
        state = gate_dense @ state
    return state

def apply_circuit_sparse(circuit_operators, initial_state_sparse):
    """
    Applies the circuit using SciPy Sparse CSR matrix multiplication.
    Extracts the SciPy sparse format directly from QuTiP's internal data.
    """
    state = initial_state_sparse
    for op in circuit_operators:
        # Use .as_scipy() to get the standard SciPy CSR matrix natively
        gate_sparse = op.data.as_scipy() 
        state = gate_sparse @ state
    return state

def run_benchmark():
    num_layers = 1000
    time_limit = 120.0  # 2 minutes
    
    qubit_counts = []
    dense_times = []
    sparse_times = []
    
    num_qubits = 3
    
    print("==================================================")
    print(" Starting Benchmark: 1000 Layers (Sparse vs Dense)")
    print("==================================================")
    
    while True:
        print(f"\nTesting with {num_qubits} qubits...")
        
        # 1. Generate the random circuit
        # NEW
        ops, _, _ = generate_random_circuit(num_qubits, num_layers)
        
        # 2. Prepare initial state |00...0>
        ket0 = qt.basis(2, 0)
        initial_state = qt.tensor([ket0 for _ in range(num_qubits)])
        
        # Prepare Dense and Sparse state representations
        initial_state_dense = initial_state.full()
        initial_state_sparse = sp.csr_matrix(initial_state_dense)
        
        # 3. Benchmark Sparse Multiplication
        start_time = time.perf_counter()
        apply_circuit_sparse(ops, initial_state_sparse)
        sparse_time = time.perf_counter() - start_time
        
        # 4. Benchmark Dense Multiplication (Only if it won't crash memory/take forever)
        # Dense matrices grow as 2^N x 2^N. We stop dense tracking if it gets too slow.
        # NEW
        if len(dense_times) == 0 or (dense_times[-1] is not None and dense_times[-1] < 30.0):
            start_time = time.perf_counter()
            apply_circuit_dense(ops, initial_state_dense)
            dense_time = time.perf_counter() - start_time
        else:
            dense_time = None # Skip dense for very large N to avoid freezing
            
        print(f" -> Sparse Time: {sparse_time:.4f} seconds")
        if dense_time:
            print(f" -> Dense Time:  {dense_time:.4f} seconds")
        else:
            print(f" -> Dense Time:  Skipped (Too slow/Memory limit)")
            
        # Record results
        qubit_counts.append(num_qubits)
        sparse_times.append(sparse_time)
        dense_times.append(dense_time)
        
        # 5. Check break condition (Sparse takes > 2 minutes)
        if sparse_time >= time_limit:
            print(f"\nReached time limit ({sparse_time:.2f}s >= {time_limit}s). Stopping benchmark.")
            break
            
        num_qubits += 1

    # ==========================================
    # Plotting the Results
    # ==========================================
    plt.figure(figsize=(10, 6))
    
    plt.plot(qubit_counts, sparse_times, marker='o', linestyle='-', color='blue', label='SciPy Sparse Matrices')
    
    # Filter out skipped dense times for plotting
    valid_dense_counts = [q for q, t in zip(qubit_counts, dense_times) if t is not None]
    valid_dense_times = [t for t in dense_times if t is not None]
    if valid_dense_times:
        plt.plot(valid_dense_counts, valid_dense_times, marker='s', linestyle='--', color='red', label='Dense NumPy Matrices')
    
    plt.axhline(y=120, color='gray', linestyle=':', label='2 Minute Limit')
    
    plt.title('Quantum Circuit Simulation Benchmark (1000 Layers)')
    plt.xlabel('Number of Qubits (N)')
    plt.ylabel('Execution Time (seconds)')
    plt.yscale('log') # Log scale is best for exponentially growing matrices
    plt.xticks(qubit_counts)
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend()
    
    # Save and show the plot
    plt.savefig('benchmark_results.png')
    print("\nBenchmark complete! Plot saved as 'benchmark_results.png'.")
    plt.show()

if __name__ == "__main__":
    run_benchmark()