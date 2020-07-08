import BeautifulSoup4 as bs4
import re

def get_html(url):
    return html

def get_soup(url):
    return bs4(get_html(url))

def download_op_grants():
    openphil_url = 'https://www.openphilanthropy.org/giving/grants/spreadsheet'

def download_ea_funds_grants():
    funds = [
        'global-development',
        'animal-welfare',
        'far-future',
        'ea-community',
    ]
    fund_report_url = 'https://app.effectivealtruism.org/funds/{}/payouts'

def scrape_founders_pledge():
    fp_url = 'https://founderspledge.com/'
    soup = get_soup(fp_url)

    # Scrape total pledged
    pledge_str = soup.div['resource--stat--total-value-pledged'].get_text()
    pledge_pattern = r'\$(\d.\d\d) billion Total Value Pledged'
    (pledge_match,)  = re.match(pledge_pattern, pledge_str).groups()
    total_pledged = float(pledge_match) * 10**9

    # Scrape total committed
    committed_str = soup.div['resource--stat--fulfilled-commitments'].get_text()
    committed_pattern = r'\$(\d+) million Fulfilled Commitments'
    (committed_match,)  = re.match(committed_pattern, committed_str).groups()
    total_committed = int(pledge_match) * 10**6

    # Scrape number members
    members = soup.div['resource--stat--in-30-countries'].get_text()
    members_pattern = r'(\d+) members In (\d+) Countries '
    (members_match, countries_match)  = re.match(pledge_pattern, pledge_str).groups()
    n_members, n_countries = int(members_match), int(countries_match)

    return {
        'pleged': total_pledged,
        'committed': total_committed,
        'members': n_members,
        'countries': n_countries
    }
