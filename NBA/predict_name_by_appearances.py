import pandas as pd
import sys

# **读取 player_appearances.txt**
appearances_file = "player_appearances.txt"

try:
    # **使用 read_fwf() 解析固定宽度列**
    player_appearances = pd.read_fwf(
        appearances_file, 
        skiprows=2,  # **跳过前两行（表头 & === 分隔线）**
        names=["Index", "Player", "Team", "Appearances"],  # **手动指定列名**
        header=None
    )
except Exception as e:
    print("error")

# 测试数据文件 
test_file = "matchups-2009.csv" #✅

# **读取完整数据**
test_data = pd.read_csv(test_file)

# **确保所有球员列都是字符串**
player_columns = ["home_0", "home_1", "home_2", "home_3", "home_4"]
for col in player_columns:
    test_data[col] = test_data[col].astype(str)

# **存储预测结果**
correct_predictions = 0
total_predictions = 0

total_rows = len(test_data)

# **遍历测试数据**
for idx, row in enumerate(test_data.itertuples(index=False), start=1):
    home_team = row.home_team
    existing_players = {row.home_0, row.home_1, row.home_2, row.home_3}
    true_fifth_player = row.home_4

    # **从 player_appearances.txt 选择出场最多的可用球员**
    available_players = player_appearances[
        (player_appearances["Team"] == home_team) & 
        (~player_appearances["Player"].isin(existing_players))
    ]

    # **按出场次数降序排序，选取最多的球员**
    if not available_players.empty:
        predicted_fifth_player = available_players.iloc[0]["Player"]
    else:
        predicted_fifth_player = None  # 可能某些队伍数据不足

    # **比较预测结果**
    if predicted_fifth_player == true_fifth_player:
        correct_predictions += 1
    
    total_predictions += 1
    
    # **更新进度条**
    progress = f"Processing: {idx}/{total_rows} ({(idx/total_rows)*100:.2f}%)\r"
    sys.stdout.write(progress)
    sys.stdout.flush()

# **计算正确率**
accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
print(f"\npredict_name_by_appearances_acc:🔹 {accuracy:.2%}  ({correct_predictions} / {total_predictions})") 