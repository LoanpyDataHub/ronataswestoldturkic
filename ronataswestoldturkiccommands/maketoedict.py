"""
Read col CV_Segments in forms.csv
Apply custom alignment
Write to edictor/wot.tsv
"""
from loanpy.recovery import uralign

def prefilter(data):
    """
    Keep only cogsets where H and EAH occurs, ditch OH and LAH
    """
    cogid = 1
    cogset = set()
    triplet = []
    table = []
    # loop through rows of cldf/cognates.csv
    for row in data[1:]:
        if int(row[9]) == cogid:  # for cogset
            if row[0][0] in {"H", "E"}:  # if ID has H EAH WOT in it
                cogset.add(row[0][0])  # add H E or W to the set
                triplet.append(row)  # add row to cluster of rows
        else:  # don't turn this to an elif!
            if cogset == {"H", "E"}:  # if H, EAH, and WOT were in the cogset
                for r in triplet:  # add all three rows to the table
                    table.append(r)
            cogid += 1  # reset variables for next round of the loop
            cogset.clear()
            triplet.clear()

            # add stuff from the queue
            if row[0][0] in {"H", "E"}:  # if ID has H EAH WOT in it
                cogset.add(row[0][0])  # add H E or W to the set
                triplet.append(row)  # add row to cluster of rows
    # add last row
    for r in triplet:  # add all three rows to the table
        table.append(r)

    # assert entire table goes H E H E H E H E
    itertable = iter(table)

    while True:
        try:
            assert next(itertable)[0][0] == "H"
            assert next(itertable)[0][0] == "E"
        except StopIteration:
            break

    return table

def run(args):
    """
    Read col CV_Segments in forms.csv
    Apply custom alignment
    Write to edictor/wot.tsv
    """

    with open("cldf/forms.csv", "r") as f:
        dfwot = prefilter([i.split(",") for i in f.read().split("\n")[1:][:-1]])
    iterwot = iter(dfwot)
    dfalign = "ALIGNMENT"
    while True:
        try:
            dfalign += "\n" + uralign(next(iterwot)[13], next(iterwot)[13])
        except StopIteration:
            break

    # add other cols
    final = "ID\tDOCULECT\tALIGNMENT\tCOGID"
    assert len(dfalign.split("\n")[1:]) == len(dfwot)  # subtract header on left

    for i, (ra, rb) in enumerate(zip(dfalign.split("\n")[1:], dfwot)):
        final += "\n" + "\t".join([str(i), rb[12], ra, rb[9]])

    with open("edictor/toedict0.tsv", "w+") as f:
        f.write(final)
