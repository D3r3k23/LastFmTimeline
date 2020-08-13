
from time import time, sleep
import requests, requests_cache

requests_cache.install_cache()

API_URL       = 'http://ws.audioscrobbler.com/2.0/'
API_CALL_RATE = 5 # calls per second
API_CALL_INT  = 1 / API_CALL_RATE


# Interface class for requesting data from the last.fm API
class LastFmApi:
    # Initializes request data
    def __init__(self, key, userAgent, format='json'):
        self.key     = key
        self.headers = { 'user_agent': userAgent }
        self.format  = format

    # Appends API key and format to the payload and returns the formatted API Response
    def get_response(self, payload):
        payload['api_key'] = self.key
        payload['format']  = self.format

        self.rate_limiter()
        response = requests.get(API_URL, headers = self.headers, params = payload)

        if response.status_code != requests.codes.ok:
            print(response.text)
            return 0

        if not hasattr(self, 'lastApiCall') or 'from_cache' not in response:
            self.lastApiCall = time() # Updates time of last API call

        if self.format == 'json':
            return response.json()
        else:
            return response

    # Waits until the required interval between API calls is reached
    def rate_limiter(self):
        if hasattr(self, 'lastApiCall'):
            timeSince = time() - self.lastApiCall
            if timeSince < API_CALL_INT:
                sleep(API_CALL_INT - timeSince)


    # API Method Wrappers

    def user_info(self, user):
        payload = { "method": "user.getInfo",
                    "user"  : user }

        return self.get_response(payload)

    def user_recent_tracks(self, user, limit=50, page=1):
        payload = { "method": "user.getRecentTracks",
                    "user"  : user,
                    "limit" : limit,
                    "page"  : page }

        return self.get_response(payload)

    def user_top_artists(self, user, limit=50, page=1):
        payload = { "method": "user.getTopArtists",
                    "user"  : user,
                    "limit" : limit,
                    "page"  : page }

        return self.get_response(payload)

    def user_top_albums(self, user, limit=50, page=1):
        payload = { "method": "user.getTopAlbums",
                    "user"  : user,
                    "limit" : limit,
                    "page"  : page }

        return self.get_response(payload)

    def user_top_tracks(self, user, limit=50, page=1):
        payload = { "method": "user.getTopTracks",
                    "user"  : user,
                    "limit" : limit,
                    "page"  : page }

        return self.get_response(payload)

    def user_weekly_chart_list(self, user):
        payload = { "method": "user.getWeeklyChartList",
                    "user"  : user }

        return self.get_response(payload)

    def user_weekly_artists_chart(self, user, start=0, end=0):
        payload = { "method": "user.getWeeklyArtistChart",
                    "user"  : user,
                    "from"  : start,
                    "to"    : end }

        return self.get_response(payload)

    def user_weekly_albums_chart(self, user, start=-1, end=-1):
        payload = { "method": "user.getWeeklyAlbumChart",
                    "user"  : user,
                    "from"  : start,
                    "to"    : end }

        return self.get_response(payload)

    def user_weekly_tracks_chart(self, user, start=-1, end=-1):
        payload = { "method": "user.getWeeklyTrackChart",
                    "user"  : user,
                    "from"  : start,
                    "to"    : end }

        return self.get_response(payload)
