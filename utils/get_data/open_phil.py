import requests
import os

def download_grants():
    openphil_url = 'https://www.openphilanthropy.org/giving/grants/spreadsheet'
    print('Downloading Open Philanthropy grants...')
    return requests.get(openphil_url, headers={'User-Agent': ''}).text

def save_grants():

    data_dir = os.path.abspath('./assets/data/open_philanthropy/')
    if not os.path.exists(data_dir):
        os.path.makedirs(data_dir)

    grants_raw = download_grants()
    print('latest OP grant: ', new_op_data.split('\n')[1])
    grants_path = os.path.join(data_dir, 'open_philanthropy_grants.csv')
    with open(grants_path, 'w') as f:
        f.write(grants_raw)

def process_grants(grants_df):

    grants_df['Amount'] = grants_df['Amount'].apply(
        lambda x: int(x[1:].replace(',','')) if type(x)==str else x
    )

    def normalize_orgname(orgname):
        if type(orgname) == str:
            orgname = orgname.strip()
        if orgname == 'Hellen Keller International':
            orgname = 'Helen Keller International'
        if orgname == 'Alliance for Safety and Justice':
            orgname = 'Alliance for Safety and Justice Action Fund'
        return orgname
    op_grants['Organization Name'] = op_grants['Organization Name'].apply(normalize_orgname)

    op_grants['Date'] = pd.to_datetime(op_grants['Date'], format='%m/%Y')
    op_grants = op_grants.sort_values(by='Date', ascending=False)
    op_grants['Date_readable'] = op_grants['Date'].dt.strftime('%B %Y')

def group_by_month(grants_df):

    min_date = grants_df['Date'].min()
    max_date = grants_df['Date'].max()
    dates = pd.date_range(start=min_date, end=max_date, freq='M')

    grants_by_month = pd.DataFrame(columns=[
        'date',
        'total_amount',
        'n_grants',
    ])

    for i, date in enumerate(dates):
        grants_by_month_i = grants_df.loc[ grants_df['Date'] == date ]
        grants_by_month.loc[i, 'date'] = date
        grants_by_month.loc[i, 'total_amount'] = grants_by_month_i['Amount'].sum()
        grants_by_month.loc[i, 'n_grants'] = len(grants_by_month_i)

    return grants_by_month

def group_by_org(grants_df):
    orgs_df = op_grants.groupby(by='Organization Name', as_index=False).sum()
    orgs_df = orgs_df.sort_values(by='Amount')

def group_by_focus_area(grants_df):
    orgs_df = op_grants.groupby(by='Organization Name', as_index=False).sum()
    orgs_df = orgs_df.sort_values(by='Amount')
