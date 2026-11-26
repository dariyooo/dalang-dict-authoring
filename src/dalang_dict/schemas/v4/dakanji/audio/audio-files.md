# Audio Dictionary Format 1: Filename-Based

This format requires no JSON mapping files for the audio. The system parses the term, reading, and pitch accent directly from the audio file's name.

## Archive Structure

Your `.zip` file must contain `yomitan_index.json` (follows the [yomitan schema](../../yomitan/dictionary-index-schema.json)) and the audio files (`aac`, `mp3`, `ogg`, `opus`, `flac`, `wav`, the extension in any case). The importer finds `yomitan_index.json`, `index.json`, `entries.json` and the audio files by their name in any folder of the archive; `audios/` is the convention.

``` bash
dictionary.zip
├── yomitan_index.json      # Required dictionary metadata
├── manual.pdf              # (Optional) Manual, see Manual section
├── manual.md               # (Optional) Manual, see Manual section
├── manual_icon.svg         # (Optional) Manual icon, see Manual section
└── audios/                 # Audio folder (by convention)
    ├── 食べる [たべる] (2).mp3   # Term, Reading, and Pitch
    ├── 走る [はしる].ogg         # Term and Reading only
    └── 飲む.mp3                 # Term only
```

## File Naming Convention

The parser uses the following pattern to extract data from the file name (excluding the extension):
`Term [Reading] (Pitch)`

* **Term:** (Required) The base word (e.g., `食べる`).
* **Reading:** (Optional) Enclosed in square brackets `[]` or `【】` (e.g., `[たべる]`).
* **Pitch Accent:** (Optional) Enclosed in parentheses `()` or `（）`. A number is the downstep position (e.g. `(2)`, 0 heiban), stored as given with the pattern computed from it, one letter per mora. Letters are the pattern itself (e.g. `(LHH)`), stored upper-cased: one `H` or `L` per mora of the reading. Without a reading, or with a number past the reading's morae or letters that are not such a pattern, no pitch is stored: the file is kept and the import warns once with the count.

## Manual

A dictionary can include a manual that will be displayed in the app's manual section (e.g. kanji etymology).
All manual files must be placed at the top level of the archive.
The following optional files are supported:

* `manual.pdf` - the manual content as a PDF document (prioritized over `manual.md` if both are provided).
* `manual.md` - the manual content as a Markdown document.
* `manual_icon.svg` - the icon used to represent this manual in the manual section.
