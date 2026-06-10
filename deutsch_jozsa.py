import numpy as np
import qutip as qt
from black_box import black_box

def create_dj_oracle(num_qubits: int, oracle_type: str) -> qt.Qobj:
    """
    Creates the Unitary matrix (U_f) for a Deutsch-Jozsa Oracle.
    Input: A binary string (represented by the basis states).
    Output: Phase flip (-1) if f(x) == 1, else no phase flip (+1).
    """
    dim = 2 ** num_qubits
    
    # We define the oracle as a diagonal matrix
    # U_f |x> = (-1)^f(x) |x>
    diagonal_elements = np.ones(dim)
    
    if oracle_type == "constant_0":
        # f(x) = 0 for all x. (-1)^0 = 1
        pass # diagonal stays all 1s
        
    elif oracle_type == "constant_1":
        # f(x) = 1 for all x. (-1)^1 = -1
        diagonal_elements = -1 * diagonal_elements
        
    elif oracle_type == "balanced":
        # f(x) = 0 for half, 1 for half. 
        # If the integer 'x' has an odd number of 1s in binary, f(x) = 1.
        for x in range(dim):
            # Count the number of 1s in the binary representation of x
            bit_sum = bin(x).count('1')
            if bit_sum % 2 == 1:
                diagonal_elements[x] = -1
    elif oracle_type == "balanced_first_qubit":
        # f(x) = 1 only if the FIRST qubit (Most Significant Bit) is 1.
        # For N=3 (states 0 to 7), the first bit is '1' for numbers 4, 5, 6, and 7.
        half_dim = dim // 2
        for x in range(dim):
            if x >= half_dim:
                diagonal_elements[x] = -1        
    else:
        raise ValueError("Invalid oracle type. Use 'constant_0', 'constant_1', or 'balanced'.")

    # Create the QuTiP Unitary Operator
    U_f = qt.Qobj(np.diag(diagonal_elements), dims=[[2]*num_qubits, [2]*num_qubits])
    return U_f
def indToState(n, k):
    """Provided by the notebook: Converts integer k to a binary array of length n."""
    num = bin(k)[2:].zfill(n)
    return np.array([int(x) for x in str(num)])

def create_dynamic_oracle(num_qubits: int, func) -> qt.Qobj:
    """
    Evaluates an arbitrary blackbox python function to build the U_f matrix.
    """
    dim = 2 ** num_qubits
    diagonal_elements = np.zeros(dim)
    
    for k in range(dim):
        # 1. Convert the classical index into a binary array (e.g. 3 -> [0, 1, 1])
        bit_string = indToState(num_qubits, k)
        
        # 2. Feed the binary array into the mystery blackbox
        f_x = func(bit_string)
        
        # 3. Apply the Quantum Phase Kickback: (-1)^f(x)
        diagonal_elements[k] = (-1) ** f_x
        
    # Build and return the massive QuTiP diagonal matrix
    return qt.Qobj(np.diag(diagonal_elements), dims=[[2]*num_qubits, [2]*num_qubits])
# --- Quick Test ---
if __name__ == "__main__":
    print("Testing 3-Qubit Balanced Oracle Matrix:")
    U = create_dj_oracle(3, "balanced")
    print(U.diag())