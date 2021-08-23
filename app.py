# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_html_components as html
from sections.donations import content as donations
from sections.demographics import Demographics
from sections.growth import Growth
from sections.geography import Geography
from sections.title import content as title
# from sections.open_phil import content as open_phil
from utils.refresh_data import refresh_data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Effective Altruism Data Viewer'
server = app.server

# refresh_data()

# def serve_layout():
app.layout = html.Div(
#     return html.Div(
        [
            title,
            Demographics(),
            Geography(),
            # open_phil,
            donations,
            Growth(),
        ],
        className = 'scroll-snapper',
    )

# app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=False)
