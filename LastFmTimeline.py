
from LastFmApi   import *
from functions   import *
from collections import OrderedDict


LastFmGet = LastFmApi(
    key       = "13b760489bb27cd06eada7872c9b394a",
    userAgent = "D3r3k523")


username = get_username(LastFmGet)
mode     = get_mode()
sort     = get_sort()
numItems = get_num_items(mode)

charts = get_target_charts(LastFmGet, username)
items  = get_items(LastFmGet, username, mode, numItems)

data = OrderedDict()
init_data(charts, items, data)
load_data(LastFmGet, username, mode, sort, charts, data)

print_data(data)
