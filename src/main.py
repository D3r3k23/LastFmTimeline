import argparse
import enum

class Mode(enum.Enum):
    Artists = enum.auto()
    Albums  = enum.auto()
    Tracks  = enum.auto()

class Sort(enum.Enum):
    Scrobbles = enum.auto()
    Rank      = enum.auto()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('user',  type=str,  help='Username')
    parser.add_argument('mode',  type=Mode, help='artists, albums, tracks')
    parser.add_argument('sort',  type=Sort, help='scrobbles, rank')
    parser.add_argument('items', type=int,  help='Number of items to display')
    args = parser.parse_args()



if __name__ == '__main__':
    main()
