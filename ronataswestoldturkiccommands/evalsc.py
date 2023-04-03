"""
read edicted.tsv
read heuristics file
indicate adapt= True or False
specify guesslist
indicate prosody= True or False
"""

import ast
import json
import csv
from loanpy.eval_sca import eval_all

def register(parser):
    parser.add_argument("srclg")
    parser.add_argument("tgtlg")
    parser.add_argument("guesslist", nargs="?")
    parser.add_argument("adapt", nargs="?")
    parser.add_argument("prosody", nargs="?")
    parser.add_argument("heur", nargs="?")

def run(args):
    """
    """
    # load sound correspondence file
    with open(f"edictor/{args.srclg}2{args.tgtlg}edicted.tsv") as f:
        dfedicted = list(csv.reader(f, delimiter="\t"))

    # load heuristics file
    if args.heur:
        with open(f"loanpy/{args.heur}", "r") as f:
            args.heur = json.load(f)

    # define guesslist
    args.guesslist = ast.literal_eval(args.guesslist)

    # define adapt
    if args.adapt:
        args.adapt = ast.literal_eval(args.adapt)

    # define prosody
    if args.prosody:
        args.prosody = ast.literal_eval(args.prosody)

    out = eval_all(dfedicted, args.heur, args.adapt, args.guesslist, args.prosody)

    with open(f"loanpy/tpfp{args.srclg}2{args.tgtlg}0.json", "w+") as f:
        json.dump(out, f)  # list of tuples, can be plotted and AUC etc.
