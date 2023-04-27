Part 3: Analyse data with loanpy
================================

The following six steps describe how to input aligned CLDF data to `loanpy
<https://loanpy.readthedocs.io/en/latest/home.html>`_, and how to mine sound
correspondences and evaluate and visualise their predictive power.

Step 1: Mine phonotactic inventory
----------------------------------

These are necessary to predict phonotactic repairs during loanword adaptation.

.. code-block:: sh

   cldfbench ronataswestoldturkic.mineEAHinvs invs.json

.. automodule:: ronataswestoldturkiccommands.mineEAHinvs
   :members:

Step 2: Create heuristic sound substitutions
--------------------------------------------

Since any existing phoneme can be adapted when entering a language through
a loanword, we have to create a heuristic adaptation prediction for as many
IPA characters as possible, in this case 6491.

.. code-block:: sh

   cldfbench ronataswestoldturkic.makeheur EAH heur.json

.. automodule:: ronataswestoldturkiccommands.makeheur
   :members:

Step 3: Mine vertical and horizontal sound correspondences
----------------------------------------------------------

The output will serve as fuel for predicting loanword adaptations and
historical reconstructions later on.

.. code-block:: sh

   cldfbench ronataswestoldturkic.minesc H EAH

.. code-block:: sh

   cldfbench ronataswestoldturkic.minesc WOT EAH heur.json

.. automodule:: ronataswestoldturkiccommands.minesc
   :members:

Step 4: Make sound correspondences human-readable
-------------------------------------------------

The sound-correspondence file is stored as a computer-readable json.
To create a human-readable tsv-file, run:

.. code-block:: sh

   cldfbench ronataswestoldturkic.vizsc H EAH
   cldfbench ronataswestoldturkic.vizsc WOT EAH

.. automodule:: ronataswestoldturkiccommands.vizsc
   :members:

Step 5: Evaluate vertical and horizontal sound correspondences
--------------------------------------------------------------

In this section, we are checking the predictive power of the mined
sound correspondences with loanpy's `eval_all
<https://loanpy.readthedocs.io/en/latest/documentation.html#loanpy.eval_sca.eval_all>`_
function

.. code-block:: sh

   cldfbench ronataswestoldturkic.evalsc H EAH "[10, 100, 500, 700, 1000, 5000, 7000]"

.. code-block:: sh

   cldfbench ronataswestoldturkic.evalsc WOT EAH "[10, 100, 500, 700, 1000, 5000, 7000]" True True heur.json

The result:

.. image:: ../loanpy/H2EAH.jpeg

.. image:: ../loanpy/H2EAH.jpeg

TODO add image description and alt text

What happened under the hood:

.. automodule:: ronataswestoldturkiccommands.evalsc
   :members:

Step 6: Plot the evaluations
----------------------------

To gauge the performance of the model, we can plot an ROC curve, calculate its
optimum cut-off value and its Area under the curve (AUC), a common metric
to evaluate predictive models:

.. code-block:: sh

   cldfbench ronataswestoldturkic.plot_eval H EAH
   cldfbench ronataswestoldturkic.plot_eval WOT EAH

.. automodule:: ronataswestoldturkiccommands.plot_eval
   :members:

TODO show performance after leaving out unique sound correspondences
