# DaKanji dictionary (`dakanji-dictionary`)

A Yomitan dictionary with extensions only the apps read.

## Archive structure

```text
dictionary.zip
├── index.json          # Required dictionary metadata
├── term_bank_1.json    # Yomitan banks, see ../../yomitan/README.md
├── audio_list.json     # (Optional) Audio sources, see audio-list-schema.json
├── manual.pdf          # (Optional) Manual, prioritized over manual.md
├── manual.md           # (Optional) Manual
└── manual_icon.svg     # (Optional) Icon of the manual
```

## Schema

[audio-list-schema.json](audio-list-schema.json): `audio_list.json`, the audio sources of the dictionary.
It is not Yomitan's [custom-audio-list-schema.json](../../yomitan/custom-audio-list-schema.json), which describes the
response of a custom audio server.

## Sample

[kanji-networks-etymology-yomitan](https://github.com/dariyooo/kanji-networks-etymology-yomitan) (`-dadb.zip`, with manual)
