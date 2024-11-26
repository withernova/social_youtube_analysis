import numpy as np

# 参数设置
N = 1000  # 用户总数
a = 1.5   # 齐普夫分布参数，控制陡峭程度

# 生成齐普夫分布
user_ranks = np.arange(1, N + 1)  # 用户排名 1 到 N
zipf_probs = 1 / (user_ranks ** a)  # 齐普夫公式
zipf_probs /= zipf_probs.sum()  # 归一化为概率分布

# 输出部分用户的概率
print("前10名用户的发起概率:", zipf_probs[:10])
print("后10名用户的发起概率:", zipf_probs[-10:])

# 蒙特卡洛模拟
num_simulations = 1000  # 模拟次数
user_initiate_counts = np.zeros(N)  # 每个用户发起行为的计数

for _ in range(num_simulations):
    for i in range(N):
        if np.random.random() < zipf_probs[i]:  # 根据概率判断是否发起
            user_initiate_counts[i] += 1

# 发起概率的归一化处理
user_initiate_probs = user_initiate_counts / num_simulations

# 输出结果
print("前10名用户的发起概率:", user_initiate_probs[:10])
print("后10名用户的发起概率:", user_initiate_probs[-10:])


import matplotlib.pyplot as plt

# 绘制用户发起概率分布
plt.figure(figsize=(10, 6))
plt.plot(user_ranks, user_initiate_probs, label='User Initiation Probability', color='blue')
plt.xlabel('User Rank')
plt.ylabel('Probability')
plt.title('User Initiation Probability by Rank (Zipf Distribution)')
plt.grid()
plt.legend()
plt.show()