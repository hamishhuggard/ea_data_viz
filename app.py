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

demo_pies = []
for table_name in [
        'age_group', 'diet', 'gender', 'employment', 'ethnicity', 'subject',
        ]:

    path = f"./rp_survey_data/{table_name}.csv"
    demo_table = pd.read_csv(path, sep='\t')
    title = demo_table.columns[0]

    # remove the 'Total' row
    demo_table = demo_table[ ~demo_table[title].isin(['Total', 'Total respondents']) ]
    demo_table['label'] = demo_table[title] + demo_table['Percent']
    # convert '5%' to 5
    demo_table['Percent'] = demo_table['Percent'].apply(lambda x: float(x[:-1]))


    pie_fig = px.pie(demo_table, values='Percent', names=title, title=title)#, hovertext='label')
    # pie_fig.update_trace(hovertemplate=)
    pie_fig.update_traces(hoverinfo='none', textinfo='none')
    pie_fig.update(layout_showlegend=False)
    this_pie = dcc.Graph(
        id=title,
        figure=pie_fig
    )

    demo_pies.append(this_pie)

##################################
###         WORLD MAP          ###
##################################

# source: https://plotly.com/python/bubble-maps/

countries = pd.read_csv('./rp_survey_data/country.csv')
countries = countries[
    ~countries['Country'].isin(['All other stated countries', 'Total respondents'])
]
# df = px.data.gapminder()
# print(df)
map_fig = px.scatter_geo(countries, locations="Country", #color="continent",
                     hover_name="Country", 
                     size="Responses",
                     # animation_frame="year",
                     projection="natural earth"
)


app.layout = html.Div(children=[
    html.H1('Effective Altruism Dashboard'),

    # html.Div('''
    #     Dash: A web application framework for Python.
    # '''),

    dcc.Graph(
        id='map_fig',
        figure=map_fig
    ),

    html.Div(demo_pies, style={'columnCount': 2, 'width': '49%', 'display': 'inline-block'})

    html.Div(map_fig, style={'width': '75%', 'display': 'inline-block'})

])

if __name__ == '__main__':
    app.run_server(debug=True)