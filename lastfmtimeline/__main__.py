import argparse

import lastfmget
lastfmget.init('api_cfg.yaml')

from Util import *
from TimelineData import TimelineData
from LastFmTimeline import LastFmTimeline

MAX_ITEMS = 100

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('user')
    parser.add_argument('--item_type',   '-i', type=Item.from_str, default=Item.Artists,   choices=[ mode for mode in list(Item) ])
    parser.add_argument('--mode',        '-m', type=Mode.from_str, default=Mode.Scrobbles, choices=[ sort for sort in list(Mode) ])
    parser.add_argument('--num_items',   '-n', type=int, default=10, choices=range(1, MAX_ITEMS+1), metavar=f'[1, {MAX_ITEMS}]')
    parser.add_argument('--display',     '-d', action='store_true')
    parser.add_argument('--timeline_fn', '-s', default=None, help='.png')
    args = parser.parse_args()

    print('Creating timeline:')
    print(f'  username:  {args.user}')
    print(f'  item type: {args.item_type}')
    print(f'  mode:      {args.mode}')
    print(f'  num items: {args.num_items}')
    timeline = create_timeline(args.user, args.item_type, args.mode, args.num_items)

    # if args.display:
    #     timeline.display()
    
    # if args.timeline_fn:
    #     timeline.save(f'data/{args.timeline_fn})
    #     print(f'Timeline saved to: {args.timeline_fn}')

def create_timeline(username, itemtype, mode, numitems):
    print('Loading timeline data')
    data = TimelineData(username, itemtype, numitems)
    print(f'Number of charts to load: {len(data.charts)}')
    data.load()
    data.dump('data/timeline_data.pickle')
    data.print('data/timeline_data.yaml')

    if mode == Mode.Rank:
        data.convert_to_rank()
        data.print('data/timeline_rankdata.yaml')

    print('Creating timeline')
    timeline = LastFmTimeline(data.get(), itemtype, mode, numitems)
    timeline.create()

    # return timeline

    return None

if __name__ == '__main__':
    main()
