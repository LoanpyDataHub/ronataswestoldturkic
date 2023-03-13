"""
Read edictor/edicted.tsv and cldf/forms.csv
and add col CV_Segments to edicted.tsv
"""

def run(args):
    with open("cldf/forms.csv", "r") as f:
        cvdict = {}
        for row in f.read().split("\n")[1:][:-1]:
            row = row.split(",")
            cvdict[row[2]+row[9]] = row[14]

    with open("edictor/edicted.tsv", "r") as f:
        data = f.read().split("\n")[:-1]
        lines = data.pop(0) + "\tCV_SEGMENTS" # header
        for row in data:
            rs = row.split("\t")
            lines += "\n" + row + "\t" + cvdict[rs[1] + rs[3]]

    with open("edictor/edicted2.tsv", "w+") as f:
        f.write(lines)
