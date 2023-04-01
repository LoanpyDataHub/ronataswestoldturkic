### How to create the cldf folder and how to use these commands.

1. create a virtual environment and activate it with `python -m venv venv && source venv/bin/activate`
2. cd to the directory where this repository is saved
3. run `pip install -e ronataswestoldturkic`
4. run `cldfbench ronataswestoldturkic.your_script`. E.g. the script makesc.py is run with `cldfbench ronataswestoldturkic.makesc` (without the .py extension)

### In which order to use the commands and what they do

1. `makeHortho.py`: This script creates the orthography profile for Hungarian.
2. Run `bash wot.sh`: This will run the lexibank script and create the data in the cldf-folder
3. Run `maketoedict_rc.py` for reconstructions or maketoedict_ad for adaptations: This will create the input file for the Edictor at digling.org/edictor.
4. Upload the file to the Edictor, edit it, download the result and save it in the same edictor-folder.
5. Run evaledicted.py to evaluate whether the format serves as input for loanpy
6. Run cvgapedicted to replace the "-" symbol with "C" or "V", which is necessary for loanpy to work.
7. Congratulations, you have a ready input-file for loanpy.
