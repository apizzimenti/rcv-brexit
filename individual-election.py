
import pickle as pkl
import json
import sys
from math import log, log2
from collections import Counter
import random

from Election import Election
from util import riffle


# Do we want to randomize exhaustible ballots?
randomize = False

# Here, we choose the way we weight each of the probabilities outlined in REFERENCE!!!
weighting_types = set([
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
])

# Here, we want to abide by the procedure outlined in (1.4.2). First, we get the
# data from the MPs and parties.
with open("./data/pickled-mps.pkl", "rb") as f:
    mps = pkl.load(f)

with open("./data/pickled-parties.pkl", "rb") as f:
    parties = pkl.load(f)

# Create our sample space; call this sample space `M` for Motions. `bad` is just
# the set of motions for which we have no or corrupted vote data.
first, last, bad = 402, 689, set([475, 520])
M = set(list(range(first, last + 1))) - bad

# Find the preference lists for each of the parties.
with open("./data/party-info.json", "r") as f:
    party_info = json.loads(f.read())

# Now, we want to define, for MPs, parties, and motions, what conditional
# probability looks like. We use conditional probability because just taking
# the intersection of the party and the MP will artificially weight parties who
# vote positively on lots of stuff. First, though, we define a function to
# compute probability.
def probability(Ω, A):
    """
    Returns the probability of an event A.

    :Ω:         The sample space.
    :A:         An event; a subset of Ω.
    :returns:   A number in [0, 1].
    """
    return len(A) / len(Ω)

# Now, based on our earlier probability measure, we can create a new one
# defining conditional probability.
def conditional(Ω, A, B):
    """
    Returns the conditional probability of A and B; i.e. returns P(A|B). Note
    that, in most all of these use cases, that A and B are not independent.

    :Ω:         The sample space.
    :A:         An event; a subset of Ω.
    :B:         An event; a subset of Ω.
    :returns:   A number in [0, 1].
    """
    probB = probability(Ω, B)
    return probability(Ω, A&B) / probB if probB != 0 else 0


def determine_weight(size, choice, Ω, A, B):
    """
    Determines the weight applied to a given party based on some probability
    and party size.
    """
    intersection = probability(Ω, A & B)
    # The conditional probability can be modified by interchanging B and A.
    cond = conditional(Ω, B, A)
    xor = probability(Ω, A ^ B)
    ratio = probability(Ω, A & B) / xor if xor != 0 else 0

    if choice not in weighting_types:
        print("Invalid weighting type. Defaulting to `intersection`.")
        return intersection

    if choice == "intersection":
        weight = intersection
    elif choice == "intersection-log2":
        weight = log2(size) * intersection
    elif choice == "intersection-log10":
        weight = log(size, 10) * intersection
    elif choice == "intersection-ln":
        weight = log(size) * intersection
    elif choice == "intersection-raw":
        weight = size * intersection
    elif choice == "conditional":
        weight = cond
    elif choice == "conditional-log2":
        weight = log2(size) * cond
    elif choice == "conditional-log10":
        weight = log(size, 10) * cond
    elif choice == "conditional-ln":
        weight = log(size) * cond
    elif choice == "conditional-raw":
        weight = size * cond
    elif choice == "ratio":
        weight = ratio
    elif choice == "ratio-log2":
        weight = log2(size) * ratio
    elif choice == "ratio-log10":
        weight = log(size, 10) * ratio
    elif choice == "ratio-ln":
        weight = log(size) * ratio
    elif choice == "ratio-raw":
        weight = size * ratio

    return weight


# Denote these for the next step.
do_nothings = set(["Deputy Speaker", "Sinn F?in", "Speaker"])
do_littles = set([
    "Democratic Unionist Party",
    "Plaid Cymru", 
    "Scottish National Party",
    "Green Party"
])

# Get the weighting type.
try:
    weighting_type = sys.argv[1]
except Exception:
    weighting_type = "intersection"

# Now, we can go about calculating the weights for each of the individual MPs.
# This weighting is based on that outlined in (1.4.2).
for i, mp in enumerate(mps):
    ranking = []

    # Find the weight for each party. There are a number of weighting schemes,
    # and choosing one over the other can drastically change the results of this
    # simulated election.
    for party in parties:
        name = party["name"]

        if name not in do_nothings:
            members = party_info[name]["members"]
            A, B = mp["votes"], party["votes"]
            weight = determine_weight(members, weighting_type, M, A, B)
            ranking.append((party["name"], weight))

    ranking = list(reversed(sorted(ranking, key=lambda g: g[1])))
    mp["ranking"] = { party[0]: party[1] for party in ranking }


# Do a bit on randomizing ballot orders.
if randomize:
    for party in parties:
        name = party["name"]
        if name in do_littles or name in do_nothings:
            ranking = party_info[name]["ranking"]
            unranked = [k for k in ranking if ranking[k] == 0]
            sup = min([ranking[k] for k in ranking if ranking[k] > 0], default=1)

            for plan in unranked:
                ranking[plan] = random.uniform(0, sup)


# Now we actually need to weight each of the plans. There are a number of
# nuances that go into this weighting, especially if a plan isn't given a
# ranking (by one of the parties).
plans = ["B", "H", "K", "L", "O", "C", "D", "E", "G"]
brexit = Election()
brexit.add_candidates(plans)
ballots = []

mean_mps = []
mean_rankings = []

# This weighting method is described in part in (2.2.3) and in detail in
# (B.1.7).
for mp in mps:
    sum_weights = { plan: 0 for plan in plans }

    for party in party_info:
        # If the MP doesn't rank a party at all, they have a weight of 0.
        mp_weight = mp["ranking"].get(party, 0)

        for plan in plans:
            # If a party doesn't rank a plan, they give it a score of 0.
            party_weight = party_info[party]["ranking"].get(plan, 0)
            sum_weights[plan] += mp_weight * party_weight
    

    # Then we just sort the ballots and throw them into the election.
    mp_prefs = list(sorted(sum_weights, key=lambda g: -sum_weights[g]))
    ballot = { "weight": 1, "ranking": mp_prefs }
    brexit.add_ballot(ballot)

    # Some more interesting info.
    mean_mps.append(sum_weights)
    mean_rankings.append(tuple(mp_prefs))


# Do a fun little activity where we return the mean MP and most common ranking
# in this election.
total_mps = len(mean_mps)
avg_mp = { plan: 0 for plan in plans }

for mp in mean_mps:
    for plan in mp:
        avg_mp[plan] += mp[plan] / total_mps

# Get the mode ballot ranking.
mode = Counter(mean_rankings)

"""
print("average MP:")
print(json.dumps(avg_mp, indent=2))
print()
print("most common ballot ranking:")
print(mode.most_common()[0])
"""

# Run the simulation and spit out json to feed into https://sankey.csaladen.es/.
brexit.single_winner_rcv_simulation()
brexit.sankey(f"./figures/{weighting_type}-sankey.json")

# Write the winner (and whether the winner met the drop quota) to a file (for
# simulation purposes).
with open("./data/individual-winners.txt", "a") as f:
    f.write(f"{brexit.winner} ({brexit.droop(2, brexit.winner)})\n")
