"""
Read col ALIGNMENTS in edicted.csv
Find all the suffixes (beind the plus signs)
Write to edictor/suffixes.json
"""

import json

def run(args):
    """
    """

    suffixes = set()
    with open("edictor/edicted.tsv", "r") as f:
        for row in f.read().split("\n"):
            print(row.split("\t"))
            try:
                suffixes.add(row.split("\t")[2].split(" + ")[1])
            except IndexError:
                pass

    with open('loanpy/suffixes.json', 'w+') as f:
        f.write(json.dumps(list(suffixes)))
