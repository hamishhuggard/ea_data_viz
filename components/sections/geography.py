from dash import dcc
from dash import html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from plots.bar import Bar
from countryinfo import CountryInfo
from math import log
from utils.subtitle import get_subtitle

##################################
###         WORLD MAP          ###
##################################

# source: https://plotly.com/python/bubble-maps/

country = CountryInfo()
country_list = country.all().keys()

countries = pd.read_csv('./data/rp_survey_data_2019/country2.csv')

countries['Responses'] = countries['Responses'].astype('int')

countries.loc[countries['Country']=='United States of America', 'Country'] = 'United States'

MINIMUM_CIRCLE_SIZE = 0 # 20
countries['circle size'] = countries['Responses'] + MINIMUM_CIRCLE_SIZE

countries = countries.sort_values('Responses', ascending=True)

def get_population(country):
    try:
        return CountryInfo(country).population()
    except:
        return 1e9

countries['population'] = countries['Country'].apply(get_population)
countries['Density (per million)'] = countries['Responses'] / countries['population'] * 1e6
countries['Density (per million)'] = countries['Density (per million)'].apply(lambda x: round(x, 2))
countries['log density'] = countries['Density (per million)'].apply(lambda x: 1 + log(x+1))
MINIMUM_CIRCLE_SIZE = 15
countries['circle size'] = countries['Responses'] + MINIMUM_CIRCLE_SIZE

def hover(row):
    country = row['Country']
    responses = row['Responses']
    density = row['Density (per million)']
    return f'<b>{country}</b><br>{responses:,.0f} survey responses<br>{density:.2f} per million people'
countries['hover'] = countries.apply(hover, axis=1)

countries_for_map = countries.copy()
countries_for_map.loc[len(countries_for_map), ['Country', 'Responses', 'Density (per million)', 'log density']] = ('Antarctica', 0, 0, 0)

countries_for_map['hover'] = countries_for_map.apply(hover, axis=1)

# Population map

pop_map = px.scatter_geo(
    countries,
    locations="Country",
    hover_name="Country",
    locationmode='country names',
    size="circle size",
    title="Number of EAs by Country",
    hover_data = {
        'circle size': False,
        'Responses': True,
        'Country': False,
        'log density': False,
        'Density (per million)': True,
    },
    projection="equirectangular", # 'orthographic' is fun
)

pop_map.update_layout(
    margin=dict(l=0, r=0, t=80, b=0),
    title_x=0.5,
)

pop_map.update_traces(
    marker = dict(
        color ="#36859A",
    ),
    hovertext = countries['hover'],
    hovertemplate = '%{hovertext}<extra></extra>',
)

pop_map.update_geos(
    showcoastlines=False,
    landcolor="#dfe3ee",
)

# Density map

density_map = px.choropleth(
    countries_for_map,
    locations="Country",
    hover_name="Country",
    locationmode='country names',
    color='log density',
    title="EAs Per Capita (Darker/Greener is Higher)",
    color_continuous_scale=["#dfe3ee", "#007a8f"],
    hover_data = {
        'circle size': False,
        'Responses': True,
        'Country': False,
        'log density': False,
        'Density (per million)': True,
    },
    projection="equirectangular", # 'orthographic' is fun. "natural earth" is quite nice
)

density_map.update_layout(
    margin=dict(l=0, r=0, t=80, b=0),
    coloraxis_showscale=False,
    title_x=0.5,
)

density_map.update_traces(
    hovertext = countries_for_map['hover'],
    hovertemplate = '%{hovertext}<extra></extra>',
    marker_line_width=0,
)

density_map.update_geos(
    showcoastlines=False,
    landcolor="#dfe3ee",
)

countries['x'] = countries['Country']
countries['text'] = countries['Responses'].apply(lambda x: f'{x:}')
countries['y'] = countries['Responses']
countries_truncated = countries.iloc[len(countries)*2//3:]

countries_bar = Bar(
    countries_truncated,
    title = f'Countries with Most EAs',
)

countries_capita_sort = countries.sort_values(by='Density (per million)')
countries_capita_sort['x'] = countries_capita_sort['Country']
countries_capita_sort['y'] = countries_capita_sort['Density (per million)']
countries_capita_sort['text'] = countries_capita_sort['Density (per million)'].apply(lambda x: f'{x:.1f}')
countries_capita_sort_truncated = countries_capita_sort.iloc[len(countries)*2//3:]

per_capita_bar = Bar(
    countries_capita_sort_truncated,
    title = f'Top EAs per Capita (×1M)',
)

def country_total_section():
    return html.Div(
        [
            html.Div(
                html.H2('EAs by Country'),
                className='section-heading',
            ),
            get_subtitle('rethink19-geo', hover='countries or bars', extra_text='Scroll to zoom on map.'),
            html.Div(
                html.Div(
                    [
                        html.Div(
                            dcc.Graph(
                                id='pop_map',
                                figure=pop_map,
                                responsive=True,
                            ),
                            className='plot-container'
                        ),
                        html.Div(
                            countries_bar,
                            className='plot-container',
                        ),
                    ],
                    className='grid desk-cols-2-1',
                ),
                className='section-body',
            ),
        ],
        className = 'section',
        id='countries',
    )

def country_per_capita_section():
    return html.Div(
        [
            html.Div(
                html.H2('EAs per Capita by Country'),
                className='section-heading',
            ),
            get_subtitle('rethink19-geo', hover='countries or bars', extra_text='Scroll to zoom on map.'),
            html.Div(
                html.Div(
                    [
                        html.Div(
                            dcc.Graph(
                                id='density_map',
                                figure=density_map,
                                responsive=True,
                            ),
                            className='plot-container'
                        ),
                        html.Div(
                            per_capita_bar,
                            className='plot-container'
                        ),
                    ],
                    className='grid desk-cols-2-1',
                ),
                className='section-body',
            ),
        ],
        className = 'section',
        id='countries-per-capita',
    )
