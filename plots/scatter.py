import dash
from dash import dcc
import plotly.express as px

class Scatter(dcc.Graph):

    def __init__(
        self,
        df,
        id,
        x='x',
        y='y',
        x_title='',
        y_title='',
        size=None,
        color=None,
        hover=None,
        title=None,
        text=None,
        log_y=False,
    ):

        fig = px.scatter(
            df,
            x = x,
            y = y,
            log_y = log_y,
            title = title,
            size = size,
            color = color,
            text = text,
        )

        fig.update_traces(
            marker_color = "#0c869b",
        )

        if hover:
            fig.update_traces(
                hovertext = df[hover],
                hovertemplate = '%{hovertext}<extra></extra>',
            )

        fig.update_layout(
            margin = dict(l=0, r=0, t=30, b=0),
            autosize = True,
            xaxis = dict(
                title = x_title,
            ),
            yaxis = dict(
                title = y_title,
            ),
            title_x = 0.5,
            font = dict(
                family = "Raleway",
                size = 12,
            )
        )

        super().__init__(
            id = id,
            figure = fig,
            responsive = True,
        )
