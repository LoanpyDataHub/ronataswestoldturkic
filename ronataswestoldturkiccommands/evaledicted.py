"""
Check if the file edited by edictor is OK.

#. Do we have an even number of rows (excluding the header) that alternate between source and target language data (src-tgt-src-tgt-...)?
#. Do both sides of each alignment have the same number of phonemes or phoneme clusters?

If any of these conditions is not met, an assertion error will be raised.
"""
import csv
import logging

from loanpy.utils import is_valid_language_sequence, is_same_length_alignments

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )

def register(parser):
    parser.add_argument("srclg")
    parser.add_argument("tgtlg")

def run(args):
    """
    #. Read the manually fine-tuned alignments
    #. Check if sequence is src-tgt-src-tgt-...
       with `loanpy.utils.is_valid_language_sequence
       <https://loanpy.readthedocs.io/en/latest/documentation.html#loanpy.utils.is_valid_language_sequence>`_
    #. Check if each word in an alignment has the same number of
       phoneme (clusters) with `loanpy.is_same_length_alignments
       <https://loanpy.readthedocs.io/en/latest/documentation.html#loanpy.utils.is_same_length_alignments>`_
    #. Logs the number of the iteration cycle to the console if there's a
       problem.
    #. Logs OK if all is fine.
    """
    with open(f"edictor/{args.srclg}2{args.tgtlg}edicted.tsv") as f:
        data = list(csv.reader(f, delimiter="\t"))[1:]
        assert is_valid_language_sequence(data, args.srclg, args.tgtlg)
        assert is_same_length_alignments(data)

    logging.info("OK")
