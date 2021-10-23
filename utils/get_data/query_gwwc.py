import requests
import pandas as pd

NEW_PLEDGES_URL = 'https://dashboard.effectivealtruism.org/api/public/card/a8499095-be16-46fe-af1f-e3e56ee04e88/query?parameters=%5B%5D'
DONATIONS_BY_YEAR_URL = 'https://dashboard.effectivealtruism.org/api/public/card/9906735e-1350-4353-9828-bb3ec16137e3/query?parameters=%5B%5D'
DONATIONS_BY_ORG_URL = 'https://dashboard.effectivealtruism.org/api/public/card/b3887098-686a-491c-9f9c-9a5b0e2b7fd8/query?parameters=%5B%5D'

def request_data_and_parse(url):
    json_response = requests.get(url).json()
    col_data = json_response['data']['cols']
    col_names = [ col_details['name'] for col_details in col_data ]
    data = json_response['data']['rows']
    df = pd.DataFrame(columns = col_names, data = data)
    return df

def get_new_pledges():
    df = request_data_and_parse(NEW_PLEDGES_URL)
    return df

def get_donations_by_year():
    df = request_data_and_parse(DONATIONS_BY_YEAR_URL)
    return df

def get_donations_by_org():
    df = request_data_and_parse(DONATIONS_BY_ORG_URL)
    return df

def save_data():
    print('requesting new_pledges...')
    new_pledges = get_new_pledges()
    new_pledges.to_json('./data/gwwc/new_pledges.json')

    print('requesting donations_by_year...')
    donations_by_year = get_donations_by_year()
    donations_by_year.to_json('./data/gwwc/donations_by_year.json')

    print('requesting donations_by_org...')
    donations_by_org = get_donations_by_org()
    donations_by_org.to_json('./data/gwwc/donations_by_org.json')
