import plotly.express as px
import pandas as pd

from Util import *

class LastFmTimeline:
    def __init__(self, data, username, itemtype, mode):
        self.df       = pd.DataFrame(data)
        self.username = username
        self.itemtype = itemtype
        self.mode     = mode

        self.fig = None

    def create(self):
        # yaxis = [ dict(item.items()) for itemname, item in self.data.items() ]

        fig = px.line(
            data_frame = self.df
            # x = 'date'
            # y =
        )
        fig.show()


        self.fig = fig

# # Create figure
# fig, ax = pyplot.subplots(
#     figsize = [ 14, 8 ],
#     dpi     = 400)

# fig.tight_layout()

# ax.set_title(f'{username}\'s Top {numItems} {str(mode)}s Timeline')
# ax.set_ylabel(sort)

# if sort == Sort.SCROBBLES:
#     topItem = list(data.values())[0]
#     topScrobbles = list(topItem.values())[-1]
#     ax.set_ylim([ 0, round_up(topScrobbles, 100) ])
# elif sort == Sort.RANK:
#     ax.set_ylim([ 1, numItems ])
#     ax.invert_yaxis()

# ax.set_xlim([ charts[0].end, charts[-1].end ])

# ax.legend(
#     bbox_to_anchor = (1.01, 1.01),
#     loc            = 'upper left',
#     prop           = { 'size': 6 })

# # Set x-axis labels
# chartLabels = [ chart for chart in charts
#                   if chart is charts[0] or chart is charts[-1] # First and last chart
#                     or (chart.date.month == 1 and chart.date.day <= 7) ] # Chart at the beginning of each year

# ax.set_xticks([ chart.end for chart in chartLabels ])
# ax.set_xticklabels([ str(chart) for chart in chartLabels ])

# # (rotation=60)
# # (labelsize=8)
# # (labelsize=8)

# # Set gridlines
# ax.set_axisbelow(True)
# ax.get_xaxis().grid(True,
#     which     = 'major',
#     color     = (0, 0, 0, 0.6),
#     linestyle = '-')
# ax.get_yaxis().grid(True,
#     which     = 'both',
#     color     = (0, 0, 0, 0.2),
#     linestyle = '-')

# # Line color
# alphaMax = 0.7
# alphaMin = 0.2
# alphaInt = (alphaMax - alphaMin) / (numItems - 1)
# alpha = alphaMax

# # Plot data
# for rank, (itemName, itemData) in enumerate(data.items(), 1):
#     ax.plot_date(
#         x         = [ dates.date2num(week.date) for week in charts ],
#         y         = itemData.values(),
#         xdate     = True,
#         color     = (0.75, 0, 0, alpha),
#         label     = '{:>2}. '.format(str(rank)) + itemName,
#         linestyle = '-',
#         marker    = '')
#     alpha -= alphaInt


# pyplot.show()
# pyplot.gcf().savefig('timeline.png')
