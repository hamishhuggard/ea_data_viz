# -*- coding: utf-8 -*-

import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

def intro_contents():
    return [
        html.P(
            'Overview',
        ),
        html.Ul(
            [
                html.A(
                    "All Donations",
                    href="#donations-sankey"
                ),
            ]
        )
    ]

def open_phil_contents():
    return [
        html.P(
            'Open Philanthropy Grants',
        ),
        html.Ul(
            [
                html.Li(
                    html.A(
                        "Individual Grants Plot",
                        href="#op-grants-scatter-section",
                    ),
                ),
                html.Li(
                    html.A(
                        "Focus Area and Donee Organization",
                        href="#op-grants-categories",
                    ),
                ),
                html.Li(
                    html.A(
                        "Changes over Time",
                        href="#op-grants-growth",
                    ),
                ),
            ]
        )
    ]

def survey_contents():
    return [
        html.P(
            'EA Survey Results',
        ),
        html.Ul(
            [
                html.Li(
                    html.A(
                        "Countries (total)",
                        href="#countries"
                    ),
                ),
                html.Li(
                    html.A(
                        "Countries (per Capita)",
                        href="#countries-per-capita"
                    ),
                ),
                html.Li(
                    html.A(
                        "Demographics",
                        href="#demographics"
                    ),
                ),
                html.Li(
                    html.A(
                        "Beliefs and Lifestyle",
                        href="#beliefs-lifestyle"
                    ),
                ),
                html.Li(
                    html.A(
                        "Education",
                        href="#education"
                    ),
                ),
                html.Li(
                    html.A(
                        "Careers",
                        href="#careers"
                    ),
                ),
            ],
        ),
    ]

def forum_contents():
    return [
        html.P(
            'EA Forum',
        ),
        html.Ul(
            [
                html.Li(
                    html.A(
                        "Posted Date vs Karma",
                        href="#forum-scatter-section"
                    ),
                ),
                html.Li(
                    html.A(
                        "Forum Growth",
                        href="#forum-growth-section"
                    ),
                ),
                html.Li(
                    html.A(
                        "Post Distributions",
                        href="#post-wilkinson-section"
                    ),
                ),
                html.Li(
                    html.A(
                        "Author Distributions",
                        href="#author-wilkinson-section"
                    ),
                ),
            ],
        ),
    ]

def gwwc_contents():
    return [
        html.P(
            'Giving What We Can',
        ),
        html.Ul(
            [
                html.Li(
                    html.A(
                        "Pledges",
                        href="#gwwc-pledge-section",
                    ),
                ),
                html.Li(
                    html.A(
                        "Donations",
                        href="#gwwc-donations-section",
                    ),
                ),
                html.Li(
                    html.A(
                        "Donation Organizations",
                        href="#gwwc-orgs-section",
                    ),
                ),
            ],
        ),
    ]

def contents():
    return html.Div(
        [
            html.H2('Contents'),
            *intro_contents(),
            *open_phil_contents(),
            *gwwc_contents(),
            *survey_contents(),
            *forum_contents(),
        ],
        className = 'section_list',
    )

def sidebar():
    return html.Div(
        [
            html.Div(
                contents(),
                id='sidebar',
            ),
            html.Div(
                id='sidebar-buttress',
            ),
        ]
    )
