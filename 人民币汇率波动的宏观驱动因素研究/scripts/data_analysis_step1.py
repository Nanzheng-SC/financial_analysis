import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 获取脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目根目录（scripts文件夹的父目录）
project_dir = os.path.dirname(script_dir)
# 构建数据文件的绝对路径
data_path = os.path.join(project_dir, "data", "master_data.csv")
# 构建结果保存目录的绝对路径
result_dir = os.path.join(project_dir, "result")

# 读取数据
df = pd.read_csv(data_path, parse_dates=["date"])
df.set_index("date", inplace=True)

# 人民币兑美元汇率时间序列
plt.figure(figsize=(12, 6), dpi=100)
ax = df["CNY_USD"].plot(color='blue', linewidth=2)
plt.title("人民币兑美元汇率时间序列", fontsize=14, fontweight='bold')
plt.xlabel("日期", fontsize=12)
plt.ylabel("人民币/美元", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
# 保存图表
plt.savefig(os.path.join(result_dir, "cny_usd_exchange_rate.png"), dpi=300, bbox_inches='tight')
plt.show()

# 美元指数时间序列
plt.figure(figsize=(12, 6), dpi=100)
df["USD_INDEX"].plot(color='green', linewidth=2)
plt.title("美元指数时间序列", fontsize=14, fontweight='bold')
plt.xlabel("日期", fontsize=12)
plt.ylabel("指数", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
# 保存图表
plt.savefig(os.path.join(result_dir, "us_dollar_index.png"), dpi=300, bbox_inches='tight')
plt.show()

# 人民币 vs 美元指数
plt.figure(figsize=(12, 6), dpi=100)
ax1 = plt.gca()
ax2 = ax1.twinx()

line1, = ax1.plot(df.index, df["CNY_USD"], color='blue', linewidth=2, label="人民币/美元")
line2, = ax2.plot(df.index, df["USD_INDEX"], color='green', linewidth=2, label="美元指数")

ax1.set_xlabel("日期", fontsize=12)
ax1.set_ylabel("人民币/美元", fontsize=12, color='blue')
ax2.set_ylabel("美元指数", fontsize=12, color='green')

ax1.tick_params(axis='y', colors='blue')
ax2.tick_params(axis='y', colors='green')

# 添加图例
plt.legend([line1, line2], ["人民币/美元", "美元指数"], loc='upper right', fontsize=10)

plt.title("人民币汇率与美元指数对比", fontsize=14, fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
# 保存图表
plt.savefig(os.path.join(result_dir, "cny_vs_usd_index.png"), dpi=300, bbox_inches='tight')
plt.show()

# 滚动相关性

df_corr = df.loc["2005-07-21":].copy()

df_corr["cny_ret"] = np.log(df_corr["CNY_USD"] / df_corr["CNY_USD"].shift(1))
df_corr["usd_ret"] = np.log(df_corr["USD_INDEX"] / df_corr["USD_INDEX"].shift(1))

df_corr = df_corr.replace([np.inf, -np.inf], np.nan)
df_corr = df_corr.dropna(subset=["cny_ret", "usd_ret"])

rolling_corr = df_corr["cny_ret"].rolling(
    window=60,
    min_periods=40
).corr(df_corr["usd_ret"])

plt.figure(figsize=(12, 6), dpi=100)
rolling_corr.plot(color="red", linewidth=2)

plt.title("人民币汇率与美元指数滚动相关性（60日，对数收益率）",
          fontsize=14, fontweight="bold")
plt.xlabel("日期", fontsize=12)
plt.ylabel("相关性", fontsize=12)

plt.axhline(0, color="black", linewidth=0.8)
plt.grid(True, linestyle="--", alpha=0.7)
plt.tight_layout()
# 保存图表
plt.savefig(os.path.join(result_dir, "rolling_correlation.png"), dpi=300, bbox_inches='tight')
plt.show()

