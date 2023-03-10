from lexibank_ronataswestoldturkic import Dataset as WOT
from loanpy.qfysc import

# load the wordlist
ds = WOT()

# keep only cogsets where H-EAH-WOT occurs, ditch OH and LAH
cogid = 1
cogset = set()
triplet = []
table = []
# loop through rows of cldf/cognates.csv
for row in ds.cldf_dir.read_csv("cognates.csv")[1:]:
    if int(row[3]) == cogid:  # for cogset
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

lines = "ID\tDOCULECT\tALIGNMENT\tCOGID"
for i, row in enumerate(table):
    lg = row[0][0].replace("E", "EAH")
    lines += "\n" + "\t".join([str(i), lg, row[7], row[3]])

with open("wot.tsv", "w+") as f:
    f.write(lines)
