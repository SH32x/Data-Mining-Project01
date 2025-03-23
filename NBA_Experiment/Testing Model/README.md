# 🏀 NBA Starting Lineup Predictor

This repository presents a multi-model pipeline to predict the missing fifth player in NBA starting lineups based on historical game data. The primary focus is on **multi-class classification**, utilizing data from 2007–2015 to infer missing lineup components and analyze model performance.

## 📁 Repository Structure

### 📓 Notebooks

#### 1. `Nba Test Inference Submission.ipynb`
A complete end-to-end pipeline for fifth-player prediction:
- Loads and filters historical NBA matchup data (2007–2015).
- Trains **Word2Vec embeddings** on player lineups.
- Combines metadata and player embeddings into a feature matrix.
- Uses a **LightGBM multiclass classifier** for prediction.
- Evaluates top-1 and top-3 accuracy on a validation set.
- Saves models (`.pkl`) for later use.

#### 2. `NBA_Prediction_on_home_4.ipynb`
Focused on predicting the `home_4` player (fifth starter) using:
- A **Random Forest classifier** with label encoding.
- Test-time inference to generate a `Fifth_Player` prediction.
- Accuracy computation on a labeled validation set.
- Outputs results to `NBA_predictions.csv`.

#### 3. `NBA_SF.ipynb`
A sibling notebook to the one above, repeating the same process with slight tweaks (possibly for different roles like Small Forward (SF)). Also uses a Random Forest and shares logic with `NBA_Prediction_on_home_4.ipynb`.

#### 4. `Predict_With_Ensemble.ipynb`
This notebook demonstrates **seasonal model training and ensemble predictions**:
- Trains a separate model for each season from 2007–2015.
- Stores models in the `season_models` directory.
- Performs test-time predictions with these models.
- Aggregates predictions for evaluation and exports to Excel.

---

### 📊 CSV Files

#### `comparison_results_all.csv`
Contains model evaluation results:
- `Predicted_Fifth_Player`: model’s output.
- `Actual_Fifth_Player`: ground truth from labeled data.
- `Match`: boolean column indicating prediction correctness.

Useful for computing accuracy, confusion matrices, or other metrics.

#### `NBA_Prediction_on_home_4.csv`
Test inference submission results:
- `game`: identifier for each game.
- `home_team`: the team for which prediction was made.
- `Fifth_Player`: the model’s prediction for the missing player.

---

## 🧠 Problem Overview

Given a partial starting lineup (typically with one player missing), this project aims to identify the missing fifth player based on:
- Team context (home vs away)
- Historical player combinations
- Match outcome (win/loss)
- Positional patterns (implied from order)

---

## ⚙️ Requirements

- Python 3.8+
- Libraries:
  - `pandas`, `numpy`
  - `scikit-learn`
  - `lightgbm`
  - `gensim` (for Word2Vec)
  - `joblib`
  - `openpyxl` (for Excel export)



## ✅ Evaluation Metrics

- **Top-1 Accuracy**: Direct match of predicted player to ground truth.
- **Top-3 Accuracy**: Whether the true player appears in top-3 probabilities (from LightGBM).
- **Confusion matrix** (can be computed using `comparison_results_all.csv`).

---

## ✨ Future Improvements

- Add support for player position encoding.
- Incorporate player stats, injuries, and roster changes.
- Test ensemble models across seasons with majority voting.
- Deploy model as a REST API for real-time inference.

---



## 📜 License

This project is licensed under the MIT License.
