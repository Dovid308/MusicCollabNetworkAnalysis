import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import os
import matplotlib.cm as cm
import matplotlib.colors as mcolors

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def create_genre_graph(processed_data_file):
    """Create network visualization based on artist's artist_genre but saved as main_genre in graph attributes."""
    processed_data = load_json(processed_data_file)

    # Output directory
    output_dir = "graph_genre"
    os.makedirs(output_dir, exist_ok=True)

    G = nx.Graph()

    artist_to_attr = {}
    all_artists = set()
    albums = []

    for entry in processed_data["data"]:
        artist_name = entry.get("artist")
        if not artist_name:
            continue

        all_artists.add(artist_name)

        # Use artist_genre field, but save it under the name "main_genre" in the graph
        artist_genre = entry.get("artist_genre", "Unknown")
        artist_to_attr[artist_name] = artist_genre

        albums.append({
            "artist": artist_name,
            "feat": entry.get("feat", [])
        })

    # Add nodes with attribute 'main_genre'
    for artist in all_artists:
        genre = artist_to_attr.get(artist, "Unknown")
        G.add_node(artist, main_genre=genre)

    # Add edges
    added_edges = set()
    for album in albums:
        principal = album["artist"]
        for featured in album["feat"]:
            if featured in all_artists and featured != principal:
                edge = tuple(sorted([principal, featured]))
                if edge not in added_edges:
                    G.add_edge(principal, featured)
                    added_edges.add(edge)

    # Save graph files
    nx.write_graphml(G, os.path.join(output_dir, "genre_graph.graphml"))
    nx.write_gexf(G, os.path.join(output_dir, "genre_graph.gexf"))

    # Visualization
    plt.figure(figsize=(20, 16))
    pos = nx.spring_layout(G, k=0.5, seed=42)

    # Get the unique genres and create a colormap
    genres = sorted(set(nx.get_node_attributes(G, "main_genre").values()))
    colormap = cm.get_cmap("tab20", len(genres))
    genre_to_color = {genre: mcolors.to_hex(colormap(i)) for i, genre in enumerate(genres)}

    for genre in genres:
        nodes = [n for n in G.nodes() if G.nodes[n]['main_genre'] == genre]
        nx.draw_networkx_nodes(
            G, pos,
            nodelist=nodes,
            node_size=300,
            node_color=genre_to_color[genre],
            label=genre
        )

    # Draw edges and labels
    nx.draw_networkx_edges(G, pos, width=1.0, edge_color='gray', alpha=0.6)
    labels = {n: n for n in G.nodes() if G.degree(n) > 0}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=9)

    # Legend
    plt.legend(scatterpoints=1, loc='lower center', bbox_to_anchor=(0.5, -0.1), 
               ncol=min(4, len(genres)), fontsize=9)

    plt.title("Artist Collaboration Network by Genre", fontsize=16)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "genre_graph.png"), dpi=300, bbox_inches='tight')

    # Save basic stats
    with open(os.path.join(output_dir, "network_stats.txt"), "w") as f:
        f.write("ARTIST GENRE NETWORK STATISTICS\n")
        f.write("===============================\n")
        f.write(f"Total artists: {len(G.nodes())}\n")
        f.write(f"Total collaborations: {len(G.edges())}\n")

    print("Genre-based network created and saved to:", output_dir)
    return G

if __name__ == "__main__":
    create_genre_graph('data/all_genres_post_2023-01-01_albums.json')
