"""
IPA-transcribe Hungarian words
"""
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
        data = [row.split(",") for row in f.read().strip().split("\n")]

    formidx = data[0].index("Form")
    lgididx = data[0].index("Language_ID")
    lines = "Grapheme\tIPA"
    wrdlst = []
    for row in data[1:]:
        form = row[formidx]  # to avoid duplicates
        if row[lgididx] == "H" and form not in wrdlst:
            lines += f"\n^{form}$\t{segipa(form)}"
            wrdlst.append(form)

    # write csv
    with open("etc/orthography/H.tsv", "w+") as file:
        file.write(lines)
