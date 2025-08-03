"""
Graph Loader - Utility functions for loading and validating network graphs
"""
import networkx as nx
import os

def load_graph(path):
    """
    Load a network graph from various file formats.
    
    Args:
        path (str): Path to the graph file
        
    Returns:
        networkx.Graph or None: The loaded graph, or None if loading failed
    """
    try:
        # Try GraphML format first
        G = nx.read_graphml(path)
        print(f"Graph loaded successfully with {len(G.nodes())} nodes and {len(G.edges())} edges.")
        return G
    except Exception as e:
        print(f"Error loading GraphML: {e}")
        try:
            # Try GEXF format as fallback
            gexf_path = path.replace('.graphml', '.gexf')
            G = nx.read_gexf(gexf_path)
            print(f"Graph loaded successfully with {len(G.nodes())} nodes and {len(G.edges())} edges.")
            return G
        except Exception as e2:
            print(f"Error loading GEXF: {e2}")
            # Try other formats if needed
            try:
                # Try GML format
                gml_path = path.replace('.graphml', '.gml')
                G = nx.read_gml(gml_path)
                print(f"Graph loaded successfully with {len(G.nodes())} nodes and {len(G.edges())} edges.")
                return G
            except Exception as e3:
                print(f"Error loading graph: all supported formats failed.")
                return None

def validate_graph(G, required_attribute=None):
    """
    Validate that the graph has the expected structure and attributes.
    
    Args:
        G (networkx.Graph): The graph to validate
        required_attribute (str, optional): Name of an attribute that should exist on nodes
        
    Returns:
        bool: True if valid, False otherwise
    """
    if G is None:
        print("Error: Graph is None")
        return False
    
    if len(G.nodes()) == 0:
        print("Error: Graph has no nodes")
        return False
    
    if len(G.edges()) == 0:
        print("Warning: Graph has no edges")
    
    if required_attribute:
        # Check if all nodes have the required attribute
        nodes_with_attr = sum(1 for n in G.nodes() if required_attribute in G.nodes[n])
        if nodes_with_attr < len(G.nodes()):
            print(f"Warning: {len(G.nodes()) - nodes_with_attr} nodes are missing the '{required_attribute}' attribute")
            return False
    
    return True

def ensure_output_directory(directory="analysis_results"):
    """Create output directory if it doesn't exist"""
    os.makedirs(directory, exist_ok=True)
    return directory