# Audio Dictionary Format 3: Entries JSON Mapping

This format uses an `entries.json` file consisting of an array of objects. It is ideal for importing structured entry dumps where pronunciation data is nested inside the term's object.

## Archive Structure

Your `.zip` file must contain `yomitan_index.json` (follows the [yomitan schema](../../yomitan/dictionary-index-schema.json)), `entries.json` and the audio files (`aac`, `mp3`, `ogg`, `opus`, `flac`, `wav`, the extension in any case). The importer finds `yomitan_index.json`, `index.json`, `entries.json` and the audio files by their name in any folder of the archive; `audios/` is the convention.

With a mapping file, an audio file it does not name is not imported; the import warns once with the count. A file is matched by its name without the extension, in any folder. Files that share a name (without extension) are not imported; the import warns once with the count. An entry that breaks the schema is skipped and the rest imports; the import warns once with the count and the first three entries. An `entries.json` that is not valid JSON or not an array stops the import.

Each accent with a sound file is a recording of the entry's terms and keeps its pronunciation as the entry gives it (see the schema). A subentry's recordings belong to the entry's terms and kana too, labelled by the subentry's `head`, else its `number`, as written (`お昼過ぎに`, `1`).

Only recordings are imported, and the import does not warn about what it leaves out: an accent whose `soundFile` is null or missing (NHK writes one for the pattern any word ending so takes, `○○○タニ`), the pitch-only `conjugations` and `examples` (the pitch of other words, without recordings), and the notes and flags that sit only on such accents. A note no recording points to is not stored. An entry's `id`, `kanjiNotUsed`, `kanjiRaw`, `furigana`, `usage`, `category`, `type`, `class` and `references` are not read: they describe the word, which a dictionary of words describes.

```bash
dictionary.zip
├── yomitan_index.json      # Required dictionary metadata
├── manual.pdf              # (Optional) Manual, see Manual section
├── manual.md               # (Optional) Manual, see Manual section
├── manual_icon.svg         # (Optional) Manual icon, see Manual section
├── entries.json            # Array of dictionary entries
└── audios/                 # Audio folder (by convention)
    ├── audio_001.mp3
    └── audio_002.ogg
```

## Schema

[Click here for the JSON schema definition.](entries-json-schema.json)

## Manual

A dictionary can include a manual that will be displayed in the app's manual section (e.g. kanji etymology).
All manual files must be placed at the top level of the archive.
The following optional files are supported:

* `manual.pdf` - the manual content as a PDF document (prioritized over `manual.md` if both are provided).
* `manual.md` - the manual content as a Markdown document.
* `manual_icon.svg` - the icon used to represent this manual in the manual section.
