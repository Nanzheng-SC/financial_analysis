import pandas as pd
import os

# 设置文件路径
income_file = 'e:/Study/2-1/finance_analysis/data/national_data/国家财政预算收入.xls'
expense_file = 'e:/Study/2-1/finance_analysis/data/national_data/国家财政支出.xls'

# 读取财政收入数据
print("读取国家财政预算收入数据...")
income_df = pd.read_excel(income_file)

# 读取财政支出数据
print("读取国家财政支出数据...")
expense_df = pd.read_excel(expense_file)

# 合并数据
print("合并数据...")
# 使用'时间'列进行合并
fiscal_merged = pd.merge(income_df, expense_df, on='时间', how='inner')

# 计算财政赤字（支出-收入）
fiscal_merged['财政赤字(亿元)'] = fiscal_merged['国家财政支出(不含债务还本)累计值(亿元)'] - fiscal_merged['国家财政收入累计值(亿元)']

# 计算赤字率（赤字/收入 * 100%）
# 添加一个小值避免除以零的情况
fiscal_merged['赤字率(%)'] = (fiscal_merged['财政赤字(亿元)'] / (fiscal_merged['国家财政收入累计值(亿元)'] + 1e-10)) * 100

# 显示合并后的前10行数据
print(f"\n合并后的数据形状: {fiscal_merged.shape}")
print("合并后的数据前10行:")
print(fiscal_merged.head(10))

# 显示合并后的列名
print("\n合并后的列名:")
print(fiscal_merged.columns.tolist())

# 保存合并后的数据
output_file = 'e:/Study/2-1/finance_analysis/lecture_2/lecture2_coding_copilot/fiscal/fiscal_merged.xlsx'
fiscal_merged.to_excel(output_file, index=False)
print(f"\n合并后的数据已保存至: {output_file}")

# 显示一些统计信息
print("\n数据统计信息:")
print(f"数据时间范围: 从 {fiscal_merged['时间'].min()} 到 {fiscal_merged['时间'].max()}")
print(f"平均财政赤字: {fiscal_merged['财政赤字(亿元)'].mean():.2f} 亿元")
print(f"平均赤字率: {fiscal_merged['赤字率(%)'].mean():.2f}%")