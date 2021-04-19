"""
Utility Enums for configuring the timeline,
& getting user input
"""

from enum import Enum

class Mode(Enum):
    """Which type of Last.fm data to use"""
    ARTIST = 1
    ALBUM  = 2
    TRACK  = 3

    def __str__(self):
        if self is Mode.ARTIST:
            return 'Artist'
        if self is Mode.ALBUM:
            return 'Album'
        if self is Mode.TRACK:
            return 'Track'

class Sort(Enum):
    """How to sort the data"""
    SCROBBLES = 1
    RANK      = 2

    def __str__(self):
        if self is Sort.SCROBBLES:
            return 'Scrobbles'
        if self is Mode.RANK:
            return 'Rank'


def get_username(LastFmGet):
    while True:
        username = input('Enter Last.fm username: ')
        print()
        if 'error' not in LastFmGet.user_info(username):
            return username

def get_mode():
    print('[1] Artists')
    print('[2] Albums')
    print('[3] Tracks')
    while True:
        try:
            answer = int(input('Enter which data to analyze (1-3): '))
            print()
        except ValueError:
            continue

        if answer == 1:
            return Mode.ARTIST
        if answer == 2:
            return Mode.ALBUM
        if answer == 3:
            return Mode.TRACK

def get_sort():
    print('[1] Scrobbles')
    print('[2] Rank')
    while True:
        try:
            answer = int(input('Enter which method to sort data (1-2): '))
            print()
        except ValueError:
            continue

        if answer == 1:
            return Sort.SCROBBLES
        if answer == 2:
            return Sort.RANK

def get_num_items(mode):
    while True:
        try:
            numItems = int(input('Enter the number of ' + str(mode) + 's to include (0-100): '))
            print()
        except ValueError:
            continue

        if 1 <= numItems <= 100:
            return numItems

# Gets API method and keys for last.fm user top items API call
def get_user_top_items_args(LastFmGet, mode):
    if mode is Mode.ARTIST:
        dataMethod = LastFmGet.user_top_artists
        key1 = 'topartists'
        key2 = 'artist'
    elif mode is Mode.ALBUM:
        dataMethod = LastFmGet.user_top_albums
        key1 = 'topalbums'
        key2 = 'album'
    elif mode is Mode.TRACK:
        dataMethod = LastFmGet.user_top_tracks
        key1 = 'toptracks'
        key2 = 'track'
    else:
        return None

    return dataMethod, key1, key2

# Gets API method and keys for last.fm user weekly items chart API call 
def get_user_weekly_items_chart_args(LastFmGet, mode):
    if mode is Mode.ARTIST:
        dataMethod = LastFmGet.user_weekly_artists_chart
        key1 = 'weeklyartistchart'
        key2 = 'artist'
    elif mode is Mode.ALBUM:
        dataMethod = LastFmGet.user_weekly_albums_chart
        key1 = 'weeklyalbumchart'
        key2 = 'album'
    elif mode is Mode.TRACK:
        dataMethod = LastFmGet.user_weekly_tracks_chart
        key1 = 'weeklytrackchart'
        key2 = 'track'
    else:
        return None

    return dataMethod, key1, key2
