import os
import pandas as pd

# **输入和输出目录**
input_file = "./test_data/NBA_test.csv"
output_folder = "./test_data"

# **检查文件是否存在**
if not os.path.exists(input_file):
    print(f"Error: {input_file} not found.")
    exit(1)

# **读取数据**
df = pd.read_csv(input_file)

# **检查是否有 season 列**
if "season" not in df.columns:
    print("Error: 'season' column not found in the dataset.")
    exit(1)

# **获取所有独立的赛季**
unique_seasons = df["season"].unique()

# **创建输出文件**
for season in unique_seasons:
    output_file = os.path.join(output_folder, f"KNN_test_{season}.csv")
    
    if os.path.exists(output_file):
        print(f"File {output_file} already exists, skipping...")
        continue
    
    # **筛选赛季数据**
    df_season = df[df["season"] == season]
    
    # **保存文件**
    df_season.to_csv(output_file, index=False)
    print(f"Generated {output_file}")

print("\n✅ Splitting completed!")
