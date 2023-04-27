"""
Import inbuilt (csv) and third-party (loanpy) functions to read and process
data.
Register arguments for the command line interface. Run the main function.
"""
from loanpy.utils import cvgaps
import csv

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
    #. Read edictor/{srclg}2{tgtlg}edicted.tsv
    #. Replace "-" in source language data by "C" or "V" with
       `loanpy.utils.cvgaps
       <https://loanpy.readthedocs.io/en/latest/documentation.html#loanpy.utils.cvgaps>`_.
    #. Write file

    """
    with open(f"edictor/{args.srclg}2{args.tgtlg}edicted.tsv") as f:
        data = list(csv.reader(f, delimiter="\t"))
    headers = data.pop(0)
    h = {i: headers.index(i) for i in headers}

    newal = []
    for i in range(0, len(data), 2):
        newal += cvgaps(data[i][h["ALIGNMENT"]], data[i+1][h["ALIGNMENT"]])

    final = "ID\tCOGID\tDOCULECT\tALIGNMENT\tPROSODY"
    for row, new in zip(data, newal):
        final += "\n" + "\t".join(
                [row[h["ID"]], row[h["COGID"]],
                row[h["DOCULECT"]], new, row[h["PROSODY"]]]
                                  )

    with open(f"edictor/{args.srclg}2{args.tgtlg}edicted0.tsv", "w+") as f:
        f.write(final)
