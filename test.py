
from math import log, exp
import matplotlib.pyplot as plt

from Election import Election


candidates = list(sorted(["A", "C", "B", "D"]))

ballots = [
    {
        "weight": 1,
        "ranking": ["A", "C", "B", "D"]
    },
    {
        "weight": 1,
        "ranking": ["C", "B", "A", "D"]
    },
    {
        "weight": 1,
        "ranking": ["C", "A", "B", "D"]
    },
    {
        "weight": 1,
        "ranking": ["A", "C", "B", "D"]
    },
    {
        "weight": 1,
        "ranking": ["B", "C", "A", "D"]
    },
    {
        "weight": 1,
        "ranking": ["D", "B", "C", "A"]
    }
]

winners = []
election = Election()
election.add_candidates(["A", "B", "C", "D"])
[election.add_ballot(ballot) for ballot in ballots]
election.single_winner_rcv_simulation()
election.sankey()
