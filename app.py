# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_html_components as html

from components.header import header
from components.sidebar import sidebar
from components.about import about_box
from components.body import body

from utils.refresh_data import refresh_data

app = dash.Dash(
    __name__,
    meta_tags = [
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1.0',
        }
    ],
)
app.title = 'Effective Altruism Data'
server = app.server

# refresh_data()

# def serve_layout():
#     return html.Div(
app.layout = html.Div(
        [
            header(),
            html.Div(
                [
                    sidebar(),
                    about_box(),
                    body(),
                ],
                className = 'body',
            )
        ],
    )

# app.layout = serve_layout

if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server(debug=False)
