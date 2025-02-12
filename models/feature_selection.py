from utils.utils import *
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import numpy as np

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

data[features] = StandardScaler().fit_transform(data[features])

data = data[features + [label]]

train, test = train_test_split(data, test_size=0.1, random_state=42)

model = LogisticRegression()
model.fit(data[features], data[label])

res = pd.DataFrame()
res["features"] = model.feature_names_in_
res["coef"] = np.abs(model.coef_[0])


coef = res.sort_values(by=["coef"], ascending=False)

coef = coef[coef["coef"] >= 0.3]

print(list(coef["features"].values))