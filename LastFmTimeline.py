
from LastFmApi   import *
from functions   import *
from collections import OrderedDict
from matplotlib  import pyplot


LastFmGet = LastFmApi(
    key       = "REDACTED", # My key
    userAgent = "D3r3k523")

username = get_username(LastFmGet)
mode     = get_mode() # "Artist", "Album", "Track"
sort     = get_sort() # "Scrobbles", "Rank"
numItems = get_num_items(mode)

items  = get_items(LastFmGet, username, mode, numItems) # List of strings
charts = get_target_charts(LastFmGet, username)         # List of Weeks

data = OrderedDict()
init_data(items, charts, data)
load_data(LastFmGet, username, mode, sort, charts, data)
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

pyplot.title("{name}'s Top {numItems} {type}s Timeline".format(name=username, numItems=numItems, type=mode))
pyplot.xlabel("Weeks")

alphaMax = 0.6
alphaMin = 0.1
alphaInt = (alphaMax - alphaMin) / (numItems - 1)
alpha = alphaMax

for itemName, itemData in data.items():
    pyplot.plot_date(itemData.values(),
                     xdate = True,
                     color=(0.75, 0, 0, alpha),
                     label=itemName)
    alpha -= alphaInt

pyplot.legend()
pyplot.show()
