from fetcher import DataCollection, DataEntry
import argparse
from scipy.stats.stats import pearsonr as scipyp
from copy import copy
from random import shuffle

def pearsonr(x, y):
    return scipyp(x, y)[0]

def false_correlation(e1, e2):
    try:
        p_long = pearsonr(e1.data, e2.data)
        p_short = pearsonr(e1.data[2:], e2.data[2:])
    except ValueError:
        return False
    return abs(p_short) > 0.95 and abs(p_long) < 0.2


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Finds false correlations in data directory and saves them in a file")
    parser.add_argument('-i', help="Directory containing data")
    parser.add_argument('-r', '--range', help="Range for corelations")

    args = parser.parse_args()

    db = DataCollection.read(args.i)

    start, end = map(int, args.range.split('-'))
    data = db.return_range(start, end)
    data = [e for e in data if 'ogółem' not in e.name and 'sektor' not in e.name]
    shuffle(data)
    print(len(data))

    with open('pairs.txt', 'w') as file:
        result = []

        file.write(args.range + "\n")

        try:
            for e1 in data:
                temp_data = copy(data)
                shuffle(temp_data)
                for e2 in temp_data:
                    if e1 is e2 or e1.region == e2.region:
                        continue
                    try:
                        p1 = pearsonr(e1.data, e2.data)
                        p2 = pearsonr(e1.data[2:], e2.data[2:])
                    except ValueError:
                        continue
                    if false_correlation(e1, e2):
                        file.write(f"{args.i}/{e1.res_id}/{e1.region}.json, {args.i}/{e2.res_id}/{e2.region}.json, {p1}, {p2}\n")
                        file.flush()
                        break
                        # print(f"Correlation between \n{e1.name} -- {e1.topic} \n {e2.name} -- {e2.topic} \n is {p}")
                        # print()
        except KeyboardInterrupt:
            pass
