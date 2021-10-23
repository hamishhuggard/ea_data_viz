# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import html

from components.sections.forum import forum_scatter_section
from components.sections.forum import forum_count_section
from components.sections.forum import forum_post_wilkinson_section
from components.sections.forum import forum_user_wilkinson_section

from components.sections.donations_sankey import donations_sankey_section

from components.sections.demographics import demographics_section
from components.sections.demographics import beliefs_section
from components.sections.demographics import education_section
from components.sections.demographics import career_section

from components.sections.gwwc_donation_growth import get_gwwc_donation_growth_section
from components.sections.gwwc_pledges import get_gwwc_pledges_section
from components.sections.gwwc_donation_orgs import get_gwwc_donations_orgs_section

from components.sections.growth import growth1
from components.sections.growth import growth2
from components.sections.growth import growth3
from components.sections.growth import growth4

from components.sections.geography import country_total_section
from components.sections.geography import country_per_capita_section

from components.sections.open_phil import openphil_grants_scatter_section
from components.sections.open_phil import openphil_grants_categories_section

def body():
    return html.Div(
        [

            donations_sankey_section(),

            openphil_grants_scatter_section(),
            openphil_grants_categories_section(),

            get_gwwc_pledges_section(),
            get_gwwc_donation_growth_section(),
            get_gwwc_donations_orgs_section(),

            country_total_section(),
            country_per_capita_section(),

            demographics_section(),
            beliefs_section(),
            education_section(),
            career_section(),

            forum_scatter_section(),
            forum_count_section(),
            forum_post_wilkinson_section(),
            forum_user_wilkinson_section(),

        ],
        className = 'content scroll-snapper',
    )
