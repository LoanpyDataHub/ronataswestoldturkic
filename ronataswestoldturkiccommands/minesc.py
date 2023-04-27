"""
Read in aligned data and write a json-file with information about sound
correspondences.
"""

import csv
import json

from loanpy.scminer import get_correspondences

def register(parser):
    """
    Register arguments. Two arguments necessary: The ID of the target and
    source language: In horizontal transfers, the donor language is the source
    and the recipient language is the target. In vertical transfers, the
    target language is the ancestor and the source the descendant for backwards
    reconstructions. Valid IDs can be found in
    column ``ID`` in ``etc/language.csv``. A third argument is optional,
    namely the json-file containing the heuristic phoneme adaptations.
    """
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
    #. Write the sound correspondences to a file named
       ``{srclg}2{tgtlg}sc0.json`` in the folder ``loanpy``. Manually remove
       the trailing zero in the file name if the file seems fine.
    """
    if args.heur:
        with open(f"loanpy/{args.heur}", "r") as f:
            args.heur = json.load(f)
    with open(f"edictor/{args.srclg}2{args.tgtlg}edicted.tsv", "r") as f:
        tsv = list(csv.reader(f, delimiter="\t"))
        out = get_correspondences(tsv, args.heur)
    # store as json-file
    with open(f"loanpy/{args.srclg}2{args.tgtlg}sc.json", "w+") as f:
        json.dump(out, f)
