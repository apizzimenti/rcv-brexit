
# Ranked Choice Voting and Brexit
This repository is the home for code used
[in this paper.](http://bit.ly/2LlQ1W0)

## Setup
To set up this set of scripts, run `make setup`. This will create a `data/`
directory and install the [`Ranked`](https://github.com/apizzimenti/Ranked.git)
package. Make sure to visit the [repository for the package](https://github.com/apizzimenti/Ranked.git) for more instructions. You can also run the
`retrieve-mp-vote-data.py` script to download the vote files required.

Note that, to run any of the election scripts, you *must* download vote data,
then run the encoding scripts.

## Directory
Below is a directory for each script.
```
    brexit/
    |- encode-all-vote-data.py (Encodes vote data for individual MPs.)
    |- encode-party-preference-data.py (Encode party preference data.)
    |- individual-election.py (Election with individual preference data.)
    |- party-election.py (Election with party data only.)
    |- retrieve-mp-vote-data.py (Downloads the set of votes for encoding.)
    |- simulate-individual-brexit.py (Runs a bunch of individual elections.)
    |- simulate-party-brexit.py (Runs a bunch of party elections.)
    |- test.py (Some tests for the tabulator.)
    |- util.py (Some nice helper functions.)
    |- data/
        |- votes/ (Voting data; only used after retrieving vote data.)
```
