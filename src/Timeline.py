"""Creates a timeline plot from TimelineData"""

from TimelineData import TimelineData

from matplotlib import pyplot, dates

class Timeline:
    def __init__(self, data):
        self.data = data
