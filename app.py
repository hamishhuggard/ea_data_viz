# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_html_components as html
from sections.donations import Donations
from sections.demographics import Demographics
# from sections.growth import Growth
from sections.geography import Geography
from sections.title import Title
from sections.open_phil import OpenPhil
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
app.layout = html.Div(
#     return html.Div(
        [
            Title(),
            # OpenPhil(),
            Demographics(),
            Geography(),
            Donations(),
            Growth(),
        ],
        className = 'scroll-snapper',
    )

# app.layout = serve_layout

if __name__ == '__main__':
    # app.run_server(debug=True)
    app.run_server(debug=False)
