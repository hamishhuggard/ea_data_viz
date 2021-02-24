import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

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

# https://plotly.com/python-api-reference/generated/plotly.express.scatter_geo.html
map_fig = px.scatter_geo(countries,
    locations="Country",
    #color="continent",
    hover_name="Country",
    # hover_data=['Country', 'Responses'],
    locationmode='country names',
    # size="Responses",
    size="circle size",
    #marker = dict(
    #    color ="#36859A",
    #),
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
)
map_fig.update_geos(
    # resolution=50,
    showcoastlines=False, 
    # coastlinecolor="RebeccaPurple",
    # showland=True, 
    landcolor="#B8C8D3",
    #color="#36859A",
    # showocean=False,#True, oceancolor="LightBlue",
    # showlakes=True, lakecolor="Blue",
    # showrivers=True, rivercolor="Blue"
)

countries_bar = px.bar(
     countries,
     y = 'Country',
     x = 'Responses',
     orientation = 'h',
     height = 20 * len(countries),
#     title = 'no title',
)
countries_bar.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    xaxis=dict(title=''),
    yaxis=dict(title=''),
    font=dict(
        # family="Courier New, monospace",
        # size=8,
        # color="RebeccaPurple"
    )
)

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
                        'width': '75%',
#                        'background-color': 'red'
                    },
                    className='floaty-boi'
            ),
            html.Div(
               dcc.Graph(
                    id='geo_bar',
                    figure=countries_bar,
                    config={'displayModeBar': False}
               ),
               style={
                   'width': '20%',
                   'height': '425px',
#                   'background-color': 'blue',
                   'overflow-y': 'scroll',
               },
               className='floaty-boi'
            )
        ], style={'height': '80%'}),
    ],
    style = {'overflow': 'auto'}
    #className='big-box'
#    style = {
#        'height': '100vh',
#        'background-color': 'yellow'
#    }
)
