import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px

class EABarGraph(dcc.Graph):

    def __init__(self, df, height, title=None):

        self.bar = px.bar(

            df,
            y='x',
            x='y',
            title=title,
            height=height,
            orientation='h',

            # Don't provide any hover data
            hover_data={
                'x': False,
                'y': False,
            },

            # These are the labels shown in the hoverdata:
            # labels={
            #     'label': title,
            #     'Percent': 'Percentage',
            # },
        )

        self.bar.update_traces(
            # The color of the bars
            marker_color="#0c869b",
            hoverinfo='skip',

            # Template for hovertext
            # hovertemplate = '%{hover} %{Percent:$.2f} %{label}<extra></extra>',
        )

        self.bar.update_xaxes(side='top')

        self.bar.update_layout(
            margin=dict(l=0, r=0, t=30, b=0),
            hovermode=False,
            xaxis=dict(
                title='',
                fixedrange=True
            ),
            yaxis=dict(
                title='',
                fixedrange=True
            ),
            # title_x=0.5,
            font=dict(
                family="Roboto Slab",
                size=15,
                # color="#0c869b"
            )
        )

        super().__init__(
            id=title,
            figure=self.bar,
            config={
                'displayModeBar': False,
            },
        )
