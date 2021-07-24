# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_html_components as html
from sections.donations import content as donations
from sections.demographics import content as demographics
from sections.growth import content as growth
from sections.geography import content as geography
from sections.title import content as title
from sections.open_phil import content as open_phil
from utils.refresh_data import refresh_data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Effective Altruism Data Viewer'
server = app.server

refresh_data()

# def serve_layout():
app.layout = html.Div(
#     return html.Div(
        [
            title,
            demographics,
            geography,
            open_phil,
            donations,
            growth,
        ],
        className = 'scroll-snapper',
    )

# app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True)
