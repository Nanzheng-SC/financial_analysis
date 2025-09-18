import pandas as pd

# 读取合并后的数据
merged_file = 'e:/Study/2-1/finance_analysis/lecture_2/lecture2_coding_copilot/fiscal/fiscal_merged.xlsx'
print("读取合并后的数据...")
fiscal_merged = pd.read_excel(merged_file)

# 显示基本信息
print(f"合并后的数据形状: {fiscal_merged.shape}")
print("\n合并后的数据列名:")
print(fiscal_merged.columns.tolist())

# 显示前15行数据
print("\n合并后的数据前15行:")
print(fiscal_merged.head(15))

# 显示计算的财政赤字和赤字率列
print("\n财政赤字和赤字率数据预览:")
print(fiscal_merged[['时间', '国家财政收入累计值(亿元)', '国家财政支出(不含债务还本)累计值(亿元)', '财政赤字(亿元)', '赤字率(%)']].head(10))

# 显示数据统计信息
print("\n数据统计信息:")
print(f"数据时间范围: 从 {fiscal_merged['时间'].min()} 到 {fiscal_merged['时间'].max()}")
print(f"财政收入最大值: {fiscal_merged['国家财政收入累计值(亿元)'].max():.2f} 亿元")
print(f"财政支出最大值: {fiscal_merged['国家财政支出(不含债务还本)累计值(亿元)'].max():.2f} 亿元")
print(f"财政赤字最大值: {fiscal_merged['财政赤字(亿元)'].max():.2f} 亿元")
print(f"最高赤字率: {fiscal_merged['赤字率(%)'].max():.2f}%")
print(f"平均财政赤字: {fiscal_merged['财政赤字(亿元)'].mean():.2f} 亿元")
print(f"平均赤字率: {fiscal_merged['赤字率(%)'].mean():.2f}%")

# 检查是否存在异常值
print("\n异常值检查:")
negative_deficit = fiscal_merged[fiscal_merged['财政赤字(亿元)'] < 0]
print(f"存在财政盈余的记录数: {len(negative_deficit)}")
if len(negative_deficit) > 0:
    print("财政盈余记录预览:")
    print(negative_deficit[['时间', '财政赤字(亿元)', '赤字率(%)']].head())