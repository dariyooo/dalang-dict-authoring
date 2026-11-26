# Index extension

Keys DaLang reads from `index.json` (or `yomitan_index.json` in audio archives) on top of
[Yomitan's index schema](../../yomitan/dictionary-index-schema.json).

## Schema

[dictionary-index-extension-schema.json](dictionary-index-extension-schema.json)

* `exampleTokenization: "manual"`: example dictionaries whose sentences carry the searchable forms as inline markup.
* `minimumDaLangVersion`: the oldest DaLang (and app) version that reads every file of the dictionary.
