import torch
import pickle
import argparse

from model import RNNModel, LyricsGenerator

def load_char_mappings(filepath):
    """加载字符映射"""
    with open(filepath, 'rb') as f:
        char_to_idx, idx_to_char = pickle.load(f)
    return char_to_idx, idx_to_char

def main():
    # 设置设备
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"使用设备: {device}")
    
    # 加载字符映射
    char_to_idx, idx_to_char = load_char_mappings('char_mappings.pkl')
    vocab_size = len(char_to_idx)
    
    # 创建模型
    embedding_dim = 128
    hidden_dim = 256
    num_layers = 2
    
    model = RNNModel(vocab_size, embedding_dim, hidden_dim, num_layers)
    
    # 加载模型权重
    checkpoint = torch.load('lyrics_rnn_model.pth', map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    model.eval()
    
    print("模型加载完成!")
    
    # 创建歌词生成器
    generator = LyricsGenerator(model, idx_to_char, char_to_idx, device)
    
    # 生成歌词
    seed_text = "春天"
    print(f"使用种子文本: '{seed_text}'")
    
    # 不同温度参数生成歌词
    temperatures = [0.5, 1.0, 1.5]
    
    for temp in temperatures:
        print(f"\n--- 温度参数: {temp} ---")
        generated_lyrics = generator.generate(seed_text, length=100, temperature=temp)
        print(generated_lyrics)
    
    # 交互式生成
    print("\n--- 交互式生成 ---")
    while True:
        seed = input("\n请输入种子文本 (输入'quit'退出): ")
        if seed.lower() == 'quit':
            break
        
        try:
            length = int(input("请输入生成长度 (默认100): ") or "100")
        except ValueError:
            length = 100
            
        try:
            temp = float(input("请输入温度参数 (默认1.0): ") or "1.0")
        except ValueError:
            temp = 1.0
            
        generated_lyrics = generator.generate(seed, length=length, temperature=temp)
        print(f"\n生成的歌词:")
        print("-" * 40)
        print(generated_lyrics)
        print("-" * 40)

if __name__ == "__main__":
    main()