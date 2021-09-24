# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

def heading():

    lightbulb_img_url = '/assets/logo.png'

    return html.H1(
        [
            html.Img(
                src = lightbulb_img_url,
                className='lightbulb',
            ),
            html.Div(
                [
                    html.Span(
                        'Effective',
                        className = 'effective',
                    ),
                    html.Span(
                        'Altruism',
                        className = 'altruism',
                    ),
                ],
                className='effective-altruism',
            ),
            html.Div(
                [
                    html.Span(
                        'Data',
                        className = 'data',
                    ),
                    html.Span(
                        '.com',
                        className = 'dot-com',
                    ),
                ],
                className='data-dot-com',
            ),
        ],
        className='ea-data-dot-com center',
    )

def contents():
    return html.Ul(
        [
            html.P('Contents:'),
            html.Li(
                [
                    html.A(
                        "Donations Overview",
                        href="#donations-sankey"
                    ),
                ],
            ),
            html.Li(
                [
                    'Open Philanthropy grants: ',
                    html.A(
                        "Individual Grants Plot",
                        href="#op-grants-scatter-section"
                    ),
                    ', ',
                    html.A(
                        "Focus Area and Donee Organization",
                        href="#op-grants-categories"
                    ),
                ],
            ),
            html.Li(
                [
                    'Rethink Priorities survey results: ',
                    html.A(
                        "Countries (total)",
                        href="#countries"
                    ),
                    ', ',
                    html.A(
                        "Countries (per Capita)",
                        href="#countries"
                    ),
                ],
            ),
            html.Li(
                [
                    'Rethink Priorities survey results: ',
                    html.A(
                        "Demographics",
                        href="#demographics"
                    ),
                    ', ',
                    html.A(
                        "Beliefs and Lifestyle",
                        href="#beliefs-lifestyle"
                    ),
                    ', ',
                    html.A(
                        "Education",
                        href="#education"
                    ),
                    ', ',
                    html.A(
                        "Careers",
                        href="#careers"
                    ),
                ],
            ),
            html.Li(
                [
                    'EA Growth Metrics: ',
                    html.A(
                        "Reading",
                        href="#growth-reading"
                    ),
                    ', ',
                    html.A(
                        "Joining",
                        href="#growth-joining"
                    ),
                    ', ',
                    html.A(
                        "Committing",
                        href="#growth-committing"
                    ),
                    ', ',
                    html.A(
                        "Donating",
                        href="#growth-donating"
                    ),
                    ', ',
                ],
            ),
        ]
    )

def title_section():
    return html.Div(
        html.Div(
            [
                html.Div([
                    heading(),
                    html.Div(
                        [
                            html.P(
                                [
                                    dcc.Link(
                                        "Effective Altruism",
                                        href="https://www.effectivealtruism.org/"
                                    ),
                                    ' (EA) is a movement that uses reason and evidence to do the most good.',
                                ]
                            ),
                            html.P(
                                'There are several EA organisations which collect data on grants, donors, and pledges.',
                            ),
                            html.P(
                                'This website aggregates and visualizes that data.',
                            ),
                            contents(),
                            html.P(
                                [
                                    'Source code is available on ',
                                    dcc.Link(
                                        "Github",
                                        href="https://github.com/hamishhuggard/ea_data_viz"
                                    ),
                                    '.',
                                ]
                            ),
                            html.P(
                                [
                                    'Please send feedback to ',
                                    dcc.Link(
                                        "hamish.huggard@gmail.com",
                                        href="mailto:hamish.huggard@gmail.com"
                                    ),
                                    '.',
                                ],
                            ),
                        ],
                        style={
                            'text-align': 'left',
                        },
                    ),
                    html.H3(
                        '⬇️  Scroll down. ⬇️ '
                    ),
                ]),
            ],
            className='section-body center',
        ),
        className='section',
    )
