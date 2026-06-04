"""
plot_purity.py
==============
Generates large ensembles of random quantum states and plots 
the histogram of their Purity: Tr(rho^2).
"""

import numpy as np
import matplotlib.pyplot as plt

# Import your generators
from random_states import (
    haar_random_state, 
    hilbert_schmidt_random_state, 
    bures_random_state
)

def plot_purity_distributions(num_samples=10000):
    print(f"Generating {num_samples} states for each distribution. This may take a moment...")

    haar_purities = []
    hs_purities = []
    bures_purities = []

    for _ in range(num_samples):
        # 1. Haar
        rho_haar = haar_random_state(2)
        # We take .real because QuTiP traces sometimes return (value + 0j)
        haar_purities.append((rho_haar * rho_haar).tr().real)

        # 2. Hilbert-Schmidt
        rho_hs = hilbert_schmidt_random_state(2)
        hs_purities.append((rho_hs * rho_hs).tr().real)

        # 3. Bures
        rho_bures = bures_random_state(2)
        bures_purities.append((rho_bures * rho_bures).tr().real)

    # ==========================================
    # Plotting the Histograms
    # ==========================================
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    fig.suptitle("Purity Distributions of Random Single-Qubit States", fontsize=16)
    
    fixed_bins = np.linspace(0.48, 1.02, 50)

    # 1. Haar Plot
    axes[0].hist(haar_purities, bins=fixed_bins, color='#1f77b4', density=True)
    axes[0].set_title("Haar Random (Pure States)")
    axes[0].set_ylabel("Density")
    axes[0].grid(True, alpha=0.3)

    # 2. Hilbert-Schmidt Plot
    axes[1].hist(hs_purities, bins=fixed_bins, color='#2ca02c', density=True)
    axes[1].set_title("Hilbert-Schmidt (Uniform Volume)")
    axes[1].set_ylabel("Density")
    axes[1].grid(True, alpha=0.3)

    # 3. Bures Plot
    axes[2].hist(bures_purities, bins=fixed_bins, color='#d62728', density=True)
    axes[2].set_title("Bures (Surface-Biased)")
    axes[2].set_xlabel(r"Purity: $\text{Tr}(\rho^2)$", fontsize=12)
    axes[2].set_ylabel("Density")
    axes[2].grid(True, alpha=0.3)
    


    print(f"Mean HS Purity: {np.mean(hs_purities):.4f} (Theoretical: 0.8000)")
    print(f"Mean Bures Purity: {np.mean(bures_purities):.4f} (Theoretical: 0.8750)")

    # Force X-axis bounds to match theoretical limits
    plt.xlim(0.48, 1.02)
    plt.tight_layout()
    print("Done! Displaying plot...")
    plt.show()

if __name__ == "__main__":
    plot_purity_distributions(num_samples=10000)