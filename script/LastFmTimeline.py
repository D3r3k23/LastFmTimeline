
from LastFmApi   import *
from functions   import *
from collections import OrderedDict
from matplotlib  import pyplot, dates, rc

LastFmGet = LastFmApi(key='MY_KEY', userAgent='LastFmTimeline by D3r3k523')

username = get_username(LastFmGet)
mode     = get_mode() # 'Artist', 'Album', 'Track'
sort     = get_sort() # 'Scrobbles', 'Rank'
numItems = get_num_items(mode)

print("Loading...")
print("0%...")
items  = get_items(LastFmGet, username, mode, numItems) # List of strings
charts = get_target_charts(LastFmGet, username)         # List of Weeks

data = OrderedDict()
init_data(items, charts, data)
load_data(LastFmGet, username, mode, sort, charts, data)
print("100%")
# data = {
#   item1: {
#     chart1: entry,
#     chart2: entry,
#     ... },
#   item2: {
#     chart1: entry,
#     chart2: entry,
#     ... },
#   ... }

pyplot.figure(figsize=(14, 8), dpi=250)
pyplot.title(f"{username}'s Top {numItems} {mode}s Timeline")
pyplot.ylabel(sort)
pyplot.xticks(rotation=60)

# Line color
alphaMax = 0.7
alphaMin = 0.2
alphaInt = (alphaMax - alphaMin) / (numItems - 1)
alpha = alphaMax

for rank, (itemName, itemData) in enumerate(data.items(), 1):
    pyplot.plot_date([ dates.date2num(week.date) for week in charts ], # X-axis
                     itemData.values(), # Y-axis
                     xdate     = True,
                     color     = (0.75, 0, 0, alpha),
                     label     = "{:>2}. ".format(rank) + itemName,
                     linestyle = '-',
                     marker    = '')
    alpha -= alphaInt

rc('xtick', labelsize=8)
rc('ytick', labelsize=8)
pyplot.grid(b=True, axis='y', which='major', color=(1, 1, 1, 0.2), linestyle='--')
dates.DateFormatter("%b '%y")

if sort == 'Rank':
    pyplot.gcf().invert_yaxis()

pyplot.legend(bbox_to_anchor = (1.01, 1.01),
              loc            = 'upper left',
              prop           = { 'size': 6 })

pyplot.tight_layout()

def on_plot_hover(event):
    pass

pyplot.show()
pyplot.gcf().savefig("timeline.png")
