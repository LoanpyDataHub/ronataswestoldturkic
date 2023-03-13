"""
Read the manually fine-tuned alignments
Check if they have same length and dots between phonemes
Print ID if there's a problem
Print a smily if all is fine
"""

def run(args):
    with open("edictor/edicted.tsv") as f:
        rownr = -1
        iterrows = iter(f.read().split("\n")[1:][:-1])
        lines = "SUGGESTED"

        # assert entire table goes H E H E H E H E
        rownr = -1
        while True:
            try:
                assert next(iterrows).split("\t")[1][0] == "H"
                rownr += 1
                assert next(iterrows).split("\t")[1][0] == "E"
                rownr += 1
            except StopIteration:
                break
            except AssertionError:
                print(rownr)
                break

    with open("edictor/edicted.tsv") as f:
        iterrows = iter(f.read().split("\n")[1:][:-1])
        while True:
            try:
                first = next(iterrows).split("\t")[2].split(" ")
                second = next(iterrows).split("\t")[2].split(" ")
                if "(" in first:  # del brackets
                    first = first[:first.index("(")]
                rownr += 2
                try:
                    assert len(first) == len(second)
                    lines += "\n" + " ".join(first) + "\n" + " ".join(second)
                except AssertionError:
                    #print(rownr, "\n", first, "\n", second)
                    #break
                    if first[-1] == "-#":
                        first = first[:-1]
                        try:
                            assert len(first) == len(second)
                            lines += "\n" + " ".join(first) + "\n" + " ".join(second)
                        except AssertionError:
                            print(rownr, "\n", first, "\n", second)
                            break
                    else:
                        print(rownr, "\t", first, "\t", second)
                        break
            except StopIteration:
                break

    with open("edictor/suggested.tsv", "w+") as f:
        f.write(lines)
