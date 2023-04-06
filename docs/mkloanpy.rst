Part 3: Analyse data with loanpy
================================

In this section we are inputting aligned CLDF data into to loanpy to mine sound correspondence patterns and verify their predictive power.

Step 1: Extract phonotactic inventory
-------------------------------------

.. code-block:: sh

   cldfbench ronataswestoldturkic.makeEAHinvs invs.json

Step 2: Create heuristic sound substitutions
--------------------------------------------

.. code-block:: sh

   cldfbench ronataswestoldturkic.makeheur EAH heur.json

Step 3: Mine vertical sound correspondences
---------------------------------------------

.. code-block:: sh

   cldfbench ronataswestoldturkic.minesc H EAH

Step 4: Mine horizontal sound correspondences
---------------------------------------------

.. code-block:: sh

   cldfbench ronataswestoldturkic.minesc WOT EAH heur.json

Step 5: Evaluate vertical sound correspondences
-----------------------------------------------

.. code-block:: sh

   cldfbench ronataswestoldturkic.evalsc H EAH "[1, 10, 50, 100, 300]"

Step 6: Evaluate horizontal sound correspondences
-------------------------------------------------

.. code-block:: sh

   cldfbench ronataswestoldturkic.evalsc WOT EAH "[1, 10, 50, 100, 300]" True True heur.json
