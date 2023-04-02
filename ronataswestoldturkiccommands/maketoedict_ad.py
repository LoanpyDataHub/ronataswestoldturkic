"""
1. Read cognates.csv and forms.csv
2. Loop through cognates.csv
3. Add col Cognateset_ID [3] and Alignment [7] and Form_ID [1] to dict
4. Merge Form_ID [1] with ID [0] in forms.csv
5. Grab Language_ID [2], ProsodicStructure [14] from forms.csv
6. Write file with headers: ID\tCOGID\tDOCULECT\tALIGNMENT\tPROSODY
"""

import csv
from json import dump

from lingpy.align.pairwise import Pairwise
from loanpy.utils import prefilter

def register(parser):
    parser.add_argument("srclg")
    parser.add_argument("tgtlg")

def run(args):
    """
    """
    # read forms.csv
    lines = "ID\tCOGID\tDOCULECT\tALIGNMENT\tPROSODY"
    with open("cldf/forms.csv", "r") as f:
        dff = prefilter(list(csv.reader(f)), args.srclg, args.tgtlg)
        headers = dff.pop(0)
        h = {i: headers.index(i) for i in headers}
        for i in range(0, len(dff), 2):
            pw = Pairwise(seqs=dff[i][h["Segments"]],
                          seqB=dff[i+1][h["Segments"]],
                          merge_vowels=False
                          )
            pw.align()
            lines += "\n" + "\t".join([str(i), dff[i][h["Cognacy"]],
                                       dff[i][h["Language_ID"]],
                                       " ".join(pw.alignments[0][0]),
                                       dff[i][h["ProsodicStructure"]]])
            lines += "\n" + "\t".join([str(i+1), dff[i+1][h["Cognacy"]],
                                       dff[i+1][h["Language_ID"]],
                                       " ".join(pw.alignments[0][1]),
                                       dff[i+1][h["ProsodicStructure"]]])
        # keep only rows that occurred in cognates.csv

    # write file
    with open(f"edictor/{args.srclg}2{args.tgtlg}toedict0.tsv", "w+") as f:
        f.write(lines)
