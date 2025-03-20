import os

# **定义文件路径**
lstm_predictions_file = "./outcome_data/optimized_predictions.txt"
labels_file = "./test_data/labels_2007.csv"

# **检查文件是否存在**
if not os.path.exists(lstm_predictions_file):
    print(f"Error: {lstm_predictions_file} not found.")
    exit(1)

if not os.path.exists(labels_file):
    print(f"Error: {labels_file} not found.")
    exit(1)

# **读取 LSTM 预测结果**
with open(lstm_predictions_file, "r", encoding="utf-8") as f:
    lstm_predictions = [line.strip() for line in f.readlines()]

# **读取真实标签**
with open(labels_file, "r", encoding="utf-8") as f:
    true_labels = [line.strip() for line in f.readlines()][1:]  # 跳过CSV的表头

# **确保两者长度匹配**
total = min(len(lstm_predictions), len(true_labels))
correct = sum(1 for i in range(total) if lstm_predictions[i] == true_labels[i])
accuracy = correct / total if total > 0 else 0

# **打印结果**
print(f"LSTM Model Accuracy: {accuracy:.2%} ({correct}/{total} correct)")
