
import requests
import sys

# Download all the voting data for the last ~250 votes in the House of
# Commons. Then, for each dataset, trim off the top 6 rows, and save to a
# csv file.
first_vote, last_vote = 271, 689
for vote_number in range(first_vote, last_vote+1):
    # Since each of the dowload URLs are made unique just by a number, we
    # can just iterate over a range, downloading and properly reformatting
    # the csv files as we go.
    url = f"https://commonsvotes.digiminster.com/Divisions/DownloadCSV/{vote_number}"
    r = requests.get(url)
    data = r.text.split("\n")[9:]
    sys.stdout.write(f"\rdownloaded file {vote_number-first_vote} of {last_vote-first_vote}")

    # Try to get the filepath. You can specify a desired directory for vote
    # record storage by running this program like
    #
    #   $ python retrieve-mp-vote-data directory/for/vote/data
    #
    # By default, this program will assume that vote data is stored in the
    # local `./data/votes/` directory.
    try:
        filepath = sys.argv[1]
    except:
        filepath = "./data/votes/"
    
    with open(filepath + f"{vote_number}.csv", "w") as f:
        f.write("\n".join(data))

print()  
