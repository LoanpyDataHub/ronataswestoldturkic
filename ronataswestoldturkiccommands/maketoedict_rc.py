"""
Read col CV_Segments in forms.csv
Apply custom alignment
Write to edictor/wot.tsv
"""
from collections import Counter

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
        data = [row.split(",") for row in f.read().strip().split("\n")][1:]
        dfwot = prefilter(data, args.srclg, args.tgtlg)
    iterwot = iter(dfwot)
    dfalign = "ALIGNMENT"
    while True:
        try:
            dfalign += "\n" + uralign(next(iterwot)[13], next(iterwot)[13])
        except StopIteration:
            break

    # add other cols
    final = "ID\tCOGID\tDOCULECT\tALIGNMENT\tPROSODY"
    assert len(dfalign.split("\n")[1:]) == len(dfwot)  # subtract headr on left

    # create output file (= input for edictor)
    for i, (ra, rb) in enumerate(zip(dfalign.split("\n")[1:], dfwot)):
        final += "\n" + "\t".join([str(i), rb[9], rb[12], ra, rb[14]])

    # check manually if file is ok, if yes, manually remove the 0 from the name
    with open(f"edictor/{args.srclg}2{args.tgtlg}toedict0.tsv", "w+") as f:
        f.write(final)
