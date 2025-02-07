from utils.utils import *
import pandas as pd
import plotly.graph_objects as go


def get_team_data(id: int, feature: str) -> pd.DataFrame:
    query = """
    SELECT 
        date,
        CASE
            WHEN team_1_id = {} THEN team_1
            WHEN team_2_id = {} THEN team_2
        END as team,
        CASE 
            WHEN team_1_id = {} THEN team_1_{}
            WHEN team_2_id = {} THEN team_2_{}
        END AS feature
    FROM matches
    WHERE (team_1_id = {} OR team_2_id = {})
    AND season = 2024
    ORDER BY date;
    """.format(
        id, id, id, feature, id, feature, id, id
    )

    data = retrieveFromDB(query=query)
    data["date"] = pd.to_datetime(data["date"])

    return data


team_ids = [15, 12]
feature = "elo"

teams = [get_team_data(id, feature=feature) for id in team_ids]

fig = go.Figure()

for idx, data in enumerate(teams):
    fig.add_trace(
        go.Scatter(
            x=data["date"], y=data["feature"], mode="lines", name=data["team"].iloc[0]
        )
    )

fig.update_layout(
    title="{} Over Time".format(feature),
    xaxis_title="Date",
    yaxis_title=feature,
    showlegend=True,
)

fig.show()
