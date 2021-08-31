import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import string
import dash_core_components as dcc
import dash_html_components as html
from utils.subtitle import get_subtitle

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
   # remove rows with value=0 to avoid singularity in log scale
   long_df = long_df[ long_df['value']!=0 ]
   long_df['year'] = pd.to_datetime(long_df['year'], format='%Y')
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
        '','','',''
        #'low engaged',
        #'medium engaged',
        #'highly engaged',
        #'money',
    ]
):
    fig = go.Figure()
    annotations = []
    print(table['label'].unique())
    for val in table['label'].unique():

        if val in [
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
        ]:
            continue

        val_df = table.loc[ table['label']==val ]

        hover_texts = []
        def hover(row):
            label =row['label']
            value = row['value']
            year = row['year'].year
            return f'<b>{label}</b><br>{value:,.0f}<br><i>{year}</i>'
        hover_texts.extend(
            val_df.apply(hover, axis=1).tolist()
        )

        fig.add_trace(
            go.Scatter(
                x=val_df['year'],
                y=val_df['value'],
                name=val,
                hovertext = hover_texts,
                hovertemplate = '%{hovertext}<extra></extra>',
				mode='lines',
                line=dict(
                    color="#0c869b",
                ),
            )
        )
        fig.update_layout(
            title=table_name,
            #height=HEIGHT,
            # width=WIDTH,
            #showlegend=True,
            showlegend=False,
            # yaxis_type="log",
        )
        #if table is doing:
        #    fig.update_layout(
        #    yaxis_type="log",
        #)

        # Annotations
        # These aren't working?
        val_df = val_df[ val_df['value'].notnull() ].reset_index()
        last_row = val_df.iloc[len(val_df)-1]
        last_hover = hover(last_row)

        fig.add_trace(go.Scatter(
            x=[last_row['year']],
            y=[last_row['value']],
            mode='markers',
            marker=dict(
                #color=colors[i],
                color="#0c869b",
                size=10,#mode_size[i]
            ),
            hovertext = [last_hover],
            hovertemplate = '%{hovertext}<extra></extra>',
        ))

        annotations.append(dict(
            #xref='paper',
            #yref='paper',
            x=last_row['year'],
            y=last_row['value'],
            xanchor='left',
            yanchor='middle',
            text=f' {val}',
            font={
            #    'family': 'Arial',
                'size': 13,
            },
            showarrow=False,
        ))

    fig.update_layout(

        annotations=annotations,
        #margin=dict(l=0, r=0, t=30, b=0),
        margin=dict(l=0, r=0, t=0, b=0),
        title_x=0.5,

        # autosize = True,

        # Top-left corner:

        legend = dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            title_text='',
        )

        # Below:

        # legend = {
        #       'xanchor': "center",
        #       'yanchor': "top",
        #       'y': -0.3, # play with it
        #       'x': 0.5,   # play with it
        #       'title_text': '',
        # }

    )

    growing_figs.append(
        html.Div(
            dcc.Graph(
                figure=fig,
                responsive=True
            ),
        )
    )

def growth1():
    return html.Div(
        [
            html.Div(
                html.H2('Growth in EA Reading'),
                className='section-heading',
            ),
            get_subtitle('growth', hover='points'),
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
            get_subtitle('growth', hover='points'),
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
            get_subtitle('growth', hover='points'),
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
            get_subtitle('growth', hover='points'),
            html.Div(
                growing_figs[3],
                className = 'section-body',
            ),
        ],
        className = 'section',
        id='growth-donating',
    )

