import torch
import torch.nn as nn
import numpy as np
import random
import os
from collections import Counter
import pickle

from model import RNNModel

def load_char_mappings(filepath):
    """加载字符映射"""
    with open(filepath, 'rb') as f:
        char_to_idx, idx_to_char = pickle.load(f)
    return char_to_idx, idx_to_char

def load_data(file_path):
    """加载歌词数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def create_char_mappings(text):
    """创建字符到索引的映射"""
    # 获取所有唯一字符
    chars = sorted(list(set(text)))
    vocab_size = len(chars)
    
    # 创建映射
    char_to_idx = {char: idx for idx, char in enumerate(chars)}
    idx_to_char = {idx: char for idx, char in enumerate(chars)}
    
    return char_to_idx, idx_to_char, vocab_size

def prepare_data(text, char_to_idx, seq_length=25):
    """准备训练数据"""
    # 将文本转换为索引序列
    data = [char_to_idx[char] for char in text]
    
    # 创建输入序列和目标序列
    X = []
    y = []
    
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    
    return np.array(X), np.array(y)

def train_model(model, X, y, epochs=100, batch_size=64, learning_rate=0.001, device='cpu'):
    """训练模型"""
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    
    # 转换为tensor
    X = torch.tensor(X, dtype=torch.long).to(device)
    y = torch.tensor(y, dtype=torch.long).to(device)
    
    dataset_size = X.size(0)
    
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        
        # 随机打乱数据
        indices = torch.randperm(dataset_size)
        X = X[indices]
        y = y[indices]
        
        for i in range(0, dataset_size, batch_size):
            # 获取批次数据
            batch_X = X[i:i+batch_size]
            batch_y = y[i:i+batch_size]
            
            # 初始化隐藏状态
            hidden = model.init_hidden(batch_X.size(0), device)
            
            # 前向传播
            optimizer.zero_grad()
            output, hidden = model(batch_X, hidden)
            
            # 计算损失
            # output shape: (batch_size, seq_length, vocab_size)
            # batch_y shape: (batch_size,)
            # 我们只使用序列的最后一个输出来预测下一个字符
            output_last = output[:, -1, :]  # (batch_size, vocab_size)
            loss = criterion(output_last, batch_y)
            
            # 反向传播
            loss.backward()
            
            # 梯度裁剪
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5)
            
            # 更新参数
            optimizer.step()
            
            total_loss += loss.item()
        
        if (epoch + 1) % 10 == 0:
            avg_loss = total_loss / (dataset_size / batch_size)
            print(f'Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}')
    
    return model

def save_model(model, char_to_idx, idx_to_char, filepath):
    """保存模型和字符映射"""
    checkpoint = {
        'model_state_dict': model.state_dict(),
        'char_to_idx': char_to_idx,
        'idx_to_char': idx_to_char,
        'vocab_size': len(char_to_idx),
        'embedding_dim': model.embedding.embedding_dim,
        'hidden_dim': model.hidden_dim,
        'num_layers': model.num_layers
    }
    torch.save(checkpoint, filepath)
    print(f"模型已保存到 {filepath}")

def load_model(filepath, device='cpu'):
    """加载模型"""
    checkpoint = torch.load(filepath, map_location=device)
    
    model = RNNModel(
        vocab_size=checkpoint['vocab_size'],
        embedding_dim=checkpoint['embedding_dim'],
        hidden_dim=checkpoint['hidden_dim'],
        num_layers=checkpoint['num_layers']
    )
    
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    
    return model, checkpoint['char_to_idx'], checkpoint['idx_to_char']

def main():
    # 设置设备
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"使用设备: {device}")
    
    # 加载数据
    data_path = 'lyrics_dataset.txt'
    text = load_data(data_path)
    print(f"数据加载完成，总字符数: {len(text)}")
    
    # 创建字符映射
    char_to_idx, idx_to_char, vocab_size = create_char_mappings(text)
    print(f"词汇表大小: {vocab_size}")
    
    # 保存字符映射以便后续使用
    with open('char_mappings.pkl', 'wb') as f:
        pickle.dump((char_to_idx, idx_to_char), f)
    
    # 准备训练数据
    seq_length = 25
    X, y = prepare_data(text, char_to_idx, seq_length)
    print(f"训练数据准备完成，样本数: {len(X)}")
    
    # 创建模型
    embedding_dim = 128
    hidden_dim = 256
    num_layers = 2
    
    model = RNNModel(vocab_size, embedding_dim, hidden_dim, num_layers)
    print(f"模型创建完成")
    print(f"模型参数: embedding_dim={embedding_dim}, hidden_dim={hidden_dim}, num_layers={num_layers}")
    
    # 训练模型
    epochs = 100
    batch_size = 64
    learning_rate = 0.001
    
    print("开始训练...")
    model = train_model(model, X, y, epochs, batch_size, learning_rate, device)
    
    # 保存模型
    save_model(model, char_to_idx, idx_to_char, 'lyrics_rnn_model.pth')
    print("训练完成!")

if __name__ == "__main__":
    main()