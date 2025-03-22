import pandas as pd
import sys
from collections import Counter

# **获取命令行参数**
if len(sys.argv) != 3:
    print("Usage: python script.py <train_file> <test_file>")
    sys.exit(1)

train_file = sys.argv[1]
test_file = sys.argv[2]

# **读取数据**
df_train = pd.read_csv(train_file)
df_test = pd.read_csv(test_file)

# **去掉无关列**
drop_columns = ["game", "season"]
df_train = df_train.drop(columns=drop_columns, errors='ignore')
df_test = df_test.drop(columns=drop_columns, errors='ignore')

# **创建球队历史出场字典**
team_player_combinations = {}

def add_to_team_data(team, player_combination, fifth_player):
    """ 存储给定 4 名球员组合的第 5 人 """
    if team not in team_player_combinations:
        team_player_combinations[team] = {}
    
    if player_combination not in team_player_combinations[team]:
        team_player_combinations[team][player_combination] = []
    
    team_player_combinations[team][player_combination].append(fifth_player)

# **处理训练数据（主队）**
for _, row in df_train.iterrows():
    home_team = row["home_team"]
    player_combination = tuple(sorted([row["home_0"], row["home_1"], row["home_2"], row["home_3"]]))
    add_to_team_data(home_team, player_combination, row["home_4"])

# **处理训练数据（客队，视为主队）**
for _, row in df_train.iterrows():
    away_team = row["away_team"]
    player_combination = tuple(sorted([row["away_0"], row["away_1"], row["away_2"], row["away_3"]]))
    add_to_team_data(away_team, player_combination, row["away_4"])

# **测试阶段**
predictions = []
total_rows = len(df_test)

for idx, row in enumerate(df_test.itertuples(index=False), start=1):
    home_team = row.home_team
    player_combination = tuple(sorted([row.home_0, row.home_1, row.home_2, row.home_3]))

    predicted_home_4 = "Unknown"

    # **如果该球队有历史数据**
    if home_team in team_player_combinations and player_combination in team_player_combinations[home_team]:
        # **统计出现最多的第 5 人**
        most_common_player = Counter(team_player_combinations[home_team][player_combination]).most_common(1)
        
        if most_common_player:
            predicted_home_4 = most_common_player[0][0]
    
    predictions.append(predicted_home_4)
    
    # **更新进度条**
    progress = f"Processing: {idx}/{total_rows} ({(idx/total_rows)*100:.2f}%)\r"
    sys.stdout.write(progress)
    sys.stdout.flush()

# **写入预测结果到文件**
with open(".\\outcome_data\\KNN_all_predictions.txt", "w") as f:
    for prediction in predictions:
        f.write(prediction + "\n")

print("\nPredictions saved to KNN_all_predictions.txt")
