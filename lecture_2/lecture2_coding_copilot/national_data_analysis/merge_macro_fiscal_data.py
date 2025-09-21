import pandas as pd
import os

# 设置文件路径
data_folder = 'e:/Study/2-1/finance_analysis/data/national_data/'
national_analysis_folder = 'e:/Study/2-1/finance_analysis/lecture_2/lecture2_coding_copilot/national_data_analysis/'

# 读取财政合并数据
def load_fiscal_data():
    try:
        fiscal_file = os.path.join(national_analysis_folder, 'fiscal_merged.xlsx')
        df = pd.read_excel(fiscal_file)
        # 转换时间列为日期类型
        df['时间'] = pd.to_datetime(df['时间'], format='%Y年%m月', errors='coerce')
        return df
    except Exception as e:
        print(f"读取财政数据时出错: {e}")
        return pd.DataFrame()

# 读取并处理宏观经济数据
def load_macro_data():
    # 定义要读取的宏观经济数据文件
    macro_files = {
        '货币供应量': {
            'file': '货币供应量.xls',
            'key_columns': ['时间', 'M2同比增长(%)']  # 选择关键指标
        },
        '固定资产投资': {
            'file': '固定资产投资.xls',
            'key_columns': ['时间', '固定资产投资完成额累计增长(%)']
        },
        '进出口': {
            'file': '进出口.xls',
            'key_columns': ['时间', '出口金额同比增长(%)', '进口金额同比增长(%)']
        },
        '房地产': {
            'file': '房地产.xls',
            'key_columns': ['时间', '房地产开发投资完成额累计增长(%)']
        },
        '制造业PMI': {
            'file': '制造业采购经理人指数.xls',
            'key_columns': ['时间', '制造业采购经理指数(%)']
        }
    }
    
    macro_dfs = {}
    
    for name, info in macro_files.items():
        try:
            file_path = os.path.join(data_folder, info['file'])
            if os.path.exists(file_path):
                df = pd.read_excel(file_path)
                # 转换时间列为日期类型
                df['时间'] = pd.to_datetime(df['时间'], format='%Y年%m月', errors='coerce')
                
                # 检查所有关键列是否存在
                available_columns = []
                for col in info['key_columns']:
                    if col in df.columns:
                        available_columns.append(col)
                    else:
                        # 尝试找到相似的列名
                        similar_cols = [c for c in df.columns if col.split('(')[0] in c]
                        if similar_cols:
                            available_columns.append(similar_cols[0])
                
                # 重命名列以避免合并时的名称冲突
                rename_dict = {}
                for col in available_columns:
                    if col != '时间':
                        rename_dict[col] = f"{name}_{col}"
                
                df = df[available_columns].rename(columns=rename_dict)
                macro_dfs[name] = df
                print(f"成功读取 {name} 数据，时间范围: {df['时间'].min()} 到 {df['时间'].max()}")
            else:
                print(f"文件不存在: {file_path}")
        except Exception as e:
            print(f"读取 {name} 数据时出错: {e}")
    
    return macro_dfs

# 合并财政数据和宏观经济数据
def merge_all_data(fiscal_df, macro_dfs):
    # 从财政数据开始
    merged_df = fiscal_df.copy()
    
    # 逐个合并宏观经济数据
    for name, df in macro_dfs.items():
        merged_df = pd.merge(merged_df, df, on='时间', how='left')
        print(f"合并 {name} 数据后，数据形状: {merged_df.shape}")
    
    # 去除重复的时间列（如果有）
    merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]
    
    return merged_df

# 主函数
def main():
    print("开始读取财政数据...")
    fiscal_df = load_fiscal_data()
    
    if fiscal_df.empty:
        print("无法加载财政数据，程序退出。")
        return
    
    print(f"财政数据加载完成，数据形状: {fiscal_df.shape}")
    print(f"财政数据时间范围: {fiscal_df['时间'].min()} 到 {fiscal_df['时间'].max()}")
    
    print("\n开始读取宏观经济数据...")
    macro_dfs = load_macro_data()
    
    print("\n开始合并所有数据...")
    merged_df = merge_all_data(fiscal_df, macro_dfs)
    
    # 保存合并后的数据
    output_file = os.path.join(national_analysis_folder, 'fiscal_macro_merged.xlsx')
    merged_df.to_excel(output_file, index=False)
    
    print(f"\n所有数据合并完成！")
    print(f"合并后的数据形状: {merged_df.shape}")
    print(f"合并后的数据已保存至: {output_file}")
    
    # 显示合并后的列名
    print("\n合并后的列名:")
    print(merged_df.columns.tolist())

if __name__ == "__main__":
    main()