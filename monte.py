import networkx as nx
import random
import csv

def monte_carlo_sample(graph, sample_size):
    if sample_size > graph.number_of_nodes():
        raise ValueError("Sample size cannot be larger than the number of nodes in the graph.")
    
    sampled_nodes = random.sample(graph.nodes(), sample_size)
    return sampled_nodes

def save_nodes_to_csv(nodes, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Node"])
        for node in nodes:
            writer.writerow([node])

#加载图
file_path = "facebook_combined.txt/facebook_combined.txt"
facebook_combined_graph = nx.read_edgelist(file_path, nodetype=int)

#从图中抽取 5000 个结点
sample_size = 5000
sampled_nodes = monte_carlo_sample(facebook_combined_graph, sample_size)

output_file = "sampled_nodes.csv"
save_nodes_to_csv(sampled_nodes, output_file)

print(f"Sampled {sample_size} nodes and saved to {output_file}")