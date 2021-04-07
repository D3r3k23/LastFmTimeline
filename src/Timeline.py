"""Creates a timeline from TimelineData"""

import LastFmApi
from TimelineData import TimelineData

class Timeline:
    def __init__(self, data: TimelineData):
        self.data = data
