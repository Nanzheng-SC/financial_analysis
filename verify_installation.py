import sys

print("Python版本:", sys.version)
print("\n验证金融数据分析库安装状态:")

# 核心库
try:
    import numpy
    print(f"numpy: {numpy.__version__}")
except ImportError:
    print("numpy: 未安装")

try:
    import pandas
    print(f"pandas: {pandas.__version__}")
except ImportError:
    print("pandas: 未安装")

try:
    import matplotlib
    print(f"matplotlib: {matplotlib.__version__}")
except ImportError:
    print("matplotlib: 未安装")

try:
    import seaborn
    print(f"seaborn: {seaborn.__version__}")
except ImportError:
    print("seaborn: 未安装")

# 金融专用库
print("\n验证金融专用库安装状态:")
try:
    import pandas_datareader
    print(f"pandas-datareader: {pandas_datareader.__version__}")
except ImportError:
    print("pandas-datareader: 未安装")

try:
    import yfinance
    print(f"yfinance: {yfinance.__version__}")
except ImportError:
    print("yfinance: 未安装")

try:
    # 尝试不同的导入方式
    try:
        import pyfolio
        print(f"pyfolio-reloaded/pyfolio: {pyfolio.__version__}")
    except ImportError:
        try:
            import pyfolio_reloaded
            print(f"pyfolio-reloaded: {pyfolio_reloaded.__version__}")
        except ImportError:
            import empyrical_reloaded
            print(f"empyrical-reloaded (pyfolio依赖): {empyrical_reloaded.__version__}")
except ImportError:
    print("pyfolio-reloaded: 未安装或导入方式不正确")

try:
    import statsmodels
    print(f"statsmodels: {statsmodels.__version__}")
except ImportError:
    print("statsmodels: 未安装")

# 机器学习库
print("\n验证机器学习库安装状态:")
try:
    import sklearn
    print(f"scikit-learn: {sklearn.__version__}")
except ImportError:
    print("scikit-learn: 未安装")

try:
    import xgboost
    print(f"xgboost: {xgboost.__version__}")
except ImportError:
    print("xgboost: 未安装")

try:
    import lightgbm
    print(f"lightgbm: {lightgbm.__version__}")
except ImportError:
    print("lightgbm: 未安装")

try:
    import catboost
    print(f"catboost: {catboost.__version__}")
except ImportError:
    print("catboost: 未安装")

try:
    import tensorflow
    print(f"tensorflow: {tensorflow.__version__}")
except ImportError:
    print("tensorflow: 未安装")

print("\n验证完成！")