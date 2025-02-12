from utils.utils import retrieveFromDB
from sklearn.decomposition import KernelPCA
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import numpy as np
import pandas as pd
from models.plot_data import plot_data

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
data = data[features + [label]]

scaler = StandardScaler()

data[features] = scaler.fit_transform(data[features])

components = 2

pca = KernelPCA(n_components=components, kernel="cosine", random_state=42)

pca_features = pca.fit_transform(data.drop(columns=[label]))

explained = np.cumsum(pca.eigenvalues_ / np.sum(pca.eigenvalues_))

transformed = pd.DataFrame()

for c in range(components):
    transformed["pca_{}".format(c + 1)] = pca_features[:, c]

transformed["label"] = data[label]

plot_data(data=transformed, components=["pca_1", "pca_2"])

cols = transformed.columns.to_list()[:-1]

transformed[cols] = scaler.fit_transform(transformed[cols])

train, test = train_test_split(transformed, test_size=0.1, shuffle=True, random_state=42)

model = xgb.XGBClassifier(objective="binary:logistic", eval_metric="logloss", random_state=42)

model.fit(train[cols], train["label"])

pred = model.predict(test[cols])

report = classification_report(test["label"], pred)

print(report)