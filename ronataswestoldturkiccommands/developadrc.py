"""
Play around and make sure adapt() is running
"""
from ast import literal_eval as le

from loanpy import apply

def register(parser):
    parser.add_argument("ipa", nargs="?")
    parser.add_argument("hm", nargs="?")
    parser.add_argument("mrp", nargs="?")

def run(args):
    """
    """
    adrc = apply.Adrc("loanpy/wot2eahsc.json", "loanpy/heur.json")
    print(adrc.adapt(args.ipa, "", int(args.hm), le("False"),
                     le("False"), le("False"), int(args.mrp)))
