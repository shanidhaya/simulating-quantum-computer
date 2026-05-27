"""
circuit_engine.py
=================
Parses and executes quantum circuit instructions using QuTiP.
"""

import qutip as qt
from qutip_qip.operations import expand_operator
from quantum_gates import GATE_DICTIONARY,Rx, Ry, Rz
import random
import numpy as np

def apply_instruction(state: qt.Qobj, instruction: list) -> qt.Qobj:
    """
    Takes a quantum state and an instruction list, and applies the gate.
    Example instruction: ['H', [0]] or ['CNOT', [0, 1]]
    """
    gate_name = instruction[0]  
    targets = instruction[1]    
    
    # 1. Automatically detect how many qubits (N) are in the current state.

    N = len(state.dims[0])
    """
    # 2. Fetch the raw gate matrix from our dictionary
    if gate_name not in GATE_DICTIONARY:
        raise ValueError(f"Gate '{gate_name}' is not recognized.")
        
    raw_gate = GATE_DICTIONARY[gate_name]
    
    # 3. Automatically embed the gate into the N-qubit system
    expanded_gate = expand_operator(raw_gate, N=N, targets=targets)
    
    # 4. Apply the gate (Matrix multiplication)
    new_state = expanded_gate * state
    
    return new_state
    """
    # 1. Check if there are parameters (like an angle 'theta')
    params = instruction[2] if len(instruction) > 2 else []
    # 2. Build the Raw Gate
    if gate_name == 'Rx':
        raw_gate = Rx(params[0])  
    elif gate_name == 'Ry':
        raw_gate = Ry(params[0])  
    elif gate_name == 'Rz':
        raw_gate = Rz(params[0])
    # ==========================================
    # 1. Parse and Build the Raw Gate
    # ==========================================
    
    # Check if it's a dynamic Controlled-Gate (e.g., 'C-H', 'C-Z')
    elif gate_name.startswith("C-") and gate_name != "CNOT":
        # Extract the base gate (e.g., "H" from "C-H")
        base_gate_name = gate_name.split("-")[1]
        
        if base_gate_name not in GATE_DICTIONARY:
            raise ValueError(f"Base gate '{base_gate_name}' not found in GATE_DICTIONARY.")
        
        base_gate = GATE_DICTIONARY[base_gate_name]
        
        # Mathematically construct the 4x4 Controlled-U matrix
        # CU = (|0><0| x I) + (|1><1| x U)
        P0 = qt.basis(2, 0) * qt.basis(2, 0).dag()
        P1 = qt.basis(2, 1) * qt.basis(2, 1).dag()
        I = qt.qeye(2)
        
        raw_gate = qt.tensor(P0, I) + qt.tensor(P1, base_gate)
        
    # Otherwise, check if it's a standard gate
    elif gate_name in GATE_DICTIONARY:
        raw_gate = GATE_DICTIONARY[gate_name]
        
    else:
        raise ValueError(f"Gate '{gate_name}' is not recognized.")

    # ==========================================
    # 2. Expand and Apply
    # ==========================================
    
    # Expand the raw gate to the full N-qubit system
    expanded_gate = expand_operator(raw_gate, dims=[2]*N, targets=targets)
    
    # Apply the gate
    if state.isket:
        # State Vector evolution:
        return expanded_gate * state
    elif state.isoper:
        # Density Matrix evolution:
        if state.isunitary:
            return expanded_gate * state
        else:
            return expanded_gate * state * expanded_gate.dag()
    else:
        raise TypeError("Input state must be a ket vector or a density matrix.")
    
def measure_qubit(state: qt.Qobj, target_qubit: int) -> tuple[int, qt.Qobj]:
    """
    Measures a specific qubit in the computational basis.
    Collapses the quantum state and returns the classical result (0 or 1).
    Supports both state vectors (kets) and density matrices.
    
    Returns:
        tuple: (classical_result, collapsed_state)
    """
    N = len(state.dims[0])
    
    # 1. Define the 1-qubit Projectors
    P0_raw = qt.basis(2, 0) * qt.basis(2, 0).dag()  # |0><0|
    P1_raw = qt.basis(2, 1) * qt.basis(2, 1).dag()  # |1><1|
    
    # 2. Expand them to the N-qubit system
    P0 = expand_operator(P0_raw, N=N, targets=[target_qubit])
    P1 = expand_operator(P1_raw, N=N, targets=[target_qubit])
    
    # 3. Calculate the probability of measuring 0
    # Probability = Trace(P0 * state)
    prob_0 = qt.expect(P0, state)
    
    # Clean up minor floating point errors
    prob_0 = max(0.0, min(1.0, prob_0))
    
    # 4. Roll the dice to measure!
    random_roll = random.random()
    
    if random_roll <= prob_0:
        classical_result = 0
        projector = P0
        prob = prob_0
    else:
        classical_result = 1
        projector = P1
        prob = 1.0 - prob_0
        
    # 5. Collapse the state mathematically
    if state.isket:
        # Collapse vector: P |ψ> / sqrt(p)
        collapsed_state = (projector * state) / np.sqrt(prob)
    elif state.isoper:
        # Collapse density matrix: P ρ P† / p
        collapsed_state = (projector * state * projector.dag()) / prob
    else:
        raise TypeError("Input must be a ket or density matrix.")
        
    return classical_result, collapsed_state