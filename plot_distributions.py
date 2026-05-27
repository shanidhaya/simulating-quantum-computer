"""
plot_distributions.py
=====================
Generates ensembles of random single-qubit states and plots their 
distributions on the Bloch sphere to visualize their geometries.
"""

import qutip as qt
import matplotlib.pyplot as plt

# Import your excellent new generators
from random_states import (
    haar_random_state, 
    hilbert_schmidt_random_state, 
    bures_random_state
)

# Import the coordinate extractor you built previously
from bloch_sphere import get_bloch_coords

def plot_random_distributions(num_samples: int = 500):
    """
    Generates 'num_samples' states for Haar, Hilbert-Schmidt, and Bures 
    distributions and plots them as point clouds on three Bloch spheres.
    """
    # Initialize lists to hold the [x, y, z] coordinates for each distribution
    haar_coords = [[], [], []]
    hs_coords = [[], [], []]
    bures_coords = [[], [], []]

    print(f"Generating {num_samples} states for each distribution. Please wait...")

    for _ in range(num_samples):
        # 1. Haar (Pure)
        rho_haar = haar_random_state(2)
        hx, hy, hz = get_bloch_coords(rho_haar)
        haar_coords[0].append(hx)
        haar_coords[1].append(hy)
        haar_coords[2].append(hz)

        # 2. Hilbert-Schmidt (Mixed)
        rho_hs = hilbert_schmidt_random_state(2)
        hsx, hsy, hsz = get_bloch_coords(rho_hs)
        hs_coords[0].append(hsx)
        hs_coords[1].append(hsy)
        hs_coords[2].append(hsz)

        # 3. Bures (Mixed)
        rho_bures = bures_random_state(2)
        bx, by, bz = get_bloch_coords(rho_bures)
        bures_coords[0].append(bx)
        bures_coords[1].append(by)
        bures_coords[2].append(bz)

    # ==========================================
    # Rendering the Plot
    # ==========================================
    fig = plt.figure(figsize=(15, 5))

    # Sphere 1: Haar Random
    ax1 = fig.add_subplot(1, 3, 1, projection='3d')
    b1 = qt.Bloch(fig=fig, axes=ax1)
    b1.add_points(haar_coords)
    b1.point_color = ['#1f77b4']  # Blue points
    b1.point_marker = ['.']       # Make points small
    b1.render()
    ax1.set_title("1. Haar Random (Pure States)", y=1.08)

    # Sphere 2: Hilbert-Schmidt
    ax2 = fig.add_subplot(1, 3, 2, projection='3d')
    b2 = qt.Bloch(fig=fig, axes=ax2)
    b2.add_points(hs_coords)
    b2.point_color = ['#2ca02c']  # Green points
    b2.point_marker = ['.']
    b2.render()
    ax2.set_title("2. Hilbert-Schmidt (Mixed States)", y=1.08)

    # Sphere 3: Bures
    ax3 = fig.add_subplot(1, 3, 3, projection='3d')
    b3 = qt.Bloch(fig=fig, axes=ax3)
    b3.add_points(bures_coords)
    b3.point_color = ['#d62728']  # Red points
    b3.point_marker = ['.']
    b3.render()
    ax3.set_title("3. Bures (Mixed States)", y=1.08)

    plt.tight_layout()
    print("Rendering complete!")
    plt.show()

if __name__ == "__main__":
    plot_random_distributions(num_samples=500)