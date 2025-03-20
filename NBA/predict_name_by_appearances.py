import pandas as pd
import sys

# **获取命令行参数**
if len(sys.argv) != 3:
    print("Usage: python script.py <appearances_file> <test_file>")
    sys.exit(1)

appearances_file = sys.argv[1]
test_file = sys.argv[2]

try:
    # **使用 read_fwf() 解析固定宽度列**
    player_appearances = pd.read_fwf(
        appearances_file, 
        skiprows=2,  # **跳过前两行（表头 & === 分隔线）**
        names=["Index", "Player", "Team", "Appearances"],  # **手动指定列名**
        header=None
    )
except Exception as e:
    print("Error reading appearances file:", e)
    sys.exit(1)

try:
    # **读取完整数据**
    test_data = pd.read_csv(test_file)
except Exception as e:
    print("Error reading test file:", e)
    sys.exit(1)

# **确保所有球员列都是字符串**
player_columns = ["home_0", "home_1", "home_2", "home_3", "home_4"]
for col in player_columns:
    test_data[col] = test_data[col].astype(str)

# **存储预测结果**
predictions = []
total_rows = len(test_data)

# **遍历测试数据**
for idx, row in enumerate(test_data.itertuples(index=False), start=1):
    home_team = row.home_team
    existing_players = {row.home_0, row.home_1, row.home_2, row.home_3}

    # **从 player_appearances.txt 选择出场最多的可用球员**
    available_players = player_appearances[
        (player_appearances["Team"] == home_team) & 
        (~player_appearances["Player"].isin(existing_players))
    ]

    # **按出场次数降序排序，选取最多的球员**
    predicted_fifth_player = available_players.iloc[0]["Player"] if not available_players.empty else "Unknown"
    
    predictions.append(predicted_fifth_player)
    
    # **更新进度条**
    progress = f"Processing: {idx}/{total_rows} ({(idx/total_rows)*100:.2f}%)\r"
    sys.stdout.write(progress)
    sys.stdout.flush()

# **写入预测结果到文件**
with open("appearances_predictions.txt", "w") as f:
    for prediction in predictions:
        f.write(prediction + "\n")

print("\nPredictions saved to appearances_predictions.txt")