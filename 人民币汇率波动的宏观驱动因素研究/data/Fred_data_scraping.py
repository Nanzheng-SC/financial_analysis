import os
import time
import pandas as pd
from dotenv import load_dotenv
from fredapi import Fred

# --------------------------------------------------
# 1. 读取 FRED API KEY
# --------------------------------------------------
load_dotenv()
FRED_API_KEY = os.getenv("FRED_API_KEY")

fred = Fred(api_key=FRED_API_KEY)

# --------------------------------------------------
# 2. 定义我们要获取的 FRED 数据
# --------------------------------------------------
fred_series = {
    "CNY_USD": "DEXCHUS",        # 人民币兑美元
    "USD_INDEX": "DTWEXBGS",     # 名义广义美元指数
    "US_10Y": "DGS10",           # 美国10年期国债收益率
    "US_CPI": "CPIAUCSL"         # 美国CPI（月度）
}

# --------------------------------------------------
# 3. 下载数据（添加重试机制）
# --------------------------------------------------
data = {}
max_retries = 3

for name, series_id in fred_series.items():
    print(f"Downloading {name} ({series_id}) ...")
    retries = 0
    while retries < max_retries:
        try:
            data[name] = fred.get_series(series_id)
            break
        except Exception as e:
            retries += 1
            print(f"  Retry {retries}/{max_retries} failed: {e}")
            time.sleep(2)
            if retries == max_retries:
                print(f"  ❌ Failed to download {name} after {max_retries} retries")
                data[name] = None
    time.sleep(1)  # 避免 API 速率限制

# --------------------------------------------------
# 4. 合并成一个 DataFrame（处理可能的 None 值）
# --------------------------------------------------
# 过滤掉 None 值的数据
valid_data = {k: v for k, v in data.items() if v is not None}

if not valid_data:
    print("❌ No data could be downloaded!")
    exit(1)

# 创建 DataFrame 并只包含有效数据
df = pd.DataFrame(valid_data)

# --------------------------------------------------
# 5. 基本清洗
# --------------------------------------------------
df.index.name = "date"
df.sort_index(inplace=True)

# 保存原始数据
df.to_csv("fred_raw_data.csv")

print("✅ FRED data downloaded successfully!")
print(f"📊 Downloaded {len(valid_data)} out of {len(fred_series)} series.")
print(df.head())
