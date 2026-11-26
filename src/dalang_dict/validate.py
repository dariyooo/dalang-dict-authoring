"""Validation of dictionaries (see `FORMATS`) and assets (see `ASSET_FORMATS`), one set of rules per format.

Every dictionary format checks the layout DaLang's importer expects (which files, where) and validates its files
against the schemas of the latest DaLang version (schemas/v*/, see schemas/README.md): Yomitan's in yomitan/,
DaKanji's own in dakanji/.
Assets are files the apps download as they are (no zip, no index), their formats check what the apps read.
"""

import functools
import json
import re
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from jsonschema.exceptions import best_match
from jsonschema.validators import validator_for
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT7

SCHEMAS_DIR = Path(__file__).parent / "schemas"


def _version_key(path: Path) -> tuple[int, ...]:
    return tuple(int(part) for part in path.name.removeprefix("v").split("."))


def _dalang_version(path: Path) -> str:
    parts = [str(part) for part in _version_key(path)]
    return ".".join(parts + ["0"] * (2 - len(parts)))


# The newest version folder, e.g. schemas/v4/: dictionaries are built for the latest DaLang version
SCHEMA_DIR = max((p for p in SCHEMAS_DIR.glob("v*") if p.is_dir()), key=_version_key)
# The DaLang version of SCHEMA_DIR, e.g. "4.0" for v4 and "4.1" for v4.1, written as `minimumDaLangVersion`
SCHEMA_VERSION = _dalang_version(SCHEMA_DIR)
INDEX_SCHEMA = "yomitan/dictionary-index-schema.json"
INDEX_EXTENSION_SCHEMA = "dakanji/index/dictionary-index-extension-schema.json"

# bank file prefix -> schema, relative to SCHEMA_DIR
YOMITAN_BANKS: dict[str, str] = {
    "kanji_bank": "yomitan/dictionary-kanji-bank-v3-schema.json",
    "kanji_meta_bank": "yomitan/dictionary-kanji-meta-bank-v3-schema.json",
    "term_bank": "yomitan/dictionary-term-bank-v3-schema.json",
    "term_meta_bank": "yomitan/dictionary-term-meta-bank-v3-schema.json",
    "tag_bank": "yomitan/dictionary-tag-bank-v3-schema.json",
}
EXAMPLE_BANKS: dict[str, str] = {
    "example_bank": "dakanji/examples/example-bank-schema.json",
    "example_text_meta_bank": "dakanji/examples/example-text-meta-bank-schema.json",
    "tag_bank": "yomitan/dictionary-tag-bank-v3-schema.json",
}
AUDIO_LIST_SCHEMA = "dakanji/dictionary/audio-list-schema.json"
AUDIO_METADATA_SCHEMAS = {
    "index.json": "dakanji/audio/index-json-schema.json",
    "entries.json": "dakanji/audio/entries-json-schema.json",
}
RADK_SCHEMA = "dakanji/radicals/radk-schema.json"
KRAD_SCHEMA = "dakanji/radicals/krad-schema.json"
TRANSFORMS_SCHEMA = "dakanji/deinflection-rules/transforms-schema.json"
BANK_FILE = re.compile(r"^(?P<bank>[a-z_]+)_\d+\.json$")
TEXT_BANK_FILE = re.compile(r"^example_text_bank_\d+\.txt$")

AUDIO_DIR = "audios"
AUDIO_EXTENSIONS = {".aac", ".mp3", ".ogg", ".opus", ".flac", ".wav"}
AUDIO_METADATA_FILES = {"index.json", "entries.json"}
AUDIO_LIST_FILE = "audio_list.json"
MANUAL_FILES = {"manual.pdf", "manual.md", "manual_icon.svg"}
# DaLang detects a radicals archive by a file whose name contains `radk` and one whose name contains `krad`
RADK_PATTERN = "radk"
KRAD_PATTERN = "krad"
SVG_EXTENSION = ".svg"
XML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
KANJIVG_ELEMENT = re.compile(r'kvg:element="[^"]+"')


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


@functools.cache
def _validator(schema: str):
    """A validator for `schema` (relative to SCHEMA_DIR) that resolves `$ref`s to other files next to it."""
    path = SCHEMA_DIR / schema

    def retrieve(uri: str) -> Resource:
        return Resource.from_contents(_load(path.parent / uri), default_specification=DRAFT7)

    contents = _load(path)
    return validator_for(contents)(contents, registry=Registry(retrieve=retrieve))  # type: ignore[call-arg]


def _validate_data(data, schema: str, name: str) -> None:
    error = best_match(_validator(schema).iter_errors(data))
    if error is not None:
        raise ValueError(f"'{name}' is invalid: {error.message} at {list(error.absolute_path)}")


def _validate_json(path: Path, schema: str) -> None:
    _validate_data(_load(path), schema, str(path))


def list_files(directory: Path) -> list[str]:
    """All files below `directory` as sorted archive names, e.g. `audios/a.mp3`."""
    return sorted(path.relative_to(directory).as_posix() for path in directory.rglob("*") if path.is_file())


def is_audio_file(name: str) -> bool:
    """Whether `name` is an audio file in `audios/`, where the audio files of every format belong."""
    path = PurePosixPath(name)
    return str(path.parent) == AUDIO_DIR and path.suffix in AUDIO_EXTENSIONS


def _check_banks(directory: Path, files: list[str], banks: dict[str, str]) -> set[str]:
    """Validates the bank files in the root (`{bank}_{n}.json`), raises on unknown banks and returns the bank files."""
    found = set()
    for name in files:
        match = BANK_FILE.match(name)
        if not match:
            continue
        if match["bank"] not in banks:
            raise ValueError(f"Unknown bank file '{name}'")
        _validate_json(directory / name, banks[match["bank"]])
        found.add(name)
    return found


def _reject_unexpected(files: set[str], hint: str = f", audio files belong in '{AUDIO_DIR}/'") -> None:
    if files:
        raise ValueError(f"Unexpected files {sorted(files)[:5]}{hint}")


def _check_yomitan(directory: Path, files: list[str]) -> None:
    # Every file besides the banks is media, e.g. the images of structured content
    _check_banks(directory, files, YOMITAN_BANKS)
    extensions = sorted(set(files) & (MANUAL_FILES | {AUDIO_LIST_FILE}))
    if extensions:
        raise ValueError(f"{extensions} are DaKanji extensions, use the dakanji-dictionary format")


def _check_dakanji_dictionary(directory: Path, files: list[str]) -> None:
    # Yomitan plus an audio source list and a manual, which DaLang only reads in this format
    _check_banks(directory, files, YOMITAN_BANKS)
    if AUDIO_LIST_FILE in files:
        _validate_json(directory / AUDIO_LIST_FILE, AUDIO_LIST_SCHEMA)


def _check_dakanji_examples(directory: Path, files: list[str]) -> None:
    banks = _check_banks(directory, files, EXAMPLE_BANKS)
    text_banks = {name for name in files if TEXT_BANK_FILE.match(name)}
    for name in banks:
        if name.startswith("example_text_meta_bank_"):
            text_bank = name.replace("example_text_meta_bank_", "example_text_bank_").replace(".json", ".txt")
            if text_bank not in text_banks:
                raise ValueError(f"'{name}' has no text bank '{text_bank}'")
    if not text_banks and not any(name.startswith("example_bank_") for name in banks):
        raise ValueError("No example banks")
    # DaLang ignores everything besides banks and audio files
    _reject_unexpected(set(files) - banks - text_banks - {"index.json"} - set(filter(is_audio_file, files)))


def _check_dakanji_audio(directory: Path, files: list[str]) -> None:
    # Without index.json / entries.json the audio files are named `Term [Reading] (Pitch).ext`,
    # which DaLang reads from any name, so there is nothing to check about the names.
    audio_files = set(filter(is_audio_file, files))
    if not audio_files:
        raise ValueError(f"No audio files in '{AUDIO_DIR}/'")
    for name, schema in AUDIO_METADATA_SCHEMAS.items():
        if name in files:
            _validate_json(directory / name, schema)
    _reject_unexpected(set(files) - audio_files - AUDIO_METADATA_FILES - {"yomitan_index.json"})


def _root_files(files: list[str]) -> None:
    nested = [name for name in files if "/" in name]
    if nested:
        raise ValueError(f"Files {nested[:5]} belong in the zip root")


def _check_dakanji_radicals(directory: Path, files: list[str]) -> None:
    # The radk file lists the radicals with their stroke count, the krad file the radicals of every kanji.
    # DaLang also fails on a krad radical missing from the radk file,
    # that check needs DaLang's lookup tables and stays there.
    _root_files(files)
    radk = [name for name in files if RADK_PATTERN in name]
    krad = [name for name in files if KRAD_PATTERN in name and name not in radk]
    if len(radk) != 1 or len(krad) != 1:
        raise ValueError(f"Need exactly one '{RADK_PATTERN}' and one '{KRAD_PATTERN}' file, found {radk} and {krad}")
    _validate_json(directory / radk[0], RADK_SCHEMA)
    _validate_json(directory / krad[0], KRAD_SCHEMA)
    _reject_unexpected(set(files) - {radk[0], krad[0], "index.json"}, hint="")


def _check_dakanji_stroke_order(directory: Path, files: list[str]) -> None:
    # KanjiVG files, DaLang reads the character from the `kvg:element` of the first group outside comments
    _root_files(files)
    svgs = [name for name in files if name.endswith(SVG_EXTENSION)]
    if not svgs:
        raise ValueError("No SVG files")
    for name in svgs:
        if not KANJIVG_ELEMENT.search(XML_COMMENT.sub("", (directory / name).read_text(encoding="utf-8"))):
            raise ValueError(f"'{name}' has no kvg:element")
    _reject_unexpected(set(files) - set(svgs) - {"index.json"}, hint="")


@dataclass(frozen=True)
class Format:
    index_file: str
    check: Callable[[Path, list[str]], None]


# The formats DaLang imports, a dictionary declares its format when it is packaged
FORMATS = {
    "yomitan": Format("index.json", _check_yomitan),
    "dakanji-dictionary": Format("index.json", _check_dakanji_dictionary),
    "dakanji-examples": Format("index.json", _check_dakanji_examples),
    "dakanji-audio": Format("yomitan_index.json", _check_dakanji_audio),
    "dakanji-radicals": Format("index.json", _check_dakanji_radicals),
    "dakanji-stroke-order": Format("index.json", _check_dakanji_stroke_order),
}


def get_format(name: str) -> Format:
    if name not in FORMATS:
        raise ValueError(f"Unknown format '{name}', use one of {list(FORMATS)}")
    return FORMATS[name]


def validate_dictionary_dir(directory: Path, format: str = "yomitan") -> None:
    """Validates the dictionary in `directory` against the rules of `format`, raises on the first problem."""
    dictionary_format = get_format(format)
    index_path = directory / dictionary_format.index_file
    _validate_json(index_path, INDEX_SCHEMA)
    _validate_json(index_path, INDEX_EXTENSION_SCHEMA)
    dictionary_format.check(directory, list_files(directory))


# Yomitan's deinflection rules as written by converting its `*-transforms.js` files
TRANSFORMS_FILE = re.compile(r"^[a-z]+(-[a-z]+)*-transforms\.json$")
# Rule types DaLang reads, it skips the others (regex rules Yomitan names `other`)
SUPPORTED_RULE_TYPES = {"suffix", "prefix", "wholeWord"}


def _check_transforms(name: str, rules: dict) -> None:
    """Checks one transforms file against its schema and that every condition it uses is defined."""
    _validate_data(rules, TRANSFORMS_SCHEMA, name)
    conditions = rules["conditions"]
    for key, condition in conditions.items():
        if not set(condition.get("subConditions", [])) <= conditions.keys():
            raise ValueError(f"Condition '{key}' in '{name}' has unknown sub conditions")
    for key, transform in rules["transforms"].items():
        for rule in transform["rules"]:
            used = set(rule.get("conditionsIn", []) + rule.get("conditionsOut", []))
            if not used <= conditions.keys():
                raise ValueError(f"A rule of '{key}' in '{name}' uses unknown conditions: {sorted(used)}")


def _check_deinflection_rules(files: dict[str, Path]) -> None:
    for name, path in files.items():
        if not TRANSFORMS_FILE.match(name):
            raise ValueError(f"'{name}' is not named '{{language}}-transforms.json'")
        _check_transforms(name, _load(path))


def count_rules(files: dict[str, Path]) -> dict[str, int]:
    """Rules per transforms file, plus the rules DaLang skips (`{file} (unsupported)`) where there are any."""
    entries: dict[str, int] = {}
    for name, path in files.items():
        rules = [rule for transform in _load(path)["transforms"].values() for rule in transform["rules"]]
        stem = name.removesuffix(".json")
        entries[stem] = len(rules)
        if unsupported := sum(rule["type"] not in SUPPORTED_RULE_TYPES for rule in rules):
            entries[f"{stem} (unsupported)"] = unsupported
    return dict(sorted(entries.items()))


@dataclass(frozen=True)
class AssetFormat:
    check: Callable[[dict[str, Path]], None]
    count: Callable[[dict[str, Path]], dict[str, int]]


# Files the apps download as they are, e.g. the deinflection rules DaLang loads at startup
ASSET_FORMATS = {
    "yomitan-deinflection-rules": AssetFormat(_check_deinflection_rules, count_rules),
}


def get_asset_format(name: str) -> AssetFormat:
    if name not in ASSET_FORMATS:
        raise ValueError(f"Unknown asset format '{name}', use one of {list(ASSET_FORMATS)}")
    return ASSET_FORMATS[name]


def validate_assets(files: dict[str, Path], format: str) -> None:
    """Validates the asset files (names mapped to paths) against the rules of `format`, raises on the first problem."""
    if not files:
        raise ValueError("No asset files")
    get_asset_format(format).check(files)
