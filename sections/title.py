# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

lightbulb_img_url = 'https://effectivealtruism.nz/wp-content/uploads/2018/02/lightbulblogo-1.png'
lightbulb_img = html.Img(
    src = lightbulb_img_url,
    height = 60,
    style = {
        'float': 'center',
    }
)

title = html.H1(
    [
        html.Span(
            'Effective ',
            style = {
                'font-family': 'Roboto Slab',
                'font-weight': '700',
            }
        ),
        html.Span(
            'Altruism',
            style = {
                'font-family': 'Roboto Slab',
                'font-weight': '400',
            }
        )
    ],
    style = {
        'float': 'center',
    }
)

subtitle = html.H3(
    'Data Visualizer',
    style = {
        'font-family': 'Raleway',
    }
)

content = html.Div(
    [
        # lightbulb_img,
        html.Div(
            style = {
                'height': '35vh',
            }
        ),
        html.Div(
            [
                # html.Div('.', style={'width': '35%', 'float': 'left', 'font-color': 'white'}),
                lightbulb_img,
                title,
                # html.Div(style={'width': '40%'}),
            ],
            style = {
                # 'height': '10vh',
                # 'width': '40%',
                # 'float': 'center',
                # 'margin': '0 auto',
                # 'margin-right': 'auto',
                # 'margin-lrft': 'auto',
            }
        ),

          html.Div(
            [
            subtitle,
                html.Div(
                    [
                        html.P(
                            'Effective altruism is about answering one simple question: how can we use our resources to help others the most?'
                        ),
                        html.P([
                            'Learn more at ',
                            dcc.Link(
                                "effectivaltruism.org",
                                href="https://www.effectivealtruism.org/"
                            ),
                            "."
                        ]),
                        html.P(
                            'This website visualises some data relating to effective altruism.'
                        )
                    ],
                    style = {
                      'font-family': 'Raleway',
                    }
                ),
            ],
            # style = {
            #   'margin': '0',
            #   'position': 'absolute',
            #   'top': '45%',
            #   'left': '50%',
            #   '-ms-transform': 'translate(-50%, -50%)',
            #   'transform': 'translate(-50%, -50%)',
            # }
          )
    ],
    className='section',
    style = {
        'vertical-align': 'center',
        'text-align': 'center',
    }
)
