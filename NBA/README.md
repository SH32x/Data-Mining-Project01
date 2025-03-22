

# NBA Player Prediction Models

This project contains multiple models designed to predict player identities in NBA games based on various types of feature information.

## Project Structure

There are five main prediction models:

- `predict_name_by_appearances.py`  
- `predict_name_by_KNN_same_home_team_members.py`  
- `predict_name_by_KNN_same_team_member.py`  
- `predict_name_by_points.py`  
- `new_KNN.py`

Additional helper scripts include:  
- `test_all.py`: Runs the first four models in batch  
- `acc_all.py`: Evaluates the accuracy of the first four models  
- `modify_NBA_test.py`: Modifies the original test dataset to match model requirements  

## Required Libraries

Make sure the following Python libraries are installed:

```
collections  
pandas  
itertools  
tqdm
```

## Model Overview and How to Run

### First Four Models (Predict only `home_4`)

- `predict_name_by_appearances.py`  
- `predict_name_by_KNN_same_home_team_members.py`  
- `predict_name_by_KNN_same_team_member.py`  
- `predict_name_by_points.py`

These models are designed to predict only the fifth player (`home_4`). As such, they require a modified dataset named `NBA_test_modified.csv`, where all unknown player entries (`?`) have been moved to the fifth player slot.

#### Run All Models Together

You can use `test_all.py` to run the first four models in batch:

```
cd ./NBA
python test_all.py
```

- The script reads `NBA_test_modified.csv`, splits the data by year (2007 to 2016), and saves them as `test_2007.csv` to `test_2016.csv` in the `test_data/` folder.
- If these files already exist, they will not be regenerated.
- You will be asked to select a year by entering a number from 1 to 10 (corresponding to 2007 to 2016).
- The four models will be executed sequentially, and the results will be saved in the `outcome_data/` folder.

#### Accuracy Evaluation

Use `acc_all.py` to compare predictions with the actual labels:

```
cd ./NBA
python acc_all.py
```

You will be prompted to enter a year (2007 to 2016). The results will be displayed in the terminal.

#### Run a Single Model

To run any of the four models individually:

```
cd ./NBA
python <model_name.py> <appearances_file> <test_file>
```

Example:

```
python predict_name_by_appearances.py player_appearances.txt test_data/test_2007.csv
```

### `new_KNN.py` (Supports Any Unknown Position)

`new_KNN.py` is a newer version of the KNN model that can predict unknown players in any position.

#### How to Run

```
cd ./NBA
python new_KNN.py
```

- It uses test files named `KNN_test_2007.csv` through `KNN_test_2016.csv`, located in the `test_data/` folder.
- The script will automatically process each file and write the combined results to `KNN_output_all.csv`.
- It then compares the results to the labels in `NBA_test_labels.csv`.
- Final accuracy and the number of correct predictions will be printed to the console.

## Folder Descriptions

- `outcome_data/`: Contains prediction results and evaluation reports  
- `test_data/`: Contains test datasets, label files, and modified input files  
- `train_data/`: Contains training data including player performance and matchup records  
- Other `.py` scripts: Model implementations and evaluation tools  

Please refer to the project directory tree for the complete file structure.
