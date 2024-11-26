import networkx as nx
import matplotlib.pyplot as plt

def load_combined_facebook_data(file_path):
    """
    加载 combined Facebook 网络数据
    :param file_path: 文件路径 (facebook_combined.txt.gz)
    :return: NetworkX 图对象
    """
    G = nx.read_edgelist(file_path, nodetype=int)
    print(f"Loaded combined graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    return G

def analyze_and_visualize_graph(graph):
    """
    分析图的连通性并进行可视化
    :param graph: NetworkX 图对象
    """
    # 输出基础信息
    print(f"Number of nodes: {graph.number_of_nodes()}")
    print(f"Number of edges: {graph.number_of_edges()}")
    
    # 检查连通分量
    connected_components = list(nx.connected_components(graph))
    num_components = len(connected_components)
    print(f"Number of connected components: {num_components}")
    
    # 获取最大连通分量
    largest_component = max(connected_components, key=len)
    print(f"Largest connected component size: {len(largest_component)}")
    
    # 平均路径长度（仅适用于连通图）
    if nx.is_connected(graph):
        avg_path_length = nx.average_shortest_path_length(graph)
        print(f"Average path length: {avg_path_length}")
    else:
        print("The graph is not connected, skipping average path length calculation.")
    
    # 可视化图
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(graph, seed=42)  # 使用 spring 布局
    nx.draw(
        graph, pos, node_size=10, edge_color="gray", alpha=0.7, with_labels=False
    )
    plt.title("Visualization of Combined Facebook Graph")
    plt.show()

# 加载图并分析
file_path = "facebook_combined.txt/facebook_combined.txt"  # 修改为实际文件路径
facebook_combined_graph = load_combined_facebook_data(file_path)
analyze_and_visualize_graph(facebook_combined_graph)