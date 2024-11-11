import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Microsoft YaHei'

# 创建数据
data = {
    'Week1': [187, 203, 208, 207, 217, 320],
    'Week2': [207, 208, 210, 206, 212, 324],
    'Week3': [202, 210, 212, 205, 214, 330],
    'Week4': [208, 215, 217, 217, 213, 345]
}

df = pd.DataFrame(data)

# 将数据展开为一维
data_flat = df.values.flatten(order='F')

# 计算移动平均值，周期为6
moving_avg = pd.Series(data_flat).rolling(window=7).mean()

# 将移动平均值重新整形为与原数据相同的形状
moving_avg_reshaped = moving_avg.values.reshape(df.shape, order='F')

# 将移动平均值添加到DataFrame
df_moving_avg = pd.DataFrame(moving_avg_reshaped, columns=[f'Moving_Avg_{col}' for col in df.columns])

# 合并原始数据和移动平均值
df_combined = pd.concat([df, df_moving_avg], axis=1)
df_combined.to_excel('moving_avg.xlsx', index=True)

plt.plot(data_flat, 'b-*', label='actual data')
plt.plot(moving_avg, 'r-o', label='trend')
plt.grid(which='both', alpha=0.3)
plt.legend()
plt.show()

# 使用平均值预测第五周前两天
# 计算每天的平均值
daily_avg = df.mean(axis=1)

# 预测第五周前两天的值
predicted_week5 = daily_avg.head(2).astype(int)

print("预测的第五周前两天的值：")
print(predicted_week5)

