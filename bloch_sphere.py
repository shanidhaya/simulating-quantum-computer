"""
bloch_sphere
"""

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import qutip as qt

# ── Utilities ─────────────────────────────────────────────────────────────────
"""Calculate (x, y, z) Bloch coordinates using Pauli expectation values."""
def get_bloch_coords(state: qt.Qobj) -> tuple[float, float, float]:
    x = qt.expect(qt.sigmax(), state)
    y = qt.expect(qt.sigmay(), state)
    z = qt.expect(qt.sigmaz(), state)
    return float(x), float(y), float(z)

# ── Public API ────────────────────────────────────────────────────────────────
"""Plots a grid of individual Bloch spheres."""
def plot_bloch_panels(entries, ncols: int = 3,
                      suptitle = r"Single-qubit gates acting on $|1\rangle$",
                      filename: str | None = None):
    
    n = len(entries)
    nrows = (n + ncols - 1) // ncols
    fig = plt.figure(figsize=(4.5 * ncols, 4.5 * nrows))
    fig.patch.set_facecolor("#f8f9fa")

    state_1 = qt.basis(2, 1)

    for k, (label, state, color) in enumerate(entries, 1):
        ax = fig.add_subplot(nrows, ncols, k, projection="3d")
        ax.set_facecolor("#f8f9fa")
        
        b = qt.Bloch(fig=fig, axes=ax)
        b.vector_color = ["#cccccc", color]
        b.font_color = "#333333"
        b.sphere_alpha = 0.08
        b.frame_alpha = 0.15
        
        b.add_states(state_1)
        b.add_states(state)
        b.render()
        
        ax.set_title(label, fontsize=12, fontweight="bold", color="#222222", pad=2)

    legend_elems = [
        Line2D([0], [0], color="#cccccc", lw=2, label=r"$|1\rangle$ (initial)"),
        Line2D([0], [0], color="#e74c3c", lw=2, label="Output state"),
    ]
    fig.legend(handles=legend_elems, loc="lower center",
               ncol=2, fontsize=10, framealpha=0.7,
               bbox_to_anchor=(0.5, 0.01))

    fig.suptitle(suptitle, fontsize=15, fontweight="bold", color="#1a1a2e", y=1.01)
    plt.tight_layout(rect=[0, 0.04, 1, 1])

    if filename:
        fig.savefig(filename, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
        print(f"  Saved → {filename}")
        
    return fig


"""Plots multiple quantum states onto a single, shared Bloch sphere."""
def plot_all_states_single_sphere(entries, initial_state: qt.Qobj, filename: str | None = None):
    
    fig_all = plt.figure(figsize=(8, 8))
    fig_all.patch.set_facecolor("#f8f9fa")
    ax = fig_all.add_subplot(111, projection="3d")
    ax.set_facecolor("#f8f9fa")

    b_all = qt.Bloch(fig=fig_all, axes=ax)
    b_all.sphere_alpha = 0.08
    b_all.frame_alpha = 0.15

    states = [initial_state]
    colors = ["#888888"]
    legend_lines = [Line2D([0], [0], color="#888888", lw=0, marker="o", 
                           markersize=7, label=r"$|1\rangle$ (initial)")]

    for label, state, color in entries:
        states.append(state)
        colors.append(color)
        legend_lines.append(Line2D([0], [0], color=color, lw=2.2, 
                                   label=label.split("(")[-1].rstrip(")")))

    b_all.add_states(states)
    b_all.vector_color = colors
    b_all.render()

    ax.legend(handles=legend_lines, loc="upper left", fontsize=8.5, framealpha=0.85,
              bbox_to_anchor=(-0.05, 1.05), title="Gate output", title_fontsize=9)
    ax.set_title("All single-qubit gates — output states on one Bloch sphere",
                 fontsize=12, fontweight="bold", pad=10)

    fig_all.tight_layout()
    if filename:
        fig_all.savefig(filename, dpi=300, bbox_inches="tight", facecolor=fig_all.get_facecolor())
        print(f"  Saved → {filename}")
        
    return fig_all