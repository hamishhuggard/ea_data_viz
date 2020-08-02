from bs4 import BeautifulSoup
import re
import requests

def url_to_soup(url):
    page = requests.get(url, headers={'User-Agent': ''})
    return BeautifulSoup(page.content, features="html.parser")

def download_op_grants():
    openphil_url = 'https://www.openphilanthropy.org/giving/grants/spreadsheet'

def download_ea_funds_grants():
    fund_names = [
        'global-development',
        'animal-welfare',
        'far-future',
        'ea-community',
    ]
    fund_report_url = 'https://app.effectivealtruism.org/funds/{}/payouts'
    for fund_name in fund_names:
        fund_report = url_to_soup(fund_name)
        # ROADBLOCK: page is not static, which may be why this isn't working
        payout_report = fund_report.div['col-md-8 col-md-offset-2']
        payouts = payout_report.find_all('a')
    return

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

print(scrape_founders_pledge())