
from LastFmApi   import *
from functions   import *
from collections import OrderedDict


LastFmGet = LastFmApi(
    key       = "REDACTED", # My key
    userAgent = "D3r3k523")


username = get_username(LastFmGet)
print()
mode = get_mode()
print()
sort = get_sort()
print()
numItems = get_num_items(mode)
print()

charts = get_target_charts(LastFmGet, username)
items  = get_items(LastFmGet, username, mode, numItems)

data = OrderedDict()
init_data(charts, items, data)
load_data(LastFmGet, username, mode, sort, charts, data)

print_data(data)
