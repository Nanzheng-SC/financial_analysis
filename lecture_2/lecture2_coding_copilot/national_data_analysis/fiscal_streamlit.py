import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties
import numpy as np
from scipy import stats

# 设置中文显示
try:
    # 尝试使用系统中可用的中文字体
    plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei"]
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
except Exception:
    # 如果出现字体设置错误，使用默认字体配置
    pass

# 设置页面标题
st.title('国家财政数据分析')

# 添加应用介绍
st.markdown("""\n本应用用于展示和分析国家财政收支数据，包括财政收入、支出、赤字及赤字率的历史趋势和统计分析。\n您可以通过下方的时间筛选器查看不同时间段的数据情况。""")

# 读取数据
@st.cache_data

def load_data():
    try:
        # 首先尝试读取包含宏观经济数据的合并文件
        try:
            df = pd.read_excel('fiscal_macro_merged.xlsx')
            macro_included = True
        except Exception:
            # 如果没有宏观数据文件，读取原始财政数据
            df = pd.read_excel('fiscal_merged.xlsx')
            macro_included = False
        
        # 转换时间列为日期类型，确保可以正确排序
        df['时间'] = pd.to_datetime(df['时间'], format='%Y年%m月', errors='coerce')
        # 按时间排序
        df = df.sort_values('时间')
        return df, macro_included
    except Exception as e:
        st.error(f"读取数据时出错: {e}")
        return pd.DataFrame(), False

df, macro_included = load_data()

# 显示数据信息
if not df.empty:
    st.subheader('数据概览')
    st.write(f"数据包含 {len(df)} 条记录")
    st.write(f"时间范围: {df['时间'].min().strftime('%Y年%m月')} 至 {df['时间'].max().strftime('%Y年%m月')}")
    
    # 显示是否包含宏观经济数据
    if macro_included:
        st.success("已加载包含宏观经济数据的完整数据集")
        # 显示可用的宏观经济指标
        macro_cols = [col for col in df.columns if any(macro in col for macro in ['PMI', '货币', '投资', '进出口', '房地产'])]
        if macro_cols:
            st.write("包含的宏观经济指标:")
            for col in macro_cols:
                st.write(f"- {col}")
    else:
        st.info("当前使用的是基础财政数据集，未包含宏观经济数据")
    
    # 数据展示部分
    st.subheader('财政数据表格')
    # 显示时间、收入、支出、赤字和赤字率的表格
    display_columns = ['时间', '国家财政收入累计值(亿元)', '国家财政支出(不含债务还本)累计值(亿元)', '财政赤字(亿元)', '赤字率(%)']
    df_display = df.copy()
    # 将时间列格式化为更友好的显示方式
    df_display['时间'] = df_display['时间'].dt.strftime('%Y年%m月')
    st.dataframe(df_display[display_columns], use_container_width=True)
    
    # 添加赤字相关说明
    with st.expander("🔍 财政赤字与赤字率解释"):
        st.markdown("""
        ### 财政赤字
        财政赤字是指政府在一定时期内（通常为一年）的财政支出超过财政收入的部分。
        
        **计算公式**：
        
        ```
        财政赤字(亿元) = 国家财政支出(不含债务还本)累计值(亿元) - 国家财政收入累计值(亿元)
        ```
        
        ### 赤字率
        赤字率是指财政赤字占财政收入的比例，通常以百分比表示，是衡量国家财政状况的重要指标。
        
        **计算公式**：
        
        ```
        赤字率(%) = (财政赤字(亿元) / 国家财政收入累计值(亿元)) * 100%
        ```
        
        一般认为，赤字率控制在3%以内是相对安全的水平。
        """)
    
    # 可视化部分
    st.subheader('财政收支趋势分析')
    
    # 创建图表区域
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 为数据添加月份索引用于趋势线计算
    df['month_index'] = range(len(df))
    
    # 绘制收入和支出的折线图
    line1, = ax.plot(df['时间'], df['国家财政收入累计值(亿元)'], label='财政收入(亿元)', linewidth=2, alpha=0.8)
    line2, = ax.plot(df['时间'], df['国家财政支出(不含债务还本)累计值(亿元)'], label='财政支出(亿元)', linewidth=2, alpha=0.8)
    
    # 计算并绘制收入趋势线
    z_income = np.polyfit(df['month_index'], df['国家财政收入累计值(亿元)'], 1)
    p_income = np.poly1d(z_income)
    ax.plot(df['时间'], p_income(df['month_index']), linestyle='--', color=line1.get_color(), linewidth=1.5, label='收入趋势线')
    
    # 计算并绘制支出趋势线
    z_expense = np.polyfit(df['month_index'], df['国家财政支出(不含债务还本)累计值(亿元)'], 1)
    p_expense = np.poly1d(z_expense)
    ax.plot(df['时间'], p_expense(df['month_index']), linestyle='--', color=line2.get_color(), linewidth=1.5, label='支出趋势线')
    
    # 计算收支平衡线（收入-支出）
    df['收支平衡'] = df['国家财政收入累计值(亿元)'] - df['国家财政支出(不含债务还本)累计值(亿元)']
    
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
    
    # 添加收支平衡平滑曲线图表
    st.subheader('收支平衡趋势分析')
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 计算收支平衡的6个月移动平均值（平滑曲线）
    df['收支平衡平滑'] = df['收支平衡'].rolling(window=6, min_periods=1).mean()
    
    # 绘制平滑的收支平衡曲线
    ax.plot(df['时间'], df['收支平衡平滑'], label='收支平衡(平滑)', linewidth=3, color='green')
    
    # 添加零线表示收支平衡点
    ax.axhline(y=0, color='red', linestyle='-', alpha=0.5, label='收支平衡点')
    
    # 设置图表属性
    ax.set_xlabel('时间', fontsize=12)
    ax.set_ylabel('收支差额(亿元)', fontsize=12)
    ax.set_title('财政收支平衡趋势(平滑曲线)', fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    st.pyplot(fig)
    
    # 财政赤字和赤字率图表
    st.subheader('财政赤字与赤字率分析')
    
    # 创建双Y轴图表
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # 绘制财政赤字
    color = 'tab:red'
    ax1.set_xlabel('时间', fontsize=12)
    ax1.set_ylabel('财政赤字(亿元)', color=color, fontsize=12)
    bars = ax1.bar(df['时间'], df['财政赤字(亿元)'], label='财政赤字(亿元)', alpha=0.7, color=color)
    
    # 添加赤字趋势线
    z_deficit = np.polyfit(df['month_index'], df['财政赤字(亿元)'], 1)
    p_deficit = np.poly1d(z_deficit)
    ax1.plot(df['时间'], p_deficit(df['month_index']), linestyle='--', color='darkred', linewidth=2, label='赤字趋势线')
    
    ax1.tick_params(axis='y', labelcolor=color)
    
    # 创建第二个Y轴用于赤字率
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('赤字率(%)', color=color, fontsize=12)
    line, = ax2.plot(df['时间'], df['赤字率(%)'], label='赤字率(%)', color=color, linewidth=2, marker='o', markersize=4)
    
    # 添加赤字率趋势线
    z_deficit_rate = np.polyfit(df['month_index'], df['赤字率(%)'], 1)
    p_deficit_rate = np.poly1d(z_deficit_rate)
    ax2.plot(df['时间'], p_deficit_rate(df['month_index']), linestyle='--', color='navy', linewidth=1.5, label='赤字率趋势线')
    
    # 添加国际警戒线（3%）
    ax2.axhline(y=3, color='orange', linestyle='-.', alpha=0.8, label='国际警戒线(3%)')
    
    ax2.tick_params(axis='y', labelcolor=color)
    
    # 设置标题
    fig.suptitle('国家财政赤字与赤字率变化', fontsize=14)
    
    # 合并图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='best', fontsize=10)
    
    # 自动调整x轴标签，避免重叠
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 显示图表
    st.pyplot(fig)
    
    # 数据统计摘要
    st.subheader('数据统计摘要')
    stats_df = df[['国家财政收入累计值(亿元)', '国家财政支出(不含债务还本)累计值(亿元)', '财政赤字(亿元)', '赤字率(%)']].describe()
    st.dataframe(stats_df, use_container_width=True)
    
    # 添加关键指标卡片显示
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("平均财政收入", f"{df['国家财政收入累计值(亿元)'].mean():.2f}亿元")
    with col2:
        st.metric("平均财政支出", f"{df['国家财政支出(不含债务还本)累计值(亿元)'].mean():.2f}亿元")
    with col3:
        st.metric("平均财政赤字", f"{df['财政赤字(亿元)'].mean():.2f}亿元")
    with col4:
        st.metric("平均赤字率", f"{df['赤字率(%)'].mean():.2f}%")
    
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
    
    # 筛选后数据的可视化
    st.subheader('筛选后数据趋势')
    
    # 创建小型图表展示筛选后的数据趋势
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # 为筛选后的数据添加趋势线
    filtered_df_sorted = filtered_df.sort_values('时间')
    filtered_df_sorted['month_index'] = range(len(filtered_df_sorted))
    
    # 绘制筛选后的财政收入和支出
    ax.plot(filtered_df_sorted['时间'], filtered_df_sorted['国家财政收入累计值(亿元)'], label='财政收入(亿元)', linewidth=2)
    ax.plot(filtered_df_sorted['时间'], filtered_df_sorted['国家财政支出(不含债务还本)累计值(亿元)'], label='财政支出(亿元)', linewidth=2)
    
    # 设置图表属性
    ax.set_xlabel('时间')
    ax.set_ylabel('金额(亿元)')
    ax.set_title('筛选后财政收支趋势')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    st.pyplot(fig)
    
    # 筛选后数据的基本统计
    st.write("筛选后数据的基本统计:")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("平均财政收入", f"{filtered_df['国家财政收入累计值(亿元)'].mean():.2f}亿元")
    with col2:
        st.metric("平均财政支出", f"{filtered_df['国家财政支出(不含债务还本)累计值(亿元)'].mean():.2f}亿元")
    with col3:
        st.metric("平均财政赤字", f"{filtered_df['财政赤字(亿元)'].mean():.2f}亿元")
    with col4:
        st.metric("平均赤字率", f"{filtered_df['赤字率(%)'].mean():.2f}%")
        
    # 添加宏观经济数据与财政数据的关联分析
    if macro_included:
        st.subheader('宏观经济指标与财政数据关联分析')
        
        # 找出所有的宏观经济指标列
        macro_cols = [col for col in df.columns if any(macro in col for macro in ['PMI', '货币', '投资', '进出口', '房地产'])]
        fiscal_cols = ['国家财政收入累计值(亿元)', '国家财政支出(不含债务还本)累计值(亿元)', '财政赤字(亿元)', '赤字率(%)']
        
        # 相关性分析
        with st.expander("📊 相关性分析"):
            st.markdown("### 宏观经济指标与财政数据的相关性系数")
            
            # 计算相关性
            if len(macro_cols) > 0 and len(fiscal_cols) > 0:
                # 选择需要分析的列
                analysis_cols = fiscal_cols + macro_cols
                corr_df = df[analysis_cols].corr()
                
                # 显示相关性矩阵热图
                fig, ax = plt.subplots(figsize=(12, 8))
                mask = np.triu(np.ones_like(corr_df, dtype=bool))
                sns.heatmap(corr_df, annot=True, cmap='coolwarm', center=0, mask=mask, 
                           linewidths=.5, cbar_kws={"shrink": .8}, ax=ax)
                plt.title('宏观经济指标与财政数据相关性矩阵', fontsize=14)
                plt.tight_layout()
                st.pyplot(fig)
                
                # 显示相关性最高的几对指标
                st.markdown("### 相关性最高的指标对")
                corr_values = corr_df.unstack()
                corr_values = corr_values[corr_values.index.get_level_values(0) != corr_values.index.get_level_values(1)]
                corr_values = corr_values.abs().sort_values(ascending=False)
                
                top_corr = corr_values.head(10)
                top_corr_df = pd.DataFrame(top_corr, columns=['相关系数'])
                st.dataframe(top_corr_df, use_container_width=True)
            else:
                st.info("没有找到足够的宏观经济指标或财政数据列进行相关性分析")
        
        # 宏观经济指标与财政收支的散点图分析
        with st.expander("📈 散点图分析"):
            st.markdown("### 宏观经济指标与财政收支的关系")
            
            if len(macro_cols) > 0:
                # 让用户选择要分析的宏观经济指标
                selected_macro = st.selectbox("选择宏观经济指标", macro_cols)
                
                # 创建散点图
                fig, axes = plt.subplots(2, 2, figsize=(14, 10))
                axes = axes.flatten()
                
                # 绘制与各个财政指标的散点图
                for i, fiscal_col in enumerate(fiscal_cols):
                    if i < len(axes):
                        # 去除NaN值
                        plot_df = df[[selected_macro, fiscal_col]].dropna()
                        
                        # 绘制散点图
                        sns.scatterplot(x=selected_macro, y=fiscal_col, data=plot_df, ax=axes[i])
                        
                        # 计算并绘制趋势线
                        if len(plot_df) > 1:
                            slope, intercept, r_value, p_value, std_err = stats.linregress(plot_df[selected_macro], plot_df[fiscal_col])
                            x_pred = np.linspace(plot_df[selected_macro].min(), plot_df[selected_macro].max(), 100)
                            y_pred = intercept + slope * x_pred
                            axes[i].plot(x_pred, y_pred, 'r-', label=f'Trend (r={r_value:.2f})')
                            axes[i].legend()
                        
                        axes[i].set_title(f'{selected_macro} 与 {fiscal_col} 的关系')
                        axes[i].grid(True, linestyle='--', alpha=0.7)
                
                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.info("没有找到宏观经济指标进行散点图分析")
        
        # 时间序列对比分析
        with st.expander("📉 时间序列对比分析"):
            st.markdown("### 宏观经济指标与财政数据的时间趋势对比")
            
            if len(macro_cols) > 0:
                # 让用户选择要比较的宏观经济指标
                selected_macro_ts = st.selectbox("选择要比较的宏观经济指标", macro_cols, key="ts_comparison")
                selected_fiscal_ts = st.selectbox("选择要比较的财政指标", fiscal_cols)
                
                # 创建双Y轴图表进行时间序列对比
                fig, ax1 = plt.subplots(figsize=(12, 6))
                
                # 绘制财政数据
                color = 'tab:blue'
                ax1.set_xlabel('时间', fontsize=12)
                ax1.set_ylabel(selected_fiscal_ts, color=color, fontsize=12)
                ax1.plot(df['时间'], df[selected_fiscal_ts], color=color, linewidth=2, label=selected_fiscal_ts)
                ax1.tick_params(axis='y', labelcolor=color)
                
                # 创建第二个Y轴用于宏观经济指标
                ax2 = ax1.twinx()
                color = 'tab:red'
                ax2.set_ylabel(selected_macro_ts, color=color, fontsize=12)
                ax2.plot(df['时间'], df[selected_macro_ts], color=color, linewidth=2, linestyle='--', label=selected_macro_ts)
                ax2.tick_params(axis='y', labelcolor=color)
                
                # 添加标题和图例
                fig.suptitle(f'{selected_fiscal_ts} 与 {selected_macro_ts} 的时间趋势对比', fontsize=14)
                lines1, labels1 = ax1.get_legend_handles_labels()
                lines2, labels2 = ax2.get_legend_handles_labels()
                ax1.legend(lines1 + lines2, labels1 + labels2, loc='best')
                
                # 设置网格
                ax1.grid(True, linestyle='--', alpha=0.7)
                
                # 自动调整x轴标签，避免重叠
                plt.xticks(rotation=45)
                plt.tight_layout()
                
                st.pyplot(fig)
                
                # 计算滞后相关性（分析宏观经济指标变化是否领先于财政数据变化）
                st.markdown("### 滞后相关性分析")
                st.write("分析宏观经济指标变化是否领先于财政数据变化，有助于预测财政趋势。")
                
                # 计算滞后0-6个月的相关性
                max_lag = 6
                lags = range(-max_lag, max_lag + 1)
                lag_corrs = []
                
                # 确保数据是完整的
                lag_df = df[[selected_macro_ts, selected_fiscal_ts]].dropna()
                
                if len(lag_df) > 2 * max_lag:
                    for lag in lags:
                        if lag < 0:
                            # 宏观指标滞后（财政指标领先）
                            corr = lag_df[selected_macro_ts].shift(-lag).corr(lag_df[selected_fiscal_ts])
                        else:
                            # 财政指标滞后（宏观指标领先）
                            corr = lag_df[selected_macro_ts].corr(lag_df[selected_fiscal_ts].shift(lag))
                        lag_corrs.append(corr)
                    
                    # 绘制滞后相关图
                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.bar(lags, lag_corrs)
                    ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
                    ax.set_xlabel(f'滞后月数（正: {selected_macro_ts} 领先，负: {selected_fiscal_ts} 领先）')
                    ax.set_ylabel('相关系数')
                    ax.set_title(f'{selected_macro_ts} 与 {selected_fiscal_ts} 的滞后相关性')
                    ax.grid(True, linestyle='--', alpha=0.7)
                    plt.tight_layout()
                    st.pyplot(fig)
                else:
                    st.info("数据量不足，无法进行滞后相关性分析")
            else:
                st.info("没有找到宏观经济指标进行时间序列对比分析")

else:
    st.warning("未加载到数据，请检查数据文件是否存在。")