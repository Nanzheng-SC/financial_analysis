# 人民币汇率波动的宏观驱动因素研究

## 项目介绍

本项目旨在分析人民币汇率波动的宏观驱动因素，基于CPI、PMI、名义广义美元指数与社会事件等多维度数据，通过时间序列分析和事件研究法，探索各因素对人民币汇率的影响。

## 项目结构

```
人民币汇率波动的宏观驱动因素研究/
├── data/                 # 数据文件夹
│   ├── Fred_data_scraping.py     # FRED数据获取脚本
│   ├── china_CPI_month.csv       # 中国CPI月度数据
│   ├── china_PMI_month.csv       # 中国PMI月度数据
│   ├── event_list_v2.csv         # 事件列表
│   ├── fred_raw_data.csv         # FRED原始数据
│   ├── master_data.csv           # 合并后的主数据
│   └── master_data_processing.ipynb  # 数据处理 notebook
├── result/               # 结果输出文件夹
│   ├── cny_usd_exchange_rate.png    # 人民币兑美元汇率时间序列
│   ├── cny_vs_usd_index.png         # 人民币与美元指数对比
│   ├── event_study_by_type.png      # 事件研究结果
│   ├── event_window_returns.csv     # 事件窗口收益率数据
│   ├── event_type_car_boxplot.png   # 事件类型CAR箱线图
│   ├── rolling_correlation.png      # 滚动相关性分析
│   ├── tukey_test_result.png        # Tukey HSD检验结果图
│   └── us_dollar_index.png          # 美元指数时间序列
├── scripts/              # 分析脚本文件夹
│   ├── data_analysis_step1.py       # 数据可视化分析脚本
│   ├── event_study.py               # 事件研究脚本
│   └── event_study_anova.py         # 事件研究ANOVA分析脚本
├── 开题/                 # 开题相关文件
├── requirements.txt      # 依赖库列表
└── README.md             # 项目说明文档
```

## 数据说明

### 1. 原始数据来源
- **FRED数据**：通过Fred API获取，包含CNY_USD（人民币兑美元汇率）、USD_INDEX（美元指数）、US_10Y（美国10年期国债收益率）、US_CPI（美国CPI）
- **中国CPI**：从中国国家统计局获取的月度CPI数据
- **中国PMI**：从中国国家统计局获取的月度PMI数据
- **事件数据**：手动整理的影响人民币汇率的重要事件列表

### 2. 数据处理流程
1. 使用`Fred_data_scraping.py`从FRED API下载原始数据
2. 通过`master_data_processing.ipynb`合并多源数据，生成`master_data.csv`
3. 使用`data_analysis_step1.py`进行初步可视化分析
4. **事件研究第一步**：使用`event_study.py`进行基础事件研究，生成事件窗口收益率数据
5. **事件研究第二步**：使用`event_study_anova.py`进行事件研究的方差分析(ANOVA)，深入分析不同事件类型的影响差异

## 依赖库

项目使用以下主要依赖库：
- pandas>=2.0.0：数据处理与分析
- matplotlib>=3.7.0：数据可视化
- numpy>=1.24.0：数值计算
- fredapi>=0.5.0：FRED数据API访问
- python-dotenv>=1.0.0：环境变量管理
- scipy>=1.10.0：科学计算，用于方差分析
- statsmodels>=0.14.0：统计模型，用于Tukey HSD检验
- seaborn>=0.12.0：数据可视化，用于箱线图绘制

安装依赖库：
```bash
pip install -r requirements.txt
```

## 使用说明

### 1. 数据获取与处理

#### 获取FRED数据
```bash
cd data
python Fred_data_scraping.py
```

#### 处理并合并数据
打开并运行`master_data_processing.ipynb`，生成`master_data.csv`

### 2. 数据分析

#### 初步可视化分析
```bash
cd scripts
python data_analysis_step1.py
```

该脚本将生成以下可视化结果：
- 人民币兑美元汇率时间序列
- 美元指数时间序列
- 人民币与美元指数对比图
- 滚动相关性分析图

#### 事件研究分析（第一步）
```bash
cd scripts
python event_study.py
```

该脚本是事件研究的基础步骤，主要功能包括：
- 构建事件窗口（默认±10日）
- 计算事件窗口内的人民币汇率对数收益率
- 按事件类型计算平均反应
- 生成可视化图表展示不同事件类型的平均反应

**输出结果**：
- `result/event_window_returns.csv`：事件窗口收益率数据（供后续分析使用）
- `result/event_study_by_type.png`：不同事件类型的平均反应图

#### 事件研究方差分析（第二步）
```bash
cd scripts
python event_study_anova.py
```

该脚本是事件研究的深入分析步骤，**依赖于event_study.py的输出结果**，主要功能包括：
- 读取事件窗口收益率数据
- 计算[-1, +1]事件窗口的累积异常收益率(CAR)
- 进行单因素方差分析(ANOVA)，检验不同事件类型的CAR是否存在显著差异
- 执行Tukey HSD事后多重比较，确定哪些事件类型之间存在显著差异
- 生成可视化图表展示分析结果

**输出结果**：
- `result/event_type_car_boxplot.png`：不同事件类型的CAR分布箱线图
- `result/tukey_test_result.png`：Tukey HSD检验结果图

## 功能模块说明

### 1. Fred_data_scraping.py
- 从FRED API获取宏观经济数据
- 实现重试机制，处理API访问失败情况
- 保存原始数据到data/fred_raw_data.csv

### 2. master_data_processing.ipynb
- 读取并清洗多源数据
- 将数据从宽格式转换为长格式
- 合并数据生成data/master_data.csv

### 3. data_analysis_step1.py
- 人民币兑美元汇率时间序列可视化
- 美元指数时间序列可视化
- 人民币与美元指数对比分析
- 滚动相关性分析
- 生成可视化结果到result文件夹

### 4. event_study.py (事件研究基础脚本)
- **核心功能**：实现事件研究法的基础步骤
- **具体操作**：
  - 从主数据和事件表中构建事件窗口（默认±10日）
  - 计算事件窗口内的人民币汇率对数收益率
  - 按事件类型聚合计算平均反应
- **输出**：
  - `result/event_window_returns.csv`：事件窗口收益率数据（包含事件名称、类型、时间点和收益率）
  - `result/event_study_by_type.png`：不同事件类型的平均反应时间序列图
- **依赖**：主数据(master_data.csv)和事件表(event_list_v1.csv)
- **使用场景**：作为事件研究的第一步，为后续深入分析提供基础数据

### 5. event_study_anova.py (事件研究统计分析脚本)
- **核心功能**：对事件研究结果进行统计分析
- **具体操作**：
  - 读取`event_study.py`生成的事件窗口收益率数据
  - 计算[-1, +1]事件窗口的累积异常收益率(CAR)
  - 进行单因素方差分析(ANOVA)，检验不同事件类型的CAR是否存在显著差异
  - 执行Tukey HSD事后多重比较，确定哪些事件类型之间存在显著差异
- **输出**：
  - `result/event_type_car_boxplot.png`：不同事件类型的CAR分布箱线图
  - `result/tukey_test_result.png`：Tukey HSD检验结果图
- **依赖**：`event_study.py`生成的`event_window_returns.csv`
- **使用场景**：作为事件研究的第二步，深入分析不同事件类型的影响差异

### 两个脚本的关系与区别
1. **执行顺序**：必须先运行`event_study.py`，再运行`event_study_anova.py`
2. **功能定位**：
   - `event_study.py`：数据准备和初步分析，生成基础数据
   - `event_study_anova.py`：统计建模和深入分析，依赖基础数据
3. **输出内容**：
   - `event_study.py`：生成基础数据文件和趋势图
   - `event_study_anova.py`：生成统计分析结果和比较图
4. **保留建议**：两个脚本功能互补，均需保留，共同构成完整的事件研究流程

## 结果说明

### 1. 可视化结果
- **人民币兑美元汇率**：展示人民币汇率的历史走势
- **美元指数**：展示美元指数的历史走势
- **人民币与美元指数对比**：展示两者之间的关系
- **滚动相关性**：展示两者之间的动态相关性变化
- **事件研究结果**：展示不同类型事件对人民币汇率的影响
- **CAR分布箱线图**：展示不同事件类型的累积异常收益率(CAR)分布情况
- **Tukey HSD检验结果图**：展示不同事件类型CAR的事后多重比较结果

### 2. 数据文件
- **result/event_window_returns.csv**：包含各事件窗口的收益率数据
- **data/master_data.csv**：合并后的主数据，包含所有分析所需的变量

## 注意事项

1. 运行`Fred_data_scraping.py`需要FRED API密钥，请在根目录创建`.env`文件并添加：
   ```
   FRED_API_KEY=your_api_key
   ```

2. 数据文件路径已优化，脚本可在任意目录下运行

3. 结果将保存在`result`文件夹中

## 作者

张俊伟 （学号：42427086）

## 日期

2025年12月18日