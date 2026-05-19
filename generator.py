"""
generator.py
============
Generates random quantum circuits for arbitrary N-qubit systems.
Randomly chooses between 1-qubit and 2-qubit gates for each layer.
"""

import random
import qutip as qt

# Import the instruction parser from circuit engine
from circuit_engine import apply_instruction

def generate_random_circuit(num_qubits: int, num_layers: int, qubits: list[int] = None):
    """
    Generates a random quantum circuit with a fixed number of layers.
    Each layer is represented as a single N-qubit unitary operator.
    
    Args:
        num_qubits (int): Total number of qubits in the system.
        num_layers (int): Number of layers (columns) in the circuit.
        qubits (list[int], optional): Specific qubits to apply gates to. 
                                      If None, applies to all qubits.
        
    Returns:
        list[qt.Qobj]: A list of combined column operators for each layer.
        list[str]: A string description of each layer for logging.
        list[list]: A list of raw instructions for each layer (useful for visualization).
    """
    if qubits is None:
        qubits = list(range(num_qubits))
        
    # Ensure all specified qubits are valid
    if any(q < 0 or q >= num_qubits for q in qubits):
        raise ValueError(f"All qubits must be between 0 and {num_qubits - 1}")
        
    circuit_operators = []
    circuit_descriptions = []
    circuit_instructions = []  # Stores instructions for the visualizer
    
    # Standard 1-qubit gates available in dictionary
    single_qubit_gate_names = ['X', 'Y', 'Z', 'H', 'S', 'T']
    
    # Identity matrix for N qubits (the baseline state for a new column)
    identity_op = qt.tensor([qt.qeye(2) for _ in range(num_qubits)])
    
    for layer in range(num_layers):
        # Decide between 1-qubit and 2-qubit gate layer
        if len(qubits) >= 2:
            layer_type = random.choice(['1-qubit', '2-qubit'])
        else:
            layer_type = '1-qubit'
            
        combined_gate = identity_op
        current_layer_instructions = []
        
        if layer_type == '1-qubit':
            desc_parts = []
            
            # Apply a random single-qubit gate to each active qubit
            for q in qubits:
                gate_name = random.choice(single_qubit_gate_names)
                
                # Apply the single-qubit instruction using the circuit engine
                combined_gate = apply_instruction(combined_gate, [gate_name, [q]])
                
                # Record the actions
                desc_parts.append(f"{gate_name}({q})")
                current_layer_instructions.append([gate_name, [q]])
                
            circuit_operators.append(combined_gate)
            circuit_descriptions.append("1-qubit layer: " + ", ".join(desc_parts))
            
        else:
            # 2-qubit gate layer
            # Randomly select one target and control qubit (or two targets for ISWAP)
            q1, q2 = random.sample(qubits, 2)
            
            # Randomly pick a 2-qubit gate type
            """
            gate_type = random.choice(['CNOT', 'ISWAP'])
            """
            # Randomly pick a 2-qubit gate type (Now with dynamic controlled gates!)
            two_qubit_options = ['CNOT', 'ISWAP', 'C-H', 'C-Z', 'C-X', 'C-Y']
            gate_type = random.choice(two_qubit_options)
            
            # Apply the 2-qubit instruction
            combined_gate = apply_instruction(combined_gate, [gate_type, [q1, q2]])
            current_layer_instructions.append([gate_type, [q1, q2]])
            
            if gate_type == 'CNOT':
                desc = f"2-qubit layer: CNOT(control={q1}, target={q2})"
            elif gate_type == 'ISWAP':
                desc = f"2-qubit layer: ISWAP(targets=[{q1}, {q2}])"
            else:
                desc = f"2-qubit layer: {gate_type}(control={q1}, target={q2})"    
            
            circuit_operators.append(combined_gate)
            circuit_descriptions.append(desc)
            
        # Save the raw instructions for this layer
        circuit_instructions.append(current_layer_instructions)
            
    return circuit_operators, circuit_descriptions, circuit_instructions


if __name__ == "__main__":
    # test block to verify the generator runs independently
    num_q = 3
    num_l = 4
    
    print(f"Generating random circuit with {num_q} qubits and {num_l} layers...\n")
    ops, descs, instrs = generate_random_circuit(num_qubits=num_q, num_layers=num_l)
    
    for i, (op, desc, instr) in enumerate(zip(ops, descs, instrs)):
        print(f"Layer {i+1}: {desc}")
        print(f"Raw Instructions: {instr}")
        print(f"Matrix shape: {op.shape}, is_unitary: {op.isunitary}\n")