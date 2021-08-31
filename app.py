# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_html_components as html

from sections.title import title_section

from sections.donations_sankey import donations_sankey_section

from sections.demographics import demographics_section
from sections.demographics import beliefs_section
from sections.demographics import education_section
from sections.demographics import career_section

from sections.growth import growth1
from sections.growth import growth2
from sections.growth import growth3
from sections.growth import growth4

from sections.geography import country_total_section
from sections.geography import country_per_capita_section

from sections.open_phil import openphil_grants_scatter_section
from sections.open_phil import openphil_grants_categories_section

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
            title_section(),

            donations_sankey_section(),

            openphil_grants_scatter_section(),
            openphil_grants_categories_section(),

            country_total_section(),
            country_per_capita_section(),

            demographics_section(),
            beliefs_section(),
            education_section(),
            career_section(),

            growth1(),
            growth2(),
            growth3(),
            growth4(),

        ],
        className = 'scroll-snapper',
    )

# app.layout = serve_layout

if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server(debug=False)
