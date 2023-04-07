"""

"""

import csv
import json

from loanpy.scminer import get_correspondences

def register(parser):
    parser.add_argument("srclg")
    parser.add_argument("tgtlg")
    parser.add_argument("heur", nargs="?")

def run(args):
    """
    #. If argument three was provided, read the json-file containing heuristic
       phoneme adaptation predictions with the inbuilt json package.
    #. Read aligned forms from ``edictor/{srclg}2{tgtlg}edicted.tsv``
    #. Extract sound and phonotactic correspondences from the data with
       loanpy's `get_corrspondences
       <https://loanpy.readthedocs.io/en/latest/documentation.html#loanpy.scminer.get_correspondences>`_
       function
    #. Write the sound correspondences to a file named ``{srclg}2{tgtlg}.json``
       in the folder ``loanpy``.
    """
    if args.heur:
        with open(f"loanpy/{args.heur}", "r") as f:
            args.heur = json.load(f)
    with open(f"edictor/{args.srclg}2{args.tgtlg}edicted.tsv", "r") as f:
        tsv = list(csv.reader(f, delimiter="\t"))
        out = get_correspondences(tsv, args.heur)
    # store as json-file
    with open(f"loanpy/{args.srclg}2{args.tgtlg}sc0.json", "w+") as f:
        json.dump(out, f)
