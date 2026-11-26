# Stroke order (`dakanji-stroke-order`)

Stroke order SVGs in the [KanjiVG](https://kanjivg.tagaini.net) format.

## Archive structure

```text
dictionary.zip
├── index.json          # Required dictionary metadata (Yomitan index schema)
├── 04e00.svg           # One KanjiVG file per character
└── 05b57-Kaisho.svg    # Variants carry their name after a hyphen
```

There is no JSON schema, the files are SVGs:

* DaLang reads the character from the first `kvg:element` attribute outside of comments, a file without one
  fails the import.
* The variant comes from the root group's id, `kvg:StrokePaths_{codepoint}` or `kvg:StrokePaths_{codepoint}-{variant}`.

## Sample

[kanji-stroke-order-dakanji](https://github.com/dariyooo/kanji-stroke-order-dakanji)
