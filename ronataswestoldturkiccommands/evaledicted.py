"""
Read the manually fine-tuned alignments
Check if they have same length
Print ID if there's a problem
Print OK if all is fine
"""
from loanpy.helpers import evalsrctgt, evalsamelen

def register(parser):
    parser.add_argument("srclg")
    parser.add_argument("tgtlg")

def run(args):
    """
    Check if the file edited by edictor is OK.
    1. Does it go src-tgt-src-tgt-...?
    2. Do all alignments have the same length?
    """
    with open(f"edictor/{args.srclg}2{args.tgtlg}edicted.tsv") as f:
        data = [row.split("\t") for row in f.read().split("\n")[1:][:-1]]
        assert evalsrctgt(data, args.srclg, args.tgtlg)
        assert evalsamelen(data, args.srclg, args.tgtlg)

    print("OK")
