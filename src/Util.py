"""
Utility Enums for configuring the timeline,
& getting user input
"""

import enum
import math

class Mode(enum.Enum):
    Artists = enum.auto()
    Albums  = enum.auto()
    Tracks  = enum.auto()

class Sort(enum.Enum):
    Scrobbles = enum.auto()
    Rank      = enum.auto()

def round_up(x, place):
    return int(math.ceil(x / place)) * place
