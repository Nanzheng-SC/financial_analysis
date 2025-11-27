import torch
import torch.nn as nn
import random

class RNNModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, num_layers, dropout=0.5):
        super(RNNModel, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        # 词嵌入层
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        
        # LSTM层
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, num_layers, 
                            dropout=dropout, batch_first=True)
        
        # 全连接层
        self.fc = nn.Linear(hidden_dim, vocab_size)
        
        # Dropout层
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x, hidden):
        # x: (batch_size, seq_len)
        embedded = self.embedding(x)  # (batch_size, seq_len, embedding_dim)
        embedded = self.dropout(embedded)
        
        # lstm_out: (batch_size, seq_len, hidden_dim)
        # hidden: (num_layers, batch_size, hidden_dim)
        lstm_out, hidden = self.lstm(embedded, hidden)
        
        # 只使用最后一个时间步的输出
        # lstm_out = lstm_out[:, -1, :]  # (batch_size, hidden_dim)
        
        # 使用所有时间步的输出
        lstm_out = self.dropout(lstm_out)
        output = self.fc(lstm_out)  # (batch_size, seq_len, vocab_size)
        
        return output, hidden
    
    def init_hidden(self, batch_size, device):
        # 初始化隐藏状态
        h0 = torch.zeros(self.num_layers, batch_size, self.hidden_dim).to(device)
        c0 = torch.zeros(self.num_layers, batch_size, self.hidden_dim).to(device)
        return (h0, c0)

class LyricsGenerator:
    def __init__(self, model, idx_to_char, char_to_idx, device):
        self.model = model
        self.idx_to_char = idx_to_char
        self.char_to_idx = char_to_idx
        self.device = device
    
    def generate(self, seed_text, length=100, temperature=1.0):
        """生成歌词
        Args:
            seed_text: 种子文本
            length: 生成文本长度
            temperature: 温度参数，控制随机性
        """
        self.model.eval()
        with torch.no_grad():
            # 将种子文本转换为索引
            chars = list(seed_text)
            indices = [self.char_to_idx.get(c, 0) for c in chars]
            
            # 初始化隐藏状态
            hidden = self.model.init_hidden(1, self.device)
            
            # 处理种子文本
            for idx in indices:
                input_tensor = torch.tensor([[idx]], dtype=torch.long).to(self.device)
                output, hidden = self.model(input_tensor, hidden)
            
            # 生成新文本
            generated = chars[:]
            input_idx = indices[-1] if indices else 0
            
            for _ in range(length):
                input_tensor = torch.tensor([[input_idx]], dtype=torch.long).to(self.device)
                output, hidden = self.model(input_tensor, hidden)
                
                # 应用温度参数
                prediction = output.data[0, 0] / temperature
                
                # 转换为概率分布
                probabilities = torch.softmax(prediction, dim=0)
                
                # 根据概率分布选择下一个字符
                # 使用torch.multinomial而不是np.random.choice
                next_idx = torch.multinomial(probabilities, 1).item()
                next_char = self.idx_to_char[next_idx]
                
                generated.append(next_char)
                input_idx = next_idx
            
            return ''.join(generated)