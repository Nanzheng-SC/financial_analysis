import pandas as pd
from scipy import stats
import os
import matplotlib.pyplot as plt
import seaborn as sns

# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))
# 构建数据文件的绝对路径
data_path = os.path.join(script_dir, '..', 'result', 'event_window_returns.csv')
# 定义结果目录
result_dir = os.path.join(script_dir, '..', 'result')
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

# 设置中文字体，避免乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 读取事件窗口收益率数据
df = pd.read_csv(data_path)

# 显示数据的前几行和列名，以便确认数据结构
print("=== 数据基本信息 ===")
print(f"列名: {list(df.columns)}")
print("前5行数据:")
print(df.head())

# 只保留事件窗口 [-1, +1] (注意实际列名是'tau'而不是'event_time')
df_car = df[df["tau"].between(-1, 1)]

# 对每个事件计算 CAR (注意实际列名是'cny_ret'而不是'return')
car_df = (
    df_car
    .groupby(["event_name", "event_type"])["cny_ret"]
    .sum()
    .reset_index()
    .rename(columns={"cny_ret": "CAR"})
)

print("\n=== 事件CAR计算结果（前5行）===")
print(car_df.head())

# 按事件类型分组，准备 ANOVA 的输入列表
groups = [
    group["CAR"].values
    for _, group in car_df.groupby("event_type")
]

# 显示各组的事件类型和样本数量
print("\n=== ANOVA 输入组信息 ===")
event_types = list(car_df.groupby("event_type").groups.keys())
for i, (event_type, group) in enumerate(zip(event_types, groups)):
    print(f"组 {i+1} ({event_type}): {len(group)} 个样本")

# 单因素方差分析
f_stat, p_value = stats.f_oneway(*groups)

print("\n=== 单因素方差分析（ANOVA）结果 ===")
print(f"ANOVA F-statistic: {f_stat:.4f}")
print(f"ANOVA p-value: {p_value:.4f}")

# 添加结论
if p_value < 0.05:
    print("结论：在95%置信水平下，不同类型事件的CAR存在显著差异")
else:
    print("结论：在95%置信水平下，不同类型事件的CAR不存在显著差异")

# 可选：添加Tukey HSD检验进行事后多重比较
try:
    from statsmodels.stats.multicomp import MultiComparison
    
    # 执行Tukey HSD检验
    mc = MultiComparison(car_df["CAR"], car_df["event_type"])
    tukey_result = mc.tukeyhsd()
    
    print("\n=== Tukey HSD 事后多重比较结果 ===")
    print(tukey_result.summary())
    
    # 生成Tukey HSD检验结果图
    fig = tukey_result.plot_simultaneous(ylabel='事件类型', xlabel='CAR差异', figsize=(12, 8))
    plt.title('Tukey HSD 事后多重比较结果')
    plt.tight_layout()
    
    # 保存Tukey HSD检验结果图
    tukey_plot_path = os.path.join(result_dir, 'tukey_test_result.png')
    plt.savefig(tukey_plot_path, dpi=300)
    print(f"✅ Tukey HSD检验结果图已保存到 {tukey_plot_path}")
    plt.close(fig)
    
except ImportError:
    print("\n提示：未安装statsmodels库，无法进行Tukey HSD检验")
    print("可以通过 'pip install statsmodels' 安装该库")
except Exception as e:
    print(f"\n⚠️  生成Tukey HSD检验结果图失败：{e}")

# 可选：添加可视化
print("\n=== 生成可视化 ===")
try:
    
    # 绘制CAR分布箱线图
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='event_type', y='CAR', data=car_df)
    plt.title('不同事件类型的CAR分布箱线图')
    plt.xlabel('事件类型')
    plt.ylabel('累积异常收益率 (CAR)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 保存图表
    
    plot_path = os.path.join(result_dir, 'event_type_car_boxplot.png')
    plt.savefig(plot_path, dpi=300)
    print(f"✅ CAR分布箱线图已保存到 {plot_path}")
    
except ImportError as e:
    print(f"⚠️  可视化失败：{e}")
    print("可以通过 'pip install matplotlib seaborn' 安装可视化库")
