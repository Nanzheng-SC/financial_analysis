import subprocess
import sys

# 定义清华镜像源地址
TSINGHUA_MIRROR = "https://pypi.tuna.tsinghua.edu.cn/simple"

# 定义数据分析常用库列表
DATA_SCIENCE_LIBRARIES = [
    # 基础数据处理
    "numpy",
    "pandas",
    # 数据可视化
    "matplotlib",
    "seaborn",
    "plotly",
    "bokeh",
    # 科学计算与统计
    "scipy",
    "statsmodels",
    # 机器学习
    "scikit-learn",
    "xgboost",
    "lightgbm",
    "catboost",
    # 深度学习
    "tensorflow",
    "pytorch",
    # 数据读取与导出
    "openpyxl",
    "xlrd",
    "xlsxwriter",
    "pandas-datareader",
    "sqlalchemy",
    "psycopg2-binary",
    "pymysql",
    # 文本处理
    "nltk",
    "jieba",
    "wordcloud",
    # Web相关
    "requests",
    "beautifulsoup4",
    "flask",
    "fastapi",
    "uvicorn",
    "streamlit",
    # 其他工具
    "jupyter",
    "notebook",
    "ipython",
    "tqdm",
    "pyyaml",
    "click",
    "colorama"
]

def install_library(library_name):
    """使用清华镜像源安装指定的库"""
    try:
        print(f"正在安装 {library_name}...")
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "pip", 
            "install", 
            "-i", 
            TSINGHUA_MIRROR, 
            "--trusted-host", 
            "pypi.tuna.tsinghua.edu.cn",
            library_name
        ])
        print(f"✅ {library_name} 安装成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {library_name} 安装失败: {e}")
        return False

def main():
    print("======= 数据分析库安装脚本 =======")
    print(f"使用镜像源: {TSINGHUA_MIRROR}")
    print(f"共需安装 {len(DATA_SCIENCE_LIBRARIES)} 个库\n")
    
    # 更新pip到最新版本
    print("先更新pip到最新版本...")
    subprocess.call([
        sys.executable, 
        "-m", 
        "pip", 
        "install", 
        "--upgrade", 
        "pip",
        "-i", 
        TSINGHUA_MIRROR,
        "--trusted-host", 
        "pypi.tuna.tsinghua.edu.cn"
    ])
    
    # 安装所有库
    success_count = 0
    fail_count = 0
    
    for library in DATA_SCIENCE_LIBRARIES:
        if install_library(library):
            success_count += 1
        else:
            fail_count += 1
    
    # 打印安装结果汇总
    print("\n======= 安装结果汇总 =======")
    print(f"总计: {len(DATA_SCIENCE_LIBRARIES)} 个库")
    print(f"成功: {success_count} 个库")
    print(f"失败: {fail_count} 个库")
    
    if fail_count > 0:
        print("\n💡 提示：部分库安装失败，建议重新运行脚本或手动安装失败的库。")
    else:
        print("\n🎉 所有库安装成功！您现在可以开始数据分析工作了。")

if __name__ == "__main__":
    main()