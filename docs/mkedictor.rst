Part 2: Align words with Edictor
================================

In this section we are going to further process the CLDF data by adding alignments to related words. Alignments are there to tell you which sound corresponds to which in an etymology. For example, in "aːkoʃ < aːɡoʃ" the sound correspondences are "aː < aː, k < g, o < o, ʃ < ʃ". When we align words between a descendant and an ancestor language like Hungarian and Old Hungarian, words are transferred through time and sound correspondences are called historical sound changes. When we align recipient and donor languages like Early Ancient Hungarian and West Old Turkic, words are transferred through space and sound correspondences are called sound adaptations. These two types of transfers lead to fairly regular transformations. Nevertheless they differ in many ways from each other, both in how they are conceptualised and researched, as well as in their outcomes. Having good alignments for each individual etymology is the basis for identifying larger correspondence patterns over a data set. There is a multitude of automatic alignment-algorithms out there, most of which are inspired by bioinformatics. However, non of them is good enough yet to replace expert-knowledge. Therefore, a hybrid approach is currently the best: At first, related words are automatically aligned. Then, they are uploaded to the `Edictor <https://digling.org/edictor/>`_, an interactive tool to manually align words. Once the results of the algorithmic approach are complemented by expert knkowledge, the data can be downloaded. Finally, the format of the manually edited data can be checked whether it is suitable as input for `loanpy <https://pypi.org/project/loanpy/>`_, a Python software package for finding loanwords.

The following steps will guide you through the process of converting the data to Edictor-suitable input, uploading it to Edictor, editing it there, downloading it, post-editing it locally, and evaluating whether its format is suitable as input for loanpy.

Step 1: Creating input files for the Edictor
--------------------------------------------

During the CLDF-conversion we have added automated alignments to the column
`ALIGNMENTS` in `cldf/cognates.csv`. However, since these
First we create the input data for Edictor for sound corrrespondences between
Hungarian and Early Ancient Hungarian words with following command:

.. code-block:: sh

   cldfbench ronataswestoldturkic.maketoedict_rc H EAH

This is what happens under the hood when you run the script:

.. automodule:: ronataswestoldturkiccommands.maketoedict_rc
   :members:

Now that we have created automatic alignments
