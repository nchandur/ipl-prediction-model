import pandas as pd
import numpy as np
from tqdm import tqdm
from utils.utils import *


def calculate_cumulative_stats(data):
    data = data.sort_values(by=["date", "match_id"]).reset_index(drop=True)

    cumulative_cols = [
        "cumulative_runs_scored",
        "cumulative_runs_conceded",
        "cumulative_balls_faced",
        "cumulative_balls_bowled",
        "cumulative_wickets_taken",
        "cumulative_wickets_fallen",
        "cumulative_boundaries_scored",
        "cumulative_boundaries_conceded",
        "cumulative_matches_played",
    ]

    team_stats = {}

    for team_col, opponent_col in [("team_1", "team_2"), ("team_2", "team_1")]:
        for stat in cumulative_cols:
            data[f"{team_col}_{stat}"] = 0

        for team in pd.concat([data["team_1"], data["team_2"]]).unique():
            team_stats[team] = {
                "runs_scored": 0,
                "runs_conceded": 0,
                "balls_faced": 0,
                "balls_bowled": 0,
                "wickets_taken": 0,
                "wickets_fallen": 0,
                "boundaries_scored": 0,
                "boundaries_conceded": 0,
                "matches_played": 0,
            }

    for index, row in tqdm(
        data.iterrows(),
        total=data.shape[0],
        unit="game",
        desc="Calculating Cumulative Statistics",
    ):
        for team_col, opponent_col in [("team_1", "team_2"), ("team_2", "team_1")]:
            team = row[team_col]

            data.at[index, f"{team_col}_cumulative_runs_scored"] = team_stats[team][
                "runs_scored"
            ]
            data.at[index, f"{team_col}_cumulative_runs_conceded"] = team_stats[team][
                "runs_conceded"
            ]
            data.at[index, f"{team_col}_cumulative_balls_faced"] = team_stats[team][
                "balls_faced"
            ]
            data.at[index, f"{team_col}_cumulative_balls_bowled"] = team_stats[team][
                "balls_bowled"
            ]
            data.at[index, f"{team_col}_cumulative_wickets_taken"] = team_stats[team][
                "wickets_taken"
            ]
            data.at[index, f"{team_col}_cumulative_wickets_fallen"] = team_stats[team][
                "wickets_fallen"
            ]
            data.at[index, f"{team_col}_cumulative_boundaries_scored"] = team_stats[
                team
            ]["boundaries_scored"]
            data.at[index, f"{team_col}_cumulative_boundaries_conceded"] = team_stats[
                team
            ]["boundaries_conceded"]
            data.at[index, f"{team_col}_cumulative_matches_played"] = team_stats[team][
                "matches_played"
            ]

            team_stats[team]["runs_scored"] += row[f"{team_col}_total"]
            team_stats[team]["runs_conceded"] += row[f"{opponent_col}_total"]
            team_stats[team]["balls_faced"] += row[f"{team_col}_balls"]
            team_stats[team]["balls_bowled"] += row[f"{opponent_col}_balls"]
            team_stats[team]["wickets_taken"] += row[f"{opponent_col}_wickets"]
            team_stats[team]["wickets_fallen"] += row[f"{team_col}_wickets"]
            team_stats[team]["boundaries_scored"] += row[f"{team_col}_boundaries"]
            team_stats[team]["boundaries_conceded"] += row[f"{opponent_col}_boundaries"]
            team_stats[team]["matches_played"] += 1

    return data


def calculate_performance_indices(data):

    data.fillna(value=0, inplace=True)
    data.replace(to_replace=np.inf, value=0, inplace=True)
    data.replace(to_replace=-np.inf, value=0, inplace=True)

    data["team_1_rr"] = (data["team_1_cumulative_runs_scored"] * 6) / data[
        "team_1_cumulative_balls_faced"
    ]
    data["team_2_rr"] = (data["team_2_cumulative_runs_scored"] * 6) / data[
        "team_2_cumulative_balls_faced"
    ]

    data["team_1_nrr"] = (
        (
            (data["team_1_cumulative_runs_scored"] * 6)
            / data["team_1_cumulative_balls_faced"]
        )
        - (
            (data["team_1_cumulative_runs_conceded"] * 6)
            / data["team_1_cumulative_balls_bowled"]
        )
    ) / data["team_1_cumulative_matches_played"]
    data["team_2_nrr"] = (
        (
            (data["team_2_cumulative_runs_scored"] * 6)
            / data["team_2_cumulative_balls_faced"]
        )
        - (
            (data["team_2_cumulative_runs_conceded"] * 6)
            / data["team_2_cumulative_balls_bowled"]
        )
    ) / data["team_2_cumulative_matches_played"]

    data["team_1_boundaries_scored_per_over"] = (
        data["team_1_cumulative_boundaries_scored"] * 6
    ) / data["team_1_cumulative_balls_faced"]
    data["team_1_boundaries_conceded_per_over"] = (
        data["team_1_cumulative_boundaries_conceded"] * 6
    ) / data["team_1_cumulative_balls_bowled"]

    data["team_2_boundaries_scored_per_over"] = (
        data["team_2_cumulative_boundaries_scored"] * 6
    ) / data["team_2_cumulative_balls_faced"]
    data["team_2_boundaries_conceded_per_over"] = (
        data["team_2_cumulative_boundaries_conceded"] * 6
    ) / data["team_2_cumulative_balls_bowled"]

    data["team_1_boundary_idx"] = (
        data["team_1_cumulative_boundaries_scored"]
        / data["team_1_cumulative_matches_played"]
    )
    data["team_2_boundary_idx"] = (
        data["team_2_cumulative_boundaries_scored"]
        / data["team_2_cumulative_matches_played"]
    )

    data["team_1_boundary_inv_idx"] = (
        data["team_1_cumulative_boundaries_conceded"]
        / data["team_1_cumulative_matches_played"]
    )
    data["team_2_boundary_inv_idx"] = (
        data["team_2_cumulative_boundaries_conceded"]
        / data["team_2_cumulative_matches_played"]
    )

    data["team_1_rwb_idx"] = (
        data["team_1_cumulative_runs_scored"]
        - data["team_1_cumulative_boundaries_scored"]
    ) / data["team_1_cumulative_matches_played"]
    data["team_2_rwb_idx"] = (
        data["team_2_cumulative_runs_scored"]
        - data["team_2_cumulative_boundaries_scored"]
    ) / data["team_2_cumulative_matches_played"]

    data["team_1_wicket_idx"] = (
        data["team_1_cumulative_wickets_taken"]
        / data["team_1_cumulative_matches_played"]
    )
    data["team_2_wicket_idx"] = (
        data["team_2_cumulative_wickets_taken"]
        / data["team_2_cumulative_matches_played"]
    )

    data["team_1_wicket_inv_idx"] = (
        data["team_1_cumulative_wickets_fallen"]
        / data["team_1_cumulative_matches_played"]
    )
    data["team_2_wicket_inv_idx"] = (
        data["team_2_cumulative_wickets_fallen"]
        / data["team_2_cumulative_matches_played"]
    )

    data["team_1_econ"] = (data["team_1_cumulative_runs_conceded"] * 6) / data[
        "team_1_cumulative_balls_bowled"
    ]
    data["team_2_econ"] = (data["team_2_cumulative_runs_conceded"] * 6) / data[
        "team_2_cumulative_balls_bowled"
    ]

    data.fillna(value=0, inplace=True)
    data.replace(to_replace=np.inf, value=0, inplace=True)
    data.replace(to_replace=-np.inf, value=0, inplace=True)

    return data


data = retrieveFromDB(query="SELECT * FROM matches")
data = calculate_cumulative_stats(data=data)
data = calculate_performance_indices(data=data)

data = data.round(4)

pushToDB(data=data, tablename="matches")
