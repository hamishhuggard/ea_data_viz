import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
import re
from glob import glob

##################################
###       DEMOGRAPHICS         ###
##################################

def get_demo_table(demo_name):

    path = f"./data/rp_survey_data/{demo_name}.csv"
    demo_table = pd.read_csv(path, sep='\t')
    title = demo_table.columns[0]

    # remove the 'Total' row
    demo_table = demo_table[ ~demo_table[title].isin(['Total', 'Total respondents']) ]
    # demo_table['label'] = demo_table[title] + demo_table['Percent']
    # convert '5%' to 5
    demo_table['Percent'] = demo_table['Percent'].apply(lambda x: float(x[:-1]))



    subs = {
        'Eat meat, but try to reduce the amount  ': 'Reducetarian',
        # 'Eat meat': 'Meat',
        # 'Vegetarian': 'Veg.',
        # 'Pescetarian': 'Pesc.',
        'Other (please specify)': 'Other',

        'Native Hawaiian or Other Pacific Islander': 'Pacific Island', # 'Other',
        'American Indian or Alaskan Native': 'Native American', # 'Other',
        'Black or African American': 'Black',
        'Hispanic, Latino or Spanish Origin': 'Latino',

        # 'Computer Science': 'CS',
        'Math': 'Math',
        # 'Economics': 'Econ',
        # 'Social Science': 'Soc. Sci.',
        # 'Philosophy': 'Phil',
        # 'Psychology': 'Science',#'Psych',
        # 'Arts & Humanities': 'Arts',
        # 'Sciences': 'Other',
        # 'Engineering': 'Other',
        # 'Physics': 'Other',
        # 'Psychology': 'Other',
        # 'Medicine': 'Other',
        'Professional or vocational qualification': 'Professional/Vocational',

        'Employed, Full-Time': 'Employed (FT)',
        'Student, Full-Time': 'Student (FT)',
        'Employed, Part-Time': 'Employed (PT)',
        'Not employed, but looking for work': 'Seeking employment',
        'Student, Part-Time': 'Student (PT)',
        'Not employed, but not looking for work': 'Not employed',
        # 'Homemaker ': 'Other',
        # 'Student, Part-Time': 'Student',
        # 'Self-Employed': 'Self-Employ',


        'Consequentialism (utilitarian)': 'Utilitarianism',
        'Consequentualism (other than utilitarian)': 'Consequentialism',

        # '13-17': '13-17'
        # 18-24
        # 25-34
        # 35-44
        # 45-54
        # 55-64
        # 65+
    }
    max_chars = 20
    demo_table['label'] = demo_table[title].map(subs).fillna(demo_table[title])
    demo_table['label'] = demo_table['label'].apply(lambda x: x.rjust(max_chars))

    # Normalise title
    title_subs = {
        'Age Group': 'Age',
        'Employment Type': 'Employment',
        'Race/Ethnicity': 'Ethnicity',
        'Subject Studied': 'Subject Studied',
        'Moral View': 'Moral View',
        'Gender': 'Gender',
        'Diet ': 'Diet',
        'Education': 'Education',
    }
    title = title_subs[title]

    height_per_bar = 20 if len(demo_table) > 10 else 23
    height = height_per_bar * len(demo_table) + 30

    bar_fig = px.bar(
        demo_table, 
        y='label', 
        x='Percent', 
        title=title,
        hover_data={
            # 'title': True,
            'Percent': True,
            # 'label': False
        },
        height=height,
        orientation='h',
        labels={
            'label': title,
            'Percent': 'Percentage',
        },
    )
    bar_fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(title=''),
        yaxis=dict(title=''),
        font=dict(
            # family="Courier New, monospace",
            size=8,
            # color="RebeccaPurple"
        )
    )
    this_bar = dcc.Graph(
        id=title, #style={'margin': '0%'},
        figure=bar_fig,
        config={
            'displayModeBar': False,
        },
        # style={},
    )

    return this_bar

demo_names = [
        'gender', 
        'age_group', 
        'employment', 
        'ethnicity', 
        'diet', 
        'subject',
        'moral_view',
        'education2',
]

demo_bars = {
    demo_name: get_demo_table(demo_name)
    for demo_name in demo_names
}

demo_div = html.Div(
    [
        html.Div(
            html.H2('Demographics'),
            style = {
                'width': '100%',
            }
        ),
        html.Div(
            [
                demo_bars['gender'],
                demo_bars['age_group'],
                demo_bars['ethnicity'],

            ],
            className='demo-column',
            style = {
                # 'background-color': 'yellow',
            }
        ), 

        html.Div(
            [
                demo_bars['diet'],
                demo_bars['employment'],
            ],
            className='demo-column',
            style = {
                # 'background-color': 'red',
            }
        ), 

        html.Div(
            [
                demo_bars['subject'],
                demo_bars['education2'],
            ],
            className='demo-column',
            # style = {
            #     # 'background-color': 'yellow',
            # }
        ),
        html.Div(
            [
                demo_bars['moral_view'],
            ],
            className='demo-column',
            # style = {
            #     # 'background-color': 'yellow',
            # }
        ),


    ],
    style = {
        'height': '100vh',
    }
)