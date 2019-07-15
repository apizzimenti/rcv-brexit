
import json
from collections import OrderedDict

from Ranked import Election
from util import riffle


# The set of motions, as well as a variable that tells us whether our vote
# results will be randomized or not.
motions = ['B', 'C', 'D', 'E', 'G', 'H', 'K', 'L', 'O']
randomize = True

# Read in our json party information.
with open("./data/party-info.json", "r") as f:
    party_info = json.loads(f.read())

# Create a dictionary to specify parties' rankings.
rankings = { party: None for party in list(party_info) }

# We may want to adjust the preference data based on party, as some parties
# either don't vote on anything or only vote on a subset of all motions.
do_nothings = ["Deputy Speaker", "Sinn F?in", "Speaker"]
do_littles = [
    "Democratic Unionist Party",
    "Plaid Cymru",
    "Scottish National Party",
    "Green Party",
    "Liberal Democrat"
]

# For each party in our collected party data:
for party in party_info:
    # if that party doesn't ever do anything, either completely randomize their
    # results or delete them from the process.
    if party in do_nothings:
        if randomize:
            party_rank = list(party_info[party]["ranking"])
            riffle(party_rank)
            rankings[party] = party_rank
        else:
            del rankings[party]
 
    # If the party does a little and we're randomizing ballots, randomize the
    # unfilled portion of their ballot; otherwise, submit an exhaustible ballot.
    elif party in do_littles:
        voted_for = []
 
        if party == "Democratic Unionist Party":
            voted_for = ["O"]
        if party == "Plaid Cymru":
            voted_for = ["L", "D", "E", "G"]
        if party == "Scottish National Party":
            voted_for = ["L", "D", "G", "E"]
        if party == "Green Party":
            voted_for = ["L", "E", "G"]
        if party == "Liberal Democrat":
            voted_for = ["E", "L", "G", "D", "C"]
 
        if randomize:
            not_voted_for = list(set(motions) - set(voted_for))
            riffle(not_voted_for)
            voted_for = voted_for + not_voted_for
 
        rankings[party] = voted_for

    # Otherwise, the party ranking is just the order of the keys based on what
    # portion of the party voted *for* the motion.
    else:
        preferences = party_info[party]["ranking"]
        sorted_prefs = list(sorted(preferences, key=lambda g: -preferences[g]))
        rankings[party] = sorted_prefs

# Now we create a new Election object, add candidates and ballots, and
# simulate the election.
brexit = Election()
brexit.add_candidates(motions)

# Now, for each of the parties, we add a number of ballots equivalent to the
# membership of the party, each of which has an identical ranking.
for party in rankings:
    info = party_info[party]
    
    for _ in range(0, info["members"]):
        # We add ballots to each election. For the purpose of this
        # experiment, we want to add each party's number of ballots, all
        # with the same ranking.
        ballot = { "weight": 1, "ranking": rankings[party] }
        brexit.add_ballot(ballot)

brexit.single_winner_rcv()
# brexit.sankey()

with open("./data/winners.txt", "a") as f:
    f.write(f"{brexit.winner} ({brexit.droop(2, brexit.winner)})\n")
