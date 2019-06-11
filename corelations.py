from fetcher import DataCollection, DataEntry
from scipy.stats.stats import pearsonr as scipyp

def pearsonr(x, y):
    return scipyp(x, y)[0]

db = DataCollection.read('data2')

data = db.return_range(2000, 2010)
data = [e for e in data if 'ogółem' not in e.name and 'sektor' not in e.name]
print(len(data))
input()

result = []

try:
    for e1 in data:
        for e2 in data:
            if e1 is e2 or e1.region == e2.region:
                continue
            try:
                p = pearsonr(e1.data, e2.data)
                p2 = pearsonr(e1.data[2:], e2.data[2:])
            except ValueError:
                continue
            if p > 0.95:
                result.append((p2, p, (e1, e2)))
                print(f"Correlation between \n{e1.name} -- {e1.topic} \n {e2.name} -- {e2.topic} \n is {p}")
                print()
except KeyboardInterrupt:
    pass

print("corelaitons ended")
print("====================================================================================================")
result.sort(key=lambda i: abs(i[0]))
for p1, p2, (e1, e2) in result[:200]:
    print(f"{e1.name} -- {e1.topic}\n{e2.name} -- {e2.topic}\nCorrelations {p1} and {p2}\n\n")
    print(repr(e1))
