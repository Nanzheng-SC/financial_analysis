#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证RNN歌词生成器的核心功能
"""

import torch
from model import RNNModel
from train import load_data, create_char_mappings, prepare_data

def test_model_creation():
    """测试模型创建"""
    print("测试1: 模型创建...")
    vocab_size = 100  # 简化的词汇表大小
    
    model = RNNModel(vocab_size, embedding_dim=16, hidden_dim=32, num_layers=1)
    
    print("✓ 模型创建成功")
    return model

def test_training():
    """测试训练功能"""
    print("\n测试2: 训练功能...")
    
    # 加载示例数据
    lyrics_data = load_data('lyrics_dataset.txt')
    char_to_idx, idx_to_char, vocab_size = create_char_mappings(lyrics_data)
    
    # 准备训练数据
    sequences, targets = prepare_data(lyrics_data, char_to_idx, seq_length=10)
    
    # 创建模型
    model = RNNModel(vocab_size, embedding_dim=16, hidden_dim=32, num_layers=1)
    device = torch.device('cpu')
    model.to(device)
    
    # 简单训练几步
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters())
    
    # 取几个样本进行训练测试
    for i in range(3):  # 训练3步
        if i < len(sequences):
            batch_x = torch.tensor([sequences[i]], dtype=torch.long).to(device)
            batch_y = torch.tensor([targets[i]], dtype=torch.long).to(device)
            
            optimizer.zero_grad()
            output, _ = model(batch_x, model.init_hidden(1, device))
            # 使用序列的最后一个输出来预测下一个字符
            output_last = output[:, -1, :]  # (batch_size, vocab_size)
            loss = criterion(output_last, batch_y)
            loss.backward()
            optimizer.step()
    
    print("✓ 训练功能正常")
    return model

def main():
    """主测试函数"""
    print("=== RNN歌词生成器核心功能测试 ===")
    
    # 测试模型创建
    model = test_model_creation()
    
    # 测试训练功能
    model = test_training()
    
    print("\n=== 核心功能测试通过! ===")
    print("注意：生成功能已在generate.py中测试")

if __name__ == "__main__":
    main()