"""cd to folder `misc` and run `python makeortho.py` from terminal"""

from pathlib import Path
import re

import epitran
import pandas as pd
from ipatok import tokenise

# have 2 diff transcription files for Hungarian vs Pre-Hungarians
epiwot = epitran.Epitran("hun-wot").transliterate
epilatn = epitran.Epitran("hun-Latn").transliterate
def segment_wot(w):
    return ' '.join(tokenise(epiwot(w)))
def segment_latn(w):
    return ' '.join(tokenise(epilatn(w)))

def main():
    """creates othography.tsv with Graphemes 2 IPA mappings"""

    #create OH.py, EAH.py, LAH.py, WOT.py
    in_path = Path.cwd().parent.parent / "cldf" / "forms.csv"
    for i in ["H", "OH", "EAH", "LAH", "WOT"]:
        #define the transcription orthography
        if i == "H":
            segment = segment_latn
        else:
            segment = segment_wot
        # create the files
        out_path = Path.cwd().parent.parent / "etc" / "orthography" / f"{i}.tsv"
        dfo = pd.read_csv(in_path, usecols=["Form", "Language_ID", "Orthography"])

        # merge orthography and forms
        #newforms = []
        #for idx, row in dfo.iterrows():
        #    if row["Language_ID"] == "H":
        #        newforms.append(row["Orthography"].replace(" ", ""))
        #    else:
        #        newforms.append(row["Form"].replace(" ", ""))
        #dfo["Form"] = newforms

        # delete because it's merged
        #del dfo["Orthography"]

        dfo = dfo[dfo['Language_ID'] == i]
        dfo.assign(IPA=lambda x: list(map(segment, x.Form)))\
        .rename(columns={"Form": "Grapheme"})\
        .drop_duplicates(subset=["Grapheme", "IPA"])\
        .to_csv(out_path, index=False, encoding="utf-8", sep="\t")

if __name__ == "__main__":
    main()
