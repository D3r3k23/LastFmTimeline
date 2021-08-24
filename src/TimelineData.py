"""Collects and organizes the data used by the timeline"""

import lastfmget

from Util import *
from Week import Week

from collections import OrderedDict
from pprint import pprint

class TimelineData:
    def __init__(self, user, mode, sort, items):
        self.data = OrderedDict()

        self.user = user
        self.mode = mode
        self.sort = sort
        # self.items = items

        self.items  = self.get_items()
        self.charts = self.get_target_charts()

    # Initializes the data dict with item names as keys and dicts as values, with charts as keys and scrobbles as values
    def init_data(self):
        for item in self.items: # Creates a dict for each item
            self.data[item] = OrderedDict()
            for chart in self.charts: # Adds each chart as a key and initializes its value
                self.data[item][chart] = 0
    
    # Returns list of charts available in the user's history
    def get_target_charts(self):
        firstPage     = lastfmget.user_recent_tracks(self.user, 100, 1)
        totalPages    = int(firstPage['recenttracks']['@attr']['totalPages'])
        lastPage      = lastfmget.user_recent_tracks(self.user, 100, totalPages)
        firstScrobble = int(lastPage['recenttracks']['track'][-1]['date']['uts'])

        charts = []
        chartsData = lastfmget.user_weekly_chart_list(self.user)
        for chart in chartsData['weeklychartlist']['chart']:
            start = int(chart['from'])
            end   = int(chart['to'])
            if end >= firstScrobble:
                charts.append(Week(start, end))

        return charts
    
    def print(self):
        pprint(self.data)

    
# Returns a list of items from the user's profile
def get_items(self, username):
    datamethod, key1, key2 = get_user_top_items_args(self.mode)

    itemData = datamethod(self.user, self.numItems)
    items = [ item['name'] for item in itemData[key1][key2] ]
    return items

def get_user_top_items_args(mode):
    if mode is Mode.Artists:
        method = lastfmget.user_top_artists
        key1 = 'topartists'
        key2 = 'artist'
    elif mode is Mode.Albums:
        method = lastfmget.user_top_albums
        key1 = 'topalbums'
        key2 = 'album'
    elif mode is Mode.Tracks:
        method = lastfmget.user_top_tracks
        key1 = 'toptracks'
        key2 = 'track'
    else:
        return None

    return method, key1, key2

def get_user_weekly_items_chart_args(mode):
    if mode is Mode.Artists:
        method = lastfmget.user_weekly_artist_chart
        key1 = 'weeklyartistchart'
        key2 = 'artist'
    elif mode is Mode.Albums:
        method = lastfmget.user_weekly_album_chart
        key1 = 'weeklyalbumchart'
        key2 = 'album'
    elif mode is Mode.Tracks:
        method = lastfmget.user_weekly_track_chart
        key1 = 'weeklytrackchart'
        key2 = 'track'
    else:
        return None

    return method, key1, key2
