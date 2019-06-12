import matplotlib.pyplot as plt
import os.path
from fetcher import DataEntry, DataCollection
from random import shuffle
from math import log10
import numpy as np

def simple_plot(e1: DataEntry, e2: DataEntry, text="", savename=None):
    # plt.xkcd()
    x = range(e1.start_year, e1.end_year)
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    mag_order1 = round(log10(e1.data[0]))
    mag_order2 = round(log10(e2.data[0]))

    ax1.plot(x, e1.data, c="r", label=e1.name[:e1.name.find('-')])
    ax1.ticklabel_format(useOffset=False)
    ax2.plot(x, e2.data, c="b", label=e2.name[:e2.name.find('-')])
    ax2.ticklabel_format(useOffset=False)
    ax1.legend(loc="upper right")
    ax2.legend(loc="upper left")
    ax1.set_xlabel('Rok')
    ax1.set_ylabel(e1.unit, c="r")
    ax2.set_ylabel(e2.unit, c="b")
    plt.title(f"Correlation between: {e1.region} - {e1.name} {e1.topic.split('-')[-1]} \n and \n {e2.region} - {e2.name} {e2.topic.split('-')[-1]}", wrap=True)

    if savename:
        fig = plt.gcf()
        fig.text(0.3, 0.1, text, fontsize=8)
        fig.set_size_inches((8, 8), forward=False)
        fig.savefig(savename)
        plt.close()

    else:
        plt.show()



if __name__ == "__main__":

    RESULT_PATH = 'results'
    REAL_RESULT_PATH = 'real_results'

    with open('pairs.txt') as file:
        start, end = map(int, file.readline().split('-'))
        
        i = 0
        for line in file:
            data = line.split(',')
            e1 = DataEntry.from_json(open(data[0].strip())).get_range(start + 2, end)
            e2 = DataEntry.from_json(open(data[1].strip())).get_range(start + 2, end)
            simple_plot(e1, e2, f"p1={data[2]}  p2={data[3]}", os.path.join(RESULT_PATH, f'{i}.png'))
            e3 = DataEntry.from_json(open(data[0].strip())).get_range(start, end)
            e4 = DataEntry.from_json(open(data[1].strip())).get_range(start, end)
            simple_plot(e3, e4, f"p1={data[2]}  p2={data[3]}", os.path.join(REAL_RESULT_PATH, f'{i}-real.png'))
            i += 1
