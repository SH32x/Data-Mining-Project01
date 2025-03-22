import csv

# 读取KNN输出数据
with open(r'.\outcome_data\KNN_output_all.csv', 'r', encoding='utf-8') as knn_file:
    knn_reader = csv.reader(knn_file)
    knn_data = [row[0].strip() for row in knn_reader if row]  # 提取第一列内容，并去除空行

# 读取真实标签数据
with open(r'.\test_data\NBA_test_labels.csv', 'r', encoding='utf-8') as label_file:
    label_reader = csv.reader(label_file)
    label_data = [row[0].strip() for row in label_reader if row]

# 检查长度是否一致
if len(knn_data) != len(label_data):
    raise ValueError("两个文件的行数不一致，无法逐行比较。")

# 写入对比结果
with open(r'.\outcome_data\result_compare.txt', 'w', encoding='utf-8') as result_file:
    result_file.write("KNN_output\tNBA_label\tMatch\n")  # 表头
    for knn_val, label_val in zip(knn_data, label_data):
        match = str(knn_val == label_val)
        result_file.write(f"{knn_val}\t{label_val}\t{match}\n")

print("对比完成，结果已保存至 .\\outcome_data\\result_compare.txt")
