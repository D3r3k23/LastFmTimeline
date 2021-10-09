"""
TimelineData.data:
{
  item1: {
    chart1: playcount
    chart2: playcount
    ...
  }
  item2: {
    chart1: playcount
    chart2: playcount
    ...
  }
...
}

TimelineData.ranking:
{
  item1: {
    chart1: rank
    chart2: rank
    ...
  }
  item2: {
    chart1: rank
    chart2: rank
    ...
  }
...
}
"""
from collections import namedtuple

import lastfmget

from Util import *

class TimelineData:
    """
    Contains the data needed by LastFmTimeline to create a timeline
    """
    def __init__(self, username, itemtype, numitems):
        self.username = username
        self.numitems = numitems
        self.itemtype = itemtype

        self.items  = get_items(self.username, self.itemtype, self.numitems)
        self.charts = get_target_charts(self.username)
        self.init_data()

    def init_data(self):
        """
        Initialize self.data to 0
        """
        self.data = {}
        for item in self.items:
            self.data[item] = { chart: 0 for chart in self.charts }

    def load(self, mode):
        """
        For each of the user's top $numitems items ($itemtype), store cumulative scrobbles
        for each chart since the user's first scrobble.
        """
        print('' * 40)
        prevchart = None
        for i, chart in enumerate(self.charts):
            if prevchart is not None:
                # Copy each item's playount from the previous chart
                for item in self.data.values():
                    item[chart] = item[prevchart]

            # Add new playcounts from weekly chart
            weeklychart = get_user_weekly_item_chart(self.itemtype, self.username, chart.start, chart.end)
            for item in weeklychart['chart']:
                itemname = item['name']
                if itemname in self.data:
                    self.data[itemname][chart] += item['playcount']

            prevchart = chart

            if i % (len(self.charts) / 40) == 0:
                print(',', end='')
        print()
        print('' * 40)

        if (mode is Mode.Rank):
            self.convert_to_rank()

    def convert_to_rank(self):
        RankItem = namedtuple('RankItem', ['name', 'playcount'])

        rankdata = { item: {} for item in self.data.keys() }

        for chart in self.charts:
            ranking = [ RankItem(itemdata[chart], itemname) for itemname, itemdata in self.data.items() ]
            ranking.sort(key=lambda item: item.name)
            ranking.sort(key=lambda item: item.playcount, reverse=True)

            for rank, item in enumerate(ranking, 1):
                rankdata[item.name][chart] = rank

        self.data = rankdata

    def get(self):
        return self.data

    def dump(self, fn):
        dump_pickle(fn, self.data)

    def print(self, fn):
        dump_yaml(self.data, fn)

def get_items(username, itemtype, numitems):
    """
    Returns a list of items from the user's profile
    """
    if itemtype is Item.Artists:
        topartists = lastfmget.user_top_artists(username, numitems)
        return [ artist['name'] for artist in topartists ]

    if itemtype is Item.Albums:
        topalbums = lastfmget.user_top_albums(username, numitems)
        return [ f"{album['artist']} - {album['name']}" for album in topalbums ]

    if itemtype is Item.Tracks:
        toptracks = lastfmget.user_top_tracks(username, numitems)
        return [ f"{track['artist']} - {track['name']}" for track in toptracks ]

def get_user_top_items(itemtype, username, *params):    # params: limit, page
    method = getattr(lastfmget, f'user_top_{itemtype}') # Ex. Item.Artists -> lastfmget.user_top_artists
    topitems = method(username, *params)
    return topitems

def get_target_charts(username):
    """
    Returns list of charts available in the user's history
    """
    firstpage     = lastfmget.user_recent_tracks_raw(username, page=1)['recenttracks']
    totalpages    = int(firstpage['@attr']['totalPages'])
    lastpage      = lastfmget.user_recent_tracks_raw(username, page=totalpages)['recenttracks']
    firstscrobble = int(lastpage['track'][-1]['date']['uts'])

    charts = []
    for chart in lastfmget.user_weekly_chart_list(username):
        start = int(chart['start']) # int() -- Remove
        end   = int(chart['end'])   # int() -- Remove
        if end >= firstscrobble:
            charts.append(Chart(start, end))

    return charts

def get_user_weekly_item_chart(itemtype, username, *params): # params: start, end
    method = getattr(lastfmget, f'user_weekly_{str(itemtype).rstrip("s")}_chart') # Ex. Item.Artists -> lastfmget.user_weekly_artist_chart
    weeklyitemchart = method(username, *params)
    return weeklyitemchart
