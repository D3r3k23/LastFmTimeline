import pickle

import plotly.express as px

from Util import *

def main():
    with open('data/timeline_data.pickle',  'rb') as f:
        data = pickle.load(f)

    fig = px.line(
        data_frame = data,
        x = 'date'
    )
    fig.show()

if __name__ == '__main__':
    main()
