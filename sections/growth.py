import plotly.express as px
import pandas as pd
import numpy as np
import string
import dash_core_components as dcc
import dash_html_components as html

commiting = pd.read_csv('data/is_ea_growing/is_ea_growing_commiting.csv')

doing = pd.read_csv('data/is_ea_growing/is_ea_growing_doing.csv')

joining = pd.read_csv('data/is_ea_growing/is_ea_growing_joining.csv')

reading = pd.read_csv('data/is_ea_growing/is_ea_growing_reading.csv')



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
      row_df['label'] = label[:30]
      row_dfs.append(row_df)
   long_df = pd.concat(row_dfs, ignore_index=True)
   # remove rows with value=0 to avoid singularity in log scale
   long_df = long_df[ long_df['value']!=0 ]
   long_df = long_df.sort_values(by='year')

   long_dfs.append( long_df )

commiting, doing, joining, reading = long_dfs

commiting_fig = px.line(commiting, x='year', y='value', color='label', title='Committing', )
# commiting_fig.update_layout(yaxis_type="log")

doing_fig = px.line(doing, x='year', y='value', color='label', title='Doing', )
# doing_fig.update_layout(yaxis_type="log")

joining_fig = px.line(joining, x='year', y='value', color='label', title='Joining', )
# joining_fig.update_layout(yaxis_type="log")

reading_fig = px.line(reading, x='year', y='value', color='label', title='Reading', )
# reading_fig.update_layout(yaxis_type="log")

growing_figs = [commiting_fig, doing_fig, joining_fig, reading_fig]
growing_figs = [
    html.Div(
        dcc.Graph(
            figure=fig,
        ),
        style = {
            'width': '45%',
            'float': 'left',
        }
    )
    for fig in growing_figs
]

content = html.Div(
    [
        html.Div(
            html.H2('Growth'),
            className='section-heading',
        ),
    ] + growing_figs,
    className = 'section'
)
