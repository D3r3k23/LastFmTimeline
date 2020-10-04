
from Week        import Week
from collections import OrderedDict, namedtuple

def get_username(LastFmGet):
    while True:
        username = input("Enter Last.fm username: ")
        print()
        if 'error' not in LastFmGet.user_info(username):
            return username

def get_mode():
    print("[1] Artists")
    print("[2] Albums")
    print("[3] Tracks")
    while True:
        try:
            answer = int(input("Enter which data to analyze (1-3): "))
            print()
        except ValueError:
            continue

        if answer == 1:
            return 'Artist'
        if answer == 2:
            return 'Album'
        if answer == 3:
            return 'Track'

def get_sort():
    print("[1] Scrobbles")
    print("[2] Rank")
    while True:
        try:
            answer = int(input("Enter which method to sort data (1-2): "))
            print()
        except ValueError:
            continue

        if answer == 1:
            return 'Scrobbles'
        if answer == 2:
            return 'Rank'

def get_num_items(mode):
    while True:
        try:
            numItems = int(input("Enter the number of " + mode + "s to include (0-100): "))
            print()
        except ValueError:
            continue

        if 0 < numItems <= 100:
            return numItems

# Returns a list of items from the user's profile
def get_items(LastFmGet, username, mode, numItems):
    if mode == 'Artist':
        dataMethod = LastFmGet.user_top_artists
        header1 = 'topartists'
        header2 = 'artist'
    elif mode == 'Album':
        dataMethod = LastFmGet.user_top_albums
        header1 = 'topalbums'
        header2 = 'album'
    elif mode == 'Track':
        dataMethod = LastFmGet.user_top_tracks
        header1 = 'toptracks'
        header2 = 'track'
    else:
        return 0

    itemData = dataMethod(username, numItems)
    items = [ item['name'] for item in itemData[header1][header2] ]
    return items

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
    if sort == 'rank':
        data = get_rank_data(charts, data) # ?

# Gets the user's scrobble data for each chart
def get_scrobble_data(LastFmGet, username, mode, charts, data):
    if mode == 'Artist':
        dataMethod = LastFmGet.user_weekly_artists_chart
        header1 = 'weeklyartistchart'
        header2 = 'artist'
    elif mode == 'Album':
        dataMethod = LastFmGet.user_weekly_albums_chart
        header1 = 'weeklyalbumchart'
        header2 = 'album'
    elif mode == 'Track':
        dataMethod = LastFmGet.user_weekly_tracks_chart
        header1 = 'weeklytrackchart'
        header2 = 'track'
    else:
        return 0

    for index, chart in enumerate(charts):
        if index != 0:
            prevChart = charts[index - 1]
            for itemData in data.values(): # Copy each item's value from the previous chart into the current chart
                itemData[chart] = itemData[prevChart]
            print("{:>2}%...".format(index / len(charts) * 100), end='')

        chartData = dataMethod(username, chart.start, chart.end)
        for item in chartData[header1][header2]: # Iterate over items in the user's data for the current chart
            itemName = item['name']
            if itemName in data:
                data[itemName][chart] += int(item['playcount']) # Add the current chart's scrobbles to the item's previous total

    return data

# Uses the scrobble data in data to create an ranked list for every chart, and puts the rank data back into data
def get_rank_data(charts, data):
    RankItem = namedtuple('RankItem', ['scrobbles', 'name'])

    for chart in charts:
        ranking = [ RankItem(scrobbles=itemData[chart], name=itemName) for itemName, itemData in data.items() ] # List of items and their scrobble count
        ranking.sort(key=lambda x: x.name) # Sort A-Z
        ranking.sort(key=lambda x: x.scrobbles, reverse=True) # Sort by number of scrobbles, descending
        for rank, item in enumerate(ranking, 1): # Store each items position in the list into data
            data[item.name][chart] = rank

    return data

def print_data(data):
    for itemName, itemData in data.items():
        print(itemName + ":")
        for week, entry in itemData.items():
            print("\t" + str(week) + ": " + str(entry))
