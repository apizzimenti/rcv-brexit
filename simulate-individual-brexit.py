
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
from collections import Counter


try:
    os.remove("./data/winners.txt")
except OSError:
    pass

"""
num_elections = 1000

for _ in range(0, num_elections):
    sys.stdout.write(f" {round(((_ + 1)/num_elections) * 100, 3)}%\r")
    os.system("python individual-election.py ratio")

"""
weighting_types = [
    "intersection",
    "intersection-log2",
    "intersection-log10",
    "intersection-ln",
    "intersection-raw",
    "conditional",
    "conditional-log2",
    "conditional-log10",
    "conditional-ln",
    "conditional-raw",
    "ratio",
    "ratio-log2",
    "ratio-log10",
    "ratio-ln",
    "ratio-raw"
]

for weighting_type in weighting_types:
    os.system(f"python individual-election.py {weighting_type}")
print()

"""
winners = []

with open("./data/individual-winners.txt", "r") as f:
    winners = f.read().split("\n")

winners = winners[:-1]

seaborn.set()
series = pd.Series(winners)
series = series.value_counts()
series.plot(kind="bar", figsize=((5, 7)))
plt.savefig(f"./figures/individual-{num_elections}.png")

cc = Counter(winners)
won = cc.most_common(1)[0][1] / len(winners)
print(f"over {num_elections} elections, {cc.most_common(1)[0][0]} won {won * 100}% of the time.") 
"""