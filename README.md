# Effective Altruism Dashboard

Project partly inspired by the [Johns Hopkins Corona Virus Dashboard](https://coronavirus.jhu.edu/map.html).

## Precedents:
 - [EA hub map](https://eahub.org/)
 - [EA funds dashboard](https://app.effectivealtruism.org/funds/about/stats)

## Design

Intend to have five panels:
 - Total members/donations/pledges of EA
 - Demographics of EAs
 - World map of EAs
 - Sankey diagram of EA donations: sources -> cause areas -> charities
 - Timeline of growth (membership, donations)
 
We'd also like to do a map in the style of [Gapminder](https://www.gapminder.org/tools/#$chart-type=bubbles). Countries are replaced with EA orgs, and the axes are measures of growth (donations made, donations pledged, pageviews, etc). Perhaps the central map can be toggle-able between the map and this diagram.

## Data sources

### Demographics
 - [EA growth](https://forum.effectivealtruism.org/posts/MBJvDDw2sFGkFCA29/is-ea-growing-ea-growth-metrics-for-2018)
 - [2019 EA survey](https://www.rethinkpriorities.org/blog/category/EA+Survey)
 
### Dontaions and Grants
 - [Giving what we can donations](https://www.givingwhatwecan.org/) - Current total pledged and donated
 - [Rethink Priorities Survey](https://www.rethinkpriorities.org/blog/2020/2/14/ea-survey-2019-series-donation-data) - Year, amount, charity, cause area
 - [Founders pledge](https://founderspledge.com/) - Current total pledged and donated
 - [Open Philanthropy Grant Database](https://www.openphilanthropy.org/giving/grants) - CSV of grant amount, date, cause area
 - [EA Funds](https://app.effectivealtruism.org/funds/global-development#payout-reports) - Total balance, total donated, history of grants, cause area

### Global Poverty
 - [Global poverty](https://sdg-tracker.org/no-poverty)
