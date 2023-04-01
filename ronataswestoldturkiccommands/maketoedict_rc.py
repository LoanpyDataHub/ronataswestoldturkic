"""
Read col CV_Segments in forms.csv
Apply custom alignment
Write to edictor/wot.tsv
"""
from collections import Counter
import csv

from loanpy.scminer import uralign
from loanpy.utils import prefilter

def register(parser):
    parser.add_argument("srclg")
    parser.add_argument("tgtlg")

def run(args):
    """
    Read col CV_Segments in forms.csv
    Apply custom alignment
    Write to edictor/wot.tsv
    """

    with open("cldf/forms.csv", "r") as f:
        data = list(csv.reader(f))

    dfwot = prefilter(data, args.srclg, args.tgtlg)
    headers = dfwot.pop(0)
    h = {i: headers.index(i) for i in headers}
    dfalign = "ALIGNMENT"
    for i in range(0, len(dfwot), 2):
        dfalign += "\n" + uralign(
            dfwot[i][h["CV_Segments"]], dfwot[i+1][h["CV_Segments"]]
            )

    # add other cols
    final = "ID\tCOGID\tDOCULECT\tALIGNMENT\tPROSODY"
    assert len(dfalign.split("\n")[1:]) == len(dfwot)  # subtract headr on left

    # create output file (= input for edictor)
    for i, (rowa, rowb) in enumerate(zip(dfalign.split("\n")[1:], dfwot)):
        final += "\n" + "\t".join(
            [str(i), rowb[h["Cognacy"]], rowb[h["Language_ID"]], rowa, rowb[h["ProsodicStructure"]]]
            )

    # check manually if file is ok, if yes, manually remove the 0 from the name
    with open(f"edictor/{args.srclg}2{args.tgtlg}toedict0.tsv", "w+") as f:
        f.write(final)
