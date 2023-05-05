"""

#. Add tipa package import to preamble
#. Replace badges with plain links
#. Replace IPA characters that throw errors in latex2pdf conversion
with commands for the tipa LaTeX-package.

"""
TIPAPREAMBLE = {
r'\usepackage{babel}':
r'\usepackage{babel}' + '\n' + r'\usepackage[tone]{tipa}'
}

IPA2TIPA = {  # tipa encodings of ipa chars that threw an error
"ː": r"\textipa{:}",
"ʃ": r"\textipa{S}",
"ɣ": r"\textipa{G}",
"ɒ": r"\textipa{6}",
"ɯ": r"\textipa{W}",
"ɡ": r"\textipa{g}"
}

REPLACEBADGES = {  # plain links, no badges

r"\sphinxhref{https://creativecommons.org/licenses/by/4.0/}" +
r"{\sphinxincludegraphics{{/home/viktor/Documents/GitHub/" +
r"ronataswestoldturkic/docs/doctrees/images/" +
r"554312bbffabcb804cf4f8c50b1b75a140d3bd2b/by}.svg}}":

r"License: CC BY 4.0\\\\" + "\n",

r"\sphinxhref{https://dl.circleci.com/status-badge/redirect/gh/" +
r"LoanpyDataHub/ronataswestoldturkic/tree/main}{\sphinxincludegraphics" +
r"{{/home/viktor/Documents/GitHub/ronataswestoldturkic/docs/doctrees/" +
r"images/37c8488ab183241f9a195a8e4b6d134dbb76fcfb/main}.svg}}":

r"Continuous integration: " +
r"https://dl.circleci.com/status-badge/redirect/gh/" +
r"LoanpyDataHub/ronataswestoldturkic/tree/main\\\\"  + "\n",

r"\sphinxhref{https://ronataswestoldturkic.readthedocs.io/en/latest/" +
r"?badge=latest}{\sphinxincludegraphics{{/home/viktor/Documents/GitHub/" +
r"ronataswestoldturkic/docs/doctrees/images/" +
r"51c6692a033bc6b2d053338e360f0e5cb5257b2a/8" +
r"89032453c4b117e7c632a643c47384c56c00e48}.svg}}":

r"Documentation: https://ronataswestoldturkic.readthedocs.io/en/latest/\\\\" +
"\n",

r"\sphinxhref{https://github.com/martino-vic/ronataswestoldturkic/" +
r"actions?query=workflow\%3ACLDF-validation}{\sphinxincludegraphics" +
r"{{/home/viktor/Documents/GitHub/ronataswestoldturkic/docs/doctrees/" +
r"images/3d91d1e517a7c80ca0d1f5487c7a52d36188023d/badge}.svg}}":

r"CLDF validation: " +
r"https://github.com/martino-vic/ronataswestoldturkic/" +
r"actions?query=workflow\%3ACLDF-validation\\\\" +
"\n",

r"\sphinxincludegraphics{{/home/viktor/Documents/GitHub/" +
r"ronataswestoldturkic/docs/doctrees/images/" +
r"d3b7b04c8c69ea0a5a188f4f06f393e4727087af/Glottolog-57%25-red}.svg}":

r"Glottolog: 57\%\\\\" + "\n",

r"\sphinxincludegraphics{{/home/viktor/Documents/GitHub/" +
r"ronataswestoldturkic/docs/doctrees/images/" +
r"39a19d0489904f8fb53e837d46204fa4f34f1775/Concepticon-62%25-orange}.svg}":

r"Concepticon: 62\%\\\\" + "\n",

r"\sphinxincludegraphics{{/home/viktor/Documents/GitHub/" +
r"ronataswestoldturkic/docs/doctrees/images/" +
r"8610b4fe2e7a97bed23df74a39cd30feda0b8612/Source-100%25-brightgreen}.svg}":

r"Source: 100\%\\\\",

r"\sphinxincludegraphics{{/home/viktor/Documents/GitHub/" +
r"ronataswestoldturkic/docs/doctrees/images/" +
r"54c8ae34ac3ec41286b604aef9bcbad15a74f3de/BIPA-100%25-brightgreen}.svg}":

r"BIPA: 100\%\\\\" + "\n",

r"\sphinxincludegraphics{{/home/viktor/Documents/GitHub/" +
r"ronataswestoldturkic/docs/doctrees/images/" +
r"64600fa1cdb6b54d89ce1e5ebac95262ca62a8fc/" +
r"b8fdf0ffe8e33ddbdc635aa3b469289f77c84efb}.svg}":

r"CLTS SoundClass: 100\%\\\\" + "\n"

}

def process_tex_file(input_filename, output_filename):
    """
    #. Read the file from specified path
    #. Apply changes from dictionaries defined on top
    #. Write file to specified path

    For ipa2tipa cheat sheets see
    https://jon.dehdari.org/tutorials/tipachart_mod.pdf
    and https://ptmartins.info/tex/tipacheatsheet.pdf
    """
    with open(input_filename, 'r', encoding='utf-8') as input_file:
        content = input_file.read()

    for dictionary in [TIPAPREAMBLE, IPA2TIPA, REPLACEBADGES]:
        for key in dictionary:
            content = content.replace(key, dictionary[key])

    with open(output_filename, 'w', encoding='utf-8') as output_file:
        output_file.write(content)


if __name__ == "__main__":
    process_tex_file(
        'docs/latex/ronataswestoldturkic.tex',
        'docs/latex/ronataswestoldturkic2.tex'
        )
