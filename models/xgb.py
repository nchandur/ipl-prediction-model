from utils.utils import *
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report


def convert_to_features(features:list) -> list:
    res = ["team_1_{}".format(feature) for feature in features]
    res += ["team_2_{}".format(feature) for feature in features]
    return res


data = retrieveFromDB(query="SELECT * FROM matches")


indices = convert_to_features(["elo", "boundaries_scored_per_over", "boundaries_conceded_per_over", "boundary_idx", "boundary_inv_idx", "rwb_idx", "wicket_idx", "wicket_inv_idx", "econ"])
win_pcts = convert_to_features(["win_pct", "h2h_win_pct", "stadium_win_pct", "h2h_stadium_win_pct"])
cumulative = convert_to_features(["cumulative_runs_scored", "cumulative_runs_conceded", "cumulative_balls_faced", "cumulative_balls_bowled", "cumulative_wickets_taken", "cumulative_wickets_fallen", "cumulative_boundaries_scored", "cumulative_boundaries_conceded", "cumulative_matches_played"])


features = indices + win_pcts + cumulative
label = "team_1_victory"

scaler = StandardScaler()

data[features] = scaler.fit_transform(data[features])

data = data[features + [label]]

train, test = train_test_split(data, test_size=0.1, random_state=42)

model = xgb.XGBClassifier(objective="binary:logistic", eval_metric="logloss", random_state=42)
model.fit(train[features], train[label])

pred = model.predict(test[features])
report = classification_report(pred, test[label])

print(report)