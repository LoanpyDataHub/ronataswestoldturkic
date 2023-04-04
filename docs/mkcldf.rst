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

Here's a detailed description of what the script does:

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

Then, we are importing functionalities from various third-party libraries.
These dependencies were installed when running
``pip install -e ronataswestoldturkic`` eariler.

- The `attr <https://pypi.org/project/attrs/>`_ library will be used to assign
  custom columns to the output file ``cldf/forms.csv``.
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
