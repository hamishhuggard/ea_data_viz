import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import string
from dash import dcc
from dash import html
from utils.subtitle import get_subtitle
from plots.line import Line

commiting = pd.read_csv('data/is_ea_growing/is_ea_growing_commiting.csv')
doing = pd.read_csv('data/is_ea_growing/is_ea_growing_doing.csv')
joining = pd.read_csv('data/is_ea_growing/is_ea_growing_joining.csv')
reading = pd.read_csv('data/is_ea_growing/is_ea_growing_reading.csv')


# "Founder's Pledge pledges" makes more sense in "doing" than in "commiting"
doing = doing.append( commiting[ commiting['Type of data']=='Founder’s Pledge pledges' ], ignore_index=True )
commiting = commiting[ ~(commiting['Type of data']=='Founder’s Pledge pledges') ]



# Clean tables
growing_dfs = [commiting, doing, joining, reading]
for df in growing_dfs:

   # Convert column names from 'Jan-Dec 2014' to '2014'
   df.columns = [
      col.replace('Jan-Dec ', '') for col in df.columns
   ]

   # Replace 'Didn’t exist', 'No data', 'No data yet', 
   df.replace('No data', np.nan, inplace=True)
   df.replace('No data yet', np.nan, inplace=True)
   df.replace('No survey', np.nan, inplace=True)
   df.replace('Didn’t exist', np.nan, inplace=True)

   # Get rid junk in strings
   def field_to_numeric(field):
      if type(field)!=str:
         return field
      field = field.replace('K', '*10**3')
      field = field.replace('M', '*10**6')
      valid_chars = '.*' + string.digits
      field = ''.join([
         char for char in field if char in valid_chars
      ])
      return eval(field)
      return field
   for col in df.columns:
      if col == 'Type of data':
         continue
      df[col] = df[col].apply(field_to_numeric)




long_dfs = []
for df in [commiting, doing, joining, reading]:
   years = df.columns[1:]
   row_dfs = []
   for row in range(len(df)):
      label = df.loc[row, 'Type of data']
      values = df.loc[row, years]
      if df is reading:
         values = values
      else:
         values = np.nancumsum(values)
      row_df = pd.DataFrame({
         'year': years,
         'value': values,
      })
      row_df['label'] = label#[:30]
      row_dfs.append(row_df)
   long_df = pd.concat(row_dfs, ignore_index=True)
   long_df['year'] = pd.to_datetime(long_df['year'], format='%Y')

   long_dfs.append( long_df )

commiting, doing, joining, reading = long_dfs

growing_figs = []
for table, table_name in zip(
    [
        reading,
        joining,
        commiting,
        doing,
    ],
    [
        '','','',''
        #'low engaged',
        #'medium engaged',
        #'highly engaged',
        #'money',
    ]
):
    ignored_labels = [
        'EA FB “Active Users”',
        'Vox Future Perfect Newsletter sign-ups',

        'New EA Reddit subscribers',
        'EA FB membership',

        'Number of 80,000 Hours significant plan changes (not impact adjusted)',
        'Number of 80,000 Hours significant plan changes (impact adjusted)',
        'ACE money moved[x]',
        'TLYCS money moved',
        'Total OpenPhil non-GiveWell donations',
        'Total non-OpenPhil donors to GiveWell',
        '# donors in EA Survey',
        #'OpenPhil GiveWell donations',
        #'Non-OpenPhil GiveWell donations',
        'Total recorded money actually donated (not pledges) from Giving What We Can members',
        #'# donors in EA Survey',
        #'Founder’s Pledge pledges',
        'EA Funds payouts[y]',

        'Google interest in “effective altruism” (relative scoring)',
    ]

    table = table[ ~table['label'].isin(ignored_labels) ]

    def hover(row):
        label =row['label']
        value = row['value']
        year = row['year'].year
        return f'<b>{label}</b><br>{value:,.0f}<br><i>{year}</i>'

    table['hover'] = table.apply(hover, axis=1).tolist()


    growing_figs.append(
        html.Div(
            Line(
                table,
                x='year',
                y='value',
                label='label',
                title='',
                x_title='',
                y_title='',
                size=None,
                color=None,
                hover='hover',
                log_y=False,
            )
        )
    )

def growth1():
    return html.Div(
        [
            html.Div(
                html.H2('Growth in EA Reading'),
                className='section-heading',
            ),
            get_subtitle('growth', hover='points', zoom=True),
            html.Div(
                growing_figs[0],
                className = 'section-body',
            ),
        ],
        className = 'section',
        id='growth-reading',
    )

def growth2():
    return html.Div(
        [
            html.Div(
                html.H2('Growth in EA Joining'),
                className='section-heading',
            ),
            get_subtitle('growth', hover='points', zoom=True),
            html.Div(
                growing_figs[1],
                className = 'section-body',
            ),
        ],
        className = 'section',
        id='growth-joining',
    )

def growth3():
    return html.Div(
        [
            html.Div(
                html.H2('Growth in EA Committing'),
                className='section-heading',
            ),
            get_subtitle('growth', hover='points', zoom=True),
            html.Div(
                growing_figs[2],
                className = 'section-body',
            ),
        ],
        className = 'section',
        id='growth-committing',
    )

def growth4():
    return html.Div(
        [
            html.Div(
                html.H2('Growth in EA Donating'),
                className='section-heading',
            ),
            get_subtitle('growth', hover='points', zoom=True),
            html.Div(
                growing_figs[3],
                className = 'section-body',
            ),
        ],
        className = 'section',
        id='growth-donating',
    )

