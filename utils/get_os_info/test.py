import psutil

# 获取 CPU 核心的频率信息
cpu_freq = psutil.cpu_freq(percpu=True)

# 字典存储赫兹和对应的核心数量
core_counts = {}

# 定义一个阈值（可选），这里不使用
# threshold = 2000  # 设定一个频率阈值，单位为 MHz

for freq in cpu_freq:
    current_freq = freq.current
    # 如果赫兹已经在字典中，核心数量加1
    if current_freq in core_counts:
        core_counts[current_freq] += 1
    else:
        core_counts[current_freq] = 1

# 按照赫兹从高到低排序
sorted_core_counts = dict(sorted(core_counts.items(), key=lambda x: x[0], reverse=True))

# 打印结果
for freq, count in sorted_core_counts.items():
    print(f"赫兹: {freq} MHz, 核心数量: {count}")