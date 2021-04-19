"""Collects and organizes the data used by the timeline"""

import LastFmApi
import Util
from Week import Week

from collections import OrderedDict


class TimelineData:
    def __init__(self, LastFmGet, username, mode, sort, numItems):
        self.data = OrderedDict()

        self.LastFmGet = LastFmGet
        self.username = username
        self.mode = mode
        self.sort = sort
        self.numItems = numItems

        self.items  = self.get_items()
        self.charts = self.get_target_charts()

    # Initializes the data dict with item names as keys and dicts as values, with charts as keys and scrobbles as values
    def init_data(self):
        for item in self.items: # Creates a dict for each item
            self.data[item] = OrderedDict()
            for chart in self.charts: # Adds each chart as a key and initializes its value
                self.data[item][chart] = 0
    
    # Returns a list of items from the user's profile
    def get_items(self, username):
        dataMethod, key1, key2 = Util.get_user_top_items_args(LastFmGet, self.mode)

        itemData = dataMethod(self.username, self.numItems)
        items = [ item['name'] for item in itemData[key1][key2] ]
        return items
    
    # Returns list of charts available in the user's history
    def get_target_charts(self):
        firstPage     = self.LastFmGet.user_recent_tracks(self.username, 100, 1)
        totalPages    = int(firstPage['recenttracks']['@attr']['totalPages'])
        lastPage      = self.LastFmGet.user_recent_tracks(self.username, 100, totalPages)
        firstScrobble = int(lastPage['recenttracks']['track'][-1]['date']['uts'])

        charts = []
        chartsData = LastFmGet.user_weekly_chart_list(self.username)
        for chart in chartsData['weeklychartlist']['chart']:
            start = int(chart['from'])
            end   = int(chart['to'])
            if end >= firstScrobble:
                charts.append(Week(start, end))

        return charts
