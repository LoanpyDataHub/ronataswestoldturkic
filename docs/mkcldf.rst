Part 1: Create CLDF
===================

Step 1: Clone the repository
----------------------------

.. code-block:: sh

   git clone https://github.com/martino-vic/ronataswestoldturkic.git

Step 2: Clone reference catalogues
----------------------------------

.. code-block:: sh

   mkdir concepticon
   cd concepticon
   git clone https://github.com/concepticon/concepticon-data.git
   cd ..
   git clone https://github.com/glottolog/glottolog.git
   git clone https://github.com/cldf-clts/clts.git
   git clone https://github.com/martino-vic/loanpy.git
   sudo apt-get install jq


Step 3: Install commands and loanpy
----------------------------

.. code-block:: sh

   pip install -e ronataswestoldturkic
   pip install -e loanpy

Step 4: Run lexibank command
----------------------------

.. code-block:: sh

cldfbench lexibank.makecldf lexibank_ronataswestoldturkic.py \
--concepticon-version=v3.0.0 \
--glottolog-version=v4.7 \
--clts-version=v2.2.0
