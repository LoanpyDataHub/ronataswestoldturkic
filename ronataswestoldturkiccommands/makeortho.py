"""
IPA-transcribe Hungarian words
"""

from lexibank_ronataswestoldturkic import Dataset as WOT
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
    wot = WOT()
    #ds = Dataset.from_metadata("./cldf/cldf-metadata.json")
    lines = "Grapheme\tIPA"
    wrdlst = []
    for row in wot.cldf_dir.read_csv("forms.csv")[1:]:
        row[4] = sub(" ", "", row[4])
        if row[2] == "H" and row[4] not in wrdlst:
            lines += f"\n^{row[4]}$\t{segipa(row[4])}"
            wrdlst.append(row[4])

    # write csv
    with open(wot.etc_dir / "orthography" / "H.tsv", "w+") as file:
        file.write(lines)
