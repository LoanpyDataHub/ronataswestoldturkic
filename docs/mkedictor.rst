Part 2: Align words with Edictor
================================

In this section we are going to further process the CLDF data by adding
alignments to related words. Alignments are there to tell you which sound
corresponds to which in an etymology. For example, in "aːkoʃ < aːɡoʃ" the
sound correspondences are "aː < aː, k < g, o < o, ʃ < ʃ". When we align words
between a descendant and an ancestor language like Hungarian and Old
Hungarian, words are transferred through time and sound correspondences are
called historical sound changes. When we align recipient and donor languages
like Early Ancient Hungarian and West Old Turkic, words are transferred
through space and sound correspondences are called sound adaptations.
These two types of transfers lead to fairly regular transformations.
Nevertheless they differ in many ways from each other, both in how they are
conceptualised and researched, as well as in their outcomes. Having good
alignments for each individual etymology is the basis for identifying
larger correspondence patterns over a data set. There is a multitude of
automatic alignment-algorithms out there, most of which are inspired by
bioinformatics. However, non of them is good enough yet to replace
expert-knowledge. Therefore, a hybrid approach is currently the best:
At first, related words are automatically aligned. This is done with the
`lingpy <https://lingpy.org/>`_ package, which contains various different
alignment methods, and the `loanpy <https://pypi.org/project/loanpy/>`_
package, which contains a custom alignment method specifically designed
for the type of data of our use case. Then, they are uploaded to the
`Edictor <https://digling.org/edictor/>`_, an interactive tool to manually
align words. Once the results of the algorithmic approach are complemented
by expert knkowledge, the data can be downloaded. Finally, the format of
the manually edited data can be checked for suitability as input for
loanpy, a Python software package for finding loanwords.

The following steps will guide you through the process of converting the
data to Edictor-suitable input, uploading it to Edictor, editing it there,
downloading it, post-editing it locally, and evaluating whether its format is
suitable as input for loanpy.

.. seealso::

   `Edictor <https://digling.org/edictor/>`_

   `LoanPy <https://pypi.org/project/loanpy/>`_


Step 1: Create input files for Edictor
--------------------------------------

During the CLDF-conversion we have added automated alignments to the column
``ALIGNMENTS`` in ``cldf/cognates.csv``. But these are the results of aligning
cognates from *all* available languages to each other, while for our own
analyses we need alignments for only two languages. Therefore, we
first create the input data for Edictor for sound corrrespondences between
Hungarian and Early Ancient Hungarian words with following command:

.. code-block:: sh

   cldfbench ronataswestoldturkic.maketoedict_rc H EAH

The *_rc* in the script name is an internal abbreviation for "reconstruction",
since we are aiming to align words from languages that are in a historical
relationship to each other. This is what happens under the hood when running
the script:

.. automodule:: ronataswestoldturkiccommands.maketoedict_rc
   :members:

Now that we have created automatic alignments for historical reconstructions,
let's do the same for sound adaptations. This is done by running the following
command from your terminal:

.. code-block:: sh

   cldfbench ronataswestoldturkic.maketoedict_ad WOT EAH

The *_ad* in the script name is an internal abbreviation for "adaptation",
since we are aiming
to align words from languages that are in a donor-recipient relationship to
each other. This is what happens under the hood:

.. automodule:: ronataswestoldturkiccommands.maketoedict_ad
   :members:

Now that we have created suitable input files for the Edictor, it is time to
upload and edit them with our expert knowledge.

Step 2: Edit horizontal and vertical sound correspondences with Edictor
-----------------------------------------------------------------------

`Edictor <https://digling.org/edictor/>`_ is an interactive tool for managing
etymological data. We will use it to improve the automated alignments that we
have created in the previous step. To familiarise yourself with Edictor, you
can read its `release paper <https://aclanthology.org/E17-3003.pdf>`_,
`this use-case <https://hcommons.org/deposits/item/hc:43687/>`_ or watch its
`Youtube tutorial <https://www.youtube.com/watch?v=IyZuf6SmQM4>`_.

For editing vertical sound correspondences (i.e. historical sound changes):

#. Upload: Click on ``Browse``, select ``edictor/H2EAHtoedict.tsv``, click on
   ``Open the file``
#. Load columns: Click on ``select Columns`` on top, tick ``select all``,
   click ``OK``.
#. Edit alignments: Left-click once in the row of the ``ALIGNMENT``
   column that you want to edit, edit, left-click again to keep the changes.
#. Syntax of alignments:

   - Single-space: separator between IPA tokens
   - Dot symbol: separator of IPA tokens within clusters of IPA-sounds
   - Minus symbol: gap symbol for sounds that disappeared or didn't exist
   - Plus symbol: trimming border for prefixes and suffixes that will be
     ignored in analyses. The file ``etc/formspec.json`` was created
     based on these.
   - Hash symbol: Word boundary
   
#. Cache: Click on the floppy-disk symbol in the top-right corner or use
   ``Ctrl + S``
#. Download: Click on the downwards pointing arrow symbol in the top-right
   corner or use ``Ctrl + E``. Click on ``Save file``. Move it to your local
   ``edictor/`` directory and name it ``H2EAHedicted.tsv``.

In the custom-alignment of this use-case, we first clustered vowels and
consonants together with the dot-symbol and used spaces to separate those
clusters from each other. Wherever it seemed appropriate, we allowed sound
correspondences of one to many, e.g. in *aː < a.ɣ.a*, which is a well studied
pattern in our data but difficult for an algorithm to catch.

For editing horizontal sound correspondences (i.e. sound adaptations):

Follow the same steps, but this time upload ``edictor/WOT2EAHtoedict.tsv``.
Here, we are allowing only one to one correspondences and ingore word
boundaries. After downloading the aligned data, a post-editing step is
necessary. This is carried out with following command:

.. code-block:: sh

   cldfbench ronataswestoldturkic.cvgapedicted WOT EAH

.. automodule:: ronataswestoldturkiccommands.cvgapedicted
   :members:

This step has been outsourced to post-processing in order to avoid any
confusion by missing gap symbols during the manual editing process of
alignments.

Step 3: Validate whether this is suitable as input for loanpy
-------------------------------------------------------------

Now that we have improved the alignments by complementing the algorithmic
approach with expert knowledge, the only thing left to do is to validate
whether the format of our data is suitable as input for loanpy. This can be
done by running following two commands:

.. code-block:: sh

   cldfbench ronataswestoldturkic.evaledicted H EAH

and

.. code-block:: sh

   cldfbench ronataswestoldturkic.evaledicted WOT EAH

This is what happens under the hood:

.. automodule:: ronataswestoldturkiccommands.evaledicted
   :members:

Both commands printing "OK" to the console means that we have successfully
edited the alignments of our etymological data set and are ready to move on
to part 3 by clicking on the ``Next`` button.
