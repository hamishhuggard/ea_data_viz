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

# https://plotly.com/python-api-reference/generated/plotly.express.scatter_geo.html
map_fig = px.scatter_geo(countries, 
                     locations="Country", #color="continent",
                     hover_name="Country",
                     # hover_data=['Country', 'Responses'],
                     locationmode='country names',
                     size="Responses",
                     #marker = dict(
            #color ="#36859A",
        #),
                     projection="equirectangular", # 'orthographic' is fun
                     height=150,
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

geo_div = html.Div(
    [
        dcc.Graph(
            id='map_fig',
            figure=map_fig
        ),
    ],
    style = {
        'height': '100vh',
    }
)
