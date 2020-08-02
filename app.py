# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import re
from glob import glob

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

##################################
###       DEMOGRAPHICS         ###
##################################

for path in glob('./rp_survey_data/*.csv'):
    data = pd.read_csv(path, sep='\t')
    title = data.columns[0]
    print(title)
    print(data)

gender = pd.read_csv ("./rp_survey_data/gender.csv", sep='\t')
# convert '5%' to 5
gender['Percent'] = gender['Percent'].apply(lambda x: float(x[:-1]))
# remove the 'Total' row
gender = gender[ gender['Gender']!='Total' ]
# display a pie chart
gender_pie = px.pie(gender, values='Percent', names='Gender', title=gender.columns[0])


##################################
###         WORLD MAP          ###
##################################

# source: https://plotly.com/python/bubble-maps/

df = px.data.gapminder()
map_fig = px.scatter_geo(df, locations="iso_alpha", color="continent",
                     hover_name="country", size="pop",
                     animation_frame="year",
                     projection="natural earth")


app.layout = html.Div(children=[
    html.H1('Effective Altruism Dashboard'),

    # html.Div('''
    #     Dash: A web application framework for Python.
    # '''),

    dcc.Graph(
        id='gender_pie',
        figure=gender_pie
    ),

    dcc.Graph(
        id='map_fig',
        figure=map_fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)