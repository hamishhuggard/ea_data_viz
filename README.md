# [EffectiveAltruismData.com](https://effectivealtruismdata.com)

[Effective Altruism](https://www.effectivealtruism.org/) is a loose collective of quantitatively-minded philanthropists and do-gooders.

There are several EA organisations which collect data on grants, donors, and pledges, so I built this website to aggregate and visualise this data.

The website is coded in Python using Dash and Plotly, plus a bunch of HTML and CSS. It is currently deployed with Heroku at [EffectiveAltruismData.com](https://effectivealtruismdata.com).

Everything is responsive, but some of the plots are too detailed to to useful on mobile.

There may be some overlap between this project and the [EA hub map](https://eahub.org/) or [EA Funds dashboard](https://app.effectivealtruism.org/funds/about/stats).

## How to Run
1. Install [pipenv](https://pipenv.pypa.io/en/latest/)
2. In the terminal:
```
git clone https://github.com/hamishhuggard/ea_data_viz.git
cd ea_data_viz
pipenv run python app.py
```

## TODOs
- EA Funds visualisations like OP
- "storytelling with data" style line plots
- Contents with links

## Future work ideas:
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
