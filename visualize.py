"""
visualize.py
============
Draws ASCII representations of quantum circuits in the terminal.
"""

def draw_ascii_circuit(num_qubits: int, layers_instructions: list):
    """
    Prints an ASCII representation of the quantum circuit.
    
    Args:
        num_qubits (int): Total number of qubits in the system.
        layers_instructions (list): A list of layers, where each layer is a list of instructions.
    """
    # Create empty "wires" for each qubit
    wires = {q: f"q{q}: ──" for q in range(num_qubits)}

    for layer in layers_instructions:
        # Widen the column to 7 dashes to fit gates like [Rx] and [CNOT]
        col_width = 7
        layer_repr = {q: "─" * col_width for q in range(num_qubits)}

        # Track vertical lines for multi-qubit gates
        min_q, max_q = -1, -1

        # FIXED: Extract data by index instead of rigid tuple unpacking
        for instruction in layer:
            gate_name = instruction[0]
            targets = instruction[1]
            
            if len(targets) == 1:
                # 1-Qubit Gate (e.g., [H], [Rx])
                q = targets[0]
                gate_str = f"[{gate_name}]"
                
                # Pad with dashes to center it in the column
                pad_left = (col_width - len(gate_str)) // 2
                pad_right = col_width - len(gate_str) - pad_left
                layer_repr[q] = "─" * pad_left + gate_str + "─" * pad_right
                
            elif len(targets) == 2:
                # 2-Qubit Gate (e.g., CNOT, C-H)
                c, t = targets[0], targets[1]
                
                if gate_name == 'CNOT':
                    base_gate = 'X'
                elif gate_name.startswith('C-'):
                    base_gate = gate_name.split('-')[1]
                elif gate_name == 'ISWAP':
                    base_gate = 'SWP'
                    layer_repr[c] = "─[SWP]─"
                else:
                    base_gate = gate_name
                
                # Draw the Control dot (unless it's an ISWAP)
                if gate_name != 'ISWAP':
                    layer_repr[c] = "───■───"
                
                # Draw the Target gate (e.g., [H], [X])
                target_str = f"[{base_gate}]"
                pad_left = (col_width - len(target_str)) // 2
                pad_right = col_width - len(target_str) - pad_left
                layer_repr[t] = "─" * pad_left + target_str + "─" * pad_right
                
                min_q, max_q = min(c, t), max(c, t)

        # Draw vertical connection lines for 2-qubit gates
        if min_q != -1:
            for q in range(min_q + 1, max_q):
                if layer_repr[q] == "───────":
                    layer_repr[q] = "───│───"

        # Append this column to the main horizontal wires
        for q in range(num_qubits):
            wires[q] += layer_repr[q] + "──"

    # Print the final masterpiece
    print("\n=== Generated Quantum Circuit ===")
    for q in range(num_qubits):
        print(wires[q])
    print("=================================\n")