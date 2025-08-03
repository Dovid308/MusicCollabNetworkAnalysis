"""
Homophily Analysis Module - Functions to analyze homophily patterns in networks
"""
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter, defaultdict
import os
import copy

def calculate_homophily_ratio(G, attribute):
    """
    Calculate the homophily ratio based on an attribute.
    
    Args:
        G (networkx.Graph): The network graph
        attribute (str): Node attribute to analyze
        
    Returns:
        float: Homophily ratio (proportion of edges connecting nodes with the same attribute)
    """
    if len(G.edges()) == 0:
        return 0
    
    same_attr_edges = sum(1 for u, v in G.edges() 
                         if attribute in G.nodes[u] and attribute in G.nodes[v] 
                         and G.nodes[u][attribute] == G.nodes[v][attribute])
    
    return same_attr_edges / len(G.edges())

def blau_index(G, node, attribute):
    """
    Calculate Blau's Heterogeneity Index for a node's neighborhood.
    
    Args:
        G (networkx.Graph): The network graph
        node: The node to analyze
        attribute (str): Node attribute to analyze
        
    Returns:
        float: Blau's Heterogeneity Index value
    """
    neighbors = list(G.neighbors(node))
    if not neighbors:
        return 0
    
    attr_values = [G.nodes[n][attribute] for n in neighbors 
                  if attribute in G.nodes[n]]
    
    if not attr_values:
        return 0
    
    counts = Counter(attr_values)
    prop_squared_sum = sum((count / len(attr_values))**2 for count in counts.values())
    
    return 1 - prop_squared_sum

def create_mixing_matrix(G, attribute):
    """
    Create a mixing matrix showing connections between attribute values.
    
    Args:
        G (networkx.Graph): The network graph
        attribute (str): Node attribute to analyze
        
    Returns:
        pandas.DataFrame: Mixing matrix
    """
    # Get all unique attribute values
    attr_values = sorted(set(val for node in G.nodes() 
                            if attribute in G.nodes[node]
                            for val in [G.nodes[node][attribute]]))
    
    # Initialize matrix with zeros
    matrix = pd.DataFrame(0, index=attr_values, columns=attr_values)
    
    # Count edges between attribute values
    for u, v in G.edges():
        if attribute not in G.nodes[u] or attribute not in G.nodes[v]:
            continue
            
        u_attr = G.nodes[u][attribute]
        v_attr = G.nodes[v][attribute]
        
        matrix.loc[u_attr, v_attr] += 1
        if u_attr != v_attr:  # Count each edge only once if attributes differ
            matrix.loc[v_attr, u_attr] += 1
    
    return matrix

def calculate_ei_indices(G, attribute):
    """
    Calculate E-I index for each attribute value.
    
    Args:
        G (networkx.Graph): The network graph
        attribute (str): Node attribute to analyze
        
    Returns:
        dict: E-I index for each attribute value
    """
    attr_values = set(G.nodes[n][attribute] for n in G.nodes() 
                     if attribute in G.nodes[n])
    ei_indices = {}
    
    for attr_val in attr_values:
        nodes_with_attr = [n for n in G.nodes() 
                          if attribute in G.nodes[n] and G.nodes[n][attribute] == attr_val]
        
        if not nodes_with_attr:
            continue
        
        internal_edges = 0
        external_edges = 0
        
        for u in nodes_with_attr:
            for v in G.neighbors(u):
                if attribute not in G.nodes[v]:
                    continue
                    
                if G.nodes[v][attribute] == attr_val:
                    internal_edges += 1
                else:
                    external_edges += 1
        
        # Each internal edge is counted twice
        internal_edges = internal_edges / 2
        
        if internal_edges + external_edges == 0:
            ei_indices[attr_val] = 0
        else:
            ei_indices[attr_val] = (external_edges - internal_edges) / (external_edges + internal_edges)
    
    return ei_indices

def log_line(text, log_path):
    if log_path:
        with open(log_path, "a") as f:
            f.write(str(text) + "\n")

            
def homophily_analysis(G, attribute, output_dir="analysis_results", log_path=None):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    log_line("\n--- Homophily Analysis ---", log_path)
    results = {}

    # Directly analyze the graph without filtering ambiguous nodes
    hr_original = calculate_homophily_ratio(G, attribute)
    results['homophily_ratio'] = hr_original
    log_line(f"Homophily Ratio (original): {hr_original:.4f}", log_path)

    blau_indices = {node: blau_index(G, node, attribute) for node in G.nodes()
                    if any(attribute in G.nodes[n] for n in G.neighbors(node))}
    if blau_indices:
        avg_blau = sum(blau_indices.values()) / len(blau_indices)
        results['blau_indices'] = blau_indices
        results['avg_blau_index'] = avg_blau
        log_line(f"Average Blau's Heterogeneity Index: {avg_blau:.4f}", log_path)

    mixing_matrix = create_mixing_matrix(G, attribute)
    results['mixing_matrix'] = mixing_matrix

    log_line("\nMixing Matrix:", log_path)
    log_line(mixing_matrix, log_path)  # Print the full mixing matrix

    ei_indices = calculate_ei_indices(G, attribute)
    results['ei_indices'] = ei_indices

    log_line(f"\nE-I Index by {attribute.capitalize()}:", log_path)
    for val, idx in sorted(ei_indices.items(), key=lambda x: x[1]):
        log_line(f"  {val}: {idx:.4f}", log_path)

    plt.figure(figsize=(12, 6))
    plot_values = []
    plot_indices = []
    for val, idx in sorted(ei_indices.items(), key=lambda x: x[1]):
        plot_values.append(val)
        plot_indices.append(idx)

    plt.bar(plot_values, plot_indices)
    plt.axhline(y=0, color='r', linestyle='-', alpha=0.3)
    plt.title(f"E-I Index by {attribute.capitalize()}")
    plt.xlabel(attribute.capitalize())
    plt.ylabel("E-I Index")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"ei_index_{attribute}.png"), dpi=300, bbox_inches='tight')
    plt.close()

    try:
        assortativity = nx.attribute_assortativity_coefficient(G, attribute)
        results['assortativity'] = assortativity
        log_line(f"\nAttribute Assortativity Coefficient: {assortativity:.4f}", log_path)
    except:
        results['assortativity'] = None
        log_line("Could not calculate assortativity coefficient", log_path)

    return results
