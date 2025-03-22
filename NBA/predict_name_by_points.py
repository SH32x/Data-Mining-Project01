import pandas as pd
import sys
from collections import Counter

# **获取运行时参数**
if len(sys.argv) < 3:
    print("Usage: python predict_name_by_points.py <train_file> <test_file>")
    sys.exit(1)

train_file = sys.argv[1]
test_file = sys.argv[2]
output_file = ".\\outcome_data\\points_predictions.txt"

# **读取数据**
df_train = pd.read_csv(train_file)
df_test = pd.read_csv(test_file)

# **去掉无关列**
drop_columns = ["game", "season"]
df_train = df_train.drop(columns=drop_columns, errors='ignore')
df_test = df_test.drop(columns=drop_columns, errors='ignore')

# **创建球队历史出场字典**
team_player_combinations = {}

for row in df_train.itertuples(index=False):
    home_team = row.home_team
    player_combination = tuple(sorted([row.home_0, row.home_1, row.home_2, row.home_3]))
    
    if home_team not in team_player_combinations:
        team_player_combinations[home_team] = {}
    
    if player_combination not in team_player_combinations[home_team]:
        team_player_combinations[home_team][player_combination] = []
    
    team_player_combinations[home_team][player_combination].append(row.home_4)

# **测试阶段**
total_rows = len(df_test)

with open(output_file, "w") as f:
    test_tuples = df_test.itertuples(index=False)
    for idx, row in enumerate(test_tuples, start=1):
        home_team = row.home_team
        player_combination = tuple(sorted([row.home_0, row.home_1, row.home_2, row.home_3]))

        predicted_home_4 = None

        if home_team in team_player_combinations and player_combination in team_player_combinations[home_team]:
            most_common_player = Counter(team_player_combinations[home_team][player_combination]).most_common(1)
            if most_common_player:
                predicted_home_4 = most_common_player[0][0]

        # **输出到文件**
        f.write(f"{predicted_home_4}\n")

        # **更新进度条**
        progress = f"Processing: {idx}/{total_rows} ({(idx/total_rows)*100:.2f}%)\r"
        sys.stdout.write(progress)
        sys.stdout.flush()

print("\nPrediction results saved to points_predictions.txt")
