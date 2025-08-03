import json
import networkx as nx
import matplotlib.pyplot as plt
import os
from collections import defaultdict

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def create_label_graph(processed_data_file):
    """Create network visualization based on artist's major label."""
    processed_data = load_json(processed_data_file)
    
    # Output directory
    output_dir = "graph_labels"
    os.makedirs(output_dir, exist_ok=True)
    
    G = nx.Graph()
    
    # Extract artists and their labels
    artist_to_label = {}
    all_artists = set()
    artists_with_multiple_labels = set()  # Track artists with multiple labels
    
    for entry in processed_data["data"]:
        artist_id = entry.get("artist_id")
        artist_name = entry.get("artist")
        
        if not artist_id or not artist_name:
            continue
        
        # Check if the artist has multiple major labels
        major_labels = entry.get("major_labels", [])
        if len(major_labels) > 1:
            print(f"Artist '{artist_name}' has multiple labels {major_labels}. Removing from the graph.")
            artists_with_multiple_labels.add(artist_name)
            continue  # Skip this artist
        
        # Default to 'Independent' if no label or major_labels is empty
        major_label = major_labels[0] if major_labels else "Independent"
        
        all_artists.add(artist_name)
        artist_to_label[artist_name] = major_label
    
    # Remove artists with multiple labels from the graph
    artists_to_remove = artists_with_multiple_labels
    
    # Add nodes with major_label attribute for artists not in the removal list
    for artist in all_artists:
        if artist not in artists_to_remove:
            label = artist_to_label.get(artist, "Independent")
            G.add_node(artist, major_label=label)
    
    # Process albums to find connections
    featured_connections = []
    for entry in processed_data["data"]:
        artist_name = entry.get("artist")
        main_artist = entry.get("artist")
        
        # Skip if the artist has multiple labels
        if artist_name in artists_to_remove:
            continue
        
        # Get featured artists
        for featured in entry.get("feat", []):
            if featured in all_artists and featured != main_artist and featured not in artists_to_remove:
                featured_connections.append((main_artist, featured))
    
    # Add edges from featured connections
    added_edges = set()
    for source, target in featured_connections:
        edge = tuple(sorted([source, target]))
        if edge not in added_edges:
            G.add_edge(source, target)
            added_edges.add(edge)
    
    # Count connected vs isolated nodes for reporting
    isolated_nodes = [node for node in G.nodes() if G.degree(node) == 0]
    connected_nodes = [node for node in G.nodes() if G.degree(node) > 0]
    
    # Print statistics to console - matching genre graph format
    label_counts = defaultdict(int)
    for n in G.nodes():
        label = G.nodes[n].get('major_label', 'Unknown')  # Use get() with default value to avoid KeyErrors
        label_counts[label] += 1
    
    print("\nArtist distribution by major label:")
    for label, count in label_counts.items():
        connected_count = len([n for n in connected_nodes if G.nodes[n].get('major_label', 'Unknown') == label])
        isolated_count = count - connected_count
        print(f"{label}: {count} artists ({count/len(G.nodes())*100:.1f}%) - {connected_count} connected, {isolated_count} isolated")
    
    edge_count = len(G.edges())
    node_count = len(G.nodes())
    print(f"\nNetwork has {node_count} artists total:")
    print(f"- {len(connected_nodes)} connected artists with {edge_count} direct collaborations")
    print(f"- {len(isolated_nodes)} isolated artists with no collaborations")
    
    # Save graph files
    nx.write_graphml(G, os.path.join(output_dir, "label_graph.graphml"))
    nx.write_gexf(G, os.path.join(output_dir, "label_graph.gexf"))
    
    # Visualization
    plt.figure(figsize=(20, 16))
    pos = nx.spring_layout(G, k=0.5, seed=42)
    
    # Generate colors based on labels
    import matplotlib.cm as cm
    unique_labels = sorted(set([G.nodes[n].get('major_label', 'Unknown') for n in G.nodes()]))
    colormap = cm.get_cmap('tab10', max(10, len(unique_labels)))
    
    # Draw nodes by label
    for i, label in enumerate(unique_labels):
        nodes_with_label = [n for n in G.nodes() if G.nodes[n].get('major_label', 'Unknown') == label]
        if nodes_with_label:
            # Draw connected nodes
            connected_with_label = [n for n in nodes_with_label if n in connected_nodes]
            if connected_with_label:
                nx.draw_networkx_nodes(
                    G, pos,
                    nodelist=connected_with_label,
                    node_size=300,
                    node_color=[colormap(i)] * len(connected_with_label),
                    alpha=0.9
                )
            
            # Draw isolated nodes
            isolated_with_label = [n for n in nodes_with_label if n in isolated_nodes]
            if isolated_with_label:
                nx.draw_networkx_nodes(
                    G, pos,
                    nodelist=isolated_with_label,
                    node_size=150,
                    node_color=[colormap(i)] * len(isolated_with_label),
                    alpha=0.6
                )
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.3)
    
    # Draw labels for connected nodes only to reduce clutter
    node_labels = {n: n for n in connected_nodes}
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=9)
    
    # Add legend for major labels
    legend_elements = []
    for label in unique_labels:
        label_count = len([n for n in G.nodes() if G.nodes[n].get('major_label', 'Unknown') == label])
        if label_count > 0:
            legend_elements.append(
                plt.Line2D([0], [0], marker='o', color='w', 
                          markerfacecolor=colormap(list(unique_labels).index(label)), 
                          markersize=10, label=f"{label} ({label_count})")
            )
    
    # Add legend for connected vs isolated nodes
    legend_elements.extend([  
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black', 
                  markersize=10, alpha=0.9, label='Connected Artist'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black', 
                  markersize=7, alpha=0.6, label='Isolated Artist')
    ])
    
    plt.legend(handles=legend_elements, loc='lower center', 
               bbox_to_anchor=(0.5, -0.08), ncol=min(4, len(legend_elements)))
    
    plt.title("Artist Collaboration Network by Label", fontsize=16)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "label_graph.png"), dpi=300, bbox_inches='tight')
    
    # Save statistics - matching the genre graph format
    with open(os.path.join(output_dir, "network_stats.txt"), "w") as f:
        f.write("ARTIST COLLABORATION NETWORK STATISTICS\n")
        f.write("=====================================\n\n")
        
        # Count artists per label
        label_counts = defaultdict(int)
        for node in G.nodes():
            label = G.nodes[node].get('major_label', 'Unknown')
            label_counts[label] += 1
        
        f.write("Artist distribution by major label:\n")
        for label, count in label_counts.items():
            connected_count = len([n for n in connected_nodes if G.nodes[n].get('major_label') == label])
            isolated_count = count - connected_count
            f.write(f"{label}: {count} artists ({count/len(G.nodes())*100:.1f}%) - {connected_count} connected, {isolated_count} isolated\n")
        
        f.write(f"\nNetwork has {len(G.nodes())} artists total:\n")
        f.write(f"- {len(connected_nodes)} connected artists with {len(G.edges())} direct collaborations\n")
        f.write(f"- {len(isolated_nodes)} isolated artists with no collaborations\n")
    
    # Print only the file information, not the analysis
    print("""
    Files saved to graph_labels/ folder:
    1. label_graph.graphml - GraphML format with ALL artists
    2. label_graph.gexf - GEXF format with ALL artists
    3. label_graph.png - Visualization of ALL artists 
    4. network_stats.txt - Network statistics
    """)
    
    return G

if __name__ == "__main__":
    import sys
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'data/all_genres_post_2023-01-01_albums.json'
    print(f"Using input file: {input_file}")
    create_label_graph(input_file)
