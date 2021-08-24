import lastfmget
lastfmget.init('api_cfg.yaml')

from Util import *
from TimelineData import TimelineData
from LastFmTimeline import LastFmTimeline

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('user',  type=str,  help='Username')
    parser.add_argument('mode',  type=Mode, help='artists, albums, tracks')
    parser.add_argument('sort',  type=Sort, help='scrobbles, rank')
    parser.add_argument('items', type=int,  help='Number of items to display')
    args = parser.parse_args()

    data = TimelineData(args.user, args.mode, args.sort, args.items)

    timeline = LastFmTimeline(data)
    timeline.create()
    timeline.save('timeline.png')

if __name__ == '__main__':
    main()
