"""
circuit_engine.py
=================
Parses and executes quantum circuit instructions using QuTiP.
"""

import qutip as qt
from qutip_qip.operations import expand_operator
from quantum_gates import GATE_DICTIONARY

def apply_instruction(state: qt.Qobj, instruction: list) -> qt.Qobj:
    """
    Takes a quantum state and an instruction list, and applies the gate.
    Example instruction: ['H', [0]] or ['CNOT', [0, 1]]
    """
    gate_name = instruction[0]  
    targets = instruction[1]    
    
    # 1. Automatically detect how many qubits (N) are in the current state.
    # QuTiP states have a 'dims' property. A 3-qubit state dims looks like [[2, 2, 2], [1, 1, 1]]
    # Taking the length of the first array tells us N automatically!
    N = len(state.dims[0])
    
    # 2. Fetch the raw gate matrix from our dictionary
    if gate_name not in GATE_DICTIONARY:
        raise ValueError(f"Gate '{gate_name}' is not recognized.")
        
    raw_gate = GATE_DICTIONARY[gate_name]
    
    # 3. Automatically embed the gate into the N-qubit system
    expanded_gate = expand_operator(raw_gate, N=N, targets=targets)
    
    # 4. Apply the gate (Matrix multiplication)
    new_state = expanded_gate * state
    
    return new_state