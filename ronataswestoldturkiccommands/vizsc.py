"""
Read json file containing six dictionaries about sound and phonotactic
correspondences and turn it into a human-readable tsv-file with additional
info for easier manual inspection.
"""

import csv
import json

from loanpy.utils import scjson2tsv

def register(parser):
    """
    Register arguments. Two arguments necessary: The ID of the target and
    source language: In horizontal transfers, the donor language is the source
    and the recipient language is the target. In vertical transfers, the
    target language is the ancestor and the source the descendant for backwards
    reconstructions. Valid IDs can be found in
    column ``ID`` in ``etc/language.csv``.
    """
    parser.add_argument("srclg")
    parser.add_argument("tgtlg")

def run(args):
    """
    #. Read sound-correspondence json at ``loanpy/{srclg}2{tgtlg}sc.json``.
    #. Transform computer-readable data structure to human-readable tables
       with `loanpy.utils.scjson2tsv
       <https://loanpy.readthedocs.io/en/latest/documentation.html#loanpy.utils.scjson2tsv>`_
    #. Merge IDs with info from related tables for easier manual inspection.
    #. Write the correspondence tables to two files named
       ``{srclg}2{tgtlg}sc.tsv`` and ``{srclg}2{tgtlg}sc_phonotactics.tsv``
       in the folder ``loanpy``.
    """

    scjson2tsv(f"loanpy/{args.srclg}2{args.tgtlg}sc.json",
               f"loanpy/{args.srclg}2{args.tgtlg}sc.tsv",
               f"loanpy/{args.srclg}2{args.tgtlg}sc_phonotactics.tsv")

    # create dictionary of CogID2form
    with open("cldf/forms.csv", "r") as f:
        dfforms = list(csv.reader(f))
    # col 9=cogid, 5=forms, 2=Language_ID
    cogid2srcform = {row[9]: row[5] for row in dfforms[1:] if row[2] == args.srclg}
    cogid2tgtform = {row[9]: row[5] for row in dfforms[1:] if row[2] == args.tgtlg}

    # read H2EAHsc.tsv
    with open(f"loanpy/{args.srclg}2{args.tgtlg}sc.tsv", "r") as f:
        dfsc = list(csv.reader(f, delimiter="\t"))
    # merge CogIDs with forms
    with open(f"loanpy/{args.srclg}2{args.tgtlg}sc.tsv", "w") as f:
        writer = csv.writer(f, delimiter="\t")
        dfsc[0].append("forms")
        writer.writerow(dfsc[0])
        for row in dfsc[1:]:
            forms = [f"{cogid2srcform[cogid]} {cogid2tgtform[cogid]}" for cogid in row[-1].split(", ")]
            row.append(", ".join(forms))
            writer.writerow(row)

    #the same but for phonotactics
    # read H2EAHsc.tsv
    with open(f"loanpy/{args.srclg}2{args.tgtlg}sc_phonotactics.tsv", "r") as f:
        dfsc = list(csv.reader(f, delimiter="\t"))
    # merge CogIDs with forms
    with open(f"loanpy/{args.srclg}2{args.tgtlg}sc_phonotactics.tsv", "w") as f:
        writer = csv.writer(f, delimiter="\t")
        dfsc[0].append("forms")
        writer.writerow(dfsc[0])
        for row in dfsc[1:]:
            forms = [f"{cogid2srcform[cogid]} {cogid2tgtform[cogid]}" for cogid in row[-1].split(", ")]
            row.append(", ".join(forms))
            writer.writerow(row)
