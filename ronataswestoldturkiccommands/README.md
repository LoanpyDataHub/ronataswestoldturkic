# Linux Command line interface (CLI)

## How to use

- Run `pip install -e tryonbislam` from the root directory (usually GitHub)
- Run `cldfbench tryonbislama.makeortho` to create IPA-transcriptions of English words and write them to ./etc/orthography/English.tsv
- Run `cldfbench tryonbislama.makecomments` to extract comments from ./raw/bislama.tsv and write to ./etc/comments.tsv
- Run `cldfbench tryonbislama.map2concepts` to map meanings to concepticon with pysem

## When to use
- Run `cldfbench tryonbislama.makeortho` after CLDF-conversion, since forms are extracted from ./cldf/forms.csv, since orthography can only be based on cleaned forms.
- `cldfbench tryonbislama.makecomments` and `cldfbench tryonbislama.map2concepts` can be run before conversion, since input is ./raw/bislama.tsv
