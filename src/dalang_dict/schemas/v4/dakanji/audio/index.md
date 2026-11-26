# Audio Dictionary Format 2: Index JSON Mapping

This format uses an `index.json` file to map headwords to their respective audio files, allowing multiple words to share the same audio recording.

## Archive Structure
Your `.zip` file must contain `yomitan_index.json` (follows the [yomitan schema](../../yomitan/dictionary-index-schema.json)), `index.json` and the audio files (`aac`, `mp3`, `ogg`, `opus`, `flac`, `wav`, the extension in any case). The importer finds `yomitan_index.json`, `index.json`, `entries.json` and the audio files by their name in any folder of the archive; `audios/` is the convention.

With a mapping file, an audio file it does not name is not imported; the import warns once with the count. A file is matched by its name without the extension, in any folder. Files that share a name (without extension) are not imported; the import warns once with the count. A headword that breaks the schema, in its list or in a file it names, is skipped and the rest imports; the import warns once with the count and the first three headwords. An `index.json` that is not valid JSON, or lacks `headwords` or `files`, stops the import.

`meta` and each file's `pitch_pattern` are not read, and the import does not warn about them: `meta` repeats `yomitan_index.json` and where the files sit, `pitch_pattern` writes `pitch_number` in another notation.

``` bash
dictionary.zip
├── yomitan_index.json      # Required dictionary metadata
├── manual.pdf              # (Optional) Manual, see Manual section
├── manual.md               # (Optional) Manual, see Manual section
├── manual_icon.svg         # (Optional) Manual icon, see Manual section
├── index.json              # Audio mapping data
└── audios/                 # Audio folder (by convention)
    ├── taberu_native.mp3
    └── hashiru_kan.ogg
```

## Schema

[Click here for the JSON schema definition.](index-json-schema.json)

## Manual

A dictionary can include a manual that will be displayed in the app's manual section (e.g. kanji etymology).
All manual files must be placed at the top level of the archive.
The following optional files are supported:

* `manual.pdf` - the manual content as a PDF document (prioritized over `manual.md` if both are provided).
* `manual.md` - the manual content as a Markdown document.
* `manual_icon.svg` - the icon used to represent this manual in the manual section.
