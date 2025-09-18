import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties
import numpy as np

# 设置中文显示
try:
    # 尝试使用系统中可用的中文字体
    plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC", "Microsoft YaHei"]
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
except Exception:
    # 如果出现字体设置错误，使用默认字体配置
    pass

# 设置页面标题
st.title('国家财政数据分析')

# 读取数据
@st.cache_data

def load_data():
    try:
        df = pd.read_excel('fiscal_merged.xlsx')
        # 转换时间列为日期类型，确保可以正确排序
        df['时间'] = pd.to_datetime(df['时间'], format='%Y年%m月', errors='coerce')
        # 按时间排序
        df = df.sort_values('时间')
        return df
    except Exception as e:
        st.error(f"读取数据时出错: {e}")
        return pd.DataFrame()

df = load_data()

# 显示数据信息
if not df.empty:
    st.subheader('数据概览')
    st.write(f"数据包含 {len(df)} 条记录")
    st.write(f"时间范围: {df['时间'].min().strftime('%Y年%m月')} 至 {df['时间'].max().strftime('%Y年%m月')}")
    
    # 数据展示部分
    st.subheader('财政数据表格')
    # 显示时间、收入、支出、赤字和赤字率的表格
    display_columns = ['时间', '国家财政收入累计值(亿元)', '国家财政支出(不含债务还本)累计值(亿元)', '财政赤字(亿元)', '赤字率(%)']
    df_display = df.copy()
    # 将时间列格式化为更友好的显示方式
    df_display['时间'] = df_display['时间'].dt.strftime('%Y年%m月')
    st.dataframe(df_display[display_columns])
    
    # 可视化部分
    st.subheader('财政收支趋势分析')
    
    # 创建图表区域
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 绘制收入和支出的折线图
    ax.plot(df['时间'], df['国家财政收入累计值(亿元)'], label='财政收入(亿元)', linewidth=2)
    ax.plot(df['时间'], df['国家财政支出(不含债务还本)累计值(亿元)'], label='财政支出(亿元)', linewidth=2)
    
    # 设置图表属性
    ax.set_xlabel('时间', fontsize=12)
    ax.set_ylabel('金额(亿元)', fontsize=12)
    ax.set_title('国家财政收支趋势', fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # 自动调整x轴标签，避免重叠
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 显示图表
    st.pyplot(fig)
    
    # 财政赤字和赤字率图表
    st.subheader('财政赤字与赤字率分析')
    
    # 创建双Y轴图表
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # 绘制财政赤字
    color = 'tab:red'
    ax1.set_xlabel('时间', fontsize=12)
    ax1.set_ylabel('财政赤字(亿元)', color=color, fontsize=12)
    ax1.bar(df['时间'], df['财政赤字(亿元)'], label='财政赤字(亿元)', alpha=0.7, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    
    # 创建第二个Y轴用于赤字率
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('赤字率(%)', color=color, fontsize=12)
    ax2.plot(df['时间'], df['赤字率(%)'], label='赤字率(%)', color=color, linewidth=2, marker='o', markersize=4)
    ax2.tick_params(axis='y', labelcolor=color)
    
    # 设置标题
    fig.suptitle('国家财政赤字与赤字率变化', fontsize=14)
    
    # 自动调整x轴标签，避免重叠
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 显示图表
    st.pyplot(fig)
    
    # 数据统计摘要
    st.subheader('数据统计摘要')
    stats_df = df[['国家财政收入累计值(亿元)', '国家财政支出(不含债务还本)累计值(亿元)', '财政赤字(亿元)', '赤字率(%)']].describe()
    st.dataframe(stats_df)
    
    # 数据筛选器
    st.subheader('按时间范围筛选数据')
    
    # 创建时间滑块
    min_date = df['时间'].min().to_pydatetime()
    max_date = df['时间'].max().to_pydatetime()
    
    # 创建两个日期选择器
    start_date, end_date = st.date_input(
        "选择时间范围",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date,
        format="YYYY-MM-DD"
    )
    
    # 将日期转换为datetime64类型以便比较
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # 筛选数据
    filtered_df = df[(df['时间'] >= start_date) & (df['时间'] <= end_date)]
    
    # 显示筛选后的数据
    st.write(f"筛选后的数据包含 {len(filtered_df)} 条记录")
    
    # 显示筛选后的数据表格
    filtered_df_display = filtered_df.copy()
    filtered_df_display['时间'] = filtered_df_display['时间'].dt.strftime('%Y年%m月')
    st.dataframe(filtered_df_display[display_columns])
    
    # 筛选后数据的基本统计
    st.write("筛选后数据的基本统计:")
    st.write(f"平均财政收入: {filtered_df['国家财政收入累计值(亿元)'].mean():.2f} 亿元")
    st.write(f"平均财政支出: {filtered_df['国家财政支出(不含债务还本)累计值(亿元)'].mean():.2f} 亿元")
    st.write(f"平均财政赤字: {filtered_df['财政赤字(亿元)'].mean():.2f} 亿元")
    st.write(f"平均赤字率: {filtered_df['赤字率(%)'].mean():.2f}%")

else:
    st.warning("未加载到数据，请检查数据文件是否存在。")