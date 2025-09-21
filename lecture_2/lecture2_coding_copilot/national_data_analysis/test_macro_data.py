import pandas as pd
import os

# 定义要测试的宏观经济数据文件路径
data_folder = 'e:/Study/2-1/finance_analysis/data/national_data/'
macro_files = {
    '货币供应量': '货币供应量.xls',
    '固定资产投资': '固定资产投资.xls',
    '进出口': '进出口.xls',
    '房地产': '房地产.xls',
    '制造业PMI': '制造业采购经理人指数.xls'
}

# 测试读取每个文件
def test_read_macro_file(file_name, full_path):
    try:
        print(f"\n尝试读取文件: {file_name}")
        # 尝试读取Excel文件
        df = pd.read_excel(full_path)
        
        # 显示文件基本信息
        print(f"文件形状: {df.shape}")
        print(f"列名: {df.columns.tolist()}")
        print("前5行数据:")
        print(df.head())
        
        # 检查是否有时间列
        time_columns = [col for col in df.columns if '时间' in str(col) or '日期' in str(col)]
        print(f"可能的时间列: {time_columns}")
        
        return df, True
    except Exception as e:
        print(f"读取文件 {file_name} 时出错: {e}")
        return None, False

# 测试所有文件
for file_name, file_path in macro_files.items():
    full_path = os.path.join(data_folder, file_path)
    if os.path.exists(full_path):
        df, success = test_read_macro_file(file_name, full_path)
        if success and not df.empty:
            # 尝试解析时间格式
            time_columns = [col for col in df.columns if '时间' in str(col) or '日期' in str(col)]
            if time_columns:
                # 尝试将时间列转换为datetime类型
                for col in time_columns:
                    try:
                        # 尝试常见的中文日期格式
                        df[col] = pd.to_datetime(df[col], format='%Y年%m月', errors='coerce')
                        # 如果转换后有有效值，显示时间范围
                        if not df[col].isnull().all():
                            print(f"时间范围: {df[col].min()} 到 {df[col].max()}")
                            break
                    except Exception:
                        continue
    else:
        print(f"文件不存在: {full_path}")

print("\n测试完成。")