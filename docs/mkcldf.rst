Part 1: Create CLDF
===================

The following seven steps will guide you through the process of
converting raw language data to CLDF. Each step can be found in the
`continuous integration workflow
<https://app.circleci.com/pipelines/github/martino-vic/ronataswestoldturkic?branch=main>`_
as well. The data we are converting comes from
the etymological dictionary "West Old Turkic" (Róna-Tas and Berta 2011),
which contains modern Hungarian words as headwords, together with their
documented and reconstructed ancestor forms, including their
West Old Turkic donor words. West Old Turkic, also called Proto-Bolgar,
or Oghur-Turkic, or r-Turkic, is the parent language of the western branch
of Turkic languages. The raw data contains only a small fraction of the
contents of the dictionary. If you are passionate about pdf-wrangling,
Mongolic, Turkic, or Finno-Ugric languages and want to expand this data set,
definitely check out the `contribution guidelines
<https://github.com/martino-vic/ronataswestoldturkic/blob/main/CONTRIBUTING.md>`_
and let's get in touch!

Step 1: Clone the repository
----------------------------

.. code-block:: sh

   git clone https://github.com/martino-vic/ronataswestoldturkic.git

Step 2: Clone reference catalogues and loanpy
---------------------------------------------

- `Glottolog <https://glottolog.org/>`_ (Hammarström et al. 2022)
  to reference the languages in the repo.
- `Concepticon <https://concepticon.clld.org/>`_ (List et al. 2023) for
  referencing concepts.
- `loanpy <https://loanpy.readthedocs.io/en/latest/?badge=latest>`_
  (Martinović 2022). This step will not be necessary once version 3 is out.

.. code-block:: sh

   mkdir concepticon
   cd concepticon
   git clone https://github.com/concepticon/concepticon-data.git
   cd ..
   git clone https://github.com/glottolog/glottolog.git
   git clone https://github.com/cldf-clts/clts.git
   git clone https://github.com/martino-vic/loanpy.git


Step 3: Install commands
------------------------

The ``-e`` flag will install all necessary dependencies in development mode.
I.e. if you modify any code in those repositories, changes will apply
immediately.

.. code-block:: sh

   pip install -e ronataswestoldturkic
   pip install -e loanpy

Step 4: Run lexibank script
---------------------------

This script combines files from the raw and etc folders and creates and
populates the folder cldf

.. code-block:: sh

   cldfbench lexibank.makecldf lexibank_ronataswestoldturkic.py  --concepticon-version=v3.0.0 --glottolog-version=v4.5 --clts-version=v2.2.0


Below is a detailed description of what the script does. See also the tutorial at https://calc.hypotheses.org/3318, which has many similarities. This is the first lexibank script that uses the ``args.writer.align_cognates()`` prompt for automatic cognate alignment (see discussion on GitHub `here <https://github.com/lexibank/pylexibank/issues/267#issuecomment-1418959540>`_).

.. code-block:: python

   import json
   import pathlib

   import attr
   from clldutils.misc import slug
   from lingpy import prosodic_string
   from lingpy.sequence.sound_classes import token2class
   from pylexibank import Dataset as BaseDataset, FormSpec, Lexeme

First, we import two inbuilt Python-libraries.

- The The `json <https://docs.python.org/3/library/json.html>`_ library
  will be used to read the data-cleaning instructions for FormSpec
- The `pathlib <https://docs.python.org/3/library/pathlib.html>`_ library
  will be used to define file paths

Then, we import functionalities from various third-party libraries.
These dependencies were installed when running
``pip install -e ronataswestoldturkic`` eariler.

- The attr library from the PyLexibank ecosystem will create the custom language class with
  custom columns in the output file ``cldf/forms.csv``.
- The `slug <https://clldutils.readthedocs.io/en/latest/misc.html#clldutils.misc.slug>`_
  function from the clldutils library will be used to format some IDs
- The `prosodic_string <https://lingpyxrotwang.readthedocs.io/en/latest/reference    /lingpy.sequence.html#lingpy.sequence.sound_classes.prosodic_string>`_
  function from the lingpy library will be used to create the phonotactic
  structures of words.
- The `token2class <https://lingpyxrotwang.readthedocs.io/en/latest/reference/lingpy.sequence.html#lingpy.sequence.sound_classes.token2class>`_
  function from the lingpy library will be used to identify whether an IPA
  character is a vowel or a consonant
- The classes from the `pylexibank <https://pypi.org/project/pylexibank/>`_
  library are all related to specifying the output format. Dataset, for example
  loads the default data format, Lexeme will be used to customise it, and
  FormSpec will be used to document the cleaning of the raw data.

.. code-block:: python

   with open("etc/formspec.json") as f:
       REP = [(k, v) for k, v in json.load(f).items()]

The variable REP stands for 'replacements' and will later be used to create
the column "forms" from the column "values", where replacements are hard-coded.
Since the number of transformations is too large to include them in this
script, they were written to a json-file, which is loaded here.

.. code-block:: python

   @attr.s
   class CustomLexeme(Lexeme):
       CV_Segments = attr.ib(default=None)
       ProsodicStructure = attr.ib(default=None)
       FB_VowelHarmony = attr.ib(default=None)
       Year = attr.ib(default=None)

Here we define custom columns that are not included by default, using the attr library and the
Lexeme class that we have imported earlier.

.. code-block:: python

    def get_clusters(segments):
        """
        Takes a list of phonemes and segments them into consonant and vowel
        clusters, like so: "abcdeaofgh" -> ["a", "b.c.d", "e.a.o", "f.g.h"]
        """
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

Here we define a function that will segment the phonemes in a word according to consonant
and vowel clusters.

.. code-block:: python

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

Here we define a function that checks whether a word has vowel harmony or not.

.. code-block:: python

    def get_loan(loan, language):
        return loan == "TRUE" if language == "WOT" else True

Here we convert the information from the column ``WOT_loan`` in ``raw/wot.tsv`` to
booleans. This has to be a separate function and can't be implemented through a lambda.

.. code-block:: python

    class Dataset(BaseDataset):
        dir = pathlib.Path(__file__).parent
        id = "ronataswestoldturkic"
        lexeme_class = CustomLexeme
        form_spec = FormSpec(separators=",", first_form_only=True,
                             replacements= REP)

Here we define a class and inherit the default format ``BaseDataset`` that we have imported in the beginning. ``dir`` is the working directory and is defined with the help of ``pathlib`` that we have imported in the beginning. ``id`` is the name of the repository. In ``lexeme_class`` we are plugging in the custom columns that we have created earlier. In ``form_spec`` we are plugging in the data-cleaning rules that were hard coded in ``etc/formspec.json`` and read into the ``REP`` variable earlier, using the ``FormSpec`` class we have imported in the beginning.

.. code-block:: python

	def cmd_makecldf(self, args):

This function is being run when summoning the lexibank script from the command line. It converts the data from raw and etc to standardised CLDF data.

.. code-block:: python


        #add borrowing table
        args.writer.cldf.add_component(
            "BorrowingTable"
        )

Here we are creating a file ``borrowings.csv`` which will contain the IDs of
donor and recipient words.

.. code-block:: python

        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

In the first line we are adding the bibliography from ``raw/sources.bib``. This is a `BibTex <https://en.wikipedia.org/wiki/BibTeX>`_ file containing references to all sources from which the data in the folders ``raw`` and ``etc`` was acquired. In the second line we print to the console
that the sources were added successfully. This can be helpful for debugging.

.. code-block:: python

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

This section of the script creates the file ``cldf/parameters.csv``, which links the translations of words to concepts in `Concepticon <https://concepticon.clld.org/>`_. It is based on ``etc/concepts.tsv``, which was created through multiple steps. At first, the translations were mapped automatically with the `pysem <https://pypi.org/project/pysem/>`_ library. Then, these mappings were manually refined and requested to be submitted to Concepticon through a `Pull Request on GitHub <https://github.com/concepticon/concepticon-data/pull/1240>`_. After some discussion and further refinement, the conceptlist was submitted and is available `here <https://concepticon.clld.org/contributions/RonaTas-2011-431>`__. The file ``etc/concepts.tsv`` was then accordingly copied again from `GitHub <https://github.com/concepticon/concepticon-data/blob/master/concepticondata/conceptlists/RonaTas-2011-431.tsv>`_

.. code-block:: python

        #add comments
        comments = self.etc_dir.read_csv(
            "comments.tsv", delimiter="\t",
        )  # [['ENGLISH', 'Comment'], ['a', 'b'], ['c', 'd']]
        comments = {line[0]: line[1] for line in comments}
        args.log.info("added comments")

Here we are reading the file ``etc/comments.tsv``, which was originally created with a custom script from an additional column in ``raw/wot.tsv``.

.. code-block:: python

        # add language
        languages = args.writer.add_languages()
        args.log.info("added languages")

Here we read the file ``etc/languages.tsv`` which contains the references to `Glottolog <https://glottolog.org/>`_. Out of the five languages in this repository, only Hungarian
is clearly present in Glottolog. Old Hungarian is missing, but a `request <https://github.com/glottolog/glottolog/issues/899>`_ was opened to
add it and after some discussion there seems to be a plan to include it in a future version
of Glottolog.

.. code-block:: python

        # add forms and borrowings
        data = self.raw_dir.read_csv(
            "wot.tsv", delimiter="\t",
        )
        header = data[0]
        cognates = {}
        cogidx = 1
        borrid = 1

Here we read the file ``raw/wot.tsv`` and define some variables that we are going to use
in a bit.

.. code-block:: python

        for i in range(1, len(data)):
            cognates = dict(zip(header, data[i]))
            concept = data[i][7]
            eah = ""

Here we will loop through the raw data ``raw/wot.tsv`` row by row from top to bottom and define some variables that we will need later. The column "ENGLISH" is hard-coded as column seven. If it was to be moved to a different index for which ever reason, the index in this part of the code would need to be updated accordingly.

.. code-block:: python

            for language in languages:

Here we loop from left to right through the columns of each row, which contain data relating to words in different languages. The languages themselves were defined earlier in ``etc/languages.tsv``.

.. code-block:: python

                cog = cognates.get(language, "").strip()

Here we are reading the specific word in the specific language from the raw data.

.. code-block:: python

                if concept not in cognates:
                    cognates[concept] = cogidx
                    cogidx += 1
                cogid = cognates[concept]

The goal of this section is simply to assign a unique cognate ID to each English translation in column seven. Identical translations will get identical IDs. This value will appear in the column ``Cognacy`` in the output file ``cldf/forms.csv`` later.

.. code-block:: python

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

This is arguably the most important part of the script. It creates the file ``cldf/forms.csv`` which will serve as the main input file for further analyses. ``args.writer.add_forms_from_value`` creates the file, through which we then loop. The arguments in the brackets are the column names. ``Language_ID`` is the name of the language according to ``etc/languages.tsv``. ``Parameter_ID`` references the relevant row in ``parameters.csv``, which was created in an earlier code-block. ``Value`` is the original raw data. The column "Form" is automatically being created from this by applying the cleaning procedure specified in the ``formspec.json`` file which was read into the ``REP`` variable in the beginning. The column ``Comment`` uses the English translations as dictionary keys to look up the according comment as specified in ``etc/comments.tsv``. The entire data set is based on one source. In the column ``Source`` we are specifying the BibTex key of it, as described in ``raw/sources.bib``. The column ``Loan`` specifies whether a word is a loanword or not. This information is stored in column ``WOT_loan`` in ``raw/wot.tsv`` and is converted to a boolean through the function ``get_loan`` which was described in an earlier code-block. ``Cognacy`` assigns a unique identifier to each cognate set in the form of an integer that starts at 1 and is incremented by 1 with each new cognate set. The column ``Year`` is another custom column that was specified in the CustomLexeme class earlier. This information is provided in column ``Year`` in ``raw/wot.tsv``.

.. code-block:: python

                    lex["CV_Segments"] = get_clusters(lex["Segments"])
                    lex["ProsodicStructure"] = prosodic_string(lex["Segments"], _output='cv')
                    lex["FB_VowelHarmony"] = has_harmony(lex["Segments"])

Here we populate three more columns which take information in the columns of the newly generated ``cldf/forms.csv`` as input. That's why they have to be populated through a loop rather than in the brackets of the earlier function. The column ``CV_Segments`` takes the column ``Segments`` of ``cldf/forms.csv`` as input, which in turn is automatically generated from the information stored in ``etc/orthography``. But these can only be generated after the CLDF-conversion. Therefore this step does not do anything at the moment. The same applies for columns ``ProsodicStructure`` and ``FB_VowelHarmony``. These will be explained in more detail in Step 6.

.. code-block:: python

                    if language == "EAH":
                        eah = lex["ID"]

This line is storing the ID of the relevant word in ``cldf/forms.csv``, so it can later be referenced in ``cldf/borrowings.csv``.

.. code-block:: python

                    args.writer.add_cognate(
                            lexeme=lex,
                            Cognateset_ID=cogid,
                            Source="wot"
                            )

Here we create the table ``cldf/cognates.csv``. This is the table where automated alignments will be carried out, which can be used for further analyses. The term ``cognate`` here is used in its broader sense and includes all words that go back to the same etymon.

.. code-block:: python

                    if language == "WOT" and eah:
                        args.writer.objects["BorrowingTable"].append({
                            "ID": f'{borrid}-{lex["Parameter_ID"]}',
                            "Target_Form_ID": eah,
                            "Source_Form_ID": lex["ID"],
                            "Source": lex["Source"]
                            })
                        borrid += 1
                        eah = None  # reset memory

Here the file ``cldf/borrowings.csv`` is created. It contains reference keys to
``cldf/forms.csv`` to identify each donor and recipient word. It makes sure
that only those concepts are included where a form in both West Old Turkic
(the donor language) and Early Ancient Hungarian (the recipient language) exist.

.. code-block:: python

        args.writer.align_cognates()

This is the final line, which creates automated alignments with the `lingpy <https://lingpy.org/>`_ library. They are added to a newly created column called ``ALIGNMENTS`` in ``etc/cognates.csv``. This repository is the first use-case for this functionality (see `discussion on GitHub <https://github.com/lexibank/pylexibank/issues/267#issuecomment-1418959540>`_).

Step 5: Create Hungarian IPA transcriptions from cldf/forms.csv
---------------------------------------------------------------

The rules for turning words written in Hungarian orthography are generated based on ``cldf/forms.csv``. Therefore, they can only be generated after the lexibank script has run. The below command will create a list of transformation rules and write them to ``etc/orthography/H.tsv``.

.. code-block:: sh

   cd ronataswestoldturkic
   cldfbench ronataswestoldturkic.makeHortho

.. automodule:: ronataswestoldturkiccommands.makeHortho
   :members:

Step 6: Re-run lexibank script with orthography profiles
--------------------------------------------------------

After the Hungarian transcription rules were generated, we have to generate the rules for the other languages. Since they are already transcribed to a phonetic script which is unique to the source, we can create a transcription profile based on the explication of the script in the preface of the source. These transcription profiles are written to the files ``EAH.tsv`` ``LAH.tsv`` ``OH.tsv`` and ``WOT.tsv`` in the folder ``etc/orthography``. The file names have to be the language IDs, as defined in ``etc/languages.tsv``. Now that we have created some rules for IPA transcription and segmentation of words, we can rerun the lexibank script and create some more columns, which will be relevant for later analyses:

.. code-block:: sh

   cldfbench lexibank.makecldf lexibank_ronataswestoldturkic.py  --concepticon-version=v3.0.0 --glottolog-version=v4.5 --clts-version=v2.2.0

This will add columns ``Segments``, ``CV_Segments``, ``ProsodicStructure``, ``FB_VowelHarmony`` to ``cldf/forms.csv``, which were skipped in Step 4. These columns are based on tokenised IPA-strings, that were read from the files in ``etc/orthography``. After running the lexibank script, this is how your console should approximately look like:

.. image:: consoleoutput.png

Step 7: Test with pytest-cldf whether the dataset is CLDF-conform
-----------------------------------------------------------------

Now that the conversion has run successfully, the only thing left to do is to verify
that the data conforms to the CLDF standard:

.. code-block:: sh

   pip install pytest-cldf
   pytest --cldf-metadata=cldf/cldf-metadata.json test.py

This will run one single test with the `pytest <https://docs.pytest.org/en/7.2.x/>`_ library, which should pass. And with this we have converted our raw data to CLDF and thus finished part one. Click on the ``Next``-button to get to part two.
