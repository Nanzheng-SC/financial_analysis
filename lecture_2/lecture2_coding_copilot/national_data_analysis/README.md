# 财政数据分析应用

这是一个基于Streamlit的财政数据分析应用，支持宏观经济数据与财政数据的关联分析。

## 🚀 快速启动

为了避免每次在终端输入命令的麻烦，我们提供了以下便捷的启动方式：

### Windows 用户

**方法1：使用批处理文件（推荐）**
- 直接双击运行 `start_app.bat` 文件
- 应用会自动启动，并在浏览器中打开界面

**方法2：使用PowerShell脚本**
- 右键点击 `Start-App.ps1` 文件
- 选择 "使用PowerShell运行"
- （首次运行可能需要允许执行脚本）

### 手动启动（高级用户）

如果需要在特定环境或配置下启动应用，可以使用以下命令：

```powershell
# 进入应用目录
cd e:\Study\2-1\finance_analysis\lecture_2\lecture2_coding_copilot\national_data_analysis

# 安装依赖（首次运行）
pip install streamlit pandas matplotlib seaborn numpy scipy openpyxl

# 启动应用
python -m streamlit run fiscal_streamlit.py
```

## 📊 应用功能

1. **数据概览**
   - 显示数据记录数量和时间范围
   - 显示包含的宏观经济指标

2. **财政数据表格**
   - 完整财政数据展示
   - 支持时间范围筛选

3. **收支趋势分析**
   - 收入/支出趋势图（含趋势线）
   - 收支平衡平滑曲线

4. **赤字分析**
   - 赤字与赤字率图表（含国际警戒线）
   - 可展开的赤字解释说明

5. **宏观经济关联分析**（新增功能）
   - **相关性分析**：宏观经济指标与财政数据的相关性矩阵热图
   - **散点图分析**：直观展示指标间关系，含趋势线和相关系数
   - **时间序列对比**：双Y轴图表比较不同指标的时间趋势
   - **滞后相关性分析**：识别宏观经济变化对财政的领先/滞后效应

## 🛠️ 环境要求

- Python 3.7+ 
- 所需依赖包：
  - streamlit
  - pandas
  - matplotlib
  - seaborn
  - numpy
  - scipy
  - openpyxl (用于读取Excel文件)

## 📁 数据文件说明

应用使用以下数据文件：

- `fiscal_merged.xlsx`：基础财政数据（收入、支出、赤字等）
- `fiscal_macro_merged.xlsx`：合并了宏观经济数据的完整数据集

## 🔧 故障排除

如果应用无法正常启动或运行，请尝试以下解决方法：

1. **Python未找到**
   - 确保Python已正确安装并添加到系统环境变量
   - 可以在命令提示符中输入 `python --version` 验证

2. **依赖包缺失**
   - 运行 `pip install -r requirements.txt` 安装所有依赖（如果创建了requirements.txt文件）
   - 或手动安装所需包：`pip install streamlit pandas matplotlib seaborn numpy scipy openpyxl`

3. **端口被占用**
   - 如果8502端口被占用，可以使用 `streamlit run fiscal_streamlit.py --server.port 其他端口号` 更改端口

4. **数据文件问题**
   - 确保 `fiscal_merged.xlsx` 或 `fiscal_macro_merged.xlsx` 文件存在且格式正确

## 💡 使用提示

- 在时间筛选器中，可以选择特定的时间范围进行数据分析
- 所有图表都支持交互，包括缩放、平移和悬停查看详细数据
- 关联分析模块中的各项功能都以可展开面板形式展示，点击标题即可展开/收起
- 对于滞后相关性分析，可以帮助识别宏观经济变化对财政的领先/滞后关系，有助于预测未来财政趋势

## 📝 开发说明

如果需要修改或扩展应用功能，可以编辑以下文件：

- `fiscal_streamlit.py`：主应用程序文件
- `merge_fiscal_data.py`：财政数据合并脚本
- `merge_macro_fiscal_data.py`：财政与宏观经济数据合并脚本