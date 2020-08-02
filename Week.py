
from datetime import datetime


# Stores a month and year
class Week:
    def __init__(self, start, end):
        self.start = start
        self.end   = end
        self.date  = datetime.fromtimestamp(end).strftime("%m/%d/%y")

    def __str__(self):
        return self.date

    def __eq__(self, other):
        return isinstance(other, type(self)) and (self.start, self.end) == (other.start, other.end)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.start, self.end))
