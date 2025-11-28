import pandas as pd
import os

# 设置文件路径
income_file = 'e:/Study/2-1/finance_analysis/data/national_data/国家财政预算收入.xls'
expense_file = 'e:/Study/2-1/finance_analysis/data/national_data/国家财政支出.xls'

# 读取财政收入数据
print("读取国家财政预算收入数据...")
income_df = pd.read_excel(income_file)
print(f"收入数据形状: {income_df.shape}")
print("收入数据前5行:")
print(income_df.head())
print("收入数据列名:")
print(income_df.columns.tolist())
print("\n")

# 读取财政支出数据
print("读取国家财政支出数据...")
expense_df = pd.read_excel(expense_file)
print(f"支出数据形状: {expense_df.shape}")
print("支出数据前5行:")
print(expense_df.head())
print("支出数据列名:")
print(expense_df.columns.tolist())
print("\n")

# 尝试合并数据
print("尝试合并数据...")
# 假设两个表格有共同的时间列或索引可以合并
# 先检查是否有共同的列名
common_columns = set(income_df.columns).intersection(set(expense_df.columns))
print(f"共同列名: {common_columns}")

# 显示数据类型信息
print("\n收入数据类型信息:")
print(income_df.dtypes)
print("\n支出数据类型信息:")
print(expense_df.dtypes)