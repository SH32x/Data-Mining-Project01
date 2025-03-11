You can run all four models simultaneously by running `run_all_names.py`, which requires Python to be installed and the necessary libraries (this includes at least `pandas`, `collections`, `sklearn`). The training dataset and testing dataset are hardcoded in the file, so please change them manually if needed.  

I'm not sure if `run_all_names.py` will work on macOS or Linux, but if it doesn't, please run it directly as follows:

- `check_player_performance.py`
- `predict_name_by_point.py`
- `predict_name_by_point.py`
- `predict_name_by_KNN_same_home_team_members.py`
- `predict_name_by_KNN_same_team_member.py`

Note that `predict_name_by_appearances.py` must be run after `check_player_performance.py` because `check_player_performance.py` generates `"player_appearances.txt"` file for `predict_name_by_appearances.py`.
