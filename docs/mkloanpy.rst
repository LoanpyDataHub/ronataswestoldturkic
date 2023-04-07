Part 3: Analyse data with loanpy
================================

In this section we are inputting aligned CLDF data into to loanpy to mine sound correspondence patterns and verify their predictive power.

Step 1: Mine phonotactic inventory
----------------------------------

.. code-block:: sh

   cldfbench ronataswestoldturkic.mineEAHinvs invs.json

.. automodule:: ronataswestoldturkiccommands.mineEAHinvs
   :members:

Step 2: Create heuristic sound substitutions
--------------------------------------------

.. code-block:: sh

   cldfbench ronataswestoldturkic.makeheur EAH heur.json

.. automodule:: ronataswestoldturkiccommands.makeheur
   :members:

Step 3: Mine vertical and horizontal sound correspondences
----------------------------------------------------------

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
