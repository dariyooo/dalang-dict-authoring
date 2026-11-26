# Deinflection rules (asset `yomitan-deinflection-rules`)

Yomitan's deinflection rules as JSON, one `{language}-transforms.json` per language. The apps download them as they
are (no zip, no index) and use them for deconjugation.

## Schema

[transforms-schema.json](transforms-schema.json)

* `suffix`, `prefix` and `wholeWord` rules need `inflected` and `base`.
* `other` rules (Yomitan's regex rules) are allowed, the apps skip them.
* Every condition a rule or sub condition uses must be defined in `conditions`.

## Sample

[deinflection-rules-dalang](https://github.com/dariyooo/deinflection-rules-dalang)
