
import math
import random
import sys


def pad_array(counts, options):
    desired = [0] * len(options)

    for i, option in enumerate(options):
        try:
            desired[i] = counts[option]
        except:
            pass

    return desired
    

def riffle(item):
    """
    Same as implemented in `Ranked`.

    :item: Thing to be shuffled.
    """
    shuffles = math.ceil((3/2) * math.log2(len(item)) + random.randrange(0, len(item)))

    for _ in range(0, shuffles):
        random.shuffle(item)


def diagnostics_for_encoding(pings, total_pings, ranges):
    pct_pings = f"({int((pings/total_pings) * 100)}%)"
        
    if pings % 1000 in ranges[0]:
        sys.stdout.write('\033[2K\033[1G')
        sys.stdout.write('\rEncoding data' + '\t\t' + pct_pings)
    elif pings % 1000 in ranges[1]:
        sys.stdout.write('\033[2K\033[1G')
        sys.stdout.write('\rEncoding data.' + '\t\t' + pct_pings)
    elif pings % 1000 in ranges[2]:
        sys.stdout.write('\033[2K\033[1G')
        sys.stdout.write('\rEncoding data..' + '\t\t' + pct_pings)
    else:
        sys.stdout.write('\033[2K\033[1G')
        sys.stdout.write('\rEncoding data...' + '\t' + pct_pings)
