import enum
import math

class MyEnum(enum.Enum):
    def __str__(self):
        return self.name.lower()

    @classmethod
    def from_str(cls, s):
        for member in list(cls):
            if s == str(member):
                return member
        return None

class Mode(MyEnum):
    Artists = enum.auto()
    Albums  = enum.auto()
    Tracks  = enum.auto()

class Sort(MyEnum):
    Scrobbles = enum.auto()
    Rank      = enum.auto()

def round_up(x, place):
    return int(math.ceil(x / place)) * place
