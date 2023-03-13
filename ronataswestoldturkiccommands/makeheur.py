"""
Read aligned data in edictor/edicted.tsv
Input it to loanpy.recovery.qfy
Write sound correspondence file .json
"""
from loanpy.recovery import get_heur
import json

def register(parser):
    parser.add_argument("outname")

def run(args):
    """
    run analysis and store as json-file
    """
    with open(f"loanpy/{args.outname}", "w+") as f:
        json.dump(get_heur(), f)
