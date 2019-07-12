
import pandas as pd
import pickle as pkl
import cursor
import sys
import json
import matplotlib.pyplot as plt
from collections import Counter

from util import diagnostics_for_encoding


# We are going to encode MP and party data as json so we don't have to recompute
# stuff over and over again.

# Try and get the filepath.
try:
    filepath = sys.argv[1]
except:
    filepath = "./data/votes/"

# First, we get the names of all the MPs and parties.
names_df = pd.read_csv(filepath + "402.csv")
names = list(names_df["Member"])
parties = list(set(names_df["Party"]))

# Then, create lists of dictionaries, each of which contains two keys: `name`,
# which is self-explanatory, and then `votes`, the set of votes on which each
# MP or party voted positively on.
mps = [{"name": name, "votes": set()} for name in names]
parties = [{"name": party, "votes": set()} for party in parties]

# Now, we want to build out our dataset. To do so, we iterate over the files
# containing vote data for each motion. Then, for each vote data file, we find
# the vote data for each MP and party.
first, last = 271, 689
bad = set([475, 520])
ranges = [
    list(range(0, 249)),
    list(range(250, 499)),
    list(range(500, 749)),
    list(range(750, 999))
]

dup_vote_collections = []

# Some diagnostic info.
pings = 0
total_pings = (len(names_df) + 12) * (last - first - (len(bad)))
cursor.hide()

for motion in range(first, last + 1):
    # For some reason they don't have records for votes 475 and 520.
    if motion in bad:
        continue

    # Read in the vote data.
    vote_data = pd.read_csv(filepath + f"{motion}.csv")

    # For each MP, we check whether they voted "Aye" on the given motion. If
    # they did, we add the motion number to the MP's set.
    for mp in mps:
        name = mp["name"]
        row = vote_data.loc[vote_data["Member"] == name]
        aye = "Aye" in list(row["Vote"]) or "No Vote Recorded" in list(row["Vote"])
        
        # Write out some progress stuff.
        pings += 1
        diagnostics_for_encoding(pings, total_pings, ranges)

        if aye:
            mp["votes"].add(motion)

    # For each party, we check whether more than two thirds of the party's
    # members voted "Aye" on the given motion. If they did, then we add the
    # motion number to the party's set.
    for party in parties:
        name = party["name"]
        rows = vote_data[vote_data["Party"] == party["name"]]
        ayes = rows[rows["Vote"].isin(["Aye", "No Vote Recorded"])]
        percent = len(ayes)/len(rows)

        # Write out some progress stuff.
        pings += 1
        diagnostics_for_encoding(pings, total_pings, ranges)

        if percent > 0.66:
            party["votes"].add(motion)

            if name == "Democratic Unionist Party":
                dup_vote_collections.append(percent)

print()
print("Writing files...")

# Now, since we literally never want to have to run this code again, we pickle
# everything and store it. In this case, we are going to pickle each file
# separately.
with open("./data/pickled-mps.pkl", "wb") as f:
    f.write(pkl.dumps(mps))

with open("./data/pickled-parties.pkl", "wb") as f:
    f.write(pkl.dumps(parties))

# We're done, so we can un-hide the cursor.
print("Complete.")
cursor.show()

print("the DUP voted like this:")

counts = Counter(dup_vote_collections)
sums = {
    ">90%": 0,
    "<90%": 0
}
for key in counts:
    if float(key) < 0.9:
        sums["<90%"] += counts[key]
    else:
        sums[">90%"] += counts[key]

print(json.dumps(counts, indent=2))
print(json.dumps(sums, indent=2))
pct = sums[">90%"]/(sums[">90%"] + sums["<90%"]) * 100
print(f"the dup voted with more than 90% of its members {pct}% of the time.")