"""
Create heuristic predictions of phoneme adaptations based on feature vector
similarities of phonemes.
"""
from loanpy.scminer import get_heur
import json

def register(parser):
    """
    Register arguments. Two argument necessary: The ID of the target language,
    i.e. the one in which loanwords are adapted. Valid IDs can be found in
    column ``ID`` in ``etc/language.csv``. The second argument is the name of
    the output-file. Should end in ".json".
    """
    parser.add_argument("tgtlg")
    parser.add_argument("outname")

def run(args):
    """
    #. Pass on the target language ID as defined in `etc/languages.csv`
       to loanpy's `get_heur
       <https://loanpy.readthedocs.io/en/latest/documentation.html#loanpy.scminer.get_heur>`_
       function,
       which will read the `cldf/.transcription-report.json` file and
       extract the phoneme inventory of the target language from there.
       It will also read the file ipa_all.csv, which is shipped with loanpy.
       From these two files it creates a heuristic prediction of loanword
       phoneme substitution/adaptation patterns.
    #. Write the results to a file named according to the value passed to the
       second argument. It will be written to the folder ``loanpy``.
       Expected file size: ca. 2.5MB.

    """
    with open(f"loanpy/{args.outname}", "w+") as f:
        json.dump(get_heur(args.tgtlg), f)
