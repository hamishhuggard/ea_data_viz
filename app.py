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

demo_pies = []
for table_name in [
        'age_group', 'diet', 'gender', 'education', 'employment', 'ethnicity', 
        'religion', 'subject', 'work_experience'
        ]:

    path = f"./rp_survey_data/{table_name}.csv"
    demo_table = pd.read_csv(path, sep='\t')
    title = demo_table.columns[0]

    # remove the 'Total' row
    demo_table = demo_table[ ~demo_table[title].isin(['Total', 'Total respondents']) ]
    # convert '5%' to 5
    demo_table['Percent'] = demo_table['Percent'].apply(lambda x: float(x[:-1]))
    
    this_pie = dcc.Graph(
        id=title,
        figure=px.pie(demo_table, values='Percent', names=title, title=title)
    )

    demo_pies.append(this_pie)

# #### AGE PIE CHART ####
# age = pd.read_csv ("./rp_survey_data/age_group.csv", sep='\t')
# # remove the 'Total' row
# age = age[ age['Age Group']!='Total' ]
# # convert '5%' to 5
# age['Percent'] = age['Percent'].apply(lambda x: float(x[:-1]))
# # display a pie chart
# age_pie = px.pie(age, values='Percent', names='Age Group', title=age.columns[0])

# #### DIET PIE CHART ####
# diet = pd.read_csv ("./rp_survey_data/age_group.csv", sep='\t')
# # remove the 'Total' row
# age = age[ age['Age Group']!='Total' ]
# # convert '5%' to 5
# age['Percent'] = age['Percent'].apply(lambda x: float(x[:-1]))
# # display a pie chart
# age_pie = px.pie(age, values='Percent', names='Age Group', title=age.columns[0])


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
] + demo_pies)

if __name__ == '__main__':
    app.run_server(debug=True)