# Simulating a Quantum Computer (F-Praktikum)

A Python-based quantum simulator built using the **QuTiP** (Quantum Toolbox in Python) library. This project implements a scalable quantum circuit engine capable of applying $N$-qubit operations, rendering state visualizations, and evaluating quantum logic via automated testing. 

Built as part of the Physics F-Praktikum course, following theoretical foundations from *Quantum Computation and Quantum Information* (Nielsen & Chuang).

## Features
* **Instruction-Based Circuit Engine:** Build arbitrary quantum circuits using human-readable instructions (e.g., `['H', [0]]`).
* **Automated $N$-Qubit Embedding:** Seamlessly applies 1-qubit and 2-qubit gates to complex $N$-qubit systems using automated tensor product expansions.
* **Random Circuit Generation:** Dynamically construct arbitrary $N$-qubit quantum circuits of a specified depth, mixing single-qubit and multi-qubit layers.
* **ASCII Circuit Visualization:** Automatically parse circuit instructions and draw intuitive terminal-based wire diagrams showing gates, controls, and targets.
* **Performance Benchmarking:** Automated stress-testing to evaluate computational scaling and execution time across different numbers of qubits.
* **Sparse Matrix Optimization:** Extracts native QuTiP sparse data to SciPy CSR (`scipy.sparse`), drastically outperforming standard Dense (NumPy) matrices by bypassing exponential memory bottlenecks.
* **State Visualization:** Renders 3D Bloch spheres for single-qubit states and tracks multi-qubit system evolution.
* **Automated Unit Testing & Validation:** Robust testing framework (`unittest`) and programmatic "silent asserts" to mathematically prove matrix unitarity and shape validity at every circuit layer.

## Project Structure
* `quantum_gates.py`: Definitions for standard Pauli gates, rotation gates, and $N$-qubit controlled gates (CNOT, ISWAP, Toffoli). Contains the main `GATE_DICTIONARY`.
* `circuit_engine.py`: Core logic for parsing instruction lists, auto-expanding matrices to the proper $N$-qubit dimensions, and executing them.
* `generator.py`: Circuit factory script that builds scalable, randomized multi-qubit circuits and extracts raw functional instructions.
* `visualize.py`: Reads raw instructions and draws an ASCII representation of the quantum circuit directly in the terminal.
* `benchmark.py`: Stress-testing script comparing execution times of Dense vs. Sparse matrix operations, featuring safety limits, auto-scaling $N$, and logarithmic Matplotlib plotting.
* `testing_playground.ipynb` (and `circuit_testing.ipynb`): Jupyter Notebook sandboxes for interactive circuit development, visualization, and layer-by-layer mathematical checks.
* `bloch_sphere.py`: Visualization module using Matplotlib to render QuTiP Bloch spheres.
* `gate_test.py`: The `unittest` suite for validating quantum gate outputs against expected vectors.
* `simulate.py` / `bell_state.py`: Execution scripts for specific fundamental state preparations (e.g., single qubit sweeps, Bell state entanglement).
* `requirements.txt`: Frozen dependencies for reproducing the environment.

## Status: Ongoing

**Recent Milestones (This Week):**
* [x] **Arbitrary Embedding:** Upgraded the circuit engine to dynamically embed one- and two-qubit gates into arbitrary $N$-qubit systems.
* [x] **Random Circuit Generation:** Built a generator to construct N-qubit circuits with a fixed number of layers, randomly selecting target/control qubits and gate types.
* [x] **Sparse Matrix Integration:** Refactored matrix multiplication to natively utilize SciPy CSR sparse matrices, successfully resolving the exponential memory bottleneck of dense matrices.
* [x] **Performance Benchmarking:** Created a stress-test loop executing 1000-layer circuits, comparing Dense vs. Sparse execution times, and generating logarithmic performance plots up to a 2-minute compute limit.
* [x] **ASCII Visualization & Asserts:** Added terminal-based circuit wire diagrams and silent mathematical asserts to verify matrix shape and unitarity at scale.