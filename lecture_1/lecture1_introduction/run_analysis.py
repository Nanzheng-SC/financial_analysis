#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""西南财经大学与金融机构校企合作模式分析执行脚本"""

import os
import subprocess
import sys

def run_jupyter_notebook():
    """运行Jupyter Notebook中的数据分析流程"""
    print("===== 开始运行校企合作数据分析 ====")
    
    # 检查是否安装了必要的依赖包
    required_packages = ['pandas', 'numpy', 'matplotlib']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    # 安装缺失的依赖包
    if missing_packages:
        print(f"检测到缺失的依赖包：{', '.join(missing_packages)}")
        print("正在安装依赖包...")
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"成功安装 {package}")
            except subprocess.CalledProcessError:
                print(f"安装 {package} 失败，请手动安装")
                return False
    
    # 创建results文件夹（如果不存在）
    if not os.path.exists('results'):
        os.makedirs('results')
        print("创建results文件夹用于存储分析结果")
    
    # 运行Python分析脚本
    try:
        print("正在运行数据分析脚本...")
        # 获取当前脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        analysis_script = os.path.join(script_dir, 'university_industry_cooperation_analysis.py')
        subprocess.check_call([sys.executable, analysis_script])
        print("数据分析脚本运行完成")
        
        # 提示用户查看结果
        print("\n===== 数据分析完成 ====")
        print("分析结果已保存到results文件夹中，包括：")
        print("1. filtered_cooperation_data.csv - 筛选后的校企合作数据")
        print("2. monthly_trend.png - 月度合作趋势图")
        print("3. yearly_trend.png - 年度合作趋势图")
        print("\n建议在Jupyter Notebook中查看详细分析结果和图表：week1_homework.ipynb")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"数据分析脚本运行失败：{e}")
        return False
    except FileNotFoundError:
        print("找不到数据分析脚本，请确保university_industry_cooperation_analysis.py文件存在")
        return False

if __name__ == "__main__":
    success = run_jupyter_notebook()
    if not success:
        print("\n分析过程中出现错误，请检查上述错误信息并尝试解决问题后重新运行。")
    
    # 等待用户按任意键退出
    input("\n按任意键退出...")