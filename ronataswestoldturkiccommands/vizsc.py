"""
Read in sc-json and turn it into a tsv-file
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
