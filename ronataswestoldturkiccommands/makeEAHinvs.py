"""
Read aligned data in edictor/edicted.tsv
Input it to loanpy.recovery.get_invs
Write inventory to json-file
"""
import csv
import json

from loanpy.scminer import get_inventory

def register(parser):
    parser.add_argument("outname")

def run(args):
    """
    run analysis and store as json-file
    """
    with open(f"edictor/WOT2EAHedicted.tsv", "r") as f:
        out = get_inventory(list(csv.reader(f, delimiter="\t")))

    with open(f"loanpy/{args.outname}", "w+") as f:
        json.dump(out, f)
