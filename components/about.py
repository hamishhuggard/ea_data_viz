# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html

def about_box():
    return html.Div(
        [
            html.H4("About"),
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
        id = 'about-box',
        className = 'hidden',
    )
