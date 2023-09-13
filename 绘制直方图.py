import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
# 读取Excel文件或CSV文件（根据您的表格类型）
# 示例：从CSV文件中读取数据
df = pd.read_excel('统计弹幕次数.xlsx')

# 假设您的表格数据的结构如下：
# 列1：类别名称（Category）
# 列2：数据值（Value）

plt.rcParams['font.sans-serif']=['SimHei']
# 提取类别名称和数据值
categories = df['弹幕']
values = df['次数']
list=[]
for i in range(20):
    list.append((categories[i],values[i]))
labels, values = zip(*list)
plt.figure(figsize=(10, 6))  # 设置图形大小
plt.bar(labels, values, color='skyblue')
plt.xlabel('弹幕')  # 设置x轴标签
plt.ylabel('次数')  # 设置y轴标签
plt.title('弹幕次数分布直方图')  # 设置标题
plt.xticks(rotation=45)  # 旋转x轴标签，使其更可读

# 显示直方图
plt.tight_layout()  # 自动调整布局，以避免标签被截断
plt.show()