import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from ea_bar_graph import EABarGraph
from countryinfo import CountryInfo

##################################
###         WORLD MAP          ###
##################################

# source: https://plotly.com/python/bubble-maps/

countries = pd.read_csv('./data/rp_survey_data/country2.csv')
countries['Responses'] = countries['Responses'].astype('int')
countries.loc[countries['Country']=='United States of America', 'Country'] = 'United States'
MINIMUM_CIRCLE_SIZE = 20
countries['circle size'] = countries['Responses'] + MINIMUM_CIRCLE_SIZE
countries = countries.sort_values('Responses', ascending=True)

countries['population'] = countries['Country'].apply(lambda country: CountryInfo(country).population())
countries['Density (per million)'] = countries['Responses'] / countries['population'] * 1e6
# print(countries['density'])

# https://plotly.com/python-api-reference/generated/plotly.express.scatter_geo.html
map_fig = px.choropleth(
    countries,
    locations="Country",
    #color="continent",
    hover_name="Country",
    # hover_data=['Country', 'Responses'],
    locationmode='country names',
    # size="Responses",
    # size="circle size",
    color='Density (per million)',
    # color_continuous_scale=px.colors.sequential.Plasma,
    hover_data = {
        'circle size': False,
        'Responses': True,
        'Country': False,
    },
    projection="equirectangular", # 'orthographic' is fun
    # height=250,
    # config={
    #     'displayModeBar': False,
    # },
)
map_fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    coloraxis_showscale=False,
)
# map_fig.update_traces(
#     marker = dict(
#         color ="#36859A",
#     ),
# )
map_fig.update_geos(
    # resolution=50,
    showcoastlines=False, 
    # coastlinecolor="RebeccaPurple",
    # showland=True, 
    landcolor="#B8C8D3",
    # showocean=False,#True, oceancolor="LightBlue",
    # showlakes=True, lakecolor="Blue",
    # showrivers=True, rivercolor="Blue"
)

countries['x'] = countries['Country'] + countries['Responses'].apply(lambda x: f'{x:>5}')
countries['y'] = countries['Responses']

countries_bar = EABarGraph(
    countries,
    height = 20*len(countries),
    title = 'Number of EAs'
)

countries_capita_sort = countries.sort_values(by='Density (per million)')
countries_capita_sort['x'] = countries_capita_sort['Country'] + countries_capita_sort['Density (per million)'].apply(lambda x: f'{x:>5.1f}')
countries_capita_sort['y'] = countries_capita_sort['Density (per million)']

per_capita_bar = EABarGraph(
    countries_capita_sort,
    height = 20*len(countries),
    title = 'EAs per Million Capitas'
)

# countries_bar = px.bar(
#      countries,
#      y = 'Country',
#      x = 'Responses',
#      orientation = 'h',
#      height = 20 * len(countries),
# #     title = 'no title',
# )
# countries_bar.update_layout(
#     margin=dict(l=0, r=0, t=0, b=0),
#     xaxis=dict(title=''),
#     yaxis=dict(title=''),
#     font=dict(
#         # family="Courier New, monospace",
#         # size=8,
#         # color="RebeccaPurple"
#     )
# )

geo_div = html.Div(
    [
        html.Div(
            html.H2('Countries'),
            className='section-heading',
            style={'height': '20%'},
        ),
        html.Div([
            html.Div(
                    dcc.Graph(
                        id='map_fig',
                        figure=map_fig
                    ),
                    style={
                        'width': '60%',
#                        'background-color': 'red'
                    },
#                    className='floaty-boi'
                    className='demo-column'
            ),
            html.Div(
               countries_bar,
               style={
                   'width': '20%',
                   'height': '425px',
#                   'background-color': 'blue',
                   'overflow-y': 'scroll',
               },
#               className='floaty-boi'
               className='demo-column'
            ),
            html.Div(
               per_capita_bar,
               style={
                   'width': '20%',
                   'height': '425px',
                   'background-color': 'blue',
                   'overflow-y': 'scroll',
               },
#               className='floaty-boi'
               className='demo-column'
            ),
        ], style={'height': '80%'}),
    ],
    style = {'overflow': 'auto'}
    #className='big-box'
#    style = {
#        'height': '100vh',
#        'background-color': 'yellow'
#    }
)
