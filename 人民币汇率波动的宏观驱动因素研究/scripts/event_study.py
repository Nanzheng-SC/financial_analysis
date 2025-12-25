import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
# ===============================
# 1. 路径设置
# ===============================
# 获取脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目根目录
BASE_DIR = os.path.dirname(script_dir)
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULT_DIR = os.path.join(BASE_DIR, "result")
os.makedirs(RESULT_DIR, exist_ok=True)

# ===============================
# 2. 读取主数据
# ===============================
df = pd.read_csv(
    os.path.join(DATA_DIR, "master_data.csv"),
    parse_dates=["date"]
)
df.set_index("date", inplace=True)
df.sort_index(inplace=True)

# 计算对数收益率
df["cny_ret"] = np.log(df["CNY_USD"] / df["CNY_USD"].shift(1))

# ===============================
# 3. 读取事件表
# ===============================
events = pd.read_csv(
    os.path.join(DATA_DIR, "event_list_v2.csv"),
    parse_dates=["event_date"]
)

# ===============================
# 4. 事件窗口参数
# ===============================
WINDOW = 10  # ±10 日
event_results = []

# ===============================
# 5. 构造事件窗口收益率
# ===============================
for _, row in events.iterrows():
    event_date = row["event_date"]
    event_type = row["event_type"]
    event_name = row["event_name"]

    if event_date not in df.index:
        continue

    # 找到事件日在 df 中的位置
    idx = df.index.get_loc(event_date)

    # 防止窗口越界
    if idx < WINDOW or idx + WINDOW >= len(df):
        continue

    window_data = df.iloc[idx - WINDOW : idx + WINDOW + 1][["cny_ret"]].copy()
    window_data["tau"] = range(-WINDOW, WINDOW + 1)
    window_data["event_type"] = event_type
    window_data["event_name"] = event_name

    event_results.append(window_data)

# 合并所有事件结果
event_df = pd.concat(event_results, ignore_index=True)

# 保存事件窗口数据（重要）
event_df.to_csv(
    os.path.join(RESULT_DIR, "event_window_returns.csv"),
    index=False
)

print("✅ 事件窗口数据已生成")

# ===============================
# 6. 按事件类型计算平均反应
# ===============================
avg_response = (
    event_df
    .groupby(["event_type", "tau"])["cny_ret"]
    .mean()
    .reset_index()
)

# ===============================
# 7. 可视化：不同事件类型的平均反应
# ===============================
plt.figure(figsize=(12, 6))

for etype in avg_response["event_type"].unique():
    subset = avg_response[avg_response["event_type"] == etype]
    plt.plot(subset["tau"], subset["cny_ret"], label=etype)

plt.axvline(0, color="black", linestyle="--", linewidth=1)
plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)

plt.xlabel("事件窗口（天）")
plt.ylabel("平均汇率对数收益率")
plt.title("不同类型事件的人民币汇率平均反应（±10 日）")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()

plt.savefig(
    os.path.join(RESULT_DIR, "event_study_by_type.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.show()
