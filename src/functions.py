
from Week        import Week
from collections import OrderedDict, namedtuple



# Loads the user's scrobble data into data, and if sort is rank then converts data into rank data
def load_data(LastFmGet, username, mode, sort, charts, data):
    data = get_scrobble_data(LastFmGet, username, mode, charts, data)
    if sort is Sort.RANK:
        data = create_rank_data(charts, data)

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


