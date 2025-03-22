import pandas as pd
import os
import sys
from collections import defaultdict, Counter
from itertools import combinations
from tqdm import tqdm

def build_knowledge(df_train):
    """构建球队知识库"""
    team_knowledge = defaultdict(lambda: {
        'season_data': defaultdict(lambda: {
            'position_stats': [defaultdict(Counter) for _ in range(5)],
            'player_freq': [Counter() for _ in range(5)]
        }),
        'cross_season': {
            'position_stats': [defaultdict(Counter) for _ in range(5)],
            'player_freq': [Counter() for _ in range(5)]
        }
    })

    for _, row in df_train.iterrows():
        team = row["home_team"]
        season = row["season"]
        players = [row[f"home_{i}"] for i in range(5)]
        
        season_data = team_knowledge[team]['season_data'][season]
        cross_data = team_knowledge[team]['cross_season']
        
        for missing_pos in range(5):
            context = sorted([p for i,p in enumerate(players) if i != missing_pos])
            target = players[missing_pos]
            
            # 赛季特定数据
            season_data['position_stats'][missing_pos][tuple(context)][target] += 1
            season_data['player_freq'][missing_pos][target] += 1
            
            # 跨赛季数据
            cross_data['position_stats'][missing_pos][tuple(context)][target] += 1
            cross_data['player_freq'][missing_pos][target] += 1
            
            # 模糊匹配模式
            for r in [3, 2]:
                for comb in combinations(context, r):
                    weight = 0.7/r if r == 3 else 0.5/r
                    season_data['position_stats'][missing_pos][tuple(sorted(comb))][target] += weight
                    cross_data['position_stats'][missing_pos][tuple(sorted(comb))][target] += weight

    return team_knowledge

def predict_missing(team_knowledge, team, season, context, missing_pos):
    """五级预测策略"""
    # 第一级：精确匹配（同赛季）
    if team in team_knowledge:
        if season_data := team_knowledge[team]['season_data'].get(season):
            if candidates := season_data['position_stats'][missing_pos].get(tuple(sorted(context))):
                return candidates.most_common(1)[0][0]
    
    # 第二级：模糊匹配（同赛季）
    if team in team_knowledge:
        if season_data := team_knowledge[team]['season_data'].get(season):
            fuzzy_scores = Counter()
            for r in [3, 2]:
                for comb in combinations(context, r):
                    for player, count in season_data['position_stats'][missing_pos].get(tuple(sorted(comb)), {}).items():
                        fuzzy_scores[player] += count * (0.7 if r==3 else 0.5)
            if fuzzy_scores:
                return fuzzy_scores.most_common(1)[0][0]
    
    # 第三级：跨赛季精确匹配
    if team in team_knowledge:
        if candidates := team_knowledge[team]['cross_season']['position_stats'][missing_pos].get(tuple(sorted(context))):
            return candidates.most_common(1)[0][0]
    
    # 第四级：位置频率优先
    if team in team_knowledge:
        if season_data := team_knowledge[team]['season_data'].get(season):
            if freq := season_data['player_freq'][missing_pos]:
                return freq.most_common(1)[0][0]
    
    # 第五级：跨赛季位置频率
    if team in team_knowledge:
        if freq := team_knowledge[team]['cross_season']['player_freq'][missing_pos]:
            return freq.most_common(1)[0][0]
    
    return "Unknown"

def process_season(train_path, test_path):
    """处理单个赛季数据"""
    try:
        # 加载数据
        df_train = pd.read_csv(train_path)
        df_test = pd.read_csv(test_path)
        
        # 预处理
        df_train = df_train[["season","home_team","home_0","home_1","home_2","home_3","home_4"]]
        df_test = df_test[["season","home_team","home_0","home_1","home_2","home_3","home_4"]]
        
        # 构建知识库
        team_knowledge = build_knowledge(df_train)
        
        # 执行预测
        predictions = []
        for _, row in df_test.iterrows():
            team = row["home_team"]
            season = row["season"]
            current = [row[f"home_{i}"] for i in range(5)]
            
            missing = [i for i, p in enumerate(current) if p == "?"]
            if len(missing) != 1:
                predictions.append("Unknown")
                continue
                
            missing_pos = missing[0]
            context = [p for i,p in enumerate(current) if i != missing_pos and p != "?"]
            context = [p for p in context if p != "?"]  # 二次过滤
            
            pred = predict_missing(team_knowledge, team, season, context, missing_pos)
            predictions.append(pred)
            
        return predictions
    
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        return []

def main():
    # 初始化结果存储
    all_predictions = []
    
    # 创建输出目录
    os.makedirs(".\\outcome_data", exist_ok=True)
    
    # 第一部分：处理正常年份（2007-2015）
    for year in tqdm(range(2007, 2016), desc="Processing regular seasons"):
        train_path = f".\\train_data\\matchups-{year}.csv"
        test_path = f".\\test_data\\KNN_test_{year}.csv"
        
        # 检查文件存在性
        if not os.path.exists(train_path):
            print(f"\nWarning: Train file {train_path} not found")
            continue
        if not os.path.exists(test_path):
            print(f"\nWarning: Test file {test_path} not found")
            continue
            
        # 处理当前赛季
        try:
            season_preds = process_season(train_path, test_path)
            all_predictions.extend(season_preds)
            print(f"\nProcessed {year} season: {len(season_preds)} predictions")
        except Exception as e:
            print(f"\nError processing {year} season: {str(e)}")

    # 第二部分：特殊处理2015训练数据对应2016测试数据
    print("\nProcessing special case: 2015 train -> 2016 test")
    special_train_path = ".\\train_data\\matchups-2015.csv"
    special_test_path = ".\\test_data\\KNN_test_2016.csv"
    
    if os.path.exists(special_train_path) and os.path.exists(special_test_path):
        try:
            special_preds = process_season(special_train_path, special_test_path)
            all_predictions.extend(special_preds)
            print(f"Processed 2016 test season: {len(special_preds)} predictions")
        except Exception as e:
            print(f"Error processing special case: {str(e)}")
    else:
        missing_files = []
        if not os.path.exists(special_train_path):
            missing_files.append(special_train_path)
        if not os.path.exists(special_test_path):
            missing_files.append(special_test_path)
        print(f"Warning: Missing files for special case - {', '.join(missing_files)}")

    # 写入最终结果文件
    output_path = ".\\outcome_data\\KNN_output_all.csv"
    pd.DataFrame({"predicted_name": all_predictions}).to_csv(output_path, index=False)
    print(f"\nAll predictions saved to {output_path}")

    # 计算准确率
    label_path = ".\\test_data\\NBA_test_labels.csv"
    if os.path.exists(label_path):
        try:
            df_labels = pd.read_csv(label_path)
            labels = df_labels["removed_value"].tolist()
            
            # 对齐数据长度
            min_length = min(len(labels), len(all_predictions))
            labels = labels[:min_length]
            predictions = all_predictions[:min_length]
            
            correct = sum(p == t for p, t in zip(predictions, labels))
            accuracy = correct / min_length * 100
            
            print(f"\nFinal Accuracy: {accuracy:.2f}% ({correct}/{min_length})")
            
            # 生成详细报告
            report_df = pd.DataFrame({
                "True": labels,
                "Predicted": predictions,
                "Correct": [p == t for p, t in zip(predictions, labels)]
            })
            report_path = ".\\outcome_data\\detailed_accuracy_report.csv"
            report_df.to_csv(report_path, index=False)
            print(f"Detailed report saved to {report_path}")
            
        except Exception as e:
            print(f"\nError calculating accuracy: {str(e)}")
    else:
        print("\nLabel file not found, skipping accuracy calculation")

if __name__ == "__main__":
    main()