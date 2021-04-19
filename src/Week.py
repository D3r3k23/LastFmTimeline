
from datetime import datetime


# Stores start and end timestamps of a week
class Week:
    def __init__(self, start, end):
        self.start = start
        self.end   = end
    
    def date(self):
        return datetime.fromtimestamp(self.end)

    def __str__(self):
        return datetime.fromtimestamp(self.end).strftime('%m/%d/%y')

    def __eq__(self, other):
        return isinstance(other, type(self)) and (self.start, self.end) == (other.start, other.end)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.start, self.end))
