@echo off

REM 启动Streamlit应用程序的批处理文件
REM 双击此文件即可运行财政数据分析应用

REM 确保在当前目录执行
cd /d "%~dp0"

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python。请先安装Python并添加到系统环境变量。
    pause
    exit /b 1
)

REM 检查Streamlit是否安装
python -m streamlit --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 未找到Streamlit，正在尝试安装...
    pip install streamlit pandas matplotlib seaborn numpy scipy openpyxl
    if %errorlevel% neq 0 (
        echo 错误: Streamlit安装失败。请手动安装所需依赖。
        pause
        exit /b 1
    )
)

REM 启动Streamlit应用
echo 正在启动财政数据分析应用...
echo 应用启动后，浏览器将自动打开。
echo 如果浏览器未自动打开，请访问 http://localhost:8502
python -m streamlit run fiscal_streamlit.py

REM 如果应用意外关闭，显示错误信息
if %errorlevel% neq 0 (
    echo 应用程序意外关闭。
    pause
    exit /b %errorlevel%
)