"""
Read aligned data in edictor/edicted.tsv
Input it to loanpy.recovery.qfy
Write sound correspondence file .json
"""
from loanpy.scminer import get_correspondences
from json import load, dump

def register(parser):
    parser.add_argument("inname")
    parser.add_argument("outname")
    parser.add_argument("heurname", nargs="?")

def run(args):
    with open(f"loanpy/{args.heurname}", "r") as f:
        heur = load(f)
    with open(f"edictor/{args.inname}", "r") as f:
        tsv = [row.strip().split("\t") for row in f.read().strip().split("\n")]
        out = get_correspondences(tsv, heur)
    # store as json-file
    with open(f"loanpy/{args.outname}", "w+") as f:
        dump(out, f)
