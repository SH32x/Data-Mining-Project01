import csv

# 读取KNN输出球员名称（跳过表头）
with open(r'.\outcome_data\KNN_output_all.csv', 'r', encoding='utf-8') as knn_file:
    knn_reader = csv.reader(knn_file)
    next(knn_reader)  # 跳过表头
    fifth_players = [row[0].strip() for row in knn_reader if row]

# 读取NBA_test.csv中的Home_Team（第二列，跳过表头）
with open(r'.\test_data\NBA_test.csv', 'r', encoding='utf-8') as test_file:
    test_reader = csv.reader(test_file)
    next(test_reader)  # 跳过表头
    home_teams = [row[1].strip() for row in test_reader if row]

# 检查数量是否一致
if len(fifth_players) != len(home_teams):
    raise ValueError("球员数量与主队数量不一致，无法一一对应。")

# 写入最终结果
with open(r'.\outcome_data\FINAL_RESULT.csv', 'w', encoding='utf-8', newline='') as result_file:
    writer = csv.writer(result_file)
    writer.writerow(['Game_ID', 'Home_Team', 'Fifth_Player'])  # 写入表头

    for idx, (home_team, player) in enumerate(zip(home_teams, fifth_players), start=1):
        writer.writerow([idx, home_team, player])

print("FINAL_RESULT.csv 生成成功，已跳过表头。")
