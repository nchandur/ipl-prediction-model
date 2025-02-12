import numpy as np
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from utils.utils import retrieveFromDB

def convert_to_features(features:list) -> list:
    res = ["team_1_{}".format(feature) for feature in features]
    res += ["team_2_{}".format(feature) for feature in features]
    return res

def fit_model():

    data = retrieveFromDB(query="SELECT * FROM matches")

    indices = convert_to_features(["elo", "boundaries_scored_per_over", "boundaries_conceded_per_over", "boundary_idx", "boundary_inv_idx", "rwb_idx", "wicket_idx", "wicket_inv_idx", "econ"])
    win_pcts = convert_to_features(["win_pct", "h2h_win_pct", "stadium_win_pct", "h2h_stadium_win_pct"])
    cumulative = convert_to_features(["cumulative_runs_scored", "cumulative_runs_conceded", "cumulative_balls_faced", "cumulative_balls_bowled", "cumulative_wickets_taken", "cumulative_wickets_fallen", "cumulative_boundaries_scored", "cumulative_boundaries_conceded", "cumulative_matches_played"])


    features = indices + win_pcts + cumulative
    label = "team_1_victory"

    scaler = StandardScaler()

    data[features] = scaler.fit_transform(data[features])

    train, test = train_test_split(data, test_size=0.1, random_state=42, shuffle=True)

    model_1 = xgb.XGBClassifier(objective="binary:logistic", eval_metric="logloss")
    model_2 = RandomForestClassifier()

    model_1.fit(train[features], train[label])
    model_2.fit(train[features], train[label])

    xgb_pred = model_1.predict_proba(test[features])[:, -1]
    rf_pred = model_2.predict_proba(test[features])[:, -1]


    meta_features = np.column_stack((xgb_pred, rf_pred))

    meta_model = LogisticRegression()
    meta_model.fit(meta_features, test[label])

    pred = meta_model.predict(meta_features)

    report = classification_report(test[label], pred)

    print(report)

    return meta_model