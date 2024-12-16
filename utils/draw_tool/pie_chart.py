import os
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # 从文件中读取数据
    data = pd.read_csv('pie_data.csv')
    labels = data['label'].tolist()
    sizes = data['size'].tolist()
    colors = data['color'].tolist()
    explode = (0.1, 0, 0, 0)  # 仅“炸开”第一块

    # 创建饼图
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)

    # 使饼图为正圆形
    plt.axis('equal')

    # 显示图形
#     plt.title('饼图示例', fontproperties='SimHei')  # 使用 SimHei 字体显示中文
    plt.title('饼图示例', fontproperties='Noto Sans CJK')  # 替换为可用的中文字体

    # 保存图形到指定目录
    save_dir = "images"  # 替换为你的目录
    os.makedirs(save_dir, exist_ok=True)  # 创建目录（如果不存在）
    plt.savefig(os.path.join(save_dir, '饼图示例.svg'))  # 保存图形

    plt.show()