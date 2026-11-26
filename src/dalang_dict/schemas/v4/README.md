# DaLang 4

Everything DaLang 4 imports. Every archive has an `index.json` following
[Yomitan's index schema](yomitan/dictionary-index-schema.json) plus the [DaKanji index extension](dakanji/index/README.md),
audio archives name it `yomitan_index.json`.

## Dictionaries

* [Yomitan](yomitan/README.md): term, kanji, meta and tag banks; source and target language in the index are important
* [DaKanji dictionary](dakanji/dictionary/README.md): Yomitan plus `audio_list.json` and a manual
* [Radicals](dakanji/radicals/README.md): radk + krad JSON
* [Stroke order](dakanji/stroke-order/README.md): KanjiVG SVGs

## Audio

* [Audio files](dakanji/audio/audio-files.md): files named `Term [Reading] (Pitch).ext`
* [Index](dakanji/audio/index.md): `index.json` maps headwords to files
* [Entries](dakanji/audio/entries.md): `entries.json`, an array of entries with their audio

Sample: [japanese-vocabulary-audio-dakanji](https://github.com/dariyooo/japanese-vocabulary-audio-dakanji)

## Example sentences

* [Example banks](dakanji/examples/example-banks.md): `example_bank_N.json`
* [Example texts](dakanji/examples/example-texts.md): `example_text_bank_N.txt` + `example_text_meta_bank_N.json`

Sample: [tatoeba-examples-dalang](https://github.com/dariyooo/tatoeba-examples-dalang)

## Assets

Files the apps download as they are, without zip and index:

* [Deinflection rules](dakanji/deinflection-rules/README.md): `{language}-transforms.json`

## Conversion

Tools that convert between dictionary formats:

* [yomitan-import](https://github.com/yomidevs/yomitan-import): converts custom dictionary files for Yomitan
* [pyglossary](https://github.com/ilius/pyglossary): converts dictionary files (glossaries)
