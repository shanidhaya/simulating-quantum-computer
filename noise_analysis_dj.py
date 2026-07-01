import matplotlib.pyplot as plt
import numpy as np
from deutch_jozsa_noisy import run_noisy_dj

def plot_custom_noise_analysis(experiments, num_points=20):
    """
    Runs a customized list of noise sweeps and plots them together.
    """
    import matplotlib.pyplot as plt
    import numpy as np
    from deutch_jozsa_noisy import run_noisy_dj
    
    noise_probs = np.linspace(0, 1.0, num_points)
    
    plt.figure(figsize=(10, 6))
    
    # Loop through each experiment configuration provided by the user
    for exp in experiments:
        accuracies = []
        # Run the sweep for this specific configuration
        for p in noise_probs:
            # FIX 1: Use 'secret_function' instead of 'oracle_type'
            prob_000 = run_noisy_dj(
                num_qubits=exp['n'], 
                secret_function=exp['oracle'], 
                noise_channel=exp['channel'], 
                noise_prob=p, 
                noise_loc=exp['location']
            )
            
            # FIX 2: Calculate true accuracy here to prevent the flatline bug!
            if isinstance(exp['oracle'], str) and "balanced" in exp['oracle']:
                accuracies.append(1.0 - prob_000) # Balanced wants anything BUT |0...0>
            else:
                accuracies.append(prob_000)       # Constant wants |0...0>
            
        # Plot this sweep immediately
        plt.plot(noise_probs, accuracies, label=exp['label'], color=exp.get('color'), marker=exp.get('marker', 'o'))
        
    plt.xlabel("Noise Probability (p)")
    plt.ylabel("Algorithm Accuracy (1.0 = 100%)")
    plt.title("Deutsch-Jozsa: Custom Noise Analysis")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()
    
def plot_joint_benchmark(n: int, channel, loc: str, num_points=20):
    """
    Plots the success probability of BOTH a Constant and a Balanced function
    on the exact same graph to see how noise affects them differently.
    """
    import matplotlib.pyplot as plt
    import numpy as np
    from deutch_jozsa_noisy import run_noisy_dj
    
    noise_probs = np.linspace(0, 1.0, num_points)
    
    acc_constant = []
    acc_balanced = []
    
    for p in noise_probs:
        # Get RAW probabilities from the new physics engine
        prob_0_const = run_noisy_dj(n, "constant_0", channel, p, loc)
        prob_0_bal = run_noisy_dj(n, "balanced", channel, p, loc)
        
        # Calculate true accuracy!
        acc_constant.append(prob_0_const)         # Constant wants |00...0>
        acc_balanced.append(1.0 - prob_0_bal)     # Balanced wants ANYTHING BUT |00...0>
        
    plt.figure(figsize=(9, 5))
    channel_name = channel.__name__ if not isinstance(channel, list) else "Combined Noise"
    
    plt.plot(noise_probs, acc_constant, label="Constant (f(x)=0)", color="blue", marker="o")
    plt.plot(noise_probs, acc_balanced, label="Balanced (Parity)", color="green", marker="^")
    
    plt.xlabel("Noise Probability (p)")
    plt.ylabel("Success Probability / Accuracy")
    plt.title(f"Joint Benchmark: {channel_name} applied '{loc}' (N={n})")
    plt.axhline(0.5, color='gray', linestyle='--', label='Random Guess Baseline')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()
    
def plot_all_combinations(n=3, num_points=20):
    """
    Generates a comprehensive 3x4 grid benchmarking all noise channels
    across all 4 circuit locations for the DJ Algorithm.
    """
    from noise_channels import bitflip_channel, phaseflip_channel, depolarizing_channel
    
    locations = ["pre_H1", "post_H1", "post_oracle", "post_H2"]
    channels = [bitflip_channel, phaseflip_channel, depolarizing_channel]
    noise_probs = np.linspace(0, 1.0, num_points)
    
    fig, axes = plt.subplots(len(channels), len(locations), figsize=(18, 12), sharex=True, sharey=True)
    fig.suptitle(f"Deutsch-Jozsa Noise Vulnerability Matrix (N={n})", fontsize=20)
    
    for i, channel in enumerate(channels):
        for j, loc in enumerate(locations):
            acc_const = []
            acc_bal = []
            
            for p in noise_probs:
                # Get the raw probability of measuring |00...0>
                prob_0_const = run_noisy_dj(n, "constant_0", channel, p, loc)
                prob_0_bal = run_noisy_dj(n, "balanced", channel, p, loc)
                
                # Calculate Accuracy properly!
                acc_const.append(prob_0_const)         # Constant wants |00...0>
                acc_bal.append(1.0 - prob_0_bal)       # Balanced wants anything BUT |00...0>
                
            ax = axes[i, j]
            ax.plot(noise_probs, acc_const, label="Constant", color="blue", marker="o", markersize=4)
            ax.plot(noise_probs, acc_bal, label="Balanced", color="green", marker="^", markersize=4)
            
            # Formatting
            ch_name = channel.__name__.replace("_channel", "").capitalize()
            ax.set_title(f"{ch_name} @ {loc}")
            ax.axhline(0.5, color='gray', linestyle='--', alpha=0.5)
            ax.grid(True, linestyle=':', alpha=0.6)
            
            if i == len(channels) - 1:
                ax.set_xlabel("Noise Probability (p)")
            if j == 0:
                ax.set_ylabel("Accuracy")
                
    # Add a single legend for the whole figure
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right', fontsize=12)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()