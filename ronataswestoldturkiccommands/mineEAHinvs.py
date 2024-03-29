"""
Create a list of all possible prosodic structures (like "CVCV") in the
target language and store them in a json-file.
"""
import csv
import json

from loanpy.scminer import get_prosodic_inventory

def register(parser):
    """
    Register arguments. Only one argument necessary: The name of the
    output-file. Should end in *.json*.
    """
    parser.add_argument("outname")

def run(args):
    """
    #. Read the aligned data in ``edictor/WOT2EAHedicted.tsv`` with the
       inbuilt csv package
    #. Pass it on to loanpy's `get_prosodic_inventory
       <https://loanpy.readthedocs.io/en/latest/documentation.html#loanpy.scminer.get_prosodic_inventory>`_
       function, which will extract all phonotactic structures (like "CVCV")
       from the target language.
    #. Write the inventory of prosodic structures to a json-file with the
       inbuilt json package. It will have the name that was passed on as an
       argument to the command and will be written to the folder ``loanpy``.
    """
    with open(f"edictor/WOT2EAHedicted.tsv", "r") as f:
        out = get_prosodic_inventory(list(csv.reader(f, delimiter="\t")))

    with open(f"loanpy/{args.outname}", "w+") as f:
        json.dump(out, f)
