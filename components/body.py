# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import html

from sections.forum import forum_scatter_section
from sections.forum import forum_leaderboard_section

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

def body():
    return html.Div(
        [


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

            forum_scatter_section(),

        ],
        className = 'content scroll-snapper',
    )
