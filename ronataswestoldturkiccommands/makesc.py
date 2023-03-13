"""
Read aligned data in edictor/edicted.tsv
Input it to loanpy.recovery.qfy
Write sound correspondence file .json
"""
from loanpy.recovery import qfy
import json

def register(parser):
    parser.add_argument("inname")
    parser.add_argument("outname")
    parser.add_argument("heurname", nargs="?")

def run(args):
    with open(f"edictor/{args.inname}", "r") as f:
        out = qfy(f.read(), args.heurname)
    # store as json-file
    with open(f"edictor/{args.outname}", "w+") as f:
        json.dump(out, f)
