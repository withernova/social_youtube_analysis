import random
import numpy as np
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
# 定义用户状态
SUSCEPTIBLE = "S"
INFECTIOUS = "I"
PERMANENT = "P"

def initialize_states(graph, initial_spreaders=5):
    """
    初始化网络中每个节点的状态
    :param graph: NetworkX 图
    :param initial_spreaders: 初始传播者数量
    :return: 节点状态字典
    """
    states = {node: SUSCEPTIBLE for node in graph.nodes}
    spreaders = random.sample(list(graph.nodes), initial_spreaders)  # 随机选择初始传播者
    for spreader in spreaders:
        states[spreader] = INFECTIOUS
    return states

def simulate_propagation(graph, share_probability_mean, gamma=0.5, time_steps=10):
    """
    模拟传播过程
    :param graph: NetworkX 图
    :param share_probability_mean: 平均分享概率
    :param gamma: 感染者变为永久状态的概率
    :param time_steps: 模拟的时间步数
    :return: 每个状态的节点数量随时间变化
    """
    # 初始化节点状态
    node_states = {node: SUSCEPTIBLE for node in graph.nodes}
    initial_spreaders = 5  # 初始传播者数量
    spreaders = random.sample(list(graph.nodes), initial_spreaders)
    for spreader in spreaders:
        node_states[spreader] = INFECTIOUS

    # 记录状态数量
    state_counts = {SUSCEPTIBLE: [], INFECTIOUS: [], PERMANENT: []}

    for t in range(time_steps):
        new_states = node_states.copy()

        for node in graph.nodes:
            if node_states[node] == SUSCEPTIBLE:
                # 易感者被感染的概率
                if any(node_states[neighbor] == INFECTIOUS for neighbor in graph.neighbors(node)):
                    if random.random() < share_probability_mean:
                        new_states[node] = INFECTIOUS

            elif node_states[node] == INFECTIOUS:
                # 感染者变为永久状态的概率
                if random.random() < gamma:
                    new_states[node] = PERMANENT

        # 更新状态
        node_states = new_states

        # 记录每个状态的节点数量
        state_counts[SUSCEPTIBLE].append(sum(1 for s in node_states.values() if s == SUSCEPTIBLE))
        state_counts[INFECTIOUS].append(sum(1 for s in node_states.values() if s == INFECTIOUS))
        state_counts[PERMANENT].append(sum(1 for s in node_states.values() if s == PERMANENT))

    return state_counts


file_path = "facebook_combined.txt/facebook_combined.txt"  # 修改为实际文件路径
facebook_combined_graph = load_combined_facebook_data(file_path)
# 模拟传播
share_probability_mean = 0.1  # 设置分享概率均值
state_counts = simulate_propagation(
    facebook_combined_graph, share_probability_mean, gamma=0.5, time_steps=50
)

# 绘制传播规模图
plt.figure(figsize=(50, 6))
plt.plot(state_counts[SUSCEPTIBLE], label="Susceptible (S)", marker="o")
plt.plot(state_counts[INFECTIOUS], label="Infectious (I)", marker="s")
plt.plot(state_counts[PERMANENT], label="Permanent (P)", marker="^")
plt.xlabel("Time Steps")
plt.ylabel("Number of Nodes")
plt.title("Propagation Scale Over Time")
plt.legend()
plt.grid()
plt.show()