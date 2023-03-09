"""
Read comments from raw file and store them in ./etc/comments.tsv.
"""
from lexibank_ronataswestoldturkic import Dataset as WOT

def run(args):
    """
    Read comments from raw file and write to ../etc
    """
    wot = WOT()
    #print(wot.__dict__)
    lines = "Row\tComment"

    for idx, row in enumerate(wot.raw_dir.read_csv(
            "wot.tsv", delimiter="\t")[1:]):
        if row[-1]:  # =comment
            lines += f"\nWest Old Turkic{idx+1}\t{row[-1]}"

    # write csv
    with open(wot.etc_dir / "comments.tsv", "w+") as file:
        file.write(lines)
