import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np

#用户状态定义
SUSCEPTIBLE = "S"
INFECTIOUS = "I"
PERMANENT = "P"

def load_facebook_data(file_path):
    G = nx.read_edgelist(file_path, nodetype=int)
    print(f"Loaded graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    return G

def initialize_states(graph, initial_spreaders=5):
    states = {node: SUSCEPTIBLE for node in graph.nodes}
    spreaders = random.sample(list(graph.nodes), initial_spreaders)
    for spreader in spreaders:
        states[spreader] = INFECTIOUS
    return states

def calculate_zipf_mean(n, a):
    ranks = np.arange(1, n + 1)
    probabilities = 1 / ranks**a
    probabilities /= probabilities.sum()
    mean = np.sum(ranks * probabilities)
    return mean

def simulate_propagation(graph, share_probability_mean, gamma=0.5, time_steps=10):
    node_states = {node: SUSCEPTIBLE for node in graph.nodes}
    initial_spreaders = int(mean_initiated)
    spreaders = random.sample(list(graph.nodes), initial_spreaders)
    for spreader in spreaders:
        node_states[spreader] = INFECTIOUS

    state_counts = {SUSCEPTIBLE: [], INFECTIOUS: [], PERMANENT: []}

    for t in range(time_steps):
        new_states = node_states.copy()

        for node in graph.nodes:
            if node_states[node] == SUSCEPTIBLE:
                if any(node_states[neighbor] == INFECTIOUS for neighbor in graph.neighbors(node)):
                    if random.random() < share_probability_mean:
                        new_states[node] = INFECTIOUS

            elif node_states[node] == INFECTIOUS:
                if random.random() < gamma:
                    new_states[node] = PERMANENT

        node_states = new_states

        state_counts[SUSCEPTIBLE].append(sum(1 for s in node_states.values() if s == SUSCEPTIBLE))
        state_counts[INFECTIOUS].append(sum(1 for s in node_states.values() if s == INFECTIOUS))
        state_counts[PERMANENT].append(sum(1 for s in node_states.values() if s == PERMANENT))

    return state_counts


if __name__ == "__main__":
    #加载 Facebook 数据
    file_path = "facebook/1912.edges"
    facebook_graph = load_facebook_data(file_path)

    #计算发起分享和分享行为的均值
    num_users = len(facebook_graph.nodes)
    zipf_a_initiate = 1.09
    zipf_a_share = 0.44

    mean_initiated = calculate_zipf_mean(num_users, zipf_a_initiate)
    mean_shared = calculate_zipf_mean(num_users, zipf_a_share)

    print(f"Mean number of initiated videos: {mean_initiated:.2f}")
    print(f"Mean number of shared videos: {mean_shared:.2f}")

    #模拟传播
    share_probability_mean = mean_shared / num_users
    state_counts = simulate_propagation(
        facebook_graph, share_probability_mean, gamma=0.5, time_steps=20
    )

    #绘制传播规模图
    plt.figure(figsize=(10, 6))
    plt.plot(state_counts[SUSCEPTIBLE], label="Susceptible (S)", marker="o")
    plt.plot(state_counts[INFECTIOUS], label="Infectious (I)", marker="s")
    plt.plot(state_counts[PERMANENT], label="Permanent (P)", marker="^")
    plt.xlabel("Time Steps")
    plt.ylabel("Number of Nodes")
    plt.title("Propagation Scale Over Time")
    plt.legend()
    plt.grid()
    plt.show()

    #计算累计传播规模
    cumulative_views = [
        state_counts[INFECTIOUS][t] + state_counts[PERMANENT][t]
        for t in range(len(state_counts[INFECTIOUS]))
    ]

    #绘制累计传播规模
    plt.figure(figsize=(10, 6))
    plt.plot(cumulative_views, label="Cumulative Views", color="purple", marker="x")
    plt.xlabel("Time Steps")
    plt.ylabel("Number of Nodes")
    plt.title("Cumulative Propagation Scale Over Time")
    plt.legend()
    plt.grid()
    plt.show()

        #打印网络的节点总数
    print(f"Total nodes in the network: {len(facebook_graph.nodes)}")

    #打印传播结束时的永久状态节点数量
    final_permanent_nodes = state_counts[PERMANENT][-1]
    print(f"Nodes in Permanent state at the end: {final_permanent_nodes}")

    #检查传播覆盖率
    coverage_rate = final_permanent_nodes / len(facebook_graph.nodes)
    print(f"Propagation coverage rate: {coverage_rate:.2%}")