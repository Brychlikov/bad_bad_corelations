import matplotlib.pyplot as plt
import os.path
from fetcher import DataEntry, DataCollection
from random import shuffle
from math import log10
import numpy as np

def simple_plot(e1: DataEntry, e2: DataEntry, savename=None):
    # plt.xkcd()
    x = range(e1.start_year, e1.end_year)
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(x, [i / 10 ** round(log10(i)) for i in e1.data], c="r", label=e1.name)
    ax2.plot(x, [i / 10 ** round(log10(i)) for i in e2.data], c="b", label=e2.name)
    ax1.legend(loc="upper right")
    ax2.legend(loc="upper left")
    ax1.set_xlabel('Rok')
    ax1.set_ylabel(e1.unit, c="r")
    ax2.set_ylabel(e2.unit, c="b")
    plt.title(f"Correlation between: {e1.name} {e1.topic} \n and {e2.name} {e2.topic}", wrap=True)

    if savename:
        fig = plt.gcf()
        fig.set_size_inches((8, 8), forward=False)
        fig.savefig(savename)

    else:
        plt.show()



if __name__ == "__main__":

    RESULT_PATH = 'results'

    
    i = 0
    for line in open('good_pairs.txt'):
        data = line.split(',')
        e1 = DataEntry.from_json(open(f'data2/{data[0].strip()}/POLSKA.json')).get_range(2000, 2010)
        e2 = DataEntry.from_json(open(f'data2/{data[1].strip()}/POLSKA.json')).get_range(2000, 2010)
        simple_plot(e1, e2, os.path.join(RESULT_PATH, f'{i}.png'))
        i += 1

    # pair = (3146, 2131)
    # e1 = DataEntry.from_json(open(f'data2/{pair[0]}/POLSKA.json')).get_range(2000, 2010)
    # e2 = DataEntry.from_json(open(f'data2/{pair[1]}/POLSKA.json')).get_range(2000, 2010)
    # db = DataCollection.read('data2')
    # res = db.return_range(2000, 2010)
    #
    # print(len(res))
    # res = [e for e in res if len(e.data) == e.end_year - e.start_year]
    # print(len(res))
    # shuffle(res)
    # e1 = res[0]
    # e2 = res[1]
    simple_plot(e1, e2)
