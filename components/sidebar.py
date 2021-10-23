# -*- coding: utf-8 -*-

import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

def open_phil_contents():
    return html.Li(
        [
            html.A(
                'Open Philanthropy Grants',
                href="#op-grants-scatter-section"
            ),
            html.Ul(
                [
                    html.Li(
                        html.A(
                            "Individual Grants Plot",
                            href="#op-grants-scatter-section"
                        ),
                    ),
                    html.Li(
                        html.A(
                            "Focus Area and Donee Organization",
                            href="#op-grants-categories"
                        ),
                    ),
                ]
            )
        ],
    )

def survey_contents():
    return html.Li(
        [
            html.A(
                'EA Survey Results',
                href="#countries"
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
        ],
    )

def forum_contents():
    return html.Li(
        [
            html.A(
                'EA Forum',
                href="#forum-scatter-section"
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
        ],
    )

def gwwc_contents():
    return html.Li(
        [
            html.A(
                'Giving What We Can',
                href="#gwwc-pledge-section"
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
        ],
    )

def growth_contents():
    return html.Li(
        [
            html.A(
                'EA Growth Metrics',
                href="#growth-reading"
            ),
            html.Ul(
                [
                    html.Li(
                        html.A(
                            "Reading",
                            href="#growth-reading"
                        ),
                    ),
                    html.Li(
                        html.A(
                            "Joining",
                            href="#growth-joining"
                        ),
                    ),
                    html.Li(
                        html.A(
                            "Committing",
                            href="#growth-committing"
                        ),
                    ),
                    html.Li(
                        html.A(
                            "Donating",
                            href="#growth-donating"
                        ),
                    ),
                ],
            ),
        ],
    )

def contents():
    return html.Div(
        [
            html.H2('Contents'),
            html.Ul(
                [
                    html.Li(
                        html.A(
                            "Donations Overview",
                            href="#donations-sankey"
                        ),
                    ),
                    open_phil_contents(),
                    gwwc_contents(),
                    survey_contents(),
                    forum_contents(),
                    growth_contents(),
                ]
            ),
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
