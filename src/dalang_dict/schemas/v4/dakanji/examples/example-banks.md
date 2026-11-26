# Example Sentence Format: JSON Banks

This is the primary format for importing example sentences with metadata.
It supports chunked JSON files to handle massive datasets without overloading memory, as well as bundled local audio files.

## Archive Structure

Your `.zip` file must contain an `index.json` file (which follows standard yomitan index.json; `yomitan_index.json` is read instead when there is no `index.json`), one or more chunked JSON files named `example_bank_*.json` (e.g., `example_bank_1.json`), and any associated audio files at the archive path its `source` names (an `audios/` folder is the convention).

Because tags can have rich metadata (like categories, sorting orders, and notes), this format natively supports **Yomitan Tag Banks**. You should define your tags in `tag_bank_*.json` files.

```bash
dictionary.zip
├── index.json              # Required dictionary metadata (or yomitan_index.json)
├── manual.pdf              # (Optional) Manual, see Manual section
├── manual.md               # (Optional) Manual, see Manual section
├── manual_icon.svg         # (Optional) Manual icon, see Manual section
├── tag_bank_1.json         # (Optional) Yomitan-formatted tag definitions
├── example_bank_1.json     # First chunk of sentences
├── example_bank_2.json     # Second chunk of sentences
└── audios/                 # (Optional) Folder containing the audio files
    ├── apple.mp3
    └── cat.mp3
```

An entry that breaks the schema is skipped and the rest imports; the import warns once with the count and the first three entries. A bank that is not valid JSON or not an array stops the import.

## Schema

[Click here for the example_bank_1.json schema definition.](example-bank-schema.json)
[Click here for the tag_bank.json schema definition.](../../yomitan/dictionary-tag-bank-v3-schema.json)

## Manual

A dictionary can include a manual that will be displayed in the app's manual section (e.g. kanji etymology).
All manual files must be placed at the top level of the archive.
The following optional files are supported:

* `manual.pdf` - the manual content as a PDF document (prioritized over `manual.md` if both are provided).
* `manual.md` - the manual content as a Markdown document.
* `manual_icon.svg` - the icon used to represent this manual in the manual section.

## Important notes

Example sentences do *not* have a source *and* target language, therefore the language of the example sentences should be stored in the **source language** field and the target language is ignored.
You are also free to just store the same locale in both: source and target.
