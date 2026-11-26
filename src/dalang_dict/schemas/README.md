# Schemas

The formats DaLang (and so every app built on it, e.g. DaKanji) imports, one folder per DaLang version.

```text
schemas/
  upstream/yomitan/   Yomitan's current schemas, synced weekly to notice upstream changes (not "supported")
  v4/                 what DaLang 4 reads
    yomitan/          the Yomitan schemas it supports
    dakanji/          its own formats, one folder per format
```

## Versions

* A folder is named after the first DaLang version that reads it (`v4`, `v4.1`, ...).
  The apps use DaLang's version, so DaKanji 4.1 reads `v4.1`.
* **A released folder never changes.** Every change to a format, including taking on a changed Yomitan schema,
  goes into a new folder, which starts as a copy of the latest one.
* No new folder when nothing changes: an app version reads the newest folder at or below its version.
* `upstream/yomitan/` follows Yomitan; when it changes, deciding whether and from which version DaLang supports it is
  a deliberate step (a new folder).
* DaLang includes this repo as a submodule pinned to a tag and reads its folder from there,
  its importer tests validate their sample files against it.
* Dictionaries built with `dalang_dict` are validated against the latest folder, dictionaries in a DaKanji format get
  `minimumDaLangVersion` (the folder's version) in their index so older apps refuse them.
