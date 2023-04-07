Part 3: Analyse data with loanpy
================================

In this section we are inputting aligned CLDF data to loanpy to mine sound correspondence patterns and evaluate their predictive power.

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

Step 4: Evaluate vertical and horizontal sound correspondences
--------------------------------------------------------------

.. code-block:: sh

   cldfbench ronataswestoldturkic.evalsc H EAH "[1, 10, 50, 100, 300]"

.. code-block:: sh

   cldfbench ronataswestoldturkic.evalsc WOT EAH "[1, 10, 50, 100, 300]" True True heur.json

.. automodule:: ronataswestoldturkiccommands.evalsc
   :members:
