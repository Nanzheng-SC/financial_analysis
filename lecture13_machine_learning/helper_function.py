import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import seaborn as sns

# 设置中文字体，提供多种备选字体以确保兼容性
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题


def strategy_evaluate(log_ret_clean, plot=True):
    '''
    评估策略表现
    参数：
        log_ret_clean: pd.Series，包含对数收益率数据，索引应为日期时间类型
        plot: bool，是否绘制策略表现图表，默认True
    返回：
        dict，包含年化收益率、年化波动率、夏普比率、最大回撤
    '''
    log_ret_clean = log_ret_clean.dropna()

    annual_ret = annualized_return(log_ret_clean)
    annual_vol = annualized_volatility(log_ret_clean)
    sharpe = sharpe_ratio(log_ret_clean)
    max_dd, start_date, end_date = max_drawdown(log_ret_clean)

    # 调用函数绘图
    if plot:
        plot_wealth_from_log_returns(log_return_series=log_ret_clean)
        plt.show()
        # 可以查看计算出的财富值序列
        print(f"策略表现评估 (基于对数收益率)")
        print("=" * 40)
        print(f"年化收益率: {annual_ret:.2%}")
        print(f"年化波动率: {annual_vol:.2%}")
        print(f"夏普比率 (无风险利率2%): {sharpe:.2f}")
        print(f"最大回撤: {max_dd:.2%}")
        print(f"最大回撤期: {start_date.date()} 至 {end_date.date()}")
    
    return {"annual_ret":annual_ret,
            "annual_volitity":annual_vol,
            "sharpe":sharpe,
            "max_dd":max_dd
           }

def plot_wealth_from_log_returns(log_return_series,
                                 initial_capital=100000,
                                 title='Strategy Wealth Growth (Based on Log Returns)',
                                 figsize=(10, 6)):
    # 1. Ensure data is sorted and work on a copy
    log_returns = log_return_series.sort_index().copy()

    # 2. Calculate cumulative wealth (Core step)
    cumulative_log_return = log_returns.cumsum()
    wealth_series = initial_capital * np.exp(cumulative_log_return)

    # 3. Create plot
    fig, ax = plt.subplots(figsize=figsize)

    # 4. Plot wealth curve
    ax.plot(wealth_series.index, wealth_series.values)

    # 5. Calculate and display key statistics
    total_return_log = log_returns.sum()
    total_return = np.exp(total_return_log) - 1
    final_wealth = wealth_series.iloc[-1]

    # Calculate annualized return (assuming 252 trading days)
    if len(log_returns) > 252:
        annualized_return = np.exp(log_returns.mean() * 252) - 1
        return_info = f'Ann. Return: {annualized_return:.1%}'
    else:
        return_info = ''

    stats_text = f'''Initial Capital: ¥{initial_capital:,.0f}
Final Wealth: ¥{final_wealth:,.0f}
Total Return: {total_return:+.1%}
{return_info}'''

    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
            verticalalignment='top', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9),
            family='monospace')

    # 6. Format the chart
    ax.set_xlabel('Date')
    ax.set_ylabel('Wealth (¥)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--', zorder=1)

    # Format x-axis dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    fig.autofmt_xdate(rotation=30, ha='right')

    # Format y-axis as currency
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'¥{x:,.0f}'))

    plt.tight_layout()
    return fig, ax, wealth_series


def max_drawdown(log_returns):
    """
    计算最大回撤
    参数：
        log_returns: pd.Series，对数收益率序列
    返回：
        tuple，包含 (最大回撤值, 最大回撤开始日期, 最大回撤结束日期)
    """
    # 检查输入是否为空
    if log_returns.empty:
        raise ValueError("log_returns 不能为空")
    # 根据对数收益率计算净值曲线
    
    # 1. Set initial capital (assume $100000)
    initial_capital = 100000
    # 2. Calculate cumulative wealth (Core step)
    cumulative_log_return = log_returns.cumsum()
    net_values = initial_capital * np.exp(cumulative_log_return)
    # 计算累积最大值（到当前日期为止的历史最高点）
    cumulative_max = net_values.expanding().max()
    # 计算每个时间点的回撤（从最高点的下跌幅度）
    drawdown = (net_values - cumulative_max) / cumulative_max
    # 找到最大回撤及其位置
    max_dd = drawdown.min()
    end_date = drawdown.idxmin()
    # 寻找最大回撤开始日期（回撤开始前的最后一个高点日期）
    start_date = net_values[:end_date].idxmax() if not pd.isnull(end_date) else None
    return max_dd, start_date, end_date


def sharpe_ratio(log_returns, risk_free_rate=0.02, periods_per_year=252):
    """
    计算夏普比率
    参数：
        log_returns: pd.Series，对数收益率序列
        risk_free_rate: float，年化无风险利率（默认2%）
        periods_per_year: int，年化周期数（默认252个交易日）
    返回：
        float，夏普比率
    """
    # 检查输入是否为空
    if log_returns.empty:
        raise ValueError("log_returns 不能为空")
    
    # 检查波动率是否为零，避免除零错误
    volatility = annualized_volatility(log_returns, periods_per_year)
    if volatility == 0:
        return 0.0
    
    excess_return = annualized_return(log_returns, periods_per_year) - risk_free_rate
    return excess_return / volatility


def annualized_volatility(log_returns, periods_per_year=252):
    """
    计算年化波动率
    参数：
        log_returns: pd.Series，对数收益率序列
        periods_per_year: int，年化周期数（默认252个交易日）
    返回：
        float，年化波动率
    """
    # 检查输入是否为 pd.Series
    if not isinstance(log_returns, pd.Series):
        raise TypeError("log_returns 必须是 pd.Series 类型")
    
    # 检查 periods_per_year 是否为正整数
    if not isinstance(periods_per_year, int) or periods_per_year <= 0:
        raise ValueError("periods_per_year 必须是正整数")
    
    # 计算年化波动率
    return log_returns.std() * np.sqrt(periods_per_year)

def annualized_return(log_returns, periods_per_year=252):
    """
    计算年化收益率
    参数：
        log_returns: pd.Series，对数收益率序列
        periods_per_year: int，年化周期数（默认252个交易日）
    返回：
        float，年化收益率
    """
    if log_returns.empty:
        return np.nan
    total_return = log_returns.sum()
    years = len(log_returns) / periods_per_year
    return np.exp(total_return / years) - 1

def calculate_log_returns(price_series):
    """
    计算对数收益率序列
    参数：
        price_series: pd.Series，包含价格数据（通常是收盘价），索引应为日期时间类型
    返回：
        pd.Series，对数收益率序列
    """
    return np.log(price_series / price_series.shift(1))


def moving_average_strategy(price_series, short_window=20, long_window=100, start_date=None):
    """
    实现双移动均线策略
    
    参数:
        price_series: pd.Series - 价格序列 (收盘价)
        short_window: int - 短期均线周期 (默认20天)
        long_window: int - 长期均线周期 (默认50天)
        start_date: str - 开始日期 (格式: 'YYYY-MM-DD')
    
    返回:
        dict - 包含策略所有结果的字典
    """
    # 准备数据
    prices = price_series.sort_index()
    if start_date:
        prices = prices[prices.index >= start_date]
    
    # 初始财富
    initial_capital = 100000
    
    # 计算移动平均线
    prices_df = pd.DataFrame(prices)
    prices_df.columns = ['Close']
    prices_df['SMA_Short'] = prices_df['Close'].rolling(window=short_window).mean()
    prices_df['SMA_Long'] = prices_df['Close'].rolling(window=long_window).mean()
    
    # 生成交易信号 (1:买入/持有, 0:卖出/空仓)
    # 当短期均线上穿长期均线时买入(金叉)
    prices_df['Signal'] = 0
    prices_df.loc[prices_df['SMA_Short'] > prices_df['SMA_Long'], 'Signal'] = 1
    
    # 计算策略收益率
    # 当日收益率 = 信号(t-1) * 当日对数收益率
    prices_df['Log_Return'] = np.log(prices_df['Close'] / prices_df['Close'].shift(1))
    prices_df['Strategy_Log_Return'] = prices_df['Signal'].shift(1) * prices_df['Log_Return']
    
    # 移除NaN值 (由于移动平均计算和shift操作)
    prices_df_clean = prices_df.dropna()
    
    # net_value buy and hold 
    net_value_buy_hold = initial_capital * np.exp(prices_df_clean['Log_Return'].dropna().cumsum())
    # strategy net value
    net_value_strategy = initial_capital * np.exp(prices_df_clean['Log_Return'].dropna().cumsum())
    
    # 提取关键序列
    results = {
        'price_series': prices_df['Close'],
        'signal_series': prices_df['Signal'],
        'log_returns':prices_df['Log_Return'].dropna(),
        'strategy_log_returns': prices_df_clean['Strategy_Log_Return'],  # 策略对数收益率
        'short_ma': prices_df['SMA_Short'],
        'long_ma': prices_df['SMA_Long'],
        'dates': prices_df.index,
        'net_value_buy_hold':net_value_buy_hold,
        'net_value_strategy':net_value_strategy,
        'df': prices_df  # 完整DataFrame
    }
    
    return results