
from Week        import *
from collections import namedtuple


def get_username(LastFmGet):
    while True:
        username = input("Enter username: ")
        if "error" not in LastFmGet.user_info(username):
            return username

def get_mode():
    print("[1] Artists")
    print("[2] Albums")
    print("[3] Tracks")
    while True:
        try:
            answer = int(input("Enter which data to analyze (1-3): "))
            if answer == 1:
                return "Artist"
            elif answer == 2:
                return "Album"
            elif answer == 3:
                return "Track"
        except ValueError:
            continue

def get_sort():
    print("[1] Scrobbles")
    print("[2] Rank")
    while True:
        try:
            answer = int(input("Enter which method to sort data (1-2): "))
            if answer == 1:
                return "Scrobbles"
            elif answer == 2:
                return "Rank"
        except ValueError:
            continue

def get_num_items(mode):
    while True:
        try:
            numItems = int(input("Enter the number of " + mode + "s to include (0-200): "))
        except ValueError:
            continue
        if numItems in range(0, 201):
            return numItems

# Returns list of weeks to analyze
def get_target_charts(LastFmGet, username):
    firstPage     = LastFmGet.user_recent_tracks(username, 200, 1)
    totalPages    = int(firstPage["recenttracks"]["@attr"]["totalPages"])
    lastPage      = LastFmGet.user_recent_tracks(username, 200, totalPages)
    firstScrobble = int(lastPage["recenttracks"]["track"][-1]["date"]["uts"])

    charts = []
    chartsData = LastFmGet.user_weekly_chart_list(username)
    for chart in chartsData["weeklychartlist"]["chart"]:
        start = int(chart["from"])
        end   = int(chart["to"])
        if firstScrobble <= end:
            charts.append(Week(start, end))

    return charts

#
def get_items(LastFmGet, username, mode, numItems):
    if mode == "Artist":
        dataMethod = LastFmGet.user_top_artists
        header1 = "topartists"
        header2 = "artist"
    elif mode == "Album":
        dataMethod = LastFmGet.user_top_albums
        header1 = "topalbums"
        header2 = "album"
    elif mode == "Track":
        dataMethod = LastFmGet.user_top_tracks
        header1 = "toptracks"
        header2 = "track"

    items = dataMethod(username, numItems)
    return items[header1][header2]

def init_data(charts, items, data):
    for item in items:
        itemName = item["name"]
        data[itemName] = {}
        for chart in charts:
            data[itemName][chart] = 0

def load_data(LastFmGet, username, mode, sort, charts, data):
    data = get_scrobble_data(LastFmGet, username, mode, charts, data)
    if sort == "rank":
        data = get_rank_data(charts, data)


def get_scrobble_data(LastFmGet, username, mode, charts, data):
    if mode == "Artist":
        dataMethod = LastFmGet.user_weekly_artists_chart
        header1 = "weeklyartistchart"
        header2 = "artist"
    elif mode == "Album":
        dataMethod = LastFmGet.user_weekly_albums_chart
        header1 = "weeklyalbumchart"
        header2 = "album"
    elif mode == "Track":
        dataMethod = LastFmGet.user_weekly_tracks_chart
        header1 = "weeklytrackchart"
        header2 = "track"

    for index, chart in enumerate(charts):
        if index != 0:
            prevChart = charts[index - 1]
            for itemData in data.values():
                itemData[chart] = itemData[prevChart]

        chartData = dataMethod(username, chart.start, chart.end)
        for item in chartData[header1][header2]:
            itemName = item["name"]
            if itemName in data:
                data[itemName][chart] += int(item["playcount"])

    return data

def get_rank_data(charts, data):
    RankItem = namedtuple("RankItem", ["scrobbles", "name"])

    for chart in charts:
        ranking = [ RankItem(scrobbles=itemData[chart], name=itemName) for itemName, itemData in data.items() ]
        ranking.sort(key=lambda x: x.name)
        ranking.sort(key=lambda x: x.scrobbles, reverse=True)
        for index, item in enumerate(ranking):
            data[chart][item.name] = index + 1

    return data

def print_data(data):
    for itemName, itemData in data.items():
        print(itemName + ":")
        for week, entry in itemData.items():
            print("\t" + str(week) + ": " + str(entry))
