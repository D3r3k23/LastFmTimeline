
from Week        import Week
from collections import OrderedDict, namedtuple
from math        import ceil


# Returns a list of items from the user's profile
def get_items(LastFmGet, username, mode, numItems):
    dataMethod, key1, key2 = get_user_top_items_args(LastFmGet, mode)

    itemData = dataMethod(username, numItems)
    items = [ item['name'] for item in itemData[key1][key2] ]
    return items

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

# Returns list of charts available in the user's history
def get_target_charts(LastFmGet, username):
    firstPage     = LastFmGet.user_recent_tracks(username, 100, 1)
    totalPages    = int(firstPage['recenttracks']['@attr']['totalPages'])
    lastPage      = LastFmGet.user_recent_tracks(username, 100, totalPages)
    firstScrobble = int(lastPage['recenttracks']['track'][-1]['date']['uts'])

    charts = []
    chartsData = LastFmGet.user_weekly_chart_list(username)
    for chart in chartsData['weeklychartlist']['chart']:
        start = int(chart['from'])
        end   = int(chart['to'])
        if end >= firstScrobble:
            charts.append(Week(start, end))

    return charts

# Initializes the data dict with item names as keys and dicts as values, with charts as keys and scrobbles as values
def init_data(items, charts, data):
    for item in items: # Creates a dict for each item
        data[item] = OrderedDict()
        for chart in charts: # Adds each chart as a key and initializes its value
            data[item][chart] = 0

# Loads the user's scrobble data into data, and if sort is rank then converts data into rank data
def load_data(LastFmGet, username, mode, sort, charts, data):
    data = get_scrobble_data(LastFmGet, username, mode, charts, data)
    if sort is Sort.RANK:
        data = create_rank_data(charts, data) # data is not used?

# Gets the user's scrobble data for each chart
def get_scrobble_data(LastFmGet, username, mode, charts, data):
    dataMethod, key1, key2 = get_user_weekly_items_chart_args(LastFmGet, mode)

    for i, chart in enumerate(charts):
        if i > 0:
            prevChart = charts[i - 1]
            for itemData in data.values(): # Copy each item's value from the previous chart into the current chart
                itemData[chart] = itemData[prevChart]

        chartData = dataMethod(username, chart.start, chart.end)
        for item in chartData[key1][key2]: # Iterate over items in the user's data for the current chart
            itemName = item['name']
            if itemName in data:
                data[itemName][chart] += int(item['playcount']) # Add the current chart's scrobbles to the item's previous total

    return data

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

# Uses the scrobble data in data to create an ranked list for every chart, and puts the rank data back into data
def create_rank_data(charts, data):
    RankItem = namedtuple('RankItem', ['scrobbles', 'name'])

    for chart in charts:
        ranking = [ RankItem(scrobbles=itemData[chart], name=itemName) for itemName, itemData in data.items() ] # List of items and their scrobble count
        ranking.sort(key=lambda x: x.name) # Sort A-Z
        ranking.sort(key=lambda x: x.scrobbles, reverse=True) # Sort by number of scrobbles, descending
        for rank, item in enumerate(ranking, 1): # Store each items position in the list into data
            data[item.name][chart] = rank

    return data


def round_up(x, place):
    return int(ceil(x / place)) * place

def print_data(data):
    for itemName, itemData in data.items():
        print(itemName + ':')
        for week, entry in itemData.items():
            print('\t' + str(week) + ': ' + str(entry))
