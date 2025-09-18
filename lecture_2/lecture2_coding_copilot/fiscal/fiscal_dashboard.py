import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

# 设置中文字体
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]

# 定义数据文件路径
DATA_DIR = "e:\\Study\\2-1\\finance_analysis\\week_1\\financial_data_analysis\\financial_data_analysis\\data\\national_data"

# 设置页面配置
st.set_page_config(
    page_title="国家财政数据分析",
    page_icon="📊",
    layout="wide"
)

# 页面标题
st.title("国家财政收入与支出数据分析")

@st.cache_data
# 读取Excel文件函数
def load_financial_data(file_name):
    try:
        file_path = os.path.join(DATA_DIR, file_name)
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        st.error(f"读取文件 {file_name} 时出错: {str(e)}")
        return None

# 读取国家财政收入数据
st.subheader("国家财政预算收入数据")
income_df = load_financial_data("国家财政预算收入.xls")

if income_df is not None:
    # 显示数据预览
    st.dataframe(income_df.head(10))
    
    # 显示数据信息
    st.write(f"数据形状: {income_df.shape}")
    st.write(f"列名: {list(income_df.columns)}")
    
    # 提供数据下载功能
    csv_income = income_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="下载财政收入数据 (CSV)",
        data=csv_income,
        file_name="国家财政预算收入.csv",
        mime="text/csv"
    )

# 读取国家财政支出数据
st.subheader("国家财政支出数据")
expenditure_df = load_financial_data("国家财政支出.xls")

if expenditure_df is not None:
    # 显示数据预览
    st.dataframe(expenditure_df.head(10))
    
    # 显示数据信息
    st.write(f"数据形状: {expenditure_df.shape}")
    st.write(f"列名: {list(expenditure_df.columns)}")
    
    # 提供数据下载功能
    csv_expenditure = expenditure_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="下载财政支出数据 (CSV)",
        data=csv_expenditure,
        file_name="国家财政支出.csv",
        mime="text/csv"
    )

# 基本数据可视化
if income_df is not None and expenditure_df is not None:
    st.subheader("数据可视化分析")
    
    # 如果两表可以合并分析，这里可以添加合并逻辑
    # 但需要根据实际数据结构进行调整
    
    # 简单的可视化示例（需要根据实际数据结构调整）
    try:
        # 创建可视化区域
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 这里只是示例，需要根据实际数据结构调整
        # 假设数据有年份列和数值列
        st.info("请根据实际数据结构修改可视化部分的代码")
        
        st.pyplot(fig)
    except Exception as e:
        st.error(f"创建可视化图表时出错: {str(e)}")

# 添加说明信息
st.markdown("""
### 使用说明
1. 本应用展示了国家财政收入与支出的基本数据
2. 可以查看数据预览、下载原始数据
3. 数据来源于 week_1 目录下的 Excel 文件
4. 请根据实际数据结构调整可视化部分的代码
""")

# 显示数据源信息
st.sidebar.header("数据源信息")
st.sidebar.write(f"数据文件位置: {DATA_DIR}")
st.sidebar.write("包含文件:")
for file in os.listdir(DATA_DIR):
    if file.endswith(".xls"):
        st.sidebar.write(f"- {file}")