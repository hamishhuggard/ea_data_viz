from bs4 import BeautifulSoup
import re
import requests
import pandas as pd
from datetime import datetime
import json

def url_to_soup(url):
    page = requests.get(url, headers={'User-Agent': ''})
    return BeautifulSoup(page.content, features="html.parser")


def download_ea_funds_grants():
    # The data can be seen at 'https://app.effectivealtruism.org/funds/{}/payouts'.
    # But the above page isn't static so can't be scraped.

    # Found this by poking around in developer tools for 20 minutes:
    data_url = 'https://cdn.contentful.com/spaces/afdyh2iav3iy/entries?access_token=630f127009ba9d044dd156ae8a6b9c5b26c66c054508f720e8b0dbbfa165d4e5&content_type=payoutReport&include=2&order=-fields.date&fields.fund.sys.contentType.sys.id=fund&fields.fund.fields.slug={}'
 
    fund_names = [
        'global-development',
        'animal-welfare',
        'far-future',
        'ea-community',
    ]

    # Store all grants in a dataframe
    grants = pd.DataFrame(columns=[
        'fund',
        'amount',
        'date',
        'title',
    ])

    for fund_name in fund_names:

        # Retrieve json data
        fund_url = data_url.format(fund_name)
        fund_response = requests.get(fund_url)
        fund_data = json.loads(fund_response.content)

        # Parse each grant
        for grant in fund_data['items']:

            fields = grant['fields']
            title = fields['title']
            amount = fields['amount']

            # date format is 2020-03-27
            date = datetime.strptime(fields['date'], '%Y-%m-%d')

            # Add to dataframe
            grants.loc[len(grants), :] = [
                fund_name,
                amount,
                date,
                title,
            ]

            # # There's also recipients data which I can't parse
            # recipients = fields['recipients']
            # for recipient in recipients:
            #     recipient_id = recipient['sys']['id'] # I don't know what to do with this

    return grants

def download_ea_funds_balances():
    
    fund_names = [
        'global-development',
        'animal-welfare',
        'far-future',
        'ea-community',
    ]

    body_left = "{\"operationName\":\"getXeroBalanceSheetByOrganization\",\"variables\":{\"reference\":\""
    body_right = "\",\"nearestReportDate\":\"2020-07-28T05:59:22.337Z\"},\"query\":\"query getXeroBalanceSheetByOrganization($reference: String!, $nearestReportDate: Date) {\\n  XeroBalanceSheet: getXeroBalanceSheetMonthlyTotalByReference(reference: $reference, nearestReportDate: $nearestReportDate) {\\n    edges {\\n      node {\\n        reportDate\\n        reference\\n        amount\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\"}"

    balances = pd.DataFrame(columns=[
        'fund',
        'amount',
        'as of',
    ])

    for fund_name in fund_names:

        # send HTTP request
        body = body_left + fund_name + body_right
        response = requests.post(
          "https://parfit.effectivealtruism.org/graphql",
          headers = {
            "accept": "*/*",
            "accept-language": "en-GB,en;q=0.9,de;q=0.8,fr;q=0.7,ru;q=0.6",
            "content-type": "application/json",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site"
          },
          data = body
        )

        # parse request
        content = json.loads(response.content)
        node = content['data']['XeroBalanceSheet']['edges'][0]['node']
        balance = node['amount']
        as_of = node['reportDate']

        # add to balances dataframe
        balances.loc[len(balances), :] = [
            fund_name,
            balance,
            as_of,
        ]

    return balances

def scrape_founders_pledge():
    fp_url = 'https://founderspledge.com/'
    soup = url_to_soup(fp_url)

    # Scrape total pledged
    with open('text', 'w') as f:
        f.write(str(soup))
    pledge_str = soup.select('div.resource--stat--total-value-pledged')[0].get_text()
    pledge_pattern = r'\$(\d.\d\d) billion'
    pledge_match  = re.findall(pledge_pattern, pledge_str)[0]
    total_pledged = round( float(pledge_match) * 10**9 )

    # Scrape total committed
    committed_str = soup.select('div.resource--stat--fulfilled-commitments')[0].get_text()
    committed_pattern = r'\$(\d+) million'
    committed_match  = re.findall(committed_pattern, committed_str)[0]
    total_committed = round( float(pledge_match) * 10**6 )

    # Scrape number members
    members = soup.select('div.resource--stat--in-30-countries')[0].get_text()
    members_pattern = r'(\d+) members'
    countries_pattern = 'In (\d+) Countries'
    members_match = re.findall(members_pattern, members)[0]
    countries_match  = re.findall(countries_pattern, members)[0]
    n_members, n_countries = int(members_match), int(countries_match)

    return {
        'pleged': total_pledged,
        'committed': total_committed,
        'members': n_members,
        'countries': n_countries
    }

