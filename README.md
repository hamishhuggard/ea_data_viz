# [Effective Altruism Data](https://effectivealtruismdata.com)

![Effective Altruism Data](eadata.png)

[Effective Altruism](https://www.effectivealtruism.org/) (EA) is a philosophy and social movement that uses reason and evidence to do the most good.

There are several EA organisations that collect data on grants, donors, and pledges. This website aggregates and visualises that data.

The website is coded in Python using [Dash](https://dash.plotly.com/) and [Plotly](https://plotly.com/). It is currently deployed with Heroku at [effectivealtruismdata.com](https://effectivealtruismdata.com).

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

### Version 1 (Current Version)
- OP Line plots
    - Cumulative grants
    - Grants by month/year
- EA Funds
    - Scatter
    - Cumulative grants
    - Grants by month/year
- X-Risk
    - Probability of x-risks given by Toby Ord
- Founders pledge
    - Members over time
    - Pledged value over time
    - Fulfilled commitments over time
- Title page with summary statistics
    - X EAs have donated Y amount and pledged a further Z.
- Spin off data aggregation to own Python library
- Periodic data refreshing
- [Better bar charts](https://dkane.net/2020/better-horizontal-bar-charts-with-plotly/?utm_source=pocket_mylist)
- Space efficient data source annotations

### Version 2
- Reimplement in chart.js or D3.js
- See data as table or as plot
- Data download buttons
