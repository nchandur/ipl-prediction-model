from utils.utils import *

def convert_to_features(features:list) -> list:
    res = ["team_1_{}".format(feature) for feature in features]
    res += ["team_2_{}".format(feature) for feature in features]
    return res

query = "SELECT * FROM matches"

data = retrieveFromDB(query=query)

identifiers = ['match_type', 'team_1', 'team_2', 'stadium', 'toss', 'player_of_the_match', 'match_id', 'date', 'time', 'season', 'team_1_id', 'team_2_id', 'winner', 'winner_id', 'is_playoff', 'stadium_id']

win_pcts = convert_to_features(["win_pct", "h2h_win_pct", "stadium_win_pct", "h2h_stadium_win_pct"])

cumulative = convert_to_features(["cumulative_runs_scored", "cumulative_runs_conceded", "cumulative_balls_faced", "cumulative_balls_bowled", "cumulative_wickets_taken", "cumulative_wickets_fallen", "cumulative_boundaries_scored", "cumulative_boundaries_conceded", "cumulative_matches_played"])

indices = convert_to_features(["rr", "nrr", "boundaries_scored_per_over", "boundaries_conceded_per_over", "boundary_idx", "boundary_inv_idx", "rwb_idx", "wicket_idx", "wicket_inv_idx", "econ"])