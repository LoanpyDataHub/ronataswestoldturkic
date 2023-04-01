"""
Read edicted.tsv
Replace "-" by "C" if C disappeared, else "V"
Write file
"""
from loanpy.utils import cvgaps

def register(parser):
    parser.add_argument("srclg")
    parser.add_argument("tgtlg")

def run(args):
    """
    """
    with open(f"edictor/{args.srclg}2{args.tgtlg}edicted.tsv") as f:
        data = [row.split("\t") for row in f.read().split("\n")[1:][:-1]]
        iterrows = iter(data)

    newal = []
    while True:
        try:
            newal += cvgaps(next(iterrows)[3], next(iterrows)[3])
        except StopIteration:
            break

    final = "ID\tCOGID\tDOCULECT\tALIGNMENT\tPROSODY"
    for row, new in zip(data, newal):
        final += "\n" + "\t".join([row[0], row[1], row[2], new, row[4]])

    with open(f"edictor/{args.srclg}2{args.tgtlg}edicted0.tsv", "w+") as f:
        f.write(final)
