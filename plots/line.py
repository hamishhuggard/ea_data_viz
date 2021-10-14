import plotly.express as px
import plotly.graph_objects as go
from dash import dcc
from dash import html

class Line(dcc.Graph):

    def __init__(
        self,
        df,
        x='x',
        y='y',
        label='label',
        title=None,
        x_title='',
        y_title='',
        size=None,
        color=None,
        hover=None,
        log_y=False,
    ):

        fig = go.Figure()
        annotations = []

        for val in df[label].unique():

            val_df = df.loc[ df[label]==val ]
            val_df.sort_values(by=x, inplace=True)

            fig.add_trace(
                go.Scatter(
                    x=val_df[x],
                    y=val_df[y],
                    name=val,
                    hovertext = df[hover],
                    hovertemplate = '%{hovertext}<extra></extra>',
                    mode='lines',
                    line=dict(
                        color="#0c869b",
                    ),
                )
            )

            if log_y:
                fig.update_layout(
                    yaxis_type="log",
                )

            fig.update_layout(
                title=title,
                showlegend=False,
            )

            val_df = val_df[ val_df['value'].notnull() ].reset_index()
            last_row = val_df.iloc[len(val_df)-1]
            last_hover = last_row['hover']

            fig.add_trace(go.Scatter(
                x=[ last_row[x] ],
                y=[ last_row[y] ],
                mode='markers',
                marker=dict(
                    color="#0c869b",
                    size=10,
                    #mode_size[i]
                ),
                hovertext = [last_hover],
                hovertemplate = '%{hovertext}<extra></extra>',
            ))

            annotations.append(dict(
                #xref='paper',
                #yref='paper',
                x=last_row['year'],
                y=last_row['value'],
                xanchor='left',
                yanchor='middle',
                text=f' {val}',
                font={
                #    'family': 'Arial',
                    'size': 13,
                },
                showarrow=False,
            ))

        fig.update_layout(

            annotations=annotations,
            #margin=dict(l=0, r=0, t=30, b=0),
            margin=dict(l=0, r=0, t=0, b=0),
            title_x=0.5,

            # autosize = True,

            # Top-left corner:

            legend = dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                title_text='',
            )

            # Below:

            # legend = {
            #       'xanchor': "center",
            #       'yanchor': "top",
            #       'y': -0.3, # play with it
            #       'x': 0.5,   # play with it
            #       'title_text': '',
            # }

        )

        super().__init__(
            figure=fig,
            responsive=True
        )

