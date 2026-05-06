# Simulating a Quantum Computer (F-Praktikum)

A Python-based quantum simulator built using the **QuTiP** (Quantum Toolbox in Python) library. This project implements a scalable quantum circuit engine capable of applying $N$-qubit operations, rendering state visualizations, and evaluating quantum logic via automated testing. 

Built as part of the Physics F-Praktikum course, following theoretical foundations from *Quantum Computation and Quantum Information* (Nielsen & Chuang).

## Features
* **Instruction-Based Circuit Engine:** Build arbitrary quantum circuits using human-readable instructions (e.g., `['H', [0]]`).
* **Automated $N$-Qubit Embedding:** Seamlessly applies 1-qubit and 2-qubit gates to complex $N$-qubit systems using automated tensor product expansions.
* **State Visualization:** Renders 3D Bloch spheres for single-qubit states and density matrix "cityscapes" for entangled multi-qubit systems.
* **Automated Unit Testing:** Robust testing framework to ensure physical and mathematical accuracy of unitary matrices and amplitude probabilities.

## Project Structure
* `circuit_engine.py`: Core logic for parsing instruction lists and executing them sequentially using `functools.reduce`.
* `quantum_gates.py`: Definitions for standard Pauli gates, rotation gates, and $N$-qubit controlled gates (CNOT, ISWAP, Toffoli). Contains the main `GATE_DICTIONARY`.
* `circuit_testing.ipynb`: Jupyter Notebook environment for interactive circuit development and testing.
* `bloch_sphere.py`: Visualization module using Matplotlib to render QuTiP Bloch spheres.
* `gate_test.py`: The `unittest` suite for validating quantum gate outputs.
* `simulate.py` / `bell_state.py`: Legacy execution scripts for specific state preparations.
* `requirements.txt`: Frozen dependencies for reproducing the environment.


## Status
* ongoing