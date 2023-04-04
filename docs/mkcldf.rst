Part 1: Create CLDF
===================

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


Below is a detailed description of what the script does. See also the tutorial at https://calc.hypotheses.org/3318, which has many similarities.

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

Here we define a class and inherit the default format ``BaseDataset`` that we have imported in the beginning. ``dir`` is the working directory and is defined with the help of ``pathlib`` that we have imported in the beginning. ``id`` is the name of the repository. In ``lexeme_class`` we are plugging in the custom columns that we have created earlier. In ``form_spec`` we are plugging in the data-cleaning rules that were hard coded in ``etc/formspec.json`` and read into the ``REP`` variable earlier, using the ``FormSpec```class we have imported in the beginning.

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
        #print(concepts)

This section of the script creates the file ``cldf/parameters.csv``, which links the translations of words to concepts in `Concepticon <https://concepticon.clld.org/>`_. It is based on ``etc/concepts.tsv``, which was created through multiple steps. At first, the translations were mapped automatically with the `pysem <https://pypi.org/project/pysem/>`_ library. Then, these mappings were manually refined and requested to be submitted to Concepticon through a `Pull Request on GitHub <https://github.com/concepticon/concepticon-data/pull/1240>`_. After some discussion and further refinement, the conceptlist was submitted and is available `here <https://concepticon.clld.org/contributions/RonaTas-2011-431>`_. The file ``etc/concepts.tsv`` was then accordingly copied again from `GitHub <https://github.com/concepticon/concepticon-data/blob/master/concepticondata/conceptlists/RonaTas-2011-431.tsv>`_

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
is clearly present in Glottolog. Old Hungarian is missing, but a `request<https://github.com/glottolog/glottolog/issues/899>`_ was opened to
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



Step 5: Create Hungarian IPA transcriptions from cldf/forms.csv
---------------------------------------------------------------

.. code-block:: sh

   cd ronataswestoldturkic
   cldfbench ronataswestoldturkic.makeHortho

Step 6: Re-run lexibank script with Hungarian orthography
---------------------------------------------------------

.. code-block:: sh

   cldfbench lexibank.makecldf lexibank_ronataswestoldturkic.py  --concepticon-version=v3.0.0 --glottolog-version=v4.5 --clts-version=v2.2.0

Step 7: Test with pytest-cldf whether the dataset is CLDF-conform
-----------------------------------------------------------------


.. code-block: sh

   pip install pytest-cldf
   pytest --cldf-metadata=cldf/cldf-metadata.json test.py
