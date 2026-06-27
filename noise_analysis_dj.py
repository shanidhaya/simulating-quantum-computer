import matplotlib.pyplot as plt
import numpy as np
from deutch_jozsa_noisy import run_noisy_dj

def plot_custom_noise_analysis(experiments, num_points=20):
    """
    Runs a customized list of noise sweeps and plots them together.
    
    Args:
    experiments: A list of dictionaries, where each dictionary defines the parameters
                 for one specific sweep (e.g., {'n': 3, 'oracle': 'constant_0', ...})
    num_points: How many data points to calculate between p=0 and p=1.
    """
    noise_probs = np.linspace(0, 1.0, num_points)
    
    plt.figure(figsize=(10, 6))
    
    # Loop through each experiment configuration provided by the user
    for exp in experiments:
        accuracies = []
        # Run the sweep for this specific configuration
        for p in noise_probs:
            acc = run_noisy_dj(
                num_qubits=exp['n'], 
                oracle_type=exp['oracle'], 
                noise_channel=exp['channel'], 
                noise_prob=p, 
                noise_loc=exp['location']
            )
            accuracies.append(acc)
            
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
    noise_probs = np.linspace(0, 1.0, num_points)
    
    acc_constant = []
    acc_balanced = []
    
    for p in noise_probs:
        # The run_noisy_dj function already calculates the True Accuracy automatically!
        # No more double negation math needed here.
        acc_const = run_noisy_dj(n, "constant_0", channel, p, loc)
        acc_bal = run_noisy_dj(n, "balanced", channel, p, loc)
        
        acc_constant.append(acc_const)
        acc_balanced.append(acc_bal)
        
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