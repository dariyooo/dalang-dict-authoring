# Yomitan Format

Yomitan dictionaries can be diretly imported into the db.
You can read more [about the format it on the yomitan website](https://github.com/yomidevs/yomitan/blob/master/docs/making-yomitan-dictionaries.md).

An entry that breaks its bank's schema is skipped and the rest imports; the import warns once per bank kind with the count and the first three entries. Yomitan rejects the whole dictionary instead. A bank that is not valid JSON or not an array stops the import, and so does a dictionary whose every entry is skipped.

## Schema

* [custom-audio-list-schema.json](custom-audio-list-schema.json)
  * Meaning: Yomitan's list of URLs from which audios can be fetched. DaKanji does not read this file shape; see [audio-list-schema.json](../dakanji/dictionary/audio-list-schema.json).
  * File name pattern: `audio-list.json`
* [audio-list-schema.json](../dakanji/dictionary/audio-list-schema.json)
  * Meaning: DaKanji's list of URLs from which audios can be fetched.
  * File name pattern: `audio_list.json`
* [dictionary-index-extension-schema.json](../dakanji/index/dictionary-index-extension-schema.json)
  * Meaning: Keys DaKanji reads from `index.json` on top of the Yomitan ones.
* [dictionary-index-schema.json](dictionary-index-schema.json)
  * Meaning: Metadata about the dictionary. Please include as much detail as possible.
  * File name pattern: `index.json`
* [dictionary-kanji-bank-v3-schema.json](dictionary-kanji-bank-v3-schema.json)
  * Meaning: Information used in the kanji viewer - meanings, readings, statistics, and codepoints.
  * File name pattern: `kanji_bank_${number}.json`
* [dictionary-kanji-meta-bank-v3-schema.json](dictionary-kanji-meta-bank-v3-schema.json)
  * Meaning: Stores kanji frequency data.
  * File name pattern: `kanji_meta_bank_${number}.json`
* [dictionary-tag-bank-v3-schema.json](dictionary-tag-bank-v3-schema.json)
  * Meaning: Defines tags for kanji and term dictionaries, like parts of speech or kanken level.
  * File name pattern: `tag_bank_${number}.json`
* [dictionary-term-bank-v3-schema.json](dictionary-term-bank-v3-schema.json)
  * Meaning: Stores dictionary readings, definitions, etc.
  * File name pattern: `term_bank_${number}.json`
* [dictionary-term-meta-bank-v3-schema.json](dictionary-term-meta-bank-v3-schema.json)
  * Meaning: Stores meta information about terms, such as frequency data and pitch accent data.
  * File name pattern: `term_meta_bank_${number}.json`

## Manual

A dictionary can include a manual that will be displayed in the app's manual section (e.g. kanji etymology).
All manual files must be placed at the top level of the archive.
The following optional files are supported:

* `manual.pdf` - the manual content as a PDF document (prioritized over `manual.md` if both are provided).
* `manual.md` - the manual content as a Markdown document.
* `manual_icon.svg` - the icon used to represent this manual in the manual section.

## Important notes

Da[Kanji] differs in some ways form how yomi[chan|tan] handles things.
Here is a list

* Source and targe language annotations in the index file are **very** important for DaKanji to work properly. Not setting them *will* lead to performance issues and/or wrong langauge handling.
* Term definitions come from a term-bank entry's structured content. Yomitan assigns no meaning to the inner structure of a definition, so DaKanji recognizes the `data-content` conventions that JMdict (and its exports) use to split a definition into fields. When **none** of these conventions are found in a structured-content item, the whole item is flattened to plain text: markup dropped, ruby readings removed, block elements separated by spaces.

| Structured-content item | Indexed as |
| --- | --- |
| plain string, or `{type: "text"}` | definition |
| `{type: "image"}` | image description text |
| `data-content: "glossary"` | definition |
| `data-content: "redirect-glossary"`, `"xref"`, `"xref-glossary"` | cross-reference |
| `data-content: "example-sentence-a"` / `"example-sentence-b"` | example sentence (term / translation) |
| `data-content: "forms"` | spelling and reading variants |
| a `data` entry with a `code` key | part-of-speech tag |
| anything else | flattened to plain text |
