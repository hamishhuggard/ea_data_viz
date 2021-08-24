import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import string
import dash_core_components as dcc
import dash_html_components as html

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
      row_df['label'] = label[:30]
      row_dfs.append(row_df)
   long_df = pd.concat(row_dfs, ignore_index=True)
   # remove rows with value=0 to avoid singularity in log scale
   long_df = long_df[ long_df['value']!=0 ]
   long_df = long_df.sort_values(by='year')

   long_dfs.append( long_df )

commiting, doing, joining, reading = long_dfs

HEIGHT = 600
WIDTH = 600

growing_figs = []
for table, table_name in zip(
    [
        reading,
        joining,
        commiting,
        doing,
    ],
    [
        'low engaged',
        'medium engaged',
        'highly engaged',
        'money',
    ]
):
    fig = go.Figure()
    annotations = []
    print(table['label'].unique())
    for val in table['label'].unique():
        val_df = table.loc[ table['label']==val ]
        fig.add_trace(
            go.Scatter(
                x=val_df['year'],
                y=val_df['value'],
                name=val,
            )
        )
        fig.update_layout(
            title=table_name,
            height=HEIGHT,
            # width=WIDTH,
            showlegend=False,
            # yaxis_type="log",
        )
        annotations.append(dict(
            xref='paper',
            x=int(val_df['year'].max()),
            y=int(val_df['value'].max()),
            xanchor='left',
            yanchor='middle',
            text=f'{val}',
            font={
                'family': 'Arial',
                'size': 16,
            },
            showarrow=False
        ))
    import json
    print(json.dumps(annotations, indent=3))
    fig.update_layout(annotations=annotations)

    # fig.update_layout(

        # autosize = True,

        # Top-left corner:

        # legend = dict(
        #     yanchor="top",
        #     y=0.99,
        #     xanchor="left",
        #     x=0.01,
        #     title_text='',
        # )

        # Below:

        # legend = {
        #       'xanchor': "center",
        #       'yanchor': "top",
        #       'y': -0.3, # play with it
        #       'x': 0.5,   # play with it
        #       'title_text': '',
        # }

    # )

    growing_figs.append(
        html.Div(
            dcc.Graph(
                figure=fig,
            ),
        )
    )

class Growth(html.Div):
    def __init__(self):
        super(Growth, self).__init__(
            [
                html.Div(
                    html.H2('Growth'),
                    className='section-heading',
                ),
                html.P([
                    'Data source: ',
                    dcc.Link(
                        '2019 Rethink Priorities Survey',
                        href='https://www.rethinkpriorities.org/blog/2019/12/5/ea-survey-2019-series-community-demographics-amp-characteristics'
                    ),
                ]),
                html.Div(
                    growing_figs,
                    className = 'demographics-container grid-2-cols grid-4-cols',
                    # className = 'demographics-container',
                ),
            ],
            className = 'section'
        )
