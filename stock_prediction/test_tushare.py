import tushare as ts
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化tushare
ts.set_token(os.getenv('toshare_token'))
tushare_api = ts.pro_api()

def test_stock_code_format():
    """测试不同格式的股票代码"""
    print("测试不同格式的股票代码...")
    
    # 测试不同格式的股票代码
    test_codes = [
        "600519",         # 仅股票代码
        "600519.SH",     # 股票代码+市场后缀(SH-上海)
        "600519.ss"      # 另一种格式
    ]
    
    for code in test_codes:
        print(f"\n测试代码: {code}")
        try:
            # 尝试获取基本信息
            basic_info = tushare_api.stock_basic(ts_code=code, fields='name')
            print(f"基本信息: {basic_info}")
            
            # 尝试获取最新行情
            from datetime import datetime, timedelta
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=5)).strftime('%Y%m%d')
            
            daily_data = tushare_api.daily(ts_code=code, start_date=start_date, end_date=end_date)
            print(f"日线数据行数: {len(daily_data)} 行")
            if not daily_data.empty:
                print(f"最新收盘价: {daily_data['close'].iloc[0]}")
                
        except Exception as e:
            print(f"错误: {str(e)}")

if __name__ == "__main__":
    test_stock_code_format()
