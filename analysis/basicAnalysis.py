"""
Basic Network Analysis Module - Unified Output Version
Writes all stats to a single file and plots selected figures.
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import os

def analyze_network(G, attribute=None, output_dir="analysis_results"):
    """
    Perform basic and summary analysis on a network graph.

    Args:
        G (networkx.Graph): The graph to analyze.
        attribute (str, optional): Node attribute to analyze (e.g., 'club').
        output_dir (str): Directory to store analysis results.

    Returns:
        dict: Summary statistics.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, "network_analysis.txt")
    results = {}

    with open(output_path, "w") as f:
        f.write("NETWORK ANALYSIS REPORT\n")
        f.write("=" * 60 + "\n\n")

        # Basic Info
        num_nodes = len(G)
        num_edges = len(G.edges())
        density = nx.density(G)
        avg_clustering = nx.average_clustering(G)

        results.update({
            "num_nodes": num_nodes,
            "num_edges": num_edges,
            "density": density,
            "avg_clustering": avg_clustering,
        })

        f.write("Basic Information:\n")
        f.write(f"- Nodes: {num_nodes}\n")
        f.write(f"- Edges: {num_edges}\n")
        f.write(f"- Density: {density:.6f}\n")
        f.write(f"- Average Clustering Coefficient: {avg_clustering:.4f}\n\n")

        # Degree stats
        degrees = [d for _, d in G.degree()]
        avg_degree = np.mean(degrees)
        median_degree = np.median(degrees)
        stdev_degree = np.std(degrees)
        min_degree = min(degrees)
        max_degree = max(degrees)

        results.update({
            "avg_degree": avg_degree,
            "median_degree": median_degree,
            "stdev_degree": stdev_degree,
            "min_degree": min_degree,
            "max_degree": max_degree,
        })

        f.write("Degree Statistics:\n")
        f.write(f"- Average Degree: {avg_degree:.2f}\n")
        f.write(f"- Median Degree: {median_degree:.2f}\n")
        f.write(f"- Std Dev Degree: {stdev_degree:.2f}\n")
        f.write(f"- Min Degree: {min_degree}\n")
        f.write(f"- Max Degree: {max_degree}\n\n")

        # Degree Distribution Plot
        plt.figure(figsize=(8, 6))
        plt.hist(degrees, bins=20, alpha=0.7)
        plt.title("Degree Distribution")
        plt.xlabel("Degree")
        plt.ylabel("Count")
        plt.grid(True, alpha=0.3)
        plt.savefig(os.path.join(output_dir, "degree_distribution.png"), dpi=300, bbox_inches='tight')
        plt.close()

        # Component analysis
        components = list(nx.connected_components(G))
        largest_cc = max(components, key=len)
        largest_subgraph = G.subgraph(largest_cc)

        num_components = len(components)
        largest_size = len(largest_cc)
        largest_ratio = largest_size / num_nodes

        results.update({
            "num_components": num_components,
            "largest_component_size": largest_size,
            "largest_component_ratio": largest_ratio,
        })

        f.write("Component Analysis:\n")
        f.write(f"- Connected Components: {num_components}\n")
        f.write(f"- Largest Component Size: {largest_size}\n")
        f.write(f"- Largest Component Ratio: {largest_ratio:.2%}\n\n")

        # Path metrics
        if nx.is_connected(G):
            avg_path_length = nx.average_shortest_path_length(G)
            diameter = nx.diameter(G)

            results["avg_path_length"] = avg_path_length
            results["diameter"] = diameter

            f.write("Path Metrics (Whole Graph):\n")
            f.write(f"- Average Path Length: {avg_path_length:.4f}\n")
            f.write(f"- Diameter: {diameter}\n\n")
        else:
            avg_path_length = nx.average_shortest_path_length(largest_subgraph)
            diameter = nx.diameter(largest_subgraph)

            results["avg_path_length_lcc"] = avg_path_length
            results["diameter_lcc"] = diameter

            f.write("Path Metrics (Largest Component):\n")
            f.write(f"- Average Path Length: {avg_path_length:.4f}\n")
            f.write(f"- Diameter: {diameter}\n\n")

        # Optional Attribute Distribution
        if attribute and all(attribute in G.nodes[n] for n in G.nodes()):
            attr_values = [G.nodes[n][attribute] for n in G.nodes()]
            attr_counts = Counter(attr_values)
            results['attribute_counts'] = dict(attr_counts)

            f.write(f"{attribute.capitalize()} Distribution:\n")
            for val, count in attr_counts.most_common():
                percent = (count / num_nodes) * 100
                f.write(f"- {val}: {count} ({percent:.2f}%)\n")
            f.write("\n")

            # Bar plot of top values
            top_vals = [v for v, _ in attr_counts.most_common(15)]
            top_counts = [attr_counts[v] for v in top_vals]

            plt.figure(figsize=(10, 6))
            plt.bar(top_vals, top_counts)
            plt.title(f"{attribute.capitalize()} Distribution")
            plt.xlabel(attribute.capitalize())
            plt.ylabel("Count")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f"{attribute}_distribution.png"), dpi=300, bbox_inches='tight')
            plt.close()

    return results
