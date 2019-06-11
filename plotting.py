import matplotlib.pyplot as plt
from fetcher import DataEntry, DataCollection
from random import shuffle
from math import log10

def simple_plot(e1: DataEntry, e2: DataEntry):
    plt.plot(range(e1.start_year, e1.end_year), [i / 10 ** round(log10(i)) for i in e1.data])
    plt.plot(range(e2.start_year, e2.end_year), [i / 10 ** round(log10(i)) for i in e2.data])
    plt.show()


if __name__ == "__main__":
    db = DataCollection.read('data2')
    res = db.return_range(2000, 2010)
    print(len(res))
    res = [e for e in res if len(e.data) == e.end_year - e.start_year]
    print(len(res))
    shuffle(res)
    e1 = res[0]
    e2 = res[1]
    simple_plot(e1, e2)
