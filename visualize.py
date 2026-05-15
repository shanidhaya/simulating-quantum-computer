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
                                    e.g., [ [['H', [0]], ['X', [1]]], [['CNOT', [0, 1]]] ]
    """
    # Create empty "wires" for each qubit
    wires = {q: f"q{q}: ──" for q in range(num_qubits)}

    for layer in layers_instructions:
        # Default empty space for this column/layer
        col_width = 5
        layer_repr = {q: "─" * col_width for q in range(num_qubits)}

        # Track vertical lines for multi-qubit gates
        min_q, max_q = -1, -1

        for gate_name, targets in layer:
            if len(targets) == 1:
                # 1-Qubit Gate (e.g., [H], [X])
                q = targets[0]
                gate_str = f"[{gate_name}]"
                
                # Pad with dashes to center it in the column
                pad_left = (col_width - len(gate_str)) // 2
                pad_right = col_width - len(gate_str) - pad_left
                layer_repr[q] = "─" * pad_left + gate_str + "─" * pad_right
                
            elif gate_name == 'CNOT':
                # 2-Qubit Gate: CNOT
                c, t = targets[0], targets[1]
                layer_repr[c] = "──■──"
                layer_repr[t] = "─(X)─"
                min_q, max_q = min(c, t), max(c, t)
                
            elif gate_name == 'ISWAP':
                # 2-Qubit Gate: ISWAP
                q1, q2 = targets[0], targets[1]
                layer_repr[q1] = "──x──"
                layer_repr[q2] = "──x──"
                min_q, max_q = min(q1, q2), max(q1, q2)

        # Draw vertical connection lines for 2-qubit gates
        if min_q != -1:
            for q in range(min_q + 1, max_q):
                if layer_repr[q] == "─────":
                    layer_repr[q] = "──│──"

        # Append this column to the main horizontal wires
        for q in range(num_qubits):
            wires[q] += layer_repr[q] + "──"

    # Print the final masterpiece
    print("\n=== Generated Quantum Circuit ===")
    for q in range(num_qubits):
        print(wires[q])
    print("=================================\n")


if __name__ == "__main__":
    from generator import generate_random_circuit
    
    num_q = 4
    num_l = 6
    
    # Generate a circuit and catch the new 3rd return variable (instructions)
    ops, descs, instructions = generate_random_circuit(num_qubits=num_q, num_layers=num_l)
    
    # Draw it!
    draw_ascii_circuit(num_q, instructions)