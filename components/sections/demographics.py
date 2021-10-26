import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import re
from glob import glob
from utils.plots.bar import Bar
from utils.subtitle import get_data_source
from utils.subtitle import get_instructions

def get_demo_table(demo_name):

    path = f"./assets/data/rp_survey_data_2019/{demo_name}.csv"
    demo_table = pd.read_csv(path, sep='\t')
    title = demo_table.columns[0]

    # remove the 'Total' row
    demo_table = demo_table[ ~demo_table[title].isin(['Total', 'Total respondents']) ]
    # convert '5%' to 5
    demo_table['Percent'] = demo_table['Percent'].apply(lambda x: float(x[:-1]))


    # Substitute the long labels for something shorter
    subs = {
        'Eat meat, but try to reduce the amount  ': 'Reducetarian',
        'Other (please specify)': 'Other',

        'Native Hawaiian or Other Pacific Islander': 'Hawaiian or Pacific Islander',
        'American Indian or Alaskan Native': 'Native American/Alaskan',
        'Hispanic, Latino or Spanish Origin': 'Hispanic or Latino',

        'Professional or vocational qualification': 'Professional or Vocational',

        'Not employed, but looking for work': 'Not employed, looking for work',
        'Not employed, but not looking for work': 'Not employed, not looking for work',

        'Work at a non-profit (not an EA organization)': 'Non-profit (not EA org)',
        'Work at a non-profit (EA organization)': 'Non-profit (EA org)',


        'Consequentialism (utilitarian)': 'Utilitarianism',
        'Consequentualism (other than utilitarian)': 'Other Consequentialism',
    }
    demo_table['label_original'] = demo_table[title]
    demo_table['label'] = demo_table[title].map(subs).fillna(demo_table[title])

    demo_table = demo_table.iloc[::-1]
    if title == 'Moral View':
        demo_table = demo_table.loc[[ 4, 2, 3, 1, 0, ], :]
    elif title == 'Race/Ethnicity':
        # Move "other" to the bottom
        inds = list(range(6, -1, -1))
        inds.insert(0, inds.pop(3))
        demo_table = demo_table.loc[inds, :]
    elif title == 'Education':
        # Move "other" to the bottom
        inds = list(range(4, -1, -1))
        inds.insert(0, inds.pop(4))
        demo_table = demo_table.loc[inds, :]
    elif title == 'Diet ':
        # Move "other" to the bottom
        inds = list(range(6))
        inds.insert(0, inds.pop(4))
        demo_table = demo_table.loc[inds, :]

    demo_table['x'] = demo_table['label']
    demo_table['y'] = demo_table['Percent']
    demo_table['text'] = demo_table['Percent'].apply(lambda x: f'{x:.1f}%')

    def hover(row):
        label = row['label_original']
        responses = row['Responses']
        percent = row['Percent']
        return f'<b>{label}</b><br>{responses} responses ({percent}%)'

    demo_table['hover'] = demo_table.apply(hover, axis=1)

    return demo_table

def get_bar_chart(demo_name):
    demo_table = get_demo_table(demo_name)
    title = demo_table.columns[0]
    return Bar(demo_table, title=title)


def demographics_section():
    return html.Div(
        [
            html.Div(
                html.H2('EA Demographics'),
                className='section-title',
            ),
            get_instructions(),
            html.Div(
                [
                    html.Div(
                        get_bar_chart('gender'),
                        className='plot-container'
                    ),
                    html.Div(
                        get_bar_chart('age_group'),
                        className='plot-container'
                    ),
                    html.Div(
                        get_bar_chart('ethnicity'),
                        className='plot-container tab-span-2-cols'
                    ),
                ],
                className = 'grid tab-cols-2 desk-cols-3 section-body',
            ),
            get_data_source('rethink19'),
        ],
        className = 'section',
        id='demographics',
    )


def beliefs_section():
    return html.Div(
        [
            html.Div(
                html.H2('EA Beliefs and Lifestyle'),
                className='section-title',
            ),
            get_instructions(),
            html.Div(
                [
                    html.Div(
                        get_bar_chart('political_belief'),
                        className='plot-container'
                    ),
                    html.Div(
                        get_bar_chart('diet'),
                        className='plot-container'
                    ),
                    html.Div(
                        get_bar_chart('moral_view'),
                        className='plot-container tab-span-2-cols'
                    ),
                ],
                className = 'grid tab-cols-2 desk-cols-3 section-body',
            ),
            get_data_source('rethink19'),
        ],
        className = 'section',
        id='beliefs-lifestyle',
    )

def education_section():
    return html.Div(
        [
            html.Div(
                html.H2('EA Education'),
                className='section-title',
            ),
            get_instructions(),
            html.Div(
                [
                    html.Div(
                        get_bar_chart('education2'),
                        className='plot-container'
                    ),
                    html.Div(
                        get_bar_chart('subject'),
                        className='plot-container'
                    ),
                ],
                className = 'grid tab-cols-2 desk-cols-2 section-body',
            ),
            get_data_source('rethink19'),
        ],
        className = 'section',
        id='education',
    )

def career_section():
    return html.Div(
        [
            html.Div(
                html.H2('EA Careers'),
                className='section-title',
            ),
            get_instructions(),
            html.Div(
                [
                    html.Div(
                        get_bar_chart('career_path'),
                        className='plot-container'
                    ),
                    html.Div(
                        get_bar_chart('employment'),
                        className='plot-container'
                    ),
                ],
                className = 'grid tab-cols-2 desk-cols-2 section-body',
            ),
            get_data_source('rethink19'),
        ],
        className = 'section',
        id='careers',
    )
