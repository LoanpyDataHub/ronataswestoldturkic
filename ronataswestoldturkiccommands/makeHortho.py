"""
IPA-transcribe Hungarian words
"""
from ipatok import tokenise
import epitran
from re import sub

# TODO: add ng to transcription
epi = epitran.Epitran("hun-Latn").transliterate

def segipa(w):
    return ' '.join(tokenise(epi(w)))

def run(args):
    """
    Read values from forms.csv and IPA-transcribe the Spanish ones
    """

    with open("cldf/forms.csv", "r") as f:
        data = [row.split(",") for row in f.read().strip().split("\n")]

    lines = "Grapheme\tIPA"
    wrdlst = []
    for row in data[1:]:
        if row[2] == "H" and row[5] not in wrdlst:
            lines += f"\n^{row[5]}$\t{segipa(row[5])}"
            wrdlst.append(row[5])  # to avoid duplicates

    # write csv
    with open("etc/orthography/H.tsv", "w+") as file:
        file.write(lines)
