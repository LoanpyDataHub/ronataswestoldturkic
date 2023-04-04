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

The -e flag will install all necessary dependencies in development mode.
I.e. if you modify any code in those repositories, changes will apply
immediately.

.. code-block:: sh

   pip install -e ronataswestoldturkic
   pip install -e loanpy

Step 4: Run lexibank command
----------------------------

.. literalinclude:: ../../wot.sh
   :language: bash

Step 5: Create Hungarian IPA transcriptions from cldf/forms.csv
---------------------------------------------------------------

.. code-block:: sh
