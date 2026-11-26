# Example Sentence Format: Plain Text (Monolingual)

This is the simplest way to import bulk example sentences. This format takes standard `.txt` files containing texts.
The system will automatically segment and index the sentences during import.

## Archive Structure

Your `.zip` file must contain `index.json` (or `yomitan_index.json` when there is no `index.json`) and one or more `example_text_bank_N.txt` files in the root directory.
Optionally, an `example_text_meta_bank_N.json` with the same number supplies metadata. A metadata field that breaks the schema is left out and the others apply; the import warns once with the count. A metadata file that is not valid JSON or not an object stops the import.

``` bash
dictionary.zip
├── index.json                    # Required dictionary metadata
├── manual.pdf                    # (Optional) Manual, see Manual section
├── manual.md                     # (Optional) Manual, see Manual section
├── manual_icon.svg               # (Optional) Manual icon, see Manual section
├── example_text_bank_1.txt       # Plain text file 1 (UTF-8)
├── example_text_meta_bank_1.json # (Optional) metadata that is applied to all extracted sentences from example_text_bank_1
├── example_text_bank_2.txt       # Next Plain text file (UTF-8)
└── example_text_meta_bank_2.json # (Optional) metadata that is applied to all extracted sentences from example_text_bank_2
```

## File Formatting

## Schema

[Click here for the example_text_meta_bank_ JSON schema definition.](example-text-meta-bank-schema.json)

## Manual

A dictionary can include a manual that will be displayed in the app's manual section (e.g. kanji etymology).
All manual files must be placed at the top level of the archive.
The following optional files are supported:

* `manual.pdf` - the manual content as a PDF document (prioritized over `manual.md` if both are provided).
* `manual.md` - the manual content as a Markdown document.
* `manual_icon.svg` - the icon used to represent this manual in the manual section.
