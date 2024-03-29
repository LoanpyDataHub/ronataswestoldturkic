"""
Specify the aligned wordlist data together with a few arguemnts
and pass them on to loanpy's evaluator module. Write the output
to a json-file. It is a list of tuples with pairs of
false and true positives.
"""

import ast
import json
import csv
from loanpy.eval_sca import eval_all

def register(parser):
    """
    Register arguments. Three arguments necessary: The first two are the IDs
    of the target and source language, as specified in column ``ID`` in
    ``etc/language.csv``. The third is a list of integers that specifies
    how many guesses should be made per input word during each iteration.
    This roughly corresponds to the false positive rate. Another three
    arguments are optional: Set adapt=True if we are dealing with horizontal
    transfers, prosody=True if phonotactics should be repaired during
    loanword adaptation prediction, and pass a file name to parameter "heur",
    to add heuristic predictions of sound adaptations.
    """
    parser.add_argument("srclg")
    parser.add_argument("tgtlg")
    parser.add_argument("guesslist")
    parser.add_argument("adapt", nargs="?")
    parser.add_argument("prosody", nargs="?")
    parser.add_argument("heur", nargs="?")

def run(args):
    """
    #. Read aligned data between forms of the source and target language
       with the inbuilt csv library.
    #. If a filename was passed to parameter "heur", open that file. It has
       to be located in the ``loanpy`` folder.
    #. Read the other parameters with the inbuilt ``literal_eval`` function.
    #. Pass the parameters and the data to loanpy's `eval_all
       <https://loanpy.readthedocs.io/en/latest/documentation.html#loanpy.eval_sca.eval_all>`_
       function
    #. Write the results to a file called ``tpfp{srclg}2{tgtlg}.json``.

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

    out = {}
    out["tp_fp"] = eval_all(dfedicted, args.heur, args.adapt, args.guesslist,
                            args.prosody)
    out["fp"] = args.guesslist
    out["tp"] = len(dfedicted)

    with open(f"loanpy/tpfp{args.srclg}2{args.tgtlg}.json", "w+") as f:
        json.dump(out, f)  # list of tuples, can be plotted and AUC etc.
