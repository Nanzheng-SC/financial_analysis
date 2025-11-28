#!/bin/bash

# 设置Python环境变量
export PYTHONUNBUFFERED=1

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    python -m venv venv
fi

# 激活虚拟环境（在Streamlit Cloud上可能不需要这一步）
# source venv/bin/activate

# 升级pip
pip install --upgrade pip

# 安装依赖项
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# 输出安装的包列表，用于调试
pip list

# 创建.env文件的示例（如果不存在）
if [ ! -f ".env" ]; then
    echo "# Tushare API Token
toshare_token=your_token_here

# Doubao API Key
Doubao_API_KEY=your_api_key_here" > .env
    echo "已创建.env文件示例，请修改其中的API密钥"
fi