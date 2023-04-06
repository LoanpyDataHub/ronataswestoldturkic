"""
Import inbuilt (collections, csv) and third party (loanpy)
programs for reading, filtering, and aligning
data. Register arguments for the command line interface.
Run the main function.
"""
from collections import Counter
import csv

from loanpy.scminer import uralign
from loanpy.utils import prefilter

def register(parser):
    """
    Two non-optional argments will be registered:
    ``srclg`` (source language) and ``tgtlg`` (target langauge).
    Only strings contained in column ``ID`` in ``etc/languages.csv`` are valid
    arguments.
    """
    parser.add_argument("srclg")
    parser.add_argument("tgtlg")

def run(args):
    """
    #. Read col ``CV_Segments`` in ``cldf/forms.csv``
    #. Prefilter data: Only words from the source and target language, as
      specified in the command arguments, are accepted to the output data
      frame. Cognate sets that are lacking forms in either the source or the
      target language are ignored.
    #. Apply custom alignment for historical sound changes in Uralic data.
      See `loanpy's documentation
      <https://loanpy.readthedocs.io/en/latest/documentation.html#loanpy.scminer.uralign>`_
      for more details.
    #. Write results to ``edictor/{srclg}2{tgtlg}toedict0.tsv``
    #. Manually inspect whether the output is satisfying. If so, remove the
      trailing zero from the file name, which is there to avoid accidentally
      overwriting any manually edited files with this function.
    """

    with open("cldf/forms.csv", "r") as f:
        data = list(csv.reader(f))

    dfwot = prefilter(data, args.srclg, args.tgtlg)
    headers = dfwot.pop(0)
    h = {i: headers.index(i) for i in headers}
    dfalign = "ALIGNMENT"
    for i in range(0, len(dfwot), 2):
        dfalign += "\n" + uralign(
            dfwot[i][h["CV_Segments"]], dfwot[i+1][h["CV_Segments"]]
            )

    # add other cols
    final = "ID\tCOGID\tDOCULECT\tALIGNMENT\tPROSODY"
    assert len(dfalign.split("\n")[1:]) == len(dfwot)  # subtract headr on left

    # create output file (= input for edictor)
    for i, (rowa, rowb) in enumerate(zip(dfalign.split("\n")[1:], dfwot)):
        final += "\n" + "\t".join(
            [str(i), rowb[h["Cognacy"]], rowb[h["Language_ID"]],
             rowa, rowb[h["ProsodicStructure"]]]
            )

    # check manually if file is ok, if yes, manually remove the 0 from the name
    with open(f"edictor/{args.srclg}2{args.tgtlg}toedict0.tsv", "w+") as f:
        f.write(final)
