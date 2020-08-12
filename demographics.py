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

demo_pies = []
for table_name in [
        'age_group', 'diet', 'gender', 'employment', 'ethnicity', 'subject',
        ]:

    path = f"./data/rp_survey_data/{table_name}.csv"
    demo_table = pd.read_csv(path, sep='\t')
    title = demo_table.columns[0]

    # remove the 'Total' row
    demo_table = demo_table[ ~demo_table[title].isin(['Total', 'Total respondents']) ]
    # demo_table['label'] = demo_table[title] + demo_table['Percent']
    # convert '5%' to 5
    demo_table['Percent'] = demo_table['Percent'].apply(lambda x: float(x[:-1]))


    subs = {
        'Eat meat, but try to reduce the amount  ': 'Reduce',
        'Eat meat': 'Meat',
        'Vegetarian': 'Veg.',
        'Pescetarian': 'Pesc.',
        'Other (please specify)': 'Other',

        'Native Hawaiian or Other Pacific Islander': 'Other',
        'American Indian or Alaskan Native': 'Other',
        'Black or African American': 'Black',
        'Hispanic, Latino or Spanish Origin': 'Latino',

        # 'Sciences': 'Sci',
        'Engineering': 'Eng',
        'Psychology': 'Psych',
        'Computer Science': 'CS',
        'Professional or vocational qualification': 'Vocation',
        'Economics': 'Econ',
        'Arts & Humanities': 'Arts',
        # 'Philosophy': 'Phil',
        'Social Science': 'Social Sci',
        # 'Medicine': 'Med',

        'Employed, Full-Time': 'Employed',
        'Student, Full-Time': 'Student',
        'Employed, Part-Time': 'Part-Timte',
        'Not employed, but looking for work': 'Unemployed',
        'Student, Part-Time': 'Student',
        'Not employed, but not looking for work': 'Not looking for work',

        'Age Group': 'Age',
        'Employment Type': 'Employment',
        'Race/Ethnicitiy': 'Ethnicity',
        'Subject Studied': 'Subject',
    }
    demo_table['label'] = demo_table[title].map(subs).fillna(demo_table[title])

    pie_fig = px.bar(
        demo_table, 
        y='label', 
        x='Percent', 
        title=title,
        hover_data={
            # title: True,
            'Percent': True,
            # 'label': False
        },
        height=300,
        orientation='h',
        labels={
            'label': '',
            'Percent': '',
        },
        # layout={
        #     'l': 0,
        #     'r': 0,
        #     'b': 0,
        #     't': 0,
        # }

    )#, hovertext='label')
    # # pie_fig.update_trace(hovertemplate=)
    # pie_fig.update_traces(hoverinfo='none', textinfo='label')
    # # pie_fig.update_traces(textposition='inside')
    # pie_fig.update_traces(insidetextorientation='horizontal')
    # pie_fig.update(layout_showlegend=False)
    pie_fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
    )
    this_pie = dcc.Graph(
        id=title, #style={'margin': '0%'},
        figure=pie_fig,
        # style={},
    )

    demo_pies.append(this_pie)
