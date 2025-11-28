#!/bin/bash

# 设置Python环境变量
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
# 设置超时环境变量，避免API调用长时间挂起
export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200
export STREAMLIT_SERVER_MAX_MESSAGE_SIZE=200
export STREAMLIT_SERVER_SCRIPT_RUNNER_TIMEOUT=180
export STREAMLIT_CLIENT_PAGE_LOAD_TIMEOUT=30

# 检查Python版本
echo "检查Python版本..."
python --version

# 升级pip到最新版本
echo "升级pip..."
pip install --upgrade pip

# 在Streamlit Cloud上，我们不需要创建虚拟环境
# 因为平台会自动处理环境隔离

# 安装依赖项，添加--no-cache-dir以避免缓存问题
echo "安装依赖项..."
if [ -f "requirements.txt" ]; then
    pip install --no-cache-dir -r requirements.txt
fi

# 单独安装一些可能需要编译的包
echo "安装额外依赖..."
pip install --no-cache-dir numpy --upgrade
pip install --no-cache-dir pandas --upgrade

# 输出已安装的包列表
echo "已安装的包列表："
pip list

# 创建.env文件示例（如果不存在）
if [ ! -f ".env" ]; then
    echo "创建.env文件示例..."
    cat > .env << EOL
# .env文件示例
# 请将下面的示例值替换为实际的配置值

# Tushare API Token
toshare_token=your_tushare_token_here

# Doubao API Key
Doubao_API_KEY=your_doubao_api_key_here

# Doubao API Base URL
Doubao_API_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
EOL
    
    echo ".env文件示例已创建，请根据需要修改配置"
else
    echo ".env文件已存在，跳过创建"
fi

# 创建缓存目录
echo "创建Streamlit缓存目录..."
mkdir -p .streamlit/cache

# 设置文件权限
echo "设置文件权限..."
chmod -R 755 .streamlit

echo "环境设置完成！Streamlit应用已准备好部署。"