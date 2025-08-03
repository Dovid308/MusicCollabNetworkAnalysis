"""
Null Model Analysis Module - Compare observed network patterns with null models
"""
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from scipy import stats
import os
from homophily import calculate_homophily_ratio


def null_model_analysis(G, attribute, num_iterations=100, rewiring_iterations=10, output_dir="analysis_results", log_path=None):
    """
    Compare the original graph with null models.
    
    Args:
        G (networkx.Graph): The network graph
        attribute (str): Node attribute to analyze
        num_iterations (int): Number of randomized networks to generate
        rewiring_iterations (int): Number of edge swaps per edge in the rewiring process
        output_dir (str): Directory to save output figures
        log_path (str): Path to the log file for results
        
    Returns:
        dict: Results of null model analysis
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    def log(message):
        if log_path:
            with open(log_path, "a") as f:
                f.write(message + "\n")

    log("\n--- Null Model Analysis ---")
    results = {}

    # Original graph metrics
    original_homophily = calculate_homophily_ratio(G, attribute)
    original_assortativity = nx.attribute_assortativity_coefficient(G, attribute)
    results['original_homophily'] = original_homophily
    results['original_assortativity'] = original_assortativity
    log(f"Original homophily ratio: {original_homophily:.4f}")
    log(f"Original assortativity coefficient: {original_assortativity:.4f}")

    # Storage for null model metrics
    rewired_homophily_scores = []
    rewired_assortativity_scores = []
    attr_shuffled_homophily_scores = []
    attr_shuffled_assortativity_scores = []

    # 1. Rewiring Model (degree-preserving randomization)
    for i in range(num_iterations):
        if i > 0 and i % 10 == 0:
            log(f"  Running rewiring model iteration {i}/{num_iterations}")
        
        # Create a copy of the original graph
        G_rewired = G.copy()
        
        # Calculate number of edge swaps to perform (typically |E| * rewiring_iterations)
        num_edge_swaps = len(G.edges()) * rewiring_iterations
        
        # Perform edge swaps using built-in NetworkX function
        # This preserves the degree distribution while randomizing connections
        nx.double_edge_swap(G_rewired, nswap=num_edge_swaps, max_tries=num_edge_swaps*10, seed=random.randint(1, 1000))
            
        # Calculate metrics
        rewired_homophily_scores.append(calculate_homophily_ratio(G_rewired, attribute))
        rewired_assortativity_scores.append(nx.attribute_assortativity_coefficient(G_rewired, attribute))

    results['rewired_homophily'] = np.mean(rewired_homophily_scores)
    results['rewired_assortativity'] = np.mean(rewired_assortativity_scores)
    log(f"Rewiring Model - Avg homophily: {results['rewired_homophily']:.4f}")
    log(f"Rewiring Model - Avg assortativity: {results['rewired_assortativity']:.4f}")

    # 2. Attribute Shuffling Model
    for i in range(num_iterations):
        if i > 0 and i % 10 == 0:
            log(f"  Running attribute shuffling iteration {i}/{num_iterations}")
        G_shuffle = G.copy()
        attr_values = list(nx.get_node_attributes(G, attribute).values())
        random.shuffle(attr_values)
        for i, node in enumerate(G_shuffle.nodes()):
            G_shuffle.nodes[node][attribute] = attr_values[i]
        attr_shuffled_homophily_scores.append(calculate_homophily_ratio(G_shuffle, attribute))
        attr_shuffled_assortativity_scores.append(nx.attribute_assortativity_coefficient(G_shuffle, attribute))

    results['attribute_shuffled_homophily'] = np.mean(attr_shuffled_homophily_scores)
    results['attribute_shuffled_assortativity'] = np.mean(attr_shuffled_assortativity_scores)
    log(f"Attribute Shuffling - Avg homophily: {results['attribute_shuffled_homophily']:.4f}")
    log(f"Attribute Shuffling - Avg assortativity: {results['attribute_shuffled_assortativity']:.4f}")

    # Statistical tests
    results['rewired_p_value'] = stats.ttest_1samp(rewired_homophily_scores, original_homophily).pvalue
    results['attr_p_value'] = stats.ttest_1samp(attr_shuffled_homophily_scores, original_homophily).pvalue
    log("\nStatistical significance (p-values):")
    log(f"Rewiring Model: {results['rewired_p_value']:.6f}")
    log(f"Attribute Shuffling: {results['attr_p_value']:.6f}")

    # Plot 1: Homophily Distribution
    plt.figure(figsize=(10, 6))
    plt.hist(rewired_homophily_scores, bins=30, alpha=0.6, label="Rewiring", color='skyblue', density=True)
    plt.hist(attr_shuffled_homophily_scores, bins=30, alpha=0.6, label="Attribute Shuffling", color='lightcoral', density=True)
    plt.axvline(original_homophily, color='red', linestyle='--', linewidth=2, label=f"Original ({original_homophily:.3f})")
    plt.legend(loc='upper right', fontsize=10)
    plt.title("Homophily Ratio Distribution", fontsize=14)
    plt.xlabel("Homophily Ratio", fontsize=12)
    plt.ylabel("Density", fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "homophily_distribution.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # Plot 2: Assortativity Distribution
    plt.figure(figsize=(10, 6))
    plt.hist(rewired_assortativity_scores, bins=30, alpha=0.6, label="Rewiring", color='lightgreen', density=True)
    plt.hist(attr_shuffled_assortativity_scores, bins=30, alpha=0.6, label="Attribute Shuffling", color='plum', density=True)
    plt.axvline(original_assortativity, color='darkblue', linestyle='--', linewidth=2, label=f"Original ({original_assortativity:.3f})")
    plt.legend(loc='upper right', fontsize=10)
    plt.title("Assortativity Coefficient Distribution", fontsize=14)
    plt.xlabel("Assortativity", fontsize=12)
    plt.ylabel("Density", fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "assortativity_distribution.png"), dpi=300, bbox_inches='tight')
    plt.close()

    
    # Plot comparison bar chart
    models = ['Original', 'Rewiring', 'Attr. Shuffling']
    homophily_values = [original_homophily, results['rewired_homophily'], results['attribute_shuffled_homophily']]
    assortativity_values = [original_assortativity, results['rewired_assortativity'], results['attribute_shuffled_assortativity']]
    
    x = np.arange(len(models))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, homophily_values, width, label='Homophily Ratio')
    rects2 = ax.bar(x + width/2, assortativity_values, width, label='Assortativity')
    
    ax.set_ylabel('Value')
    ax.set_title('Comparison of Network Metrics Across Models')
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.legend()
    
    # Add value labels on bars
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.3f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
    
    autolabel(rects1)
    autolabel(rects2)
    
    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, "metrics_comparison_bar.png"), dpi=300, bbox_inches='tight')
    plt.close()

    return results