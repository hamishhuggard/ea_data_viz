import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
import plotly.express as px

class Bar(dcc.Graph):

    def __init__(self, df, height=None, title=None):

        if 'text' in df.columns:
            text_col = 'text'
        else:
            text_col = 'y'

        if 'hover' in df.columns:
            hover_col = 'hover'
        else:
            hover_col = 'x'

        self.bar = px.bar(
            df,
            y='x',
            x='y',
            text=text_col,
            title=title,
            height=height,
            orientation='h',
        )

        self.bar.update_traces(
            marker_color="#0c869b",
            hovertext = df[hover_col],
            hovertemplate = '%{hovertext}<extra></extra>',
        )

        self.bar.update_xaxes(side='top')

        self.bar.update_layout(
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis=dict(
                title='',
                fixedrange=True
            ),
            yaxis=dict(
                title='',
                # dtick=1,
                fixedrange=True
            ),
            title_x=0.5,
            font=dict(
                family="Raleway",
                size=12,
            )
        )

        super().__init__(
            id=title,
            figure=self.bar,
            responsive=True,
            config={
                'displayModeBar': False,
            },
        )
