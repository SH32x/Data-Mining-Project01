import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from keras.models import Model
from keras.layers import Input, Embedding, LSTM, Dense, Concatenate, Flatten
from keras.callbacks import EarlyStopping

# 数据预处理
def preprocess_data(train_path, test_path, player_threshold=5):
    # 读取数据
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    # 收集所有球员和球队
    all_players = []
    for col in ['home_0', 'home_1', 'home_2', 'home_3', 'home_4', 
                'away_0', 'away_1', 'away_2', 'away_3', 'away_4']:
        all_players.extend(train_df[col].tolist())
    
    # 统计球员频率
    player_counts = pd.Series(all_players).value_counts().to_dict()
    train_players = [k for k, v in player_counts.items() if v >= player_threshold]
    train_players.append('<UNK>')  # 添加未知标记

    # 球队处理
    all_teams = list(set(train_df['home_team'].tolist() + train_df['away_team'].tolist()))
    all_teams.append('<UNK>')

    # 创建编码器
    player_encoder = LabelEncoder()
    player_encoder.fit(train_players)
    team_encoder = LabelEncoder()
    team_encoder.fit(all_teams)

    # 替换低频球员和未知球队
    def replace_unk(df):
        for col in ['home_0', 'home_1', 'home_2', 'home_3', 'home_4',
                   'away_0', 'away_1', 'away_2', 'away_3', 'away_4']:
            df[col] = df[col].apply(lambda x: x if x in player_encoder.classes_ else '<UNK>')
        df['home_team'] = df['home_team'].apply(lambda x: x if x in team_encoder.classes_ else '<UNK>')
        df['away_team'] = df['away_team'].apply(lambda x: x if x in team_encoder.classes_ else '<UNK>')
        return df

    train_df = replace_unk(train_df)
    test_df = replace_unk(test_df)

    # 转换为编码
    for col in ['home_0', 'home_1', 'home_2', 'home_3', 'home_4',
                'away_0', 'away_1', 'away_2', 'away_3', 'away_4']:
        train_df[col] = player_encoder.transform(train_df[col])
        test_df[col] = player_encoder.transform(test_df[col])
    
    train_df['home_team'] = team_encoder.transform(train_df['home_team'])
    train_df['away_team'] = team_encoder.transform(train_df['away_team'])
    test_df['home_team'] = team_encoder.transform(test_df['home_team'])
    test_df['away_team'] = team_encoder.transform(test_df['away_team'])

    # 生成排序后的序列
    def sort_players(row, prefix, count):
        return sorted([row[f'{prefix}_{i}'] for i in range(count)])

    train_home = [sort_players(row, 'home', 4) for _, row in train_df.iterrows()]
    train_away = [sort_players(row, 'away', 5) for _, row in train_df.iterrows()]
    test_home = [sort_players(row, 'home', 4) for _, row in test_df.iterrows()]
    test_away = [sort_players(row, 'away', 5) for _, row in test_df.iterrows()]

    return {
        'train': (train_home, train_away, 
                 train_df['home_team'].values, train_df['away_team'].values,
                 train_df['home_4'].values),
        'test': (test_home, test_away,
                test_df['home_team'].values, test_df['away_team'].values,
                test_df['home_4'].values if 'home_4' in test_df.columns else None),
        'encoders': (player_encoder, team_encoder)
    }

# 构建模型
def build_model(player_vocab_size, team_vocab_size):
    # 输入层
    home_players = Input(shape=(4,), name='home_players')
    away_players = Input(shape=(5,), name='away_players')
    home_team = Input(shape=(1,), name='home_team')
    away_team = Input(shape=(1,), name='away_team')

    # 嵌入层
    player_embed = Embedding(player_vocab_size, 32)
    team_embed = Embedding(team_vocab_size, 8)

    # 处理球员序列
    home_embedded = player_embed(home_players)
    home_lstm = LSTM(64)(home_embedded)
    
    away_embedded = player_embed(away_players)
    away_lstm = LSTM(64)(away_embedded)

    # 处理球队
    home_t = Flatten()(team_embed(home_team))
    away_t = Flatten()(team_embed(away_team))

    # 合并特征
    concat = Concatenate()([home_lstm, away_lstm, home_t, away_t])
    
    # 全连接层
    dense = Dense(128, activation='relu')(concat)
    output = Dense(player_vocab_size, activation='softmax')(dense)

    model = Model(inputs=[home_players, away_players, home_team, away_team], 
                 outputs=output)
    model.compile(optimizer='adam',
                 loss='sparse_categorical_crossentropy',
                 metrics=['accuracy'])
    return model

# 主程序
if __name__ == "__main__":
    # 预处理数据
    data = preprocess_data('matchups-2008.csv', 'matchups-2009.csv')
    (train_home, train_away, train_h_team, train_a_team, y_train) = data['train']
    (test_home, test_away, test_h_team, test_a_team, y_test) = data['test']
    player_encoder, team_encoder = data['encoders']

    # 转换为numpy数组
    X_train = {
        'home_players': np.array(train_home),
        'away_players': np.array(train_away),
        'home_team': np.array(train_h_team),
        'away_team': np.array(train_a_team)
    }
    X_test = {
        'home_players': np.array(test_home),
        'away_players': np.array(test_away),
        'home_team': np.array(test_h_team),
        'away_team': np.array(test_a_team)
    }

    # 构建模型
    model = build_model(len(player_encoder.classes_), len(team_encoder.classes_))

    # 训练模型
    early_stop = EarlyStopping(monitor='val_loss', patience=3)
    history = model.fit(X_train, y_train,
                       validation_split=0.2,
                       epochs=50,
                       batch_size=32,
                       callbacks=[early_stop],
                       verbose=1)

    # 预测测试集
    predictions = model.predict(X_test)
    predicted_labels = np.argmax(predictions, axis=1)
    predicted_players = player_encoder.inverse_transform(predicted_labels)

    # 保存结果
    test_df = pd.read_csv('matchups-2009.csv')
    test_df['predicted_home_4'] = predicted_players
    test_df.to_csv('predictions-2009.csv', index=False)

    # 计算准确率（如果测试集有标签）
    if y_test is not None:
        y_test_players = player_encoder.inverse_transform(y_test)
        correct_predictions = np.sum(predicted_players == y_test_players)  # 计算预测正确的数量
        total_predictions = len(y_test_players)  # 总预测数
        accuracy = correct_predictions / total_predictions  # 计算准确率
        print(f"Test Accuracy: {accuracy:.4f} ({correct_predictions}/{total_predictions} correct)")
    else:
        print("Predictions saved to predictions-2009.csv")
