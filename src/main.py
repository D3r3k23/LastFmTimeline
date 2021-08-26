import lastfmget
lastfmget.init('api_cfg.yaml')

from Util import *
from TimelineData import TimelineData
from LastFmTimeline import LastFmTimeline

import argparse

MAX_ITEMS = 100

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('user', help='Username')
    parser.add_argument('mode', type=Mode.from_str, choices=[ str(mode) for mode in list(Mode) ])
    parser.add_argument('sort', type=Sort.from_str, choices=[ str(sort) for sort in list(Sort) ])
    parser.add_argument('numitems', type=int, choices=range(1, MAX_ITEMS+1))
    args = parser.parse_args()

    data = TimelineData(args.user, args.mode, args.sort, args.numitems)

    timeline = LastFmTimeline(data)
    timeline.create()
    timeline.save('timeline.png')

if __name__ == '__main__':
    main()
