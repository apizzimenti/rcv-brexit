
import pandas as pd
import json
import sys

from util import pad_array


# Doing a better job collecting data. Eliminating any semblance of
# variance in the data collection process.

# Data was collected from commonsvotes.digiminister.com, which provides
# voting data for all the votes in the House of Commons. Here, we specify
# the vote numbers for each of the Brexit plans. Votes took place on two
# separate occasions: March 27th, 2019 and April 1st, 2019.

# NOTE: we skip the first vote on the "Common Market 2.0 (D)" plan because
# it's voted on again. We also do the same thing with the "Customs Union (C)"
# plan. We are abiding by our "most recent information" principle set out in
# (1.2), wherein we only consider the most recent vote data for motions voted
# on more than once.
vote_numbers = [655, 657, 659, 660, 662, 666, 667, 668, 669]
motions = ["B", "H", "K", "L", "O", "C", "D", "E", "G"]
motion_map = { motion: vote_numbers[i] for i, motion in enumerate(motions) }

# Try and get the filepath.
try:
    filepath = sys.argv[1]
except:
    filepath = "./data/votes/"

# Now, we want to go through each of the votes and collect data on them.
# To do this, we read in the proper csv file. Since we want to build a
# dictionary where party vote splits can be looked up by motion, this
# serves as nice way to do this, as each motion (at least each Brexit
# motion) was only voted on once in the selection of votes we look at.

# Collect the names of all the parties. Do this by reading in a random
# csv, selecting the names of the parties, and then getting rid of the
# dataframe.
pdf = pd.read_csv(filepath + "655.csv")
parties = list(set(pdf["Party"]))

# Create a dictionary to index votes.
votes = {motion: {**splits} for motion in motions}
rankings = {party: None for party in parties}
members = {party: None for party in parties}
info = {}

# We follow a simple procedure:
#
#   1.  for each motion:
#       1.  read the proper data into a dataframe;
#       2.  for each party:
#           1.  find the subframe of data belonging to the party:
#           2.  find the vote split for that party and add it to `votes`,
#               keyed by party;
#   2.  sort each of the party's rankings for votes;
#   3.  remove the vote split values;
#   4.  serialize the info and store it.

# (1)
for motion in motion_map:
    # (1.1)
    vote_number = motion_map[motion]
    vote_record = pd.read_csv(filepath + f"{vote_number}.csv")

    # (1.2)
    for party in parties:
        # (1.2.1)
        is_party = vote_record["Party"] == party
        subframe = vote_record[is_party]

        # (1.2.2)
        vote_type = ["Aye", "No", "No Vote Recorded"]
        split = pad_array(subframe["Vote"].value_counts(), vote_type)
        yes = split[0] / sum(split)
        compact = (motion, yes)
        votes[motion][party].append(compact)

        members[party] = sum(split)

# (2)
for vote in votes:
    for party in parties:
        votes[vote][party] = list(sorted(votes[vote][party], key= lambda g: -g[1]))
        # (3)
        rankings[party] = { vote[0]: vote[1] for vote in votes[vote][party] }
    break

for party in rankings:
    info[party] = { "members": int(members[party]), "ranking": rankings[party] }


# (4)
with open("./data/party-info.json", "w") as f:
    f.write(json.dumps(info, indent=2))
