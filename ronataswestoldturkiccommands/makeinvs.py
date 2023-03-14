"""
Read aligned data in edictor/edicted.tsv
Input it to loanpy.recovery.get_invs
Write inventory to json-file
"""
from loanpy.recovery import get_invs
import json

def register(parser):
    parser.add_argument("outname")

def run(args):
    """
    run analysis and store as json-file
    """
    with open(f"edictor/edicted.tsv", "r") as f:
        out = get_invs(f.read())

    with open(f"loanpy/{args.outname}", "w+") as f:
        json.dump(out, f)
