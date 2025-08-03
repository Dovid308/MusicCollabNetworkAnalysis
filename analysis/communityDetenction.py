from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import seaborn as sns
from sklearn.metrics import normalized_mutual_info_score as normalized_mutual_information_score
from sklearn.metrics import adjusted_rand_score
import community as community_louvain
import os
import matplotlib.patches as mpatches
import numpy as np


def plot_stacked_bar_chart(composition_df, communities_to_plot, community_sizes, attribute, attr_values, output_dir):
    """
    Create a fixed stacked bar chart without gaps between segments.
    """
    # Limit to top communities for visibility
    max_communities_to_plot = 15
    top_communities = communities_to_plot[:max_communities_to_plot]
    
    # Create a pivot table for stacked bar chart
    pivot_for_stacked = composition_df.pivot_table(
        index='Community', 
        columns='Attribute', 
        values='Percentage',
        fill_value=0
    ).loc[top_communities]
    
    # Convert to the format needed for stacked bars
    stacked_df = pivot_for_stacked.T  # Transpose so attributes are rows
    
    # Create figure
    plt.figure(figsize=(max(12, len(top_communities) * 0.8), 8))
    
    # Choose colormap
    if len(attr_values) <= 10:
        cmap = plt.cm.tab10
    elif len(attr_values) <= 20:
        cmap = plt.cm.tab20
    else:
        cmap = plt.cm.viridis
    
    # Attribute to color mapping
    attr_colors = {attr: cmap(i / max(1, len(attr_values) - 1)) 
                   for i, attr in enumerate(attr_values)}
    
    # Plot bars
    bottom = np.zeros(len(top_communities))
    for attr in attr_values:
        if attr in stacked_df.index:
            values = stacked_df.loc[attr, top_communities].values
            plt.bar(
                range(len(top_communities)),
                values,
                bottom=bottom,
                label=attr,
                color=attr_colors[attr],
                edgecolor='white',
                linewidth=0.5
            )
            bottom += values

    # Formatting
    attribute_label = "Genre" if attribute == "main_genre" else "Label"
    plt.xlabel("Community")
    plt.ylabel("Percentage (%)")
    plt.title(f"Composition of Top Communities by {attribute_label} (%)")
    plt.xticks(
        range(len(top_communities)),
        [f"Comm {c}\n(n={community_sizes[c]})" for c in top_communities],
        rotation=45
    )
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.yticks([0, 25, 50, 75, 100])
    plt.ylim(0, 100)
    plt.legend(title=attribute_label, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "community_stacked_bar_percent_fixed.png"), 
                dpi=300, bbox_inches='tight')
    plt.close()


def community_detection(G, attribute='main_genre', output_dir="analysis_results", log_path=None):
    """Detect communities in artist graph, compare with attribute, and visualize results."""
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    def log(message):
        if log_path:
            with open(log_path, "a") as f:
                f.write(message + "\n")

    log("\n--- Community Detection ---")

    # Attribute config
    if attribute == "main_genre":
        attribute_label = "Genre"
        communities_plot_filename = "genre_communities.png"
        composition_title = "Genre Composition of Louvain Communities"
        composition_xlabel = "Genre"
    elif attribute == "major_label":
        attribute_label = "Label"
        communities_plot_filename = "label_communities.png"
        composition_title = "Label Composition of Louvain Communities"
        composition_xlabel = "Label"
    else:
        log(f"Error: Unsupported attribute '{attribute}'")
        print(f"Unsupported attribute '{attribute}' in community_detection")
        return

    # Ensure undirected and connected
    if hasattr(G, 'is_directed') and G.is_directed():
        G = G.to_undirected()

    if not nx.is_connected(G):
        largest_cc = max(nx.connected_components(G), key=len)
        G = G.subgraph(largest_cc).copy()
        log(f"Using largest connected component with {len(G.nodes())} nodes")
    else:
        log("Using full graph (connected)")

    # Attribute communities
    node_to_attr_community = {node: G.nodes[node][attribute] for node in G.nodes()}
    attr_values = sorted(set(node_to_attr_community.values()))
    attr_to_community = {attr: i for i, attr in enumerate(attr_values)}
    attr_communities = {node: attr_to_community[node_to_attr_community[node]] for node in G.nodes()}

    # Louvain detection
    louvain_communities = community_louvain.best_partition(G)
    log(f"Number of attribute-based communities: {len(set(attr_communities.values()))}")
    log(f"Number of Louvain-detected communities: {len(set(louvain_communities.values()))}")

    # Evaluation metrics
    nodes_sorted = sorted(G.nodes())
    attr_membership = [attr_communities[node] for node in nodes_sorted]
    louvain_membership = [louvain_communities[node] for node in nodes_sorted]

    nmi = normalized_mutual_information_score(attr_membership, louvain_membership)
    ari = adjusted_rand_score(attr_membership, louvain_membership)
    log(f"Normalized Mutual Information (NMI): {nmi:.4f}")
    log(f"Adjusted Rand Index (ARI): {ari:.4f}")

    # Modularity
    def calc_modularity(communities): return community_louvain.modularity(communities, G)
    attr_modularity = calc_modularity(attr_communities)
    louvain_modularity = calc_modularity(louvain_communities)
    log(f"Modularity of attribute-based partition: {attr_modularity:.4f}")
    log(f"Modularity of Louvain partition: {louvain_modularity:.4f}")

    # Graph layout
    pos = nx.spring_layout(G, seed=42)

    # Plot attribute communities
    color_map = {val: plt.cm.tab20(i / max(1, len(attr_values))) for i, val in enumerate(attr_values)}
    node_colors_attr = [color_map[node_to_attr_community[node]] for node in G.nodes()]
    plt.figure(figsize=(12, 10))
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    nx.draw_networkx_nodes(G, pos, node_color=node_colors_attr, node_size=50)
    patches = [mpatches.Patch(color=color_map[val], label=val) for val in attr_values]
    plt.legend(handles=patches, title=attribute_label, loc='best', fontsize='small')
    plt.title(f"Artist Network - {attribute_label} Communities")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, communities_plot_filename), dpi=300, bbox_inches='tight')
    plt.close()

    # Plot Louvain communities
    plt.figure(figsize=(12, 10))
    unique_communities = sorted(set(louvain_communities.values()))
    community_to_color = {comm: plt.cm.tab20(i / max(1, len(unique_communities))) for i, comm in enumerate(unique_communities)}
    node_colors_louvain = [community_to_color[louvain_communities[node]] for node in G.nodes()]
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    nx.draw_networkx_nodes(G, pos, node_color=node_colors_louvain, node_size=50)
    patches = [mpatches.Patch(color=community_to_color[c], label=f"Community {c}") for c in unique_communities]
    plt.legend(handles=patches, title="Louvain Community", loc='best', fontsize='small')
    plt.title("Artist Network - Louvain Communities")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "louvain_communities.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # Analyze community composition
    def analyze_community_composition(G, communities, attribute):
        counts = defaultdict(lambda: defaultdict(int))
        for node in G.nodes():
            comm = communities[node]
            attr_val = G.nodes[node][attribute]
            counts[comm][attr_val] += 1
        rows = []
        for comm, attr_counts in counts.items():
            total = sum(attr_counts.values())
            for attr_val, count in attr_counts.items():
                rows.append({
                    'Community': comm,
                    'Attribute': attr_val,
                    'Count': count,
                    'Percentage': count / total * 100
                })
        return pd.DataFrame(rows)

    composition_df = analyze_community_composition(G, louvain_communities, attribute)
    community_sizes = Counter(louvain_communities.values())
    communities_to_plot = [comm for comm, _ in community_sizes.most_common()]

    # Heatmap
    pivot = composition_df.pivot_table(index='Community', columns='Attribute', values='Percentage', fill_value=0)
    pivot = pivot.reindex(communities_to_plot)
    fig_width = max(14, pivot.shape[1] * 0.7)
    fig_height = max(12, pivot.shape[0] * 0.4)
    plt.figure(figsize=(fig_width, fig_height))
    show_annotations = pivot.shape[0] * pivot.shape[1] <= 500
    sns.heatmap(
        pivot, 
        annot=show_annotations,
        fmt=".1f" if show_annotations else "",
        cmap="viridis",
        linewidths=0.5,
        cbar_kws={'label': 'Percentage (%)'}
    )
    plt.title(composition_title)
    plt.xlabel(composition_xlabel)
    plt.ylabel("Community ID")
    plt.xticks(rotation=45, ha='right')
    if pivot.shape[0] > 20:
        step = max(1, pivot.shape[0] // 20)
        plt.yticks(
            range(0, pivot.shape[0], step),
            [pivot.index[i] for i in range(0, pivot.shape[0], step)]
        )
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "community_composition_full.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # Stacked bar chart using helper function
    plot_stacked_bar_chart(
        composition_df=composition_df,
        communities_to_plot=communities_to_plot,
        community_sizes=community_sizes,
        attribute=attribute,
        attr_values=attr_values,
        output_dir=output_dir
    )

    return {
        'nmi': nmi,
        'ari': ari,
        'attr_modularity': attr_modularity,
        'louvain_modularity': louvain_modularity,
        'attr_communities': attr_communities,
        'louvain_communities': louvain_communities,
        'community_composition': composition_df
    }
