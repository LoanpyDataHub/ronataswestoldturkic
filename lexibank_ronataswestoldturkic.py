import pathlib

import attr
from clldutils.misc import slug
from lingpy import prosodic_string
from lingpy.sequence.sound_classes import token2class
from pylexibank import (
Dataset as BaseDataset, FormSpec, Language, Lexeme, progressbar as pb)
from re import sub

@attr.s
class CustomLexeme(Lexeme):
    CV_Segments = attr.ib(default=None)
    ProsodicStructure = attr.ib(default=None)
    FB_VowelHarmony = attr.ib(default=None)
    Year = attr.ib(default=None)

# todo: import the next 3 functions from loanpy

def get_clusters(segments):
    """
    Takes a list of phonemes and segments them into consonant and vowel
    clusters, like so: "abcdeaofgh" -> ["a", "b.c.d", "e.a.o", "f.g.h"]
    (c) List 2022"""
    out = [segments[0]]
    for i in range(1, len(segments)):
        # can be optimized
        prev, this = token2class(segments[i-1], "cv"), token2class(
                segments[i], "cv")
        if prev == this:
            out[-1] += "."+segments[i]
        else:
            out += [segments[i]]
    return " ".join(out)

def has_harmony(segments):
    """
    See issue #22!
    if no front vowels in word: has harmony.
    if front vowels and no back vowels: also.
    """
    # if word contains at least one front vowel
    if any(i in segments for i in ['y', 'yː', 'ø', 'øː']):
        # check if it contains a back-vowel
        if any(i in segments for i in ['a', 'aː', 'ɒ', 'ɯ', 'u', 'uː', 'o']):
            return "false"  # if yes: no vowel harmony
    return "true"

def get_loan(loan, language):
    return loan == "TRUE" if language == "WOT" else True

class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "ronataswestoldturkic"
    lexeme_class = CustomLexeme
    form_spec = FormSpec(separators=",", first_form_only=True,
                         replacements= [(" ", "")])

    def cmd_makecldf(self, args):

        #add borrowing table
        args.writer.cldf.add_component(
            "BorrowingTable"
            #{"name": "lol", "datatype": "string"},
        )
        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        # add concept
        concepts = {}
        for i, concept in enumerate(self.concepts):
            idx = str(i)+"_"+slug(concept["ENGLISH"])
            concepts[concept["ENGLISH"]] = idx
            args.writer.add_concept(
                    ID=idx,
                    Name=concept["ENGLISH"],
                    Concepticon_ID=concept["CONCEPTICON_ID"],
                    Concepticon_Gloss=concept["CONCEPTICON_GLOSS"],
                    )

        args.log.info("added concepts")
        #print(concepts)

        #add comments
        comments = self.etc_dir.read_csv(
            "comments.tsv", delimiter="\t",
        )  # [['ENGLISH', 'Comment'], ['a', 'b'], ['c', 'd']]
        comments = {line[0]: line[1] for line in comments}
        args.log.info("added comments")

        # add language
        languages = args.writer.add_languages()
        args.log.info("added languages")


        # add forms and borrowings
        data = self.raw_dir.read_csv(
            "wot.tsv", delimiter="\t",
        )
        header = data[0]
        cognates = {}
        cogidx = 1
        borrid = 1

        for i in range(1, len(data)):
            cognates = dict(zip(header, data[i]))
            #print(cognates)
            concept = data[i][7]
            eah = ""
            for language in languages:
                #print(language)
                cog = cognates.get(language, "").strip()
                #print(cog)
                if concept not in cognates:
                    cognates[concept] = cogidx
                    cogidx += 1
                cogid = cognates[concept]
                for lex in args.writer.add_forms_from_value(
                        Language_ID=language,
                        Parameter_ID=concepts[concept],
                        Value=cog,
                        Comment=comments.get(concept, ""),
                        Source="wot",
                        Loan=get_loan(cognates["WOT_loan"], language),
                        Cognacy=cogid,
                        Year=cognates["Year"]
                        ):
                    lex["CV_Segments"] = get_clusters(lex["Segments"])
                    lex["ProsodicStructure"] = prosodic_string(lex["Segments"], _output='cv')
                    lex["FB_VowelHarmony"] = has_harmony(lex["Segments"])
                    if language == "EAH":
                        eah = lex["ID"]

                    #if language != "WOT":
                    args.writer.add_cognate(
                            lexeme=lex,
                            Cognateset_ID=cogid,
                            Source="wot"
                            )
                    #elif eah:
                    if eah:
                        args.writer.objects["BorrowingTable"].append({
                            "ID": f'{borrid}-{lex["Parameter_ID"]}',
                            "Target_Form_ID": eah,
                            "Source_Form_ID": lex["ID"],
                            "Source": lex["Source"]
                            })
                        borrid += 1

        args.writer.align_cognates()
