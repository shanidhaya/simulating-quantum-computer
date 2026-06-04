# Simulating a Quantum Computer (F-Praktikum)

A Python-based quantum simulator built using the **QuTiP** (Quantum Toolbox in Python) library. This project implements a scalable quantum circuit engine capable of applying $N$-qubit operations, rendering state visualizations, and evaluating quantum logic via automated testing. 

Built as part of the Physics F-Praktikum course, following theoretical foundations from *Quantum Computation and Quantum Information* (Nielsen & Chuang).

## Features
* **Instruction-Based Circuit Engine:** Build arbitrary quantum circuits using human-readable instructions (e.g., `['H', [0]]`).
* **Automated $N$-Qubit Embedding:** Seamlessly applies 1-qubit and 2-qubit gates to complex $N$-qubit systems using automated tensor product expansions.
* **Dynamic Controlled Gates:** Engine dynamically calculates and generates controlled versions of arbitrary single-qubit gates (e.g., Controlled-Hadamard, Controlled-Z) on the fly without requiring hardcoded matrices.
* **Density Matrix Support:** Executes quantum evolution on both pure states (state vectors) and mixed states (density matrices), laying the groundwork for real-world noise simulation.
* **Quantum Measurement:** Simulates projective measurements in the computational basis, accurately calculating measurement probabilities and applying post-measurement wave-function collapse.
* **Random Circuit Generation:** Dynamically construct arbitrary $N$-qubit quantum circuits of a specified depth, mixing single-qubit and multi-qubit layers.
* **ASCII Circuit Visualization:** Automatically parse circuit instructions and draw intuitive terminal-based wire diagrams showing gates, controls, and targets.
* **Performance Benchmarking:** Automated stress-testing to evaluate computational scaling and execution time across different numbers of qubits.
* **Sparse Matrix Optimization:** Extracts native QuTiP sparse data to SciPy CSR (`scipy.sparse`), drastically outperforming standard Dense (NumPy) matrices by bypassing exponential memory bottlenecks.
* **State Visualization:** Renders 3D Bloch spheres for single-qubit states and tracks multi-qubit system evolution.
* **Automated Unit Testing & Validation:** Robust testing framework (`unittest`) and programmatic "silent asserts" to mathematically prove matrix unitarity and shape validity at every circuit layer.
* **Random Matrix Ensembles (arXiv:1010.3570):** Generates Haar (Pure), Hilbert-Schmidt (Uniformly Mixed), and Bures (Surface-Biased) random density matrices using complex Ginibre matrices and rejection-sampled unitaries.
* **Statistical Distribution Analysis:** Visualizes large ensembles of quantum states mapped to the Bloch sphere and generates Purity ($\text{Tr}(\rho^2)$) histograms to verify theoretical geometric properties.
* **Theoretical vs. Physical Benchmarking:** Automated test suites comparing the execution time of physical circuit tracing (simulating System + Environment) vs. mathematical Random Matrix Theory (RMT) formulations.
* **Quantum Noise Simulation:** Implements environmental decoherence via Kraus operators, including Bitflip, Phaseflip, Amplitude Damping, and scalable $N$-qubit Depolarizing channels (Nielsen & Chuang Ch. 8).
* **Quantum Algorithms:** Native execution of the Deutsch-Jozsa algorithm, featuring dynamic Oracle (Blackbox) generation to prove exponential quantum computational advantage.
* **Interactive Jupyter Interface:** Culminating `F_Praktikum_Summary.ipynb` report combining LaTeX physics explanations with live, interactive code execution of the engine's features.

## Project Structure
* `quantum_gates.py`: Definitions for standard Pauli gates, rotation gates, and $N$-qubit controlled gates (CNOT, ISWAP, Toffoli). Contains the main `GATE_DICTIONARY`.
* `circuit_engine.py`: Core logic for parsing instruction lists, auto-expanding matrices, handling state evolution, and executing computational measurements.
* `generator.py`: Circuit factory script that builds scalable, randomized multi-qubit circuits and extracts raw functional instructions.
* `visualize.py`: Reads raw instructions and draws an ASCII representation of the quantum circuit directly in the terminal.
* `benchmark.py`: Stress-testing script comparing execution times of Dense vs. Sparse matrix operations.
* `random_states.py`: Mathematical engine generating Haar, Hilbert-Schmidt, and Bures random density matrices.
* `plot_distributions.py` & `plot_purity.py`: Visualization modules rendering 3D Bloch distributions and statistical probability density histograms for random state ensembles.
* `benchmark_random_states.py`: High-resolution performance comparison demonstrating the exponential cost of circuit-based mixed state generation vs. NumPy matrix formulations.
* `noise_channels.py`: Implementation of standard quantum error channels using Operator-Sum (Kraus) representation and scalable depolarizing formulas.
* `noise_test.py`: Demonstration script explicitly showing how environmental noise channels degrade the purity and Bloch coordinates of pure states.
* `deutsch_jozsa.py`: Oracle generator that builds global Unitary matrices for Constant and Balanced binary functions.
* `run_deutsch_josa.py`: Orchestrator script executing the full Deutsch-Jozsa algorithm sequence (Superposition -> Oracle -> Interference -> Measurement).
* `test_deutch_jozsa.py`, `test_circuit_states.py`, `test_random_states.py`: Unit test suites asserting the fundamental laws of quantum physics and the mathematical correctness of algorithm outputs.
* `testing_playground.ipynb`: Jupyter Notebook sandboxes for interactive circuit development.
* `F_Praktikum_Summary.ipynb`: Professional Jupyter Notebook summarizing the project methodology and providing an executable interface.

## Status: Ongoing

*Milestones (Phase 2 & 3: Multi-Qubit & Core Engine):*
* [x] **Arbitrary Embedding:** Upgraded the circuit engine to dynamically embed one- and two-qubit gates into arbitrary $N$-qubit systems.
* [x] **Random Circuit Generation:** Built a generator to construct N-qubit circuits with a fixed number of layers.
* [x] **Sparse Matrix Integration:** Refactored matrix multiplication to natively utilize SciPy CSR sparse matrices.
* [x] **Performance Benchmarking:** Created a stress-test loop executing 1000-layer circuits, comparing Dense vs. Sparse execution times.
* [x] **ASCII Visualization & Asserts:** Added terminal-based circuit wire diagrams and silent mathematical asserts.
* [x] **Dynamic Controlled Gates:** Upgraded the circuit engine to interpret and mathematically construct arbitrary controlled operations (e.g., C-H, C-Z) on the fly.
* [x] **Density Matrix Integration:** Refactored the core execution loop to natively route and compute both pure state vectors and mixed density matrices.
* [x] **Computational Measurement:** Implemented classical projective measurements, allowing wave-function collapse.

*Milestones (Phase 4: Random Matrices & Open Quantum Systems):*
* [x] **Random Mixed States:** Implemented Haar, Hilbert-Schmidt, and Bures random density matrix ensembles.
* [x] **Distribution Analysis:** Rendered 3D visual mappings of state geometries on the Bloch sphere alongside detailed statistical histograms.
* [x] **Physical vs. Mathematical Benchmarking:** Successfully simulated physical environmental entanglement to contrast with rapid RMT arrays.

**Milestones (Phase 5: Noise Channels & Algorithms):**
* [x] **Distribution Verification:** Programmatically verified the exact mean purities of the generated Hilbert-Schmidt (0.80) and Bures (0.875) distributions with proper axis labeling.
* [x] **Quantum Noise Channels:** Implemented single-qubit environmental noise models from Nielsen & Chuang 8.3 (Bitflip, Phaseflip, Amplitude Damping).
* [x] **$N$-Qubit Depolarizing Channel:** Implemented a scalable, parameter-driven depolarizing channel for arbitrary system sizes (using Eq. 8.100).
* [x] **Deutsch-Jozsa Algorithm:** Built a quantum oracle (Blackbox) generator capable of creating Unitary matrices for Constant and Balanced functions, and successfully executed the algorithm to demonstrate single-query quantum advantage.