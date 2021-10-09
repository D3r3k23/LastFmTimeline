import enum
import math
import pickle
from dataclasses import dataclass
from datetime import datetime

import yaml

class MyEnum(enum.Enum):
    def __str__(self):
        return self.name.lower()

    @classmethod
    def from_str(cls, s):
        for member in list(cls):
            if s == str(member):
                return member
        return None

class Item(MyEnum):
    Artists = enum.auto()
    Albums  = enum.auto()
    Tracks  = enum.auto()

class Mode(MyEnum):
    Scrobbles = enum.auto()
    Rank      = enum.auto()

@dataclass(frozen=True)
class Chart:
    start: int
    end: int

    def date(self):
        return datetime.fromtimestamp(self.start)

    def __str__(self):
        return self.date().strftime('%m/%d/%y')

def chart_representer(dumper, chart):
    return yaml.ScalarNode('Chart', str(chart))

yaml.add_representer(Chart, chart_representer)

def dump_yaml(data, fn):
    with open(fn, 'w') as f:
        yaml.dump(data, f, sort_keys=False)

def dump_pickle(fn, data):
    with open(fn, 'wb') as f:
        pickle.dump(data, f)

def load_pickle(fn):
    with open(fn, 'rb') as f:
        return pickle.load(f)

def round_up(x, place):
    return int(math.ceil(x / place)) * place
