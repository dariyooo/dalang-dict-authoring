# Radicals (`dakanji-radicals`)

Radicals of the kanji for the radical search, from KRADFILE/RADKFILE.

## Archive structure

```text
dictionary.zip
├── index.json          # Required dictionary metadata (Yomitan index schema)
├── radkfile.json       # The radicals with their stroke count, name contains `radk`
└── kradfile.json       # The radicals of every kanji, name contains `krad`
```

DaLang detects the archive by one file whose name contains `radk` and one whose name contains `krad`.
Both are read from the zip root.

## Schemas

* [radk-schema.json](radk-schema.json)
* [krad-schema.json](krad-schema.json)

Every radical a kanji names in the krad file must be in the radk file (after DaLang's lookup of variant forms),
otherwise the import fails.

## Sample

[kanji-radicals-dakanji](https://github.com/dariyooo/kanji-radicals-dakanji)
