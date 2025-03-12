import pandas as pd

# **文件路径**
file_paths = ["./matchups-2008.csv", "./matchups-2007.csv"]  

# **读取第一个文件，保留表头**
df_list = [pd.read_csv(file_paths[0])]

# **读取其余文件，但跳过表头**
for file in file_paths[1:]:
    df_temp = pd.read_csv(file, header=None, skiprows=1, names=df_list[0].columns)
    df_list.append(df_temp)

# **合并所有数据**
df = pd.concat(df_list, ignore_index=True)

# 确保球员列为字符串
player_columns = ["home_0", "home_1", "home_2", "home_3", "home_4",
                  "away_0", "away_1", "away_2", "away_3", "away_4"]

for col in player_columns:
    df[col] = df[col].astype(str)

# 计算球员得分
player_points = pd.concat([
    df.groupby(["home_0"])["pts_home"].mean().reset_index().rename(columns={"home_0": "player"}),
    df.groupby(["home_1"])["pts_home"].mean().reset_index().rename(columns={"home_1": "player"}),
    df.groupby(["home_2"])["pts_home"].mean().reset_index().rename(columns={"home_2": "player"}),
    df.groupby(["home_3"])["pts_home"].mean().reset_index().rename(columns={"home_3": "player"}),
    df.groupby(["home_4"])["pts_home"].mean().reset_index().rename(columns={"home_4": "player"}),

    df.groupby(["away_0"])["pts_visitor"].mean().reset_index().rename(columns={"away_0": "player"}),
    df.groupby(["away_1"])["pts_visitor"].mean().reset_index().rename(columns={"away_1": "player"}),
    df.groupby(["away_2"])["pts_visitor"].mean().reset_index().rename(columns={"away_2": "player"}),
    df.groupby(["away_3"])["pts_visitor"].mean().reset_index().rename(columns={"away_3": "player"}),
    df.groupby(["away_4"])["pts_visitor"].mean().reset_index().rename(columns={"away_4": "player"})
])

# 合并相同球员的得分
player_points = player_points.groupby("player", as_index=False).agg({
    "pts_home": "sum",
    "pts_visitor": "sum"
})
player_points["total_pts"] = player_points["pts_home"] + player_points["pts_visitor"]

# 统计球员出场次数
player_appearances = pd.concat([
    df[player_columns].melt(value_name="player")["player"]
]).value_counts().reset_index()
player_appearances.columns = ["player", "appearances"]

# 关联球员所属球队
player_teams = pd.concat([
    df[["home_0", "home_team"]].rename(columns={"home_0": "player"}),
    df[["home_1", "home_team"]].rename(columns={"home_1": "player"}),
    df[["home_2", "home_team"]].rename(columns={"home_2": "player"}),
    df[["home_3", "home_team"]].rename(columns={"home_3": "player"}),
    df[["home_4", "home_team"]].rename(columns={"home_4": "player"})
])

player_teams = player_teams.drop_duplicates(subset=["player"], keep="first")

# **合并所有数据**
player_stats = player_points.merge(player_teams, on="player", how="left")
player_stats = player_stats.merge(player_appearances, on="player", how="left")

# **按球队分组，并按 appearances 从大到小排序**
player_stats = player_stats.sort_values(by=["home_team", "appearances"], ascending=[True, False])

# **重置索引**
player_stats_reset = player_stats.reset_index(drop=True)
player_stats_reset.index += 1  # 让序号从 1 开始

# **格式化输出到 TXT 文件**
output_file_points = "formatted_player_points.txt"
output_file_appearances = "player_appearances.txt"

# 让列名对齐
formatted_header_points = "{:<6} {:<20} {:<8} {:<10} {:<10} {:<10}".format(
    "Index", "Player", "Team", "PTS_Home", "PTS_Away", "Total PTS"
)

formatted_header_appearances = "{:<6} {:<20} {:<8} {:<10}".format(
    "Index", "Player", "Team", "Appearances"
)

# 保存球员得分数据
with open(output_file_points, "w", encoding="utf-8") as f:
    f.write(formatted_header_points + "\n")
    f.write("=" * len(formatted_header_points) + "\n")
    
    for idx, row in player_stats_reset.iterrows():
        formatted_row = "{:<6} {:<20} {:<8} {:<10.2f} {:<10.2f} {:<10.2f}".format(
            idx, row["player"], row["home_team"] if pd.notna(row["home_team"]) else "N/A",
            row["pts_home"], row["pts_visitor"], row["total_pts"]
        )
        f.write(formatted_row + "\n")

# 保存球员出场次数数据
with open(output_file_appearances, "w", encoding="utf-8") as f:
    f.write(formatted_header_appearances + "\n")
    f.write("=" * len(formatted_header_appearances) + "\n")
    
    for idx, row in player_stats_reset.iterrows():
        formatted_row = "{:<6} {:<20} {:<8} {:<10}".format(
            idx, row["player"], row["home_team"] if pd.notna(row["home_team"]) else "N/A",
            row["appearances"]
        )
        f.write(formatted_row + "\n")

print(f"Player scores have been saved to {output_file_points}")
print(f"Player appearances have been saved to {output_file_appearances}")  
