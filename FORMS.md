## Specification of form manipulation


Specification of the value-to-form processing in Lexibank datasets:

The value-to-form processing is divided into two steps, implemented as methods:
- `FormSpec.split`: Splits a string into individual form chunks.
- `FormSpec.clean`: Normalizes a form chunk.

These methods use the attributes of a `FormSpec` instance to configure their behaviour.

- `brackets`: `{'(': ')'}`
  Pairs of strings that should be recognized as brackets, specified as `dict` mapping opening string to closing string
- `separators`: `,`
  Iterable of single character tokens that should be recognized as word separator
- `missing_data`: `('?', '-')`
  Iterable of strings that are used to mark missing data
- `strip_inside_brackets`: `True`
  Flag signaling whether to strip content in brackets (**and** strip leading and trailing whitespace)
- `replacements`: `[('ajnároz', 'ajn'), ('ápol', 'áp'), ('áporodik', 'áporo'), ('árik', 'ár'), ('baszik', 'basz'), ('bocsánik', 'bocsán'), ('bakancs', 'bakan'), ('borít', 'bor'), ('burok', 'bur'), ('bűvös', 'bű'), ('csatol', 'csat'), ('csekély', 'csek'), ('csökok', 'csök'), ('csökönyös', 'csököny'), ('egyház', 'egy'), ('enged', 'eng'), ('engesztel', 'eng'), ('gyaláz', 'gyalá'), ('gyarapodik', 'gyarap'), ('gyarapszik', 'gyarap'), ('ijed', 'ije'), ('ijeszt', 'ije'), ('illik', 'ill'), ('imád', 'im'), ('izzik', 'izzi'), ('kárókatona', 'kárókaton'), ('kérődzik', 'kér'), ('késik', 'kés'), ('koldul', 'koldu'), ('koldus', 'koldu'), ('köpcsös', 'köpcö'), ('mónár köd', 'mónár'), ('oktat', 'okt'), ('önik', 'ön'), ('örül', 'ör'), ('sebes', 'seb'), ('serte', 'sert'), ('séd', 'sé'), ('sólyom', 'sólyo'), ('szender', 'szend'), ('szöndör', 'szönd'), ('szöcske', 'szöcsk'), ('szökik', 'szök'), ('szűnik', 'szűn'), ('táplál', 'táplá'), ('lengődik', 'leng'), ('térül', 'tér'), ('tojik', 'toj'), ('torlódik', 'torló'), ('torlik', 'torli'), ('tökéletes', 'töké'), ('töméntelen', 'tömén'), ('történik', 'történ'), ('üdül', 'üdü'), ('kara katona', 'karakatona'), ('kara kotan', 'karakotan'), ('kenä šū', 'kenäšū')]`
  List of pairs (`source`, `target`) used to replace occurrences of `source` in formswith `target` (before stripping content in brackets)
- `first_form_only`: `True`
  Flag signaling whether at most one form should be returned from `split` - effectively ignoring any spelling variants, etc.
- `normalize_whitespace`: `True`
  Flag signaling whether to normalize whitespace - stripping leading and trailing whitespace and collapsing multi-character whitespace to single spaces
- `normalize_unicode`: `None`
  UNICODE normalization form to use for input of `split` (`None`, 'NFD' or 'NFC')