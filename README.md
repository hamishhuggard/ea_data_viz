# Effective Altruism Dashboard

## Plan for next few weeks:
1. Cosmetics
 - Redoop spacing
 - Add explanatory text
 - Fix hovertext
2. Create visualisations for OP grants
3. Format the visualisations
4. Set up auto-scraping of OP grants

## TODO:
- Refactor
- Redoop the spacing
- Fix the hovertext on the map
- Fix the plot titles
- Add writing
 - How to interact
 - Where the data comes from
 - What are these things
- OP grants
 - Chuck in vizs
 - Sort out layout
 - Auto data updates
- Growth metrics


- Toggle for per capita / total
- Add percentage to country bar
- Make a floating top bar
- Blurb of EA survey data sources
- OpenPhilanthropy
 - Total grants
 - Grants over time
 - Grants by cause area
 - Grants by org
 - Most recent grants
- EA Funds
 - Grants over time
 - Grants by fund
 - Grants by org
 - Most recent grants
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

This is a dashboard to provide a quick overview of some key statistics of the [effective altruism](https://www.effectivealtruism.org/) (EA) movement.

## Precedents:

We are aware of the following existing dashboards relating to EA
 - [EA hub map](https://eahub.org/)
 - [EA funds dashboard](https://app.effectivealtruism.org/funds/about/stats)

## Design

We intend to have five panels:
 - Total members/donations/pledges of EA
 - Demographics of EAs
 - World map of EAs
 - Sankey diagram of EA donations: sources -> cause areas -> charities
 - Timeline of growth (membership, donations)
 
We'd also like to do a map in the style of [Gapminder](https://www.gapminder.org/tools/#$chart-type=bubbles). Countries are replaced with EA orgs, and the axes are measures of growth (donations made, donations pledged, pageviews, etc). Perhaps the central panel can be toggle-able between the map and this diagram.

## Data sources

### Demographics
 - [EA growth](https://forum.effectivealtruism.org/posts/MBJvDDw2sFGkFCA29/is-ea-growing-ea-growth-metrics-for-2018)
 - [2019 EA survey](https://www.rethinkpriorities.org/blog/category/EA+Survey)
 
### Donations and Grants
 - [Giving what we can donations](https://www.givingwhatwecan.org/) - Current total pledged and donated
 - [Rethink Priorities Survey](https://www.rethinkpriorities.org/blog/2020/2/14/ea-survey-2019-series-donation-data) - Year, amount, charity, cause area
 - [Founders pledge](https://founderspledge.com/) - Current total pledged and donated
 - [Open Philanthropy Grant Database](https://www.openphilanthropy.org/giving/grants) - CSV of grant amount, date, cause area
 - [EA Funds](https://app.effectivealtruism.org/funds/global-development#payout-reports) - Total balance, total donated, history of grants, cause area

### Global Poverty
 - [Global poverty](https://sdg-tracker.org/no-poverty)


## Maybe TODOs
- Find hex values of colors that represent:
  - EA in general
  - Open Philanthropy
  - GiveWell?
  - AMF?
- Graphical representations of growth
- Apply org-specific colors to sankey diagram
- Choose growth data
- Create growth plot
- From Rethink Priorities:
  - Check if there is more recent growth data
  - Get donations data
  - GiveDirectly

