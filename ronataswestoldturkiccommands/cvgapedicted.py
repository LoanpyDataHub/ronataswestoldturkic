"""
Read edicted.tsv
Replace "-" by "C" if C disappeared, else "V"
Write file
"""
from loanpy.utils import cvgaps
import csv

def register(parser):
    parser.add_argument("srclg")
    parser.add_argument("tgtlg")

def run(args):
    """
    """
    with open(f"edictor/{args.srclg}2{args.tgtlg}edicted.tsv") as f:
        data = list(csv.reader(f, delimiter="\t"))
    headers = data.pop(0)
    h = {i: headers.index(i) for i in headers}

    newal = []
    for i in range(0, len(data), 2):
        newal += cvgaps(data[i][3], data[i+1][3])

    final = "ID\tCOGID\tDOCULECT\tALIGNMENT\tPROSODY"
    for row, new in zip(data, newal):
        final += "\n" + "\t".join([row[0], row[1], row[2], new, row[4]])

    with open(f"edictor/{args.srclg}2{args.tgtlg}edicted0.tsv", "w+") as f:
        f.write(final)
