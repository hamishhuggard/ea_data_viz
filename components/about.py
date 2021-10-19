# -*- coding: utf-8 -*-

import dash
from dash import dcc
from dash import html

def about_box():
    return html.Div(
        [
            html.H4("About"),
            html.P(
                [
                    html.A(
                        "Effective Altruism",
                        href="https://www.effectivealtruism.org/"
                    ),
                    ' (EA) is a movement that uses reason and evidence to do the most good.',
                ]
            ),
            html.P(
                'This website aggregates and visualizes data from EA organisations, including grants, donors, and pledges.',
            ),
            html.P(
                [
                    'More information on this website can be found ',
                    html.A(
                        "here",
                        href="https://forum.effectivealtruism.org/posts/CQaNyJfsRFZhseiLZ/effectivealtruismdata-com-a-website-for-aggregating-and"
                    ),
                    '.',
                ]
            ),
            html.P(
                [
                    'Source code is available on ',
                    html.A(
                        "GitHub",
                        href="https://github.com/hamishhuggard/ea_data_viz"
                    ),
                    '.',
                ]
            ),
            html.P(
                [
                    'Please send feedback to ',
                    html.A(
                        "hamish.huggard@gmail.com",
                        href="mailto:hamish.huggard@gmail.com"
                    ),
                    '.',
                ],
            ),
        ],
        id = 'about-box',
        className = 'hidden',
    )
