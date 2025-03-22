

# NBA Starting Lineup Prediction

## Final Model

- **Model File**: `new_KNN.py`  
- **Output Files**:
  - `FINAL_RESULT.csv`: Final result file containing `Game_ID`, `Home_Team`, and `Fifth_Player`.
  - `result_compare.csv`: File comparing model predictions with ground truth, with columns `KNN_output`, `NBA_label`, and `Match`.
  - `.\outcome_data\KNN_output_all.csv`: Consolidated file containing all predictions.



## Data Structure

- `Original_training_data/`: Contains raw training data (unmodified).
- `Modified_test_data/`: Contains test data. Files named like `KNN_test_20XX.csv` are subsets of the test set, split by season (e.g., `KNN_test_2007.csv`, `KNN_test_2008.csv`).

**Important**: All input and output paths in the models are hardcoded.  
To successfully run `new_KNN.py` or any other model, you **must navigate into the `NBA/` directory** and follow the instructions in its internal `readme.md`.  
If the file structure does not match the expected format, the scripts will not run correctly.



## Model Logic (`new_KNN.py`)

The final model is based on a KNN-like logic, designed to find similar lineups and return the most probable fifth starter.

### Training Phase

- Reads game records for the specified season.
- Records all 5-player starting combinations that have appeared for each team.
- Tracks the most frequent player for each position (e.g., `home_4`) per team and season.

### Prediction Phase

Predictions are made following a prioritized multi-step process:

1. **Exact Match (Same Season, Same Team)**  
   - Looks for a historical lineup with the same four known players.
   - If found, directly returns the fifth player from that combination.

2. **Fuzzy Match (Same Season, Partial Overlap)**  
   - If no exact match is found, looks for 3-player or 2-player overlapping combinations.

3. **Cross-Season Search**  
   - If no match is found in the current season, performs the above two steps across past seasons for the same team.

4. **Position-Based Heuristic**  
   - If still unmatched, returns the most frequently appearing player at the missing position for the team in that season.


## Unused Models

Note: All earlier models were developed under the assumption that we only needed to predict the player at the `home_4` position. Therefore, they could not work directly on the original `NBA_test.csv`, which contains unknowns (`?`) at various positions.  
Even if all unknowns are shifted to the `home_4` column, their prediction accuracy remains poor.  
Only after discovering that the same season's training data could be used for predictions (e.g., predicting 2007 games using 2007 data), we moved forward with the revised KNN model.

### `predict_name_by_appearances.py`

- `checkplayerperformance.py` counts all players who played at the `home_4` position in the training set.
- Outputs a file at `.\train_data\player_appearances.txt`, listing players by appearance count for each team.
- `predict_name_by_appearances.py` selects the player with the highest appearance count among those not already starting.

### `predict_name_by_points.py`

- Similar to the above, but sorts players by average points instead of appearances.
- Uses `.\train_data\formatted_player_points.txt` for input.
- Predicts the highest-scoring player among those not already in the lineup.

### `predict_name_by_KNN_same_home_team_members.py`

- **Training**: For each team (as the home team), records the most frequent fifth player for fixed 4-player combinations.
- **Prediction**: For a given 4-player input, returns the most frequent fifth player historically used with that exact group.
- If the combination is unseen, the output is `"Unknown"`, which results in a large number of unknowns when predicting games from different seasons.

### `predict_name_by_KNN_same_team_member.py`

- Extends the above model by also including games where the team was the **away** team during training.
- Provides more training data, but the `"Unknown"` issue persists and limits prediction accuracy.


## Model Accuracy (If Only Predicting `home_4`)

| Training & Testing Season | Appearance-Based | Point-Based | KNN (Home Only) | KNN (Home + Away) |
|---------------------------|------------------|-------------|------------------|--------------------|
| Same Season               | ~30%             | ~30%        | ~50%             | ~60%               |
| Different Seasons         | ~10%             | ~10%        | ~15%             | ~15%               |

> Note: When the task requires predicting unknown players at **random positions** (as in `NBA_test.csv`), none of these four models achieves over 10% accuracy.

