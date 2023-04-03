"""
Read aligned data in edictor/edicted.tsv
Input it to loanpy.recovery.qfy
Write sound correspondence file .json
"""

import csv
import json

from loanpy.scminer import get_correspondences

def register(parser):
    parser.add_argument("srclg")
    parser.add_argument("tgtlg")
    parser.add_argument("heur", nargs="?")

def run(args):
    if args.heur:
        with open(f"loanpy/{args.heurname}", "r") as f:
            args.heur = json.load(f)
    with open(f"edictor/{args.srclg}2{args.tgtlg}edicted.tsv", "r") as f:
        tsv = list(csv.reader(f, delimiter="\t"))
        out = get_correspondences(tsv, args.heur)
    # store as json-file
    with open(f"loanpy/{args.srclg}2{args.tgtlg}sc0.json", "w+") as f:
        json.dump(out, f)
