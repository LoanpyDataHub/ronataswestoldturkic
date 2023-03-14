"""
1. Read cognates.csv and forms.csv
2. Loop through cognates.csv
3. Add col Cognateset_ID [3] and Alignment [7] and Form_ID [1] to dict
4. Merge Form_ID [1] with ID [0] in forms.csv
5. Grab Language_ID [2], ProsodicStructure [14] from forms.csv
6. Write file with headers: ID\tCOGID\tDOCULECT\tALIGNMENT\tPROSODY
"""

from json import dump

from loanpy.helpers import prefilter

def register(parser):
    parser.add_argument("srclg")
    parser.add_argument("tgtlg")

def run(args):
    """
    """
    # read forms.csv
    final = {}
    with open("cldf/forms.csv", "r") as f:
        dfforms = prefilter(f.read(), args.srclg, args.tgtlg)
        # keep only rows that occurred in cognates.csv
        final["DOCULECT"] = [row[2] for row in dfforms]
        final["PROSODY"] = [row[14] for row in dfforms]
        final["FORMID"] = [row[0] for row in dfforms]

    # read cognates.csv
    with open("cldf/cognates.csv", "r") as f:
        dfcog = [row.split(",") for row in f.read().split("\n")[1:][:-1]]
        dfcog = [row for row in dfcog if row[1] in final["FORMID"]]
        # grab data
        final["COGID"] = [row[3] for row in dfcog]
        final["ALIGNMENT"] = [row[7] for row in dfcog]


    # create file
    out = "ID\tCOGID\tDOCULECT\tALIGNMENT\tPROSODY"
    for i, (a, b, c, d) in enumerate(zip(final["COGID"], final["DOCULECT"],
            final["ALIGNMENT"], final["PROSODY"])):
        out += "\n" + "\t".join([str(i), a, b, c, d])

    # write file
    with open(f"edictor/{args.srclg}2{args.tgtlg}toedict0.tsv", "w+") as f:
        f.write(out)
