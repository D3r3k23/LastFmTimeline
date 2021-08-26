import lastfmget

from Util import *
from Week import Week

from pprint import pprint

class TimelineData:
    def __init__(self, user, mode, sort, numitems):
        self.user = user
        self.mode = mode
        self.sort = sort
        self.numitems = numitems

        self.data = self.load_data()

    def load_data(self):
        items  = get_items(self.user, self.mode, self.numitems)
        charts = self.get_target_charts()


        return {}

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
def get_items(username, mode, numitems):
    if mode is Mode.Artists:
        artists = lastfmget.user_top_artists(username, numitems)
        return [ artist['name'] for artist in artists ]

    if mode is Mode.Albums:
        albums = lastfmget.user_top_albums(username, numitems)
        return [ album['artist'] + ' - ' + album['name'] for album in albums ]

    if mode is Mode.Tracks:
        tracks = lastfmget.user_top_tracks(username, numitems)
        return [ track['artist'] + ' - ' + track['name'] for track in tracks ]

def get_user_top_items(mode, user, *params): # params: limit, page
    method = getattr(lastfmget, 'user_top_' + str(mode)) # Ex. Mode.Artists -> lastfmget.user_top_artists
    topitems = method(user, *params)

def get_user_top_items_keys(mode):
    key1 = 'top' + str(mode)     # Ex: Mode.Artists -> 'topartists'
    key2 = str(mode).rstrip('s') # Ex: Mode.Artists -> 'artist'
    return key1, key2

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
