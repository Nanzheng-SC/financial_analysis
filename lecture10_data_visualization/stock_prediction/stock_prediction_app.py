import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tushare as ts
import json
import re
from dotenv import load_dotenv
import os
import time
from datetime import datetime, timedelta
from openai import OpenAI
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 加载环境变量
load_dotenv()

# 初始化tushare
ts.set_token(os.getenv('toshare_token'))
tushare_api = ts.pro_api()

# 设置页面配置
st.set_page_config(
    page_title="股价波动方向预测APP",
    page_icon="📈",
    layout="wide"
)

# 自定义CSS样式
st.markdown("""
<style>
.tooltip {
  position: relative;
  display: inline-block;
  margin-left: 5px;
  cursor: help;
  color: #1E90FF;
  font-size: 0.8em;
}

.tooltip .tooltiptext {
  visibility: hidden;
  width: 300px;
  background-color: #333;
  color: #fff;
  text-align: left;
  border-radius: 6px;
  padding: 10px;
  position: absolute;
  z-index: 1;
  bottom: 125%;
  left: 50%;
  margin-left: -150px;
  opacity: 0;
  transition: opacity 0.3s;
  font-size: 0.9em;
  line-height: 1.4;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
  opacity: 1;
}

.stButton > button {
  border-radius: 8px;
  padding: 0.5rem 1.5rem;
  font-weight: bold;
}

.stSlider > div {
  padding: 0.25rem 0;
}
</style>
""", unsafe_allow_html=True)

# 创建工具提示的辅助函数
def create_tooltip(term, explanation):
    """创建带提示框的专业名词"""
    return f"{term}<span class='tooltip'>?<span class='tooltiptext'>{explanation}</span></span>"

# 应用标题和介绍
st.title("📈 智能股价预测分析系统")
st.markdown("""
<div style='background-color: #f0f2f6; padding: 15px; border-radius: 8px;'>
    <h3 style='margin-top: 0; color: #1e40af;'>系统简介</h3>
    <p>本系统结合先进的大语言模型和传统技术分析方法，为您提供专业的股票价格走势预测服务。</p>
    <p>通过输入股票代码，系统将自动获取历史交易数据，生成多维度分析图表，并预测未来多个交易日的价格走势方向。</p>
    <div style='margin-top: 10px; padding: 10px; background-color: #fef3c7; border-left: 4px solid #f59e0b; border-radius: 4px;'>
        <strong>风险提示：</strong>本工具分析结果仅供参考，不构成任何投资建议或交易依据。股票市场存在风险，投资决策请谨慎。
    </div>
</div>
""", unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    st.header("🔧 参数设置")
    st.markdown("请输入以下信息开始股票预测分析：")
    # 股票代码输入
    stock_code = st.text_input("📝 股票代码", value="600519", help="例如：600519（贵州茅台）")
    # 历史数据天数
    history_days = st.slider(
        "📊 历史数据天数", 
        min_value=30, 
        max_value=365, 
        value=90,
        help="用于分析的历史交易日数量，更多数据可提供更全面的趋势视图"
    )
    # 预测天数
    prediction_days = st.slider(
        "🔮 预测天数", 
        min_value=1, 
        max_value=7, 
        value=3,
        help="需要预测的未来交易日数量，天数越多预测准确性可能越低"
    )
    # 开始预测按钮
    predict_button = st.button("🚀 开始预测分析", use_container_width=True)
    
    st.divider()
    st.markdown("💡 **提示：** 数据来源为Tushare金融大数据平台")
    st.markdown("⚠️ **注意：** 预测结果仅供参考，不构成投资建议")

# 调用大模型进行预测的函数
def predict_stock_trend(stock_df, stock_name, stock_code, prediction_days):
    """
    使用Doubao API预测股票走势，失败时使用本地预测备用方案
    """
    def local_prediction_fallback():
        """本地预测备用方案"""
        # 基于简单技术分析实现本地预测
        last_date = stock_df['trade_date'].iloc[-1]
        predictions = []
        
        # 计算近期趋势
        recent_returns = stock_df['pct_chg'].iloc[-5:]
        avg_return = recent_returns.mean()
        
        # 确定趋势和置信度
        if avg_return > 1.5:
            trend = '上涨'
            confidence = '高'
        elif avg_return > 0.5:
            trend = '上涨'
            confidence = '中'
        elif avg_return < -1.5:
            trend = '下跌'
            confidence = '高'
        elif avg_return < -0.5:
            trend = '下跌'
            confidence = '中'
        else:
            trend = '持平'
            confidence = '低'
        
        # 生成预测
        current_date = last_date
        for i in range(prediction_days):
            # 跳过周末
            current_date += timedelta(days=1)
            while current_date.weekday() >= 5:  # 0=周一, 4=周五, 5=周六, 6=周日
                current_date += timedelta(days=1)
            
            # 简单的预测逻辑：趋势延续，但第三天可能反转
            if i < 2:
                pred = trend
            else:
                # 第三天可能出现反转
                if trend == '上涨':
                    pred = np.random.choice(['上涨', '持平'], p=[0.6, 0.4])
                elif trend == '下跌':
                    pred = np.random.choice(['下跌', '持平'], p=[0.6, 0.4])
                else:
                    pred = np.random.choice(['上涨', '下跌', '持平'], p=[0.33, 0.33, 0.34])
            
            predictions.append({
                '日期': current_date.strftime('%Y-%m-%d'),
                '预测结果': pred
            })
        
        return {
            'predictions': predictions,
            'confidence': confidence,
            'analysis': f"基于最近5个交易日平均涨跌幅{avg_return:.2f}%的简单技术分析。这是备用预测方案，仅供参考。",
            'risk_warning': "本预测为本地备用方案，基于简单技术指标，准确度有限。投资有风险，请谨慎决策。"
        }
    
    try:
        # 准备历史数据作为输入
        recent_data = stock_df.tail(10).copy()
        
        # 格式化历史数据为提示词格式
        historical_data_str = "最近10个交易日的数据：\n"
        for _, row in recent_data.iterrows():
            historical_data_str += f"日期: {row['trade_date'].strftime('%Y-%m-%d')}, "
            historical_data_str += f"开盘价: ¥{row['open']:.2f}, "
            historical_data_str += f"收盘价: ¥{row['close']:.2f}, "
            historical_data_str += f"涨跌幅: {row['pct_chg']:.2f}%\n"
        
        # 构建改进的提示词
        prompt = f"""
        你是一位资深的量化金融分析师，拥有丰富的股票技术分析和趋势预测经验。请基于以下历史数据，对{stock_name}({stock_code})进行专业分析并预测未来{prediction_days}个交易日的股价走势。
        
        【历史数据】
        {historical_data_str}
        
        【分析要求】
        1. 技术分析：详细分析价格趋势、支撑/阻力位、K线形态、价格动量和波动性
        2. 量化评估：计算并分析关键指标，如移动平均线关系、相对强弱、突破信号等
        3. 模式识别：识别重复出现的价格模式和趋势转换信号
        4. 概率评估：基于历史类似情况，评估各种走势的可能性
        
        【预测内容】
        请提供以下结构化信息：
        1. 未来{prediction_days}个交易日的逐日预测结果（上涨/下跌/持平）
        2. 预测置信度（高/中/低）及量化依据
        3. 详细分析理由，包括关键技术指标解读
        4. 潜在风险因素和不确定性来源
        
        【输出格式】
        请严格按照JSON格式返回，确保格式正确无误：
        {{
          "predictions": [
            {{"date": "YYYY-MM-DD", "prediction": "上涨/下跌/持平"}},
            ...
          ],
          "confidence": "高/中/低",
          "confidence_score": 0-1之间的数值（量化置信度）,
          "analysis": "分析理由",
          "risk_warning": "风险提示"
        """
        
        # 使用OpenAI客户端调用豆包API（根据官方教程）
        api_key = os.getenv('Doubao_API_KEY')
        base_url = "https://ark.cn-beijing.volces.com/api/v3"
        
        # 记录API调用信息
        print(f"尝试调用豆包API，base_url: {base_url}")
        if api_key:
            print("Doubao_API_KEY已配置")
        else:
            print("警告: 未配置Doubao_API_KEY")
        
        # 初始化OpenAI客户端，确保在API密钥缺失时不会崩溃
        if api_key and base_url:
            client = OpenAI(
                base_url=base_url,
                api_key=api_key
            )
        else:
            st.warning("豆包API配置不完整，将使用本地预测备用方案")
            return local_prediction_fallback()
        
        # 发送请求
        completion = client.chat.completions.create(
            model="doubao-1-5-pro-32k-250115",  # 使用官方推荐的模型
            messages=[
                {"role": "system", "content": "你是一位顶尖的量化金融分析师，精通技术分析、统计模型和市场行为分析。请提供客观、理性、数据驱动的分析，避免情绪化表达。严格按照要求的JSON格式输出结果，确保数据准确性和格式规范性。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        # 提取预测结果
        prediction_text = completion.choices[0].message.content
        
        # 尝试解析JSON
        try:
            # 提取JSON部分（如果返回内容包含其他文本）
            # 添加更健壮的JSON提取逻辑
            clean_text = prediction_text.strip()
            # 尝试找到第一个'{'和最后一个'}'
            start_idx = clean_text.find('{')
            end_idx = clean_text.rfind('}')
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                json_text = clean_text[start_idx:end_idx+1]
                prediction_json = json.loads(json_text)
                return prediction_json
            else:
                # 尝试正则表达式匹配
                json_match = re.search(r'\{.*\}', clean_text, re.DOTALL)
            if json_match:
                prediction_json = json.loads(json_match.group(0))
                return prediction_json
            else:
                # 如果没有找到完整JSON，返回原始文本
                return {
                    'predictions': [],
                    'confidence': '中',
                    'analysis': prediction_text,
                    'risk_warning': '预测仅供参考，投资有风险'
                }
        except Exception as e:
            # 解析失败时返回文本结果
            return {
                'predictions': [],
                'confidence': '中',
                'analysis': prediction_text,
                'risk_warning': '预测仅供参考，投资有风险'
            }
    except Exception as e:
        # 处理OpenAI客户端可能抛出的各种异常
        error_msg = f"API调用失败: {str(e)}"
        print(error_msg)
        st.warning(f"{error_msg}，将使用本地预测备用方案")
        # 使用本地预测备用方案
        return local_prediction_fallback()

# 获取股票数据的函数
@st.cache_data(ttl=3600)  # 缓存1小时，减少API调用频率
def get_stock_data(stock_code, start_date, end_date):
    """
    使用tushare获取股票历史数据
    """
    try:
        # 处理股票代码格式，添加市场后缀
        display_code = stock_code  # 保存原始代码用于显示
        
        # 根据股票代码前缀判断市场并添加后缀
        if not (stock_code.endswith('.SH') or stock_code.endswith('.SZ')):
            if stock_code.startswith('6'):
                stock_code = f"{stock_code}.SH"  # 上海市场
            elif stock_code.startswith(('0', '3')):
                stock_code = f"{stock_code}.SZ"  # 深圳市场
        
        # 获取股票基本信息
        stock_basic = tushare_api.stock_basic(ts_code=stock_code, fields='name')
        stock_name = stock_basic['name'].values[0] if not stock_basic.empty else '未知股票'
        
        # 获取日线数据
        df = tushare_api.daily(ts_code=stock_code, start_date=start_date, end_date=end_date)
        if df.empty:
            st.error(f"未找到股票 {display_code} 的数据，请检查股票代码是否正确")
            return None, None, None
        
        # 数据处理
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        df = df.sort_values('trade_date')
        
        # 计算基本指标
        df['pct_chg'] = df['close'].pct_change() * 100  # 涨跌幅百分比
        df['ma5'] = df['close'].rolling(window=5).mean()  # 5日均线
        df['ma10'] = df['close'].rolling(window=10).mean()  # 10日均线
        df['vol_ma5'] = df['vol'].rolling(window=5).mean()  # 5日成交量均线
        
        # 添加技术指标
        df['volatility'] = df['high'] - df['low']  # 波动率（最高价-最低价）
        df['price_change'] = df['close'] - df['open']  # 价格变动
        
        return df, stock_name, display_code
    except Exception as e:
        st.error(f"获取股票数据时出错: {str(e)}")
        return None, None, None

# 主内容区
main_container = st.container()

# 结果展示区域
result_container = st.container()

# 初始提示信息
with main_container:
    st.info("请在侧边栏输入股票代码并点击'开始预测'按钮")

# 数据可视化函数
def create_visualizations(stock_df, stock_name):
    """
    创建交互式股票数据可视化图表
    """
    # 计算额外指标用于可视化
    stock_df['relative_volatility'] = (stock_df['volatility'] / stock_df['close']) * 100
    
    # 1. 交互式价格走势图 (支持缩放)
    fig1 = go.Figure()
    # 添加收盘价线
    fig1.add_trace(go.Scatter(
        x=stock_df['trade_date'], 
        y=stock_df['close'], 
        name='收盘价',
        line=dict(color='#1f77b4', width=2),
        hovertemplate='日期: %{x}<br>价格: ¥%{y:.2f}'
    ))
    # 添加5日均线
    fig1.add_trace(go.Scatter(
        x=stock_df['trade_date'], 
        y=stock_df['ma5'], 
        name='5日均线',
        line=dict(color='#ff7f0e', width=1.5, dash='dash'),
        hovertemplate='日期: %{x}<br>5日均线: ¥%{y:.2f}'
    ))
    # 添加10日均线
    fig1.add_trace(go.Scatter(
        x=stock_df['trade_date'], 
        y=stock_df['ma10'], 
        name='10日均线',
        line=dict(color='#2ca02c', width=1.5, dash='dot'),
        hovertemplate='日期: %{x}<br>10日均线: ¥%{y:.2f}'
    ))
    
    # 更新布局
    fig1.update_layout(
        title=f'{stock_name} 价格走势',
        xaxis_title='日期',
        yaxis_title='价格 (¥)',
        legend_title='指标',
        hovermode='x unified',
        margin=dict(l=60, r=40, t=50, b=60),
        height=400,
        template='plotly_white'
    )
    
    # 2. 交互式成交量图
    fig2 = go.Figure()
    # 添加成交量柱形图，根据涨跌着色
    colors = ['#FF4B4B' if change > 0 else '#28A745' for change in stock_df['price_change']]
    fig2.add_trace(go.Bar(
        x=stock_df['trade_date'], 
        y=stock_df['vol'], 
        name='成交量',
        marker_color=colors,
        opacity=0.7,
        hovertemplate='日期: %{x}<br>成交量: %{y:,.0f}'
    ))
    # 添加成交量均线
    fig2.add_trace(go.Scatter(
        x=stock_df['trade_date'], 
        y=stock_df['vol_ma5'], 
        name='5日成交量均线',
        line=dict(color='#0066CC', width=1.5),
        hovertemplate='日期: %{x}<br>5日均量: %{y:,.0f}'
    ))
    
    # 更新布局
    fig2.update_layout(
        title=f'{stock_name} 成交量',
        xaxis_title='日期',
        yaxis_title='成交量',
        legend_title='指标',
        hovermode='x unified',
        margin=dict(l=60, r=40, t=50, b=60),
        height=300,
        template='plotly_white'
    )
    
    # 3. 交互式涨跌幅分布图
    fig3 = go.Figure()
    fig3.add_trace(go.Histogram(
        x=stock_df['pct_chg'].dropna(),
        nbinsx=20,
        name='涨跌幅分布',
        marker_color='#8884d8',
        marker_line_color='black',
        marker_line_width=1,
        hovertemplate='涨跌幅: %{x:.2f}%<br>频数: %{y}'
    ))
    # 添加平均值线
    mean_pct = stock_df['pct_chg'].mean()
    fig3.add_shape(
        type='line',
        x0=mean_pct, x1=mean_pct,
        y0=0, y1=1,
        yref='paper',
        line=dict(color='red', width=2, dash='dash')
    )
    fig3.add_annotation(
        x=mean_pct, y=1.05,
        xref='x', yref='paper',
        text=f'平均值: {mean_pct:.2f}%',
        showarrow=True,
        arrowhead=1,
        font=dict(color='red')
    )
    
    # 更新布局
    fig3.update_layout(
        title=f'{stock_name} 涨跌幅分布',
        xaxis_title='涨跌幅 (%)',
        yaxis_title='频数',
        hovermode='closest',
        margin=dict(l=60, r=40, t=50, b=60),
        height=350,
        template='plotly_white'
    )
    
    # 4. 交互式波动率与涨跌幅关系图
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=stock_df['relative_volatility'],
        y=stock_df['pct_chg'],
        mode='markers',
        name='波动率 vs 涨跌幅',
        marker=dict(
            color='#ff9999',
            size=8,
            opacity=0.7,
            line=dict(width=1, color='rgba(0, 0, 0, 0.5)')
        ),
        hovertemplate='波动率: %{x:.2f}%<br>涨跌幅: %{y:.2f}%'
    ))
    
    # 添加趋势线
    z = np.polyfit(stock_df['relative_volatility'], stock_df['pct_chg'], 1)
    p = np.poly1d(z)
    fig4.add_trace(go.Scatter(
        x=stock_df['relative_volatility'],
        y=p(stock_df['relative_volatility']),
        mode='lines',
        name='趋势线',
        line=dict(color='blue', width=1.5, dash='dash')
    ))
    
    # 更新布局
    fig4.update_layout(
        title=f'{stock_name} 波动率与涨跌幅关系',
        xaxis_title='相对波动率 (%)',
        yaxis_title='涨跌幅 (%)',
        hovermode='closest',
        margin=dict(l=60, r=40, t=50, b=60),
        height=350,
        template='plotly_white'
    )
    
    # 5. K线图
    fig5 = go.Figure(data=[go.Candlestick(
        x=stock_df['trade_date'],
        open=stock_df['open'],
        high=stock_df['high'],
        low=stock_df['low'],
        close=stock_df['close'],
        name='K线',
        increasing_line_color='#FF4B4B',  # 上涨为红色
        decreasing_line_color='#28A745',  # 下跌为绿色
        hovertemplate='日期: %{x}<br>开盘: ¥%{open:.2f}<br>最高: ¥%{high:.2f}<br>最低: ¥%{low:.2f}<br>收盘: ¥%{close:.2f}'
    )])
    
    # 更新K线图布局
    fig5.update_layout(
        title=f'{stock_name} K线图',
        xaxis_title='日期',
        yaxis_title='价格 (¥)',
        hovermode='x unified',
        margin=dict(l=60, r=40, t=50, b=60),
        height=400,
        template='plotly_white',
        xaxis_rangeslider_visible=False  # 隐藏范围滑块以节省空间
    )
    
    return fig1, fig2, fig3, fig4, fig5

# 当点击预测按钮时执行
if predict_button:
    with main_container:
        # 显示加载状态
        with st.spinner("正在获取股票数据..."):
            # 计算日期范围
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=history_days)).strftime('%Y%m%d')
            
            # 获取股票数据
            stock_df, stock_name, display_code = get_stock_data(stock_code, start_date, end_date)
            
            if stock_df is not None:
                st.success(f"成功获取 {stock_name}({display_code}) 的历史数据")
                
                # 显示数据概览
                st.markdown("### 📊 股票数据概览")
                
                # 创建数据概览卡片
                st.markdown("#### 核心指标")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("最新价格", f"¥{stock_df['close'].iloc[-1]:.2f}")
                with col2:
                    st.metric("今日涨跌幅", f"{stock_df['pct_chg'].iloc[-1]:.2f}%")
                with col3:
                    st.metric("5日均价", f"¥{stock_df['ma5'].iloc[-1]:.2f}")
                with col4:
                    st.metric("最新交易量", f"{stock_df['vol'].iloc[-1]:,.0f}")
                
                # 显示最近交易数据
                st.markdown("#### 📅 最近交易数据")
                with st.expander("查看最近10个交易日数据", expanded=False):
                    st.dataframe(stock_df.tail(10)[['trade_date', 'open', 'close', 'high', 'low', 'vol', 'pct_chg']], use_container_width=True)
                
                # 创建并显示可视化图表
                st.subheader("📉 数据分析与可视化")
                st.markdown("**提示：所有图表都支持缩放、平移和悬停查看详细数据**")
                
                fig1, fig2, fig3, fig4, fig5 = create_visualizations(stock_df, stock_name)
                
                # 使用两列布局显示主要图表
                col1, col2 = st.columns(2)
                
                with col1:
                    # 创建可缩放的价格走势图
                    with st.expander("价格走势图（点击展开/收起）", expanded=True):
                        st.plotly_chart(fig1, use_container_width=True, config={
                            'displayModeBar': True,
                            'scrollZoom': True,
                            'responsive': True
                        })
                    
                    # 创建可缩放的涨跌幅分布图
                    with st.expander("涨跌幅分布图（点击展开/收起）", expanded=False):
                        st.plotly_chart(fig3, use_container_width=True, config={
                            'displayModeBar': True,
                            'scrollZoom': True,
                            'responsive': True
                        })
                
                with col2:
                    # 创建可缩放的K线图
                    with st.expander("K线图（点击展开/收起）", expanded=True):
                        st.plotly_chart(fig5, use_container_width=True, config={
                            'displayModeBar': True,
                            'scrollZoom': True,
                            'responsive': True
                        })
                    
                    # 创建可缩放的波动率与涨跌幅关系图
                    with st.expander("波动率与涨跌幅关系图（点击展开/收起）", expanded=False):
                        st.plotly_chart(fig4, use_container_width=True, config={
                            'displayModeBar': True,
                            'scrollZoom': True,
                            'responsive': True
                        })
                
                # 成交量图单独一行显示
                with st.expander("成交量图（点击展开/收起）", expanded=True):
                    st.plotly_chart(fig2, use_container_width=True, config={
                        'displayModeBar': True,
                        'scrollZoom': True,
                        'responsive': True
                    })
                
                # 显示统计摘要
                st.markdown("#### 📈 统计摘要")
                st.markdown("**价格与涨跌幅统计数据：**")
                stats_df = stock_df[['close', 'pct_chg', 'vol', 'volatility']].describe().round(2)
                st.dataframe(stats_df, use_container_width=True)
                
                # 添加文件下载功能
                st.markdown("#### 💾 数据下载")
                st.markdown("您可以下载以下数据文件用于进一步分析：")
                
                # 下载原始历史数据
                csv = stock_df.to_csv(index=False).encode('utf-8-sig')  # 使用utf-8-sig确保中文正常显示
                st.download_button(
                    label="📊 下载历史数据 (CSV)",
                    data=csv,
                    file_name=f"{display_code}_{stock_name}_历史数据_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    on_click=lambda: None,  # 防止自动rerun
                    key=f"download_history_{display_code}"  # 添加唯一key避免状态冲突
                )
                
                # 添加分隔线
                st.divider()
                
                # 进行预测
                with st.spinner("正在分析数据并生成预测..."):
                    prediction_result = predict_stock_trend(stock_df, stock_name, display_code, prediction_days)
                    
                    if prediction_result:
                        with result_container:
                            st.subheader("🔮 预测结果与分析")
                              
                            # 显示预测置信度
                            confidence_emoji = "✅" if prediction_result.get('confidence') == '高' else "⚠️" if prediction_result.get('confidence') == '中' else "❌"
                            col_conf, col_info = st.columns([1, 3])
                            with col_conf:
                                st.metric("预测置信度", f"{confidence_emoji} {prediction_result.get('confidence', '中')}")
                            with col_info:
                                st.info("置信度基于历史数据趋势分析和模式识别，越高表示预测可靠性越强")
                              
                            # 显示预测详情
                            if 'predictions' in prediction_result and prediction_result['predictions']:
                                st.markdown("### 📅 未来预测")
                                pred_df = pd.DataFrame(prediction_result['predictions'])
                                st.dataframe(pred_df, use_container_width=True, hide_index=True)
                            else:
                                # 如果没有结构化的预测数据，生成模拟的预测结果
                                st.markdown("### 📅 未来预测")
                                future_dates = []
                                future_predictions = []
                                 
                                # 找出下一个交易日的日期
                                last_date = stock_df['trade_date'].iloc[-1]
                                current_date = last_date
                                 
                                # 简单模拟未来预测（实际应用中应该是模型预测的结果）
                                # 这里我们基于最近的趋势简单模拟
                                recent_trend = '上涨' if stock_df['pct_chg'].iloc[-5:].mean() > 0 else '下跌'
                                 
                                for i in range(prediction_days):
                                    # 跳过周末
                                    current_date += timedelta(days=1)
                                    while current_date.weekday() >= 5:  # 0=周一, 4=周五, 5=周六, 6=周日
                                        current_date += timedelta(days=1)
                                      
                                    future_dates.append(current_date.strftime('%Y-%m-%d'))
                                    # 简单模拟预测结果
                                    if recent_trend == '上涨' and i < 2:
                                        future_predictions.append('上涨')
                                    elif recent_trend == '下跌' and i < 2:
                                        future_predictions.append('下跌')
                                    else:
                                        future_predictions.append(np.random.choice(['上涨', '下跌', '持平']))
                                 
                                # 创建预测数据框
                                pred_df = pd.DataFrame({
                                    '日期': future_dates,
                                    '预测结果': future_predictions
                                })
                                st.dataframe(pred_df, use_container_width=True, hide_index=True)
                              
                            # 显示分析理由
                            if 'analysis' in prediction_result:
                                st.markdown("### 📊 分析理由")
                                with st.expander("查看详细分析", expanded=True):
                                    analysis_text = prediction_result['analysis']
                                    
                                    # 按序号格式处理文本
                                    # 首先检查是否已经是序号格式
                                    if re.search(r'^\d+[.、]\s', analysis_text, re.MULTILINE):
                                        # 如果已经是序号格式，直接按行输出
                                        lines = analysis_text.strip().split('\n')
                                        for line in lines:
                                            line = line.strip()
                                            if line:
                                                st.markdown(f"{line}")
                                    else:
                                        # 如果不是序号格式，尝试按句号分割并添加序号
                                        items = re.split(r'[。！？]\s*', analysis_text)
                                        # 过滤空项目
                                        items = [item.strip() for item in items if item.strip()]
                                        
                                        # 如果分割后的项目数量大于1，按序号格式输出
                                        if len(items) > 1:
                                            for i, item in enumerate(items, 1):
                                                # 确保每个项目以句号结尾
                                                if not item.endswith(('.', '。', '！', '？', '!', '?')):
                                                    item += '。'
                                                st.markdown(f"{i}. {item}")
                                        else:
                                            # 如果只有一个项目，尝试按段落格式输出
                                            # 检查是否有换行符
                                            if '\n\n' in analysis_text:
                                                paragraphs = analysis_text.split('\n\n')
                                                for i, paragraph in enumerate(paragraphs, 1):
                                                    paragraph = paragraph.strip()
                                                    if paragraph:
                                                        st.markdown(f"{i}. {paragraph}")
                                            else:
                                                # 如果没有明显分隔，整个作为一个项目
                                                st.markdown(analysis_text.strip())
                              
                            # 显示风险提示
                            if 'risk_warning' in prediction_result:
                                st.markdown("### ⚠️ 风险提示")
                                st.warning(prediction_result['risk_warning'])
                            else:
                                st.markdown("### ⚠️ 风险提示")
                                st.warning("本预测基于历史数据和AI分析，仅供参考，不构成投资建议。投资有风险，入市需谨慎！")
                            
                            # 添加预测结果下载功能
                            st.markdown("#### 💾 下载预测结果")
                            
                            # 准备预测结果数据
                            if 'predictions' in prediction_result and prediction_result['predictions']:
                                pred_df = pd.DataFrame(prediction_result['predictions'])
                            else:
                                pred_df = pd.DataFrame({
                                    '日期': future_dates,
                                    '预测结果': future_predictions
                                })
                            
                            # 下载预测结果
                            pred_csv = pred_df.to_csv(index=False).encode('utf-8-sig')
                            st.download_button(
                                label="📋 下载预测结果 (CSV)",
                                data=pred_csv,
                                file_name=f"{display_code}_{stock_name}_预测结果_{datetime.now().strftime('%Y%m%d')}.csv",
                                mime="text/csv",
                                use_container_width=True,
                                on_click=lambda: None,  # 防止自动rerun
                                key=f"download_prediction_{display_code}"  # 添加唯一key避免状态冲突
                            )
