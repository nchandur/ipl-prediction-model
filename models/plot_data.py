import plotly.express as px
import pandas as pd

def plot_data(data:pd.DataFrame, components:list[str]):
    fig = px.scatter(
        data_frame=data, 
        x=components[0],
        y=components[1],
        color="label",

    )

    fig.show()