"""
Create a list of all possible prosodic structures (e.g. "CVCV") in the
target language and store it in a json-file.
"""
import csv
import json

from loanpy.scminer import get_inventory

def register(parser):
    """
    Register arguments. Only one argument necessary: The name of the output-
    file. Should end in .json.
    """
    parser.add_argument("outname")

def run(args):
    """
    #. Read aligned data in ``edictor/WOT2EAHedicted.tsv`` with the inbuilt
       csv package
    #. Pass it on to loanpy's `get_inventory
       <https://loanpy.readthedocs.io/en/latest/documentation.html#loanpy.scminer.get_inventory>`_
       function, which will extract all prosodic structures (e.g. "CVCV")
       from the target language.
    #. Write the inventory of prosodic structures to a json-file with the
       inbuilt json package. It will have the name that was passed on as an
       argument to the command and will be written to the folder ``loanpy``.
    """
    with open(f"edictor/WOT2EAHedicted.tsv", "r") as f:
        out = get_inventory(list(csv.reader(f, delimiter="\t")))

    with open(f"loanpy/{args.outname}", "w+") as f:
        json.dump(out, f)
