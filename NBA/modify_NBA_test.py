import pandas as pd

# 读取数据
file_path = "NBA_test.csv"
df = pd.read_csv(file_path)

# 处理每一行，将 `?` 移动到 home_4 位置
def adjust_missing_player(row):
    home_players = [row[f'home_{i}'] for i in range(5)]
    
    # 移除 '?'
    home_players = [player for player in home_players if player != '?']
    
    # 填充缺失位置
    while len(home_players) < 5:
        home_players.append('?')
    
    # 更新行数据
    for i in range(5):
        row[f'home_{i}'] = home_players[i]
    
    return row

# 应用处理逻辑
df = df.apply(adjust_missing_player, axis=1)

# 保存新文件
output_path = "NBA_test_modified.csv"
df.to_csv(output_path, index=False)

print(f"处理完成，已生成 {output_path}")
