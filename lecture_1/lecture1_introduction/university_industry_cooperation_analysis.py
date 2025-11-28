import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from datetime import datetime
import os

# 设置中文显示 - 优先使用Windows系统常用字体
plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

class UniversityIndustryCooperationAnalyzer:
    """西南财经大学与金融机构合作模式分析工具"""
    
    def __init__(self):
        self.data = None
        self.filtered_data = None
        self.trend_data = None
        self.data_path = "../data/swufe/swufe_news.csv"
        
    def load_data(self):
        """加载原始新闻数据"""
        try:
            # 读取CSV文件
            self.data = pd.read_csv(self.data_path)
            print(f"成功加载数据，共{len(self.data)}条记录")
            return True
        except Exception as e:
            print(f"加载数据失败：{e}")
            # 尝试备用路径
            try:
                alternate_path = "c:\\Users\\Nanzheng\\大二上\\金融数据分析与可视化\\第一周\\financial_data_analysis\\financial_data_analysis\\data\\swufe\\swufe_news.csv"
                self.data = pd.read_csv(alternate_path)
                print(f"成功从备用路径加载数据，共{len(self.data)}条记录")
                return True
            except Exception as e2:
                print(f"备用路径加载失败：{e2}")
                return False
    
    def preprocess_data(self):
        """数据预处理"""
        if self.data is None:
            print("请先加载数据")
            return False
        
        # 1. 数据清洗
        # 复制数据以避免修改原始数据
        cleaned_data = self.data.copy()
        
        # 2. 处理日期格式
        def parse_date(date_str):
            try:
                # 尝试多种日期格式
                if '.' in date_str:
                    return datetime.strptime(date_str, '%Y.%m.%d')
                elif '-' in date_str:
                    return datetime.strptime(date_str, '%Y-%m-%d')
                else:
                    return None
            except:
                return None
        
        cleaned_data['date'] = cleaned_data['date'].apply(parse_date)
        
        # 3. 过滤出校企合作相关的新闻
        # 定义金融机构关键词和合作关键词
        financial_institutions = ['银行', '保险', '证券', '基金', '金融', '银保监', '税务局', '财税', '投资', '会计师事务所', '财经', '民生银行', '四川银行']
        cooperation_terms = ['合作', '协议', '签署', '共建', '战略', '基地', '产学研']
        
        # 创建正则表达式模式
        finance_pattern = '|'.join(financial_institutions)
        cooperation_pattern = '|'.join(cooperation_terms)
        
        # 筛选包含金融机构和合作关键词的新闻
        filtered_mask = (cleaned_data['title'].str.contains(finance_pattern, case=False, na=False) | 
                         cleaned_data['text'].str.contains(finance_pattern, case=False, na=False)) & (cleaned_data['title'].str.contains(cooperation_pattern, case=False, na=False) |
                         cleaned_data['text'].str.contains(cooperation_pattern, case=False, na=False))
        
        self.filtered_data = cleaned_data[filtered_mask].copy()
        self.filtered_data = self.filtered_data.sort_values('date')
        
        print(f"筛选出校企合作相关新闻{len(self.filtered_data)}条")
        return True
    
    def analyze_trend(self):
        """进行时间趋势分析"""
        if self.filtered_data is None:
            print("请先进行数据预处理")
            return False
        
        # 按年份和月份统计合作数量
        self.filtered_data['year_month'] = self.filtered_data['date'].dt.to_period('M')
        self.filtered_data['year'] = self.filtered_data['date'].dt.year
        
        # 按月统计趋势
        monthly_counts = self.filtered_data.groupby('year_month').size().reset_index(name='count')
        monthly_counts['date'] = monthly_counts['year_month'].dt.to_timestamp()
        
        # 按年统计趋势
        yearly_counts = self.filtered_data.groupby('year').size().reset_index(name='count')
        
        self.trend_data = {
            'monthly': monthly_counts,
            'yearly': yearly_counts
        }
        
        print("时间趋势分析完成")
        return True
    
    def visualize_trend(self):
        """可视化时间趋势"""
        if self.trend_data is None:
            print("请先进行趋势分析")
            return False
        
        # 创建结果文件夹
        if not os.path.exists('results'):
            os.makedirs('results')
        
        # 1. 月度趋势图
        plt.figure(figsize=(14, 6))
        plt.plot(self.trend_data['monthly']['date'], self.trend_data['monthly']['count'], 
                 marker='o', linestyle='-', color='#1f77b4')
        plt.title('西南财经大学与金融机构合作月度趋势（2020-2025）', fontsize=16)
        plt.xlabel('日期', fontsize=12)
        plt.ylabel('合作数量', fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # 设置x轴刻度为每个数据点对应的月份
        plt.xticks(self.trend_data['monthly']['date'], 
                  [date.strftime('%Y-%m') for date in self.trend_data['monthly']['date']],
                  rotation=45, ha='right', fontsize=8)
        
        plt.tight_layout()
        plt.savefig('results/monthly_trend.png', dpi=300)
        plt.close()
        
        # 2. 年度趋势图
        plt.figure(figsize=(10, 6))
        bars = plt.bar(self.trend_data['yearly']['year'].astype(str), self.trend_data['yearly']['count'], 
                      color='#2ca02c', alpha=0.8)
        plt.title('西南财经大学与金融机构合作年度趋势（2020-2025）', fontsize=16)
        plt.xlabel('年份', fontsize=12)
        plt.ylabel('合作数量', fontsize=12)
        
        # 在柱状图上添加数值标签
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.1, 
                     f'{int(height)}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('results/yearly_trend.png', dpi=300)
        plt.close()
        
        print("趋势可视化完成，图表已保存到results文件夹")
        return True
    
    def export_filtered_data(self):
        """导出筛选后的数据"""
        if self.filtered_data is None:
            print("没有可导出的数据")
            return False
        
        # 创建结果文件夹
        if not os.path.exists('results'):
            os.makedirs('results')
        
        # 导出筛选后的数据
        self.filtered_data.to_csv('results/filtered_cooperation_data.csv', index=False, encoding='utf-8-sig')
        print("筛选后的数据已导出到results/filtered_cooperation_data.csv")
        return True
    
    def analyze_cooperation_models(self):
        """分析校企合作模式"""
        if self.filtered_data is None:
            print("请先进行数据预处理")
            return False
        
        # 定义合作模式分类
        cooperation_patterns = {
            '战略合作协议': ['战略', '合作协议', '战略合作'],
            '产学研合作': ['产学研', '研究', '协同创新'],
            '实习基地': ['实习', '实践', '基地'],
            '人才培养': ['人才', '培养', '教育', '教学'],
            '科研项目': ['科研', '项目', '课题', '研究'],
            '其他合作': []
        }
        
        # 为每条新闻分类合作模式
        self.filtered_data['cooperation_model'] = '其他合作'
        
        for model, keywords in cooperation_patterns.items():
            if model == '其他合作':
                continue
            
            pattern = '|'.join(keywords)
            mask = (self.filtered_data['title'].str.contains(pattern, case=False, na=False) |
                   self.filtered_data['text'].str.contains(pattern, case=False, na=False))
            self.filtered_data.loc[mask, 'cooperation_model'] = model
        
        # 统计各合作模式数量
        model_counts = self.filtered_data['cooperation_model'].value_counts()
        
        # 保存分析结果
        self.cooperation_model_data = {
            'counts': model_counts
        }
        
        print("合作模式分析完成")
        print("各合作模式数量：")
        print(model_counts)
        return True
    
    def analyze_institution_types(self):
        """分析合作机构类型分布"""
        if self.filtered_data is None:
            print("请先进行数据预处理")
            return False
        
        # 定义机构类型关键词
        institution_types = {
            '银行': ['银行', '银保监'],
            '保险机构': ['保险', '财险', '寿险'],
            '证券/基金': ['证券', '基金', '券商'],
            '会计师事务所': ['会计师事务所', '审计', '会计'],
            '政府部门': ['税务局', '财税', '财政', '政府'],
            '其他金融机构': []
        }
        
        # 为每条新闻分类机构类型
        self.filtered_data['institution_type'] = '其他金融机构'
        
        for inst_type, keywords in institution_types.items():
            if inst_type == '其他金融机构':
                continue
            
            pattern = '|'.join(keywords)
            mask = (self.filtered_data['title'].str.contains(pattern, case=False, na=False) |
                   self.filtered_data['text'].str.contains(pattern, case=False, na=False))
            self.filtered_data.loc[mask, 'institution_type'] = inst_type
        
        # 统计各机构类型数量
        institution_counts = self.filtered_data['institution_type'].value_counts()
        
        # 保存分析结果
        self.institution_type_data = {
            'counts': institution_counts
        }
        
        print("机构类型分析完成")
        print("各机构类型数量：")
        print(institution_counts)
        return True
    
    def evaluate_implementation(self):
        """成果落地评估"""
        if not hasattr(self, 'cooperation_model_data'):
            print("请先分析合作模式")
            return False
        
        if not hasattr(self, 'institution_type_data'):
            print("请先分析机构类型")
            return False
        
        # 1. 计算合作深度指标
        # 计算合作模式多样性（熵值）
        model_probs = self.cooperation_model_data['counts'] / len(self.filtered_data)
        model_diversity = -np.sum(model_probs * np.log(model_probs + 1e-9))
        
        # 计算机构类型多样性
        inst_probs = self.institution_type_data['counts'] / len(self.filtered_data)
        inst_diversity = -np.sum(inst_probs * np.log(inst_probs + 1e-9))
        
        # 2. 计算合作持续性指标（基于时间分布）
        # 计算月度合作数量的变异系数
        monthly_std = self.trend_data['monthly']['count'].std()
        monthly_mean = self.trend_data['monthly']['count'].mean()
        continuity_score = 1 - (monthly_std / (monthly_mean + 1e-9)) if monthly_mean > 0 else 0
        
        # 确保持续性得分在0-1之间
        continuity_score = max(0, min(1, continuity_score))
        
        # 3. 计算总体评估得分
        # 综合多样性和持续性指标
        implementation_score = (model_diversity + inst_diversity + continuity_score) / 3
        
        # 保存评估结果
        self.implementation_evaluation = {
            'model_diversity': model_diversity,
            'institution_diversity': inst_diversity,
            'continuity_score': continuity_score,
            'implementation_score': implementation_score
        }
        
        print("\n===== 成果落地评估结果 =====")
        print(f"合作模式多样性: {model_diversity:.4f}")
        print(f"机构类型多样性: {inst_diversity:.4f}")
        print(f"合作持续性得分: {continuity_score:.4f}")
        print(f"总体评估得分: {implementation_score:.4f}")
        print("========================")
        
        return True
    
    def visualize_implementation(self):
        """可视化成果落地评估结果"""
        if not hasattr(self, 'implementation_evaluation'):
            print("请先进行成果落地评估")
            return False
        
        # 创建结果文件夹
        if not os.path.exists('results'):
            os.makedirs('results')
        
        # 1. 合作模式饼图
        plt.figure(figsize=(10, 8))
        model_counts = self.cooperation_model_data['counts']
        plt.pie(model_counts.values, labels=model_counts.index, autopct='%1.1f%%',
               startangle=90, shadow=True)
        plt.title('西南财经大学与金融机构合作模式分布', fontsize=16)
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig('results/cooperation_model_distribution.png', dpi=300)
        plt.close()
        
        # 2. 机构类型柱状图
        plt.figure(figsize=(12, 6))
        inst_counts = self.institution_type_data['counts']
        bars = plt.bar(inst_counts.index, inst_counts.values, color='#9467bd', alpha=0.8)
        plt.title('合作金融机构类型分布', fontsize=16)
        plt.xlabel('机构类型', fontsize=12)
        plt.ylabel('合作数量', fontsize=12)
        
        # 在柱状图上添加数值标签
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                     f'{int(height)}', ha='center', va='bottom')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('results/institution_type_distribution.png', dpi=300)
        plt.close()
        
        # 3. 评估指标雷达图
        metrics = ['模式多样性', '机构多样性', '合作持续性']
        scores = [
            self.implementation_evaluation['model_diversity'] / max(2, self.implementation_evaluation['model_diversity']),
            self.implementation_evaluation['institution_diversity'] / max(2, self.implementation_evaluation['institution_diversity']),
            self.implementation_evaluation['continuity_score']
        ]
        
        # 确保所有得分在0-1之间
        scores = [min(1, max(0, score)) for score in scores]
        
        # 雷达图数据准备
        angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
        scores = scores + scores[:1]
        angles = angles + angles[:1]
        metrics = metrics + metrics[:1]
        
        plt.figure(figsize=(10, 8))
        ax = plt.subplot(111, polar=True)
        ax.plot(angles, scores, 'o-', linewidth=2, color='#e377c2')
        ax.fill(angles, scores, alpha=0.25, color='#e377c2')
        ax.set_thetagrids(np.degrees(angles[:-1]), metrics[:-1])
        ax.set_ylim(0, 1)
        plt.title('校企合作成果落地评估雷达图', fontsize=16, pad=20)
        plt.tight_layout()
        plt.savefig('results/implementation_radar_chart.png', dpi=300)
        plt.close()
        
        print("成果落地评估可视化完成，图表已保存到results文件夹")
        return True

if __name__ == "__main__":
    # 创建分析器实例
    analyzer = UniversityIndustryCooperationAnalyzer()
    
    # 执行数据读取、预处理和趋势分析
    print("===== 开始校企合作数据分析 ====")
    print("1. 加载数据...")
    analyzer.load_data()
    
    print("\n2. 数据预处理...")
    analyzer.preprocess_data()
    
    print("\n3. 时间趋势分析...")
    analyzer.analyze_trend()
    
    print("\n4. 可视化时间趋势...")
    analyzer.visualize_trend()
    
    print("\n5. 导出处理后的数据...")
    analyzer.export_filtered_data()
    
    # 成果落地评估部分
    print("\n===== 开始成果落地评估 ====")
    print("6. 分析合作模式...")
    analyzer.analyze_cooperation_models()
    
    print("\n7. 分析机构类型分布...")
    analyzer.analyze_institution_types()
    
    print("\n8. 成果落地评估计算...")
    analyzer.evaluate_implementation()
    
    print("\n9. 可视化评估结果...")
    analyzer.visualize_implementation()
    
    print("\n===== 全部分析完成 ====")