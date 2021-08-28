# Effective Altruism Dashboard

This is a dashboard to provide a quick overview of some key statistics of the [effective altruism](https://www.effectivealtruism.org/) (EA) movement.

Built with Dash and Plotly.

This Deployed at [EffectiveAltruismData.com](https://effectivealtruismdata.com).

How to run:
1. Install [pipenv](https://pipenv.pypa.io/en/latest/)
2. In the terminal enter
```
git clone https://github.com/hamishhuggard/ea_data_viz.git
cd ea_data_viz
pipenv run python app.py
```

## TODOs
- Fix the hovertext on the map
- EA Funds visualisations like OP

## Future work ideas:
- Make a floating top bar
- OP: grant table
- Founders pledge
 - Member over time
 - Commitments over time
 - Pledges over time
- Giving what we can
 - Member over time
 - Donations over time
 - Pledges over time
- 80,000 Hours
 - Latest podcasts
 - Podcast downloads
 - Latest posts
 - Pageviews
 - 80,000 hours pageviews
- EA Forums
 - Views
 - Posts
 - Most recent posts
- On the title: X EAs have donated Y amount and pledged a further Z.
- [Gapminder-style](https://www.gapminder.org/tools/#$chart-type=bubbles) animation of EA orgs


## Precedents:

We are aware of the following existing dashboards relating to EA
 - [EA hub map](https://eahub.org/)
 - [EA funds dashboard](https://app.effectivealtruism.org/funds/about/stats)

## Data sources

### Demographics
 - [EA growth](https://forum.effectivealtruism.org/posts/MBJvDDw2sFGkFCA29/is-ea-growing-ea-growth-metrics-for-2018)
 
### Donations and Grants
 - [Giving what we can donations](https://www.givingwhatwecan.org/) - Current total pledged and donated
 - [Rethink Priorities Survey](https://www.rethinkpriorities.org/blog/2020/2/14/ea-survey-2019-series-donation-data) - Year, amount, charity, cause area
 - [Founders pledge](https://founderspledge.com/) - Current total pledged and donated
 - [Open Philanthropy Grant Database](https://www.openphilanthropy.org/giving/grants) - CSV of grant amount, date, cause area
 - [EA Funds](https://app.effectivealtruism.org/funds/global-development#payout-reports) - Total balance, total donated, history of grants, cause area

