"""
IPA-transcribe and tokenise Hungarian words:
"""
import csv

from ipatok import tokenise
import epitran
from re import sub

epi = epitran.Epitran("hun-Latn").transliterate

def segipa(w):
    """
    Use the epitran library to transcribe Hungarian to IPA based on rules.
    Then, use the ipatok library to tokenise the IPA-string.
    .. seealso::
        `epitran
        <https://pypi.org/project/epitran/>`_,
        `ipatok
        <https://pypi.org/project/ipatok/>`_
    """
    return ' '.join(tokenise(epi(w)))

def run(args):
    """
    Read values from ``cldf/forms.csv``, IPA-transcribe and tokenise them.
    Then, write the results to ``etc/orthography/H.tsv``,
    which has two columns: ``Grapheme`` and ``IPA``.
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
