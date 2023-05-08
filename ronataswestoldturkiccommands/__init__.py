"""
make cldf (download size: 1GB+):

.. code-block:: sh

   python3 -m venv venv && source venv/bin/activate

   git clone https://github.com/martino-vic/ronataswestoldturkic.git
   mkdir concepticon
   cd concepticon
   git clone https://github.com/concepticon/concepticon-data.git
   cd ..
   git clone https://github.com/glottolog/glottolog.git
   git clone https://github.com/cldf-clts/clts.git

   pip install -e ronataswestoldturkic
   pip install loanpy
   pip install pytest-cldf

   cd ronataswestoldturkic
   cldfbench lexibank.makecldf lexibank_ronataswestoldturkic.py  --concepticon-version=v3.0.0 --glottolog-version=v4.5 --clts-version=v2.2.0 --concepticon=../concepticon/concepticon-data --glottolog=../glottolog --clts=../clts

   pytest --cldf-metadata=cldf/cldf-metadata.json test.py
   

make edictor:

.. code-block:: sh

   cldfbench ronataswestoldturkic.maketoedict_rc H EAH
   cldfbench ronataswestoldturkic.maketoedict_ad WOT EAH

   cldfbench ronataswestoldturkic.cvgapedicted WOT EAH

   cldfbench ronataswestoldturkic.evaledicted H EAH
   cldfbench ronataswestoldturkic.evaledicted WOT EAH


make loanpy:

.. code-block:: sh

   cldfbench ronataswestoldturkic.mineEAHinvs invs.json
   cldfbench ronataswestoldturkic.makeheur EAH heur.json
   cldfbench ronataswestoldturkic.minesc H EAH
   cldfbench ronataswestoldturkic.minesc WOT EAH heur.json
   cldfbench ronataswestoldturkic.vizsc H EAH
   cldfbench ronataswestoldturkic.vizsc WOT EAH
   cldfbench ronataswestoldturkic.evalsc H EAH "[10, 100, 500, 700, 1000, 5000, 7000]"
   cldfbench ronataswestoldturkic.evalsc WOT EAH "[10, 100, 500, 700, 1000, 5000, 7000]" True True heur.json
   cldfbench ronataswestoldturkic.plot_eval H EAH
   cldfbench ronataswestoldturkic.plot_eval WOT EAH


"""
