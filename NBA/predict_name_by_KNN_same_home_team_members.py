import pandas as pd
import sys
from collections import Counter
from sklearn.metrics import accuracy_score

# **文件路径**
train_file = "matchups-2008.csv"#✅
test_file = "matchups-2009.csv"#✅

# **读取数据**
df_train = pd.read_csv(train_file)
df_test = pd.read_csv(test_file)

# **去掉无关列**
drop_columns = ["game", "season"]
df_train = df_train.drop(columns=drop_columns)
df_test = df_test.drop(columns=drop_columns)

# **创建球队历史出场字典**
team_player_combinations = {}

for _, row in df_train.iterrows():
    home_team = row["home_team"]
    
    # **获取当前比赛的前 4 名球员**
    player_combination = tuple(sorted([row["home_0"], row["home_1"], row["home_2"], row["home_3"]]))

    # **记录第 5 人（home_4）**
    if home_team not in team_player_combinations:
        team_player_combinations[home_team] = {}
    
    if player_combination not in team_player_combinations[home_team]:
        team_player_combinations[home_team][player_combination] = []
    
    team_player_combinations[home_team][player_combination].append(row["home_4"])

# **测试阶段**
correct_predictions = 0
total_predictions = 0
total_rows = len(df_test)

for idx, row in enumerate(df_test.iterrows(), start=1):
    home_team = row[1]["home_team"]
    player_combination = tuple(sorted([row[1]["home_0"], row[1]["home_1"], row[1]["home_2"], row[1]["home_3"]]))
    true_home_4 = row[1]["home_4"]

    predicted_home_4 = None

    # **如果该球队有历史数据**
    if home_team in team_player_combinations and player_combination in team_player_combinations[home_team]:
        # **统计出现最多的第 5 人**
        most_common_player = Counter(team_player_combinations[home_team][player_combination]).most_common(1)
        
        if most_common_player:
            predicted_home_4 = most_common_player[0][0]

    # **计算准确率**
    if predicted_home_4 == true_home_4:
        correct_predictions += 1
    
    total_predictions += 1
    
    # **更新进度条**
    progress = f"Processing: {idx}/{total_rows} ({(idx/total_rows)*100:.2f}%)\r"
    sys.stdout.write(progress)
    sys.stdout.flush()

# **输出预测结果**
accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
print(f"\npredict_name_by_KNN_same_home_team_members_acc:🔹 {accuracy:.2%}  ({correct_predictions} / {total_predictions})")
