import pandas as pd
import sys
from collections import Counter

# **File Paths**
train_file = "matchups-2008.csv"#✅
test_file = "matchups-2009.csv"#✅

# **Read Training and Testing Data**
df_train = pd.read_csv(train_file)
df_test = pd.read_csv(test_file)

# **Drop Irrelevant Columns**
drop_columns = ["game", "season"]
df_train = df_train.drop(columns=drop_columns)
df_test = df_test.drop(columns=drop_columns)

# **Create Historical Lineup Data**
team_player_combinations = {}

def add_to_team_data(team, player_combination, fifth_player):
    """ Store the fifth player for a given 4-player combination in a team """
    if team not in team_player_combinations:
        team_player_combinations[team] = {}
    
    if player_combination not in team_player_combinations[team]:
        team_player_combinations[team][player_combination] = []
    
    team_player_combinations[team][player_combination].append(fifth_player)

# **Process Training Data (Home Team)**
for _, row in df_train.iterrows():
    home_team = row["home_team"]
    player_combination = tuple(sorted([row["home_0"], row["home_1"], row["home_2"], row["home_3"]]))
    add_to_team_data(home_team, player_combination, row["home_4"])

# **Process Training Data (Away Team, Treated as Home Team)**
for _, row in df_train.iterrows():
    away_team = row["away_team"]
    player_combination = tuple(sorted([row["away_0"], row["away_1"], row["away_2"], row["away_3"]]))
    add_to_team_data(away_team, player_combination, row["away_4"])

# **Testing Phase**
correct_predictions = 0
total_predictions = 0
total_rows = len(df_test)

for idx, row in enumerate(df_test.itertuples(index=False), start=1):
    home_team = row.home_team
    player_combination = tuple(sorted([row.home_0, row.home_1, row.home_2, row.home_3]))
    true_home_4 = row.home_4

    predicted_home_4 = None

    # **If Historical Data Exists for This Team**
    if home_team in team_player_combinations and player_combination in team_player_combinations[home_team]:
        # **Find the Most Frequently Occurring Fifth Player**
        most_common_player = Counter(team_player_combinations[home_team][player_combination]).most_common(1)
        
        if most_common_player:
            predicted_home_4 = most_common_player[0][0]

    # **Calculate Accuracy**
    if predicted_home_4 == true_home_4:
        correct_predictions += 1
    
    total_predictions += 1
    
    # **更新进度条**
    progress = f"Processing: {idx}/{total_rows} ({(idx/total_rows)*100:.2f}%)\r"
    sys.stdout.write(progress)
    sys.stdout.flush()

# **Output Prediction Results**
accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
print(f"\npredict_name_by_KNN_same_team_member_acc:🔹 {accuracy:.2%}  ({correct_predictions} / {total_predictions})")
