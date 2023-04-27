"""
Import inbuilt (csv, json) and third-party (lingpy, loanpy) functinoalities to
read, filter, align, and write data.
Register arguments for the command line interface. Run the main function.
"""

import csv
from json import dump

from lingpy.align.pairwise import Pairwise
from loanpy.utils import prefilter

def register(parser):
    """
    Register command line arguments and pass them on to the main function.
    Two non-optional argments will be registered:
    ``srclg`` (source language) and ``tgtlg`` (target langauge).
    Only strings contained in column ``ID`` in ``etc/languages.csv`` are valid
    arguments.
    """
    parser.add_argument("srclg")
    parser.add_argument("tgtlg")

def run(args):
    """
    #. Read ``cldf/cognates.csv`` and ``cldf/forms.csv``.
    #. Loop through ``cldf/cognates.csv``.
    #. Align data in column ``Segments`` with `lingpy
       <https://lingpy.github.io/reference/lingpy.align.html#lingpy.align.pairwise.Pairwise.align>`__)
    #. Write output file with headers
       ``ID``, ``COGID``, ``DOCULECT``, ``ALIGNMENT``, ``PROSODY``.
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
    with open(f"edictor/{args.srclg}2{args.tgtlg}toedict.tsv", "w+") as f:
        f.write(lines)
