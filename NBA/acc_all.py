import os
import pandas as pd

# **评估预测结果**
def evaluate_predictions(test_year, outcome_folder="./outcome_data", test_folder="./test_data"):
    # 确定文件路径
    labels_file = os.path.join(test_folder, f"labels_{test_year}.csv")
    predictions_files = {
        "Appearances": os.path.join(outcome_folder, "appearances_predictions.txt"),
        "KNN All": os.path.join(outcome_folder, "KNN_all_predictions.txt"),
        "KNN Home": os.path.join(outcome_folder, "KNN_home_predictions.txt"),
        "Points": os.path.join(outcome_folder, "points_predictions.txt")
        
    }

    # 检查 labels 文件是否存在
    if not os.path.exists(labels_file):
        print(f"Error: {labels_file} not found.")
        return

    # 读取 labels
    df_labels = pd.read_csv(labels_file)
    true_values = df_labels["removed_value"].tolist()  # 真实值列表

    # 结果存储
    results = {}

    # 遍历每种预测方法
    for method, pred_file in predictions_files.items():
        if not os.path.exists(pred_file):
            print(f"Warning: {pred_file} not found, skipping {method}.")
            continue

        # 读取预测结果
        with open(pred_file, "r", encoding="utf-8") as f:
            predictions = [line.strip() for line in f.readlines()]

        # 确保预测结果和真实值长度匹配
        total = min(len(predictions), len(true_values))
        correct = sum(1 for i in range(total) if predictions[i] == true_values[i])
        accuracy = correct / total if total > 0 else 0

        results[method] = {
            "Correct": correct,
            "Total": total,
            "Accuracy": accuracy
        }

    # **打印结果**
    print("\nEvaluation Results:")
    for method, data in results.items():
        print(f"{method}: {data['Accuracy']:.2%} ({data['Correct']} / {data['Total']})")

    # **写入文件**
    output_file = os.path.join(outcome_folder, "evaluation_results.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("Evaluation Results\n")
        f.write("=" * 30 + "\n")
        for method, data in results.items():
            f.write(f"{method}: {data['Accuracy']:.2%} ({data['Correct']} / {data['Total']})\n")

    print(f"\n✅ Evaluation results saved to {output_file}")

# **主流程**
if __name__ == "__main__":
    # 让用户输入测试年份
    test_year = input("Enter the test year (2007-2016): ").strip()
    if not test_year.isdigit() or int(test_year) not in range(2007, 2017):
        print("Invalid year. Please enter a number between 2007 and 2016.")
    else:
        evaluate_predictions(test_year)
