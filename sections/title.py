# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

lightbulb_img_url = 'https://effectivealtruism.nz/wp-content/uploads/2018/02/lightbulblogo-1.png'

heading = html.Div(
    [
        html.Img(
            src = lightbulb_img_url,
            height = 60,
            style = {
                'grid-column': '1',
            }
        ),
        html.H1(
            [
                html.Span(
                    'Effective ',
                    className = 'effective',
                ),
                html.Span(
                    'Altruism ',
                    className = 'altruism',
                ),
                html.Span(
                    'Data Visualizer',
                ),
            ],
            style = {
                'grid-column': '2',
            }
        )
    ],
    style = {
        'display': 'grid',
    }
)


class Title(html.Div):
    def __init__(self):
        super(Title, self).__init__(
            html.Div([
                heading,
                html.P([
                    'This website visualises some data relating to ',
                    dcc.Link(
                        "effective altruism",
                        href="https://www.effectivealtruism.org/"
                    ),
                    "."
                ]),
                html.P(
                    'Feedback welcome at hamish.huggard@gmail.com.'
                ),
            ]),
            className='section center title',
        )
