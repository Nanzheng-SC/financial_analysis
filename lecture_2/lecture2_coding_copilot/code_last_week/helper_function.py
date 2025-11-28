def visualize_monthly_revenue(month):
    """ 
    读取国家财政预算收入数据并可视化每年特定月份的数据
    
    参数:
    month: int - 要可视化的月份（1-12）
    
    函数功能：
    1. 读取国家财政预算收入.xls数据文件
    2. 将时间列转换为日期类型并提取月份和年份
    3. 筛选出指定月份的数据
    4. 按年份排序数据
    5. 绘制指定月份的国家财政收入累计值趋势图
    """
    import matplotlib.pyplot as plt 
    import pandas as pd 
    # 设置中文字体以正常显示中文标签和负号
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签 
    plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
    # 读取数据 
    df = pd.read_excel('../data/national_data/国家财政预算收入.xls') 
    
    # 将时间列转换为日期类型并提取月份和年份 
    df['时间'] = pd.to_datetime(df['时间'], format='%Y年%m月') 
    df['月份'] = df['时间'].dt.month 
    df['年份'] = df['时间'].dt.year 
    
    # 筛选出指定月份的数据 
    monthly_data = df[df['月份'] == month] 
    
    # 按年份排序 
    monthly_data = monthly_data.sort_values('年份') 
    
    # 创建可视化 
    plt.figure(figsize=(12, 6)) 
    plt.plot(monthly_data['年份'], monthly_data['国家财政收入累计值(亿元)'], marker='o', linestyle='-', linewidth=2) 
    plt.title(f'每年{month}月份国家财政收入累计值') 
    plt.xlabel('年份') 
    plt.ylabel('国家财政收入累计值(亿元)') 
    plt.xticks(monthly_data['年份'], rotation=45) 
    plt.grid(True, linestyle='--', alpha=0.7) 
    plt.tight_layout() 
    plt.show()

def visualize_fiscal_revenue():
    """ 
    读取国家财政预算收入数据并绘制趋势图 
    
    函数功能：
    1. 读取国家财政预算收入.xls数据文件
    2. 处理中文日期格式，转换为标准日期格式
    3. 按时间排序数据
    4. 绘制国家财政收入累计值趋势图
    """
    import matplotlib.pyplot as plt 
    import pandas as pd 
    # 设置中文字体以正常显示中文标签和负号
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签 
    plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号

    # 读取数据 
    df = pd.read_excel('../data/national_data/国家财政预算收入.xls') 
    
    # 将中文日期格式转换为标准日期格式 
    # 推荐使用这个方法，处理'年'和'月'的中文格式
    df['时间'] = pd.to_datetime(df['时间'], format='%Y年%m月') 
    
    # 按时间排序数据
    df = df.sort_values('时间') 
    
    # 创建图形并绘制趋势图
    plt.figure(figsize=(12, 6)) 
    plt.plot(df['时间'], df['国家财政收入累计值(亿元)'], marker='o') 
    plt.title('国家财政收入累计值趋势') 
    plt.xlabel('时间') 
    plt.ylabel('国家财政收入累计值(亿元)') 
    plt.xticks(rotation=45) 
    plt.grid(True) 
    plt.tight_layout() 
    plt.show()

def visualize_fiscal_growth():
    """ 
    读取国家财政预算收入数据并可视化国家财政收入累计增长趋势
    
    函数功能：
    1. 读取国家财政预算收入.xls数据文件
    2. 将时间列转换为日期类型并排序
    3. 绘制国家财政收入累计增长趋势图
    """
    import pandas as pd 
    import matplotlib.pyplot as plt 
    import matplotlib as mpl 
    
    # 设置中文字体 
    mpl.rcParams['font.sans-serif'] = ['SimHei'] 
    mpl.rcParams['axes.unicode_minus'] = False 
    
    # 读取数据 
    df = pd.read_excel('../data/national_data/国家财政预算收入.xls') 
    
    # 将时间列转换为日期类型并排序 
    df['时间'] = pd.to_datetime(df['时间'], format='%Y年%m月') 
    df = df.sort_values('时间') 
    
    # 创建可视化 
    plt.figure(figsize=(12, 6)) 
    plt.plot(df['时间'], df['国家财政收入累计增长(%)'], marker='o', linestyle='-', linewidth=2) 
    plt.title('国家财政收入累计增长趋势') 
    plt.xlabel('时间') 
    plt.ylabel('国家财政收入累计增长(%)') 
    plt.xticks(rotation=45) 
    plt.grid(True, linestyle='--', alpha=0.7) 
    plt.tight_layout() 
    plt.show()

def load_fiscal_data():
    import pandas as pd
    df = pd.read_excel('../data/national_data/国家财政预算收入.xls')
    return df

# test 
