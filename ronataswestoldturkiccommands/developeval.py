"""
Play around and make sure adapt() is running
"""
from ast import literal_eval as le

from loanpy import apply

def register(parser):
    parser.add_argument("ipa", nargs="?")
    parser.add_argument("pros", nargs="?")
    parser.add_argument("hm", nargs="?")
    parser.add_argument("phf", nargs="?")
    parser.add_argument("rvh", nargs="?")
    parser.add_argument("mrp", nargs="?")
    parser.add_argument("mp2rp", nargs="?")
    parser.add_argument("dc", nargs="?")
    parser.add_argument("ic", nargs="?")
    parser.add_argument("sw", nargs="?")

def run(args):
    """
    """
    adrc = apply.Adrc("loanpy/WOT2EAHsc.json", "loanpy/invsEAH.json")
    print(adrc.adapt(args.ipa, args.pros, int(args.hm),
                     le(args.phf), le(args.rvh), int(args.mrp),
                     int(args.mp2rp), int(args.dc), int(args.ic), le(args.sw)))
    print(adrc.workflow)
