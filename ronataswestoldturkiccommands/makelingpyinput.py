"""
Read json file containing six dictionaries about sound and phonotactic
correspondences and turn it into a human-readable tsv-file with additional
info for easier manual inspection.
"""

import csv
import re

from loanpy.utils import scjson2tsv

def run(args):
    """
    #. Read forms.csv
    #. Convert it so that it corresponds to the sample input file in
       lingpy's documentation at
       https://github.com/lingpy/lingpy/blob/master/tests/test_data/KSL.qlc
    #. Write that file to the folder ``lingpy``.
    """

    with open("cldf/forms.csv") as f:
        forms = list(csv.reader(f))

    with open("lingpy/wot.csv", "w+") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow([
            ['# KSL'],
            ['ID', 'DOCULECT', 'CONCEPT', 'GlossID',
            'Orthography', 'IPA', 'Tokens', 'CogID']
            ])

        for i, row in enumerate(forms[1:]):
            if i > 0 and row[9] != forms[i-1][9]:  # cognacy
                writer.writerow(["#"])

            newrow = [i, row[2], row[3], row[9],
                      row[5], re.sub("[. ]", "", row[6]), row[6], row[0]]

            writer.writerow(newrow)
