import networkx as nx
import matplotlib.pyplot as plt

def load_combined_facebook_data(file_path):
    G = nx.read_edgelist(file_path, nodetype=int)
    print(f"Loaded combined graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    return G

def analyze_visualize(graph):
    print(f"Number of nodes: {graph.number_of_nodes()}")
    print(f"Number of edges: {graph.number_of_edges()}")
    
    connected_components = list(nx.connected_components(graph))
    num_components = len(connected_components)
    print(f"Number of connected components: {num_components}")
    
    largest_component = max(connected_components, key=len)
    print(f"Largest connected component size: {len(largest_component)}")
    
    if nx.is_connected(graph):
        avg_path_length = nx.average_shortest_path_length(graph)
        print(f"Average path length: {avg_path_length}")
    else:
        print("The graph is not connected, skipping average path length calculation.")
    
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(graph, seed=42)
    nx.draw(
        graph, pos, node_size=10, edge_color="gray", alpha=0.7, with_labels=False
    )
    plt.title("Visualization of Combined Facebook Graph")
    plt.show()

file_path = "facebook_combined.txt/facebook_combined.txt"
facebook_combined_graph = load_combined_facebook_data(file_path)
analyze_visualize(facebook_combined_graph)