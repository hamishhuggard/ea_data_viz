# [Effective Altruism Data](https://effectivealtruismdata.com)

![Effective Altruism Data](eadata.png)

[Effective Altruism](https://www.effectivealtruism.org/) (EA) is a philosophy and social movement that uses reason and evidence to do the most good.

There are several EA organisations which collect data on grants, donors, and pledges. This website aggregate and visualise that data.

The website is coded in Python using [Dash](https://dash.plotly.com/) and [Plotly](https://plotly.com/). it is currently deployed with Heroku at [effectivealtruismaata.com](https://effectivealtruismdata.com).

There may be some overlap between this project and with the [EA Hub map](https://eahub.org/) and the [EA Funds dashboard](https://app.effectivealtruism.org/funds/about/stats).

## How to run
1. Install [pipenv](https://pipenv.pypa.io/en/latest/).
2. Run the following in the terminal:
```
git clone https://github.com/hamishhuggard/ea_data_viz.git
cd ea_data_viz
pipenv run python app.py
```

## To do
- EA Funds visualisations like OP

## Ideas:
- Multipage routing
- [Better bar charts](https://dkane.net/2020/better-horizontal-bar-charts-with-plotly/?utm_source=pocket_mylist)
- Navigation bar
- OP grant table
- Reimplement in chart.js or D3.js for performance
   - With better zoom controls
- Disable the menu on the Sankey plot
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
