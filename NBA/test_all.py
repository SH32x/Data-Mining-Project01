import os
import pandas as pd
import subprocess

# **第一步: 读取NBA_test_modified.csv和NBA_test_labels.csv并按赛季拆分**
def split_season_files(data_file="./test_data/NBA_test_modified.csv", 
                       labels_file="./test_data/NBA_test_labels.csv", 
                       output_folder="./test_data"):
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found.")
        return
    
    if not os.path.exists(labels_file):
        print(f"Error: {labels_file} not found.")
        return

    # 读取 NBA_test_modified.csv
    df_data = pd.read_csv(data_file)
    unique_seasons = df_data["season"].unique()

    # 读取 NBA_test_labels.csv
    df_labels = pd.read_csv(labels_file)

    if len(df_data) != len(df_labels):
        print("Error: NBA_test_modified.csv and NBA_test_labels.csv have different lengths!")
        return

    for season in unique_seasons:
        test_file = os.path.join(output_folder, f"test_{season}.csv")
        labels_file = os.path.join(output_folder, f"labels_{season}.csv")

        if os.path.exists(test_file) and os.path.exists(labels_file):
            print(f"Files {test_file} and {labels_file} already exist, skipping...")
            continue

        # 按 `season` 过滤数据
        df_season = df_data[df_data["season"] == season]
        df_season_labels = df_labels.iloc[df_season.index]  # 取对应索引的标签

        df_season.to_csv(test_file, index=False)
        df_season_labels.to_csv(labels_file, index=False, header=True)

        print(f"Generated {test_file} and {labels_file}")

# **第二步: 预测选定年份的 test 文件**
def run_predictions():
    test_folder = "./test_data"
    train_folder = "./train_data"
    
    # 让用户选择要预测的年份
    available_years = [f"test_{year}.csv" for year in range(2007, 2017) if os.path.exists(os.path.join(test_folder, f"test_{year}.csv"))]

    if not available_years:
        print("No test files found. Please run the script again after generating test files.")
        return

    print("\nAvailable test files:")
    for i, file in enumerate(available_years, 1):
        print(f"{i}. {file}")

    choice = int(input("\nSelect a test file (enter number): ")) - 1
    if choice < 0 or choice >= len(available_years):
        print("Invalid selection.")
        return

    test_file = available_years[choice]
    test_year = int(test_file.split("_")[1].split(".")[0])  # 获取年份

    test_file_path = os.path.join(test_folder, test_file)

    # **确定训练数据文件**
    if test_year == 2007:
        train_files = [os.path.join(train_folder, f"matchups-{test_year}.csv")]
    else:
        train_files = [
            os.path.join(train_folder, f"matchups-{test_year-1}.csv"),
            os.path.join(train_folder, f"matchups-{test_year}.csv"),
        ]

    # 特殊情况: test_2016.csv 只用 matchups-2015.csv
    if test_year == 2016:
        train_files = [os.path.join(train_folder, f"matchups-2015.csv")]

    # **运行 check_player_performance.py**
    print("\nRunning check_player_performance.py...")
    subprocess.run(["python", "check_player_performance.py"] + train_files)

    # **运行 predict_name_by_appearances.py**
    appearances_file = os.path.join(train_folder, "player_appearances.txt")
    print("\nRunning predict_name_by_appearances.py...")
    subprocess.run(["python", "predict_name_by_appearances.py", appearances_file, test_file_path])

    # **运行 predict_name_by_points.py**
    print("\nRunning predict_name_by_points.py...")
    train_file = train_files[-1]  # 选择最新的匹配数据
    subprocess.run(["python", "predict_name_by_points.py", train_file, test_file_path])

    # **运行 predict_name_by_KNN_same_home_team_members.py**
    print("\nRunning predict_name_by_KNN_same_home_team_members.py...")
    subprocess.run(["python", "predict_name_by_KNN_same_home_team_members.py", train_file, test_file_path])

    # **运行 predict_name_by_KNN_same_team_member.py**
    print("\nRunning predict_name_by_KNN_same_team_member.py...")
    subprocess.run(["python", "predict_name_by_KNN_same_team_member.py", train_file, test_file_path])
    

    print("\n✅ Prediction process completed!")

# **主流程**
if __name__ == "__main__":
    split_season_files()
    run_predictions()
