# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_html_components as html
from sections.donations import donations_section
from sections.demographics import demographics_section
from sections.demographics import beliefs_section
from sections.demographics import education_section
from sections.demographics import career_section
# from sections.growth import Growth
# from sections.geography import Geography
from sections.title import Title
from sections.open_phil import openphil_section
from utils.refresh_data import refresh_data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags = [
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1.0',
        }
    ],
)
app.title = 'Effective Altruism Data Viewer'
server = app.server

# refresh_data()

# def serve_layout():
#     return html.Div(
app.layout = html.Div(
        [
            Title(),

            demographics_section(),
            beliefs_section(),
            education_section(),
            career_section(),

            openphil_section(),

            donations_section(),

            # Geography(),
            # Growth(),
        ],
        className = 'scroll-snapper',
    )

# app.layout = serve_layout

if __name__ == '__main__':
    # app.run_server(debug=True)
    app.run_server(debug=False)
