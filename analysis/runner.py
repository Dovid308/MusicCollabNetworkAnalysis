# analysis_runner.py

import os
import sys
from graphLoader import load_graph, validate_graph, ensure_output_directory
from basicAnalysis import analyze_network
from homophily import homophily_analysis
from nullModel import null_model_analysis
from communityDetenction import community_detection

def run_analysis(graph_path, attribute):
    if attribute == "main_genre":
        subfolder = "genre"
    elif attribute == "major_label":
        subfolder = "labels"
    else:
        print(f"Error: Unsupported attribute '{attribute}'. Use 'main_genre' or 'major_label'.")
        return

    output_dir = ensure_output_directory(os.path.join("analysis_results", subfolder))
    log_path = os.path.join(output_dir, "network_analysis.txt")

    G = load_graph(graph_path)
    if not validate_graph(G, required_attribute=attribute):
        print("Graph validation failed. Exiting.")
        return

    analyze_network(G, attribute=attribute, output_dir=output_dir)
    homophily_analysis(G, attribute=attribute, output_dir=output_dir, log_path=log_path)
    null_model_analysis(G, attribute=attribute, output_dir=output_dir, log_path=log_path)
    community_detection(G, attribute=attribute, output_dir=output_dir, log_path=log_path)

    print(f"\nAnalysis complete for attribute '{attribute}'. Results saved to: {output_dir}")


if __name__ == "__main__":
    def get_graph_path(attribute):
        if attribute == "main_genre":
            return "../graph_genre/genre_graph.graphml"
        elif attribute == "major_label":
            return "../graph_labels/label_graph.graphml"
        else:
            return None

    if len(sys.argv) == 2:
        attribute = sys.argv[1]
        graph_file = get_graph_path(attribute)
        if graph_file:
            run_analysis(graph_file, attribute)
        else:
            print(f"Error: Unsupported attribute '{attribute}'. Use 'main_genre' or 'major_label'.")
            sys.exit(1)

    elif len(sys.argv) == 1:
        print("No attribute specified. Running analysis for both 'main_genre' and 'major_label'.\n")
        run_analysis(get_graph_path("main_genre"), "main_genre")
        run_analysis(get_graph_path("major_label"), "major_label")

    else:
        print("Usage: python runner.py [attribute]")
        print("Accepted attributes: 'main_genre', 'major_label'")
        sys.exit(1)