"""
IPA-transcribe Hungarian words.
"""
import csv

from ipatok import tokenise
import epitran
from re import sub

epi = epitran.Epitran("hun-Latn").transliterate

def segipa(w):
    return ' '.join(tokenise(epi(w)))

def run(args):
    """
    Read values from forms.csv and IPA-transcribe the Spanish ones
    """
    with open("cldf/forms.csv", "r") as f:
        data = csv.reader(f)
        outtable = [["Grapheme", "IPA"]]
        wrdlst = []
        for i, row in enumerate(data):
            if i == 0:
                formidx = row.index("Form")
                lgididx = row.index("Language_ID")
                continue
            form = row[formidx]  # to avoid duplicates
            if row[lgididx] == "H" and form not in wrdlst:
                outtable.append([form, segipa(form)])
                wrdlst.append(form)

    # write csv
    with open("etc/orthography/H.tsv", "w+") as file:
        w = csv.writer(file, delimiter="\t")
        w.writerows(outtable)
