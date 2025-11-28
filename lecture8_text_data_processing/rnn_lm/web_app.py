#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web应用：RNN歌词生成器
"""

from flask import Flask, render_template, request, jsonify
import torch
import os
import sys
import pickle

# 获取当前脚本的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 添加项目根目录到Python路径
sys.path.append(current_dir)

from model import RNNModel, LyricsGenerator

app = Flask(__name__, 
            template_folder=os.path.join(current_dir, 'templates'))

# 全局变量存储模型和生成器
model = None
generator = None
char_to_idx = None
idx_to_char = None
device = None

def load_char_mappings(filepath):
    """加载字符映射"""
    with open(filepath, 'rb') as f:
        char_to_idx, idx_to_char = pickle.load(f)
    return char_to_idx, idx_to_char

def initialize_model():
    """初始化模型"""
    global model, generator, char_to_idx, idx_to_char, device
    
    # 设置设备
    device = torch.device('cpu')
    
    # 加载预训练权重
    checkpoint = torch.load('lyrics_rnn_model.pth', map_location=device)
    
    # 获取模型参数
    vocab_size = checkpoint['vocab_size']
    embedding_dim = checkpoint['embedding_dim']
    hidden_dim = checkpoint['hidden_dim']
    num_layers = checkpoint['num_layers']
    
    # 获取字符映射
    char_to_idx = checkpoint['char_to_idx']
    idx_to_char = checkpoint['idx_to_char']
    
    # 创建模型
    model = RNNModel(vocab_size, embedding_dim, hidden_dim, num_layers)
    
    # 加载模型权重
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    model.eval()
    
    # 创建生成器（注意参数顺序）
    generator = LyricsGenerator(model, idx_to_char, char_to_idx, device)

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_lyrics():
    """生成歌词API"""
    try:
        # 获取请求数据
        data = request.get_json()
        seed_text = data.get('seed_text', '春天')
        length = int(data.get('length', 100))
        temperature = float(data.get('temperature', 1.0))
        
        # 生成歌词
        generated_lyrics = generator.generate(seed_text, length, temperature)
        
        return jsonify({
            'success': True,
            'lyrics': generated_lyrics
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    # 初始化模型
    initialize_model()
    
    # 启动Web服务（移除调试模式）
    app.run(host='0.0.0.0', port=5000, debug=False)