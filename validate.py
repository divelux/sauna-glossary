#!/usr/bin/env python3
"""Validate the Sauna Glossary. Exit code 0 = all checks pass. Standard library only.

Checks: columns and order, required fields, no duplicate (term, language) pairs,
controlled vocabularies, language codes, a transliteration for every term in a
non-Latin script (and none for Latin-script terms), tidy text, CSV/JSON
agreement, cross-reference to the Sauna Traditions of the World dataset where a
copy is available, and banned wording.
"""
import csv
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
COLUMNS = ["term", "language", "language_code", "transliteration", "meaning_en", "category", "tradition", "notes"]
CATEGORIES = {"place", "room", "heat source", "steam", "tool", "practice", "person", "headwear", "cooling", "expression", "food and drink"}
LANGUAGES = {
    "Finnish": "fi", "Estonian": "et", "Võro": "vro", "Swedish": "sv", "Norwegian": "no", "Danish": "da", "Icelandic": "is",
    "Russian": "ru", "Ukrainian": "uk", "Latvian": "lv", "Lithuanian": "lt", "German": "de", "Dutch": "nl", "French": "fr",
    "Italian": "it", "Spanish": "es", "Turkish": "tr", "Arabic": "ar", "Georgian": "ka", "Latin": "la", "Irish": "ga",
    "Japanese": "ja", "Korean": "ko", "Lakota": "lkt", "Nahuatl": "nah",
}
# Script each language is written in here. Anything not Latin needs a transliteration.
SCRIPT = {"Russian": "CYRILLIC", "Ukrainian": "CYRILLIC", "Arabic": "ARABIC", "Georgian": "GEORGIAN", "Korean": "HANGUL", "Japanese": None}
BANNED = ["detox", "toxin", "burns fat", "burn fat", "cure", "heals", "boosts", "immune", "soak the hat",
          "wet the hat", "dampen", "best seller", "amazon"]
# Traditions that are not rows of the Sauna Traditions of the World dataset but are allowed here.
EXTRA_TRADITIONS = {"Danish sauna", "Dutch sauna"}

errors = []


def err(msg):
    errors.append(msg)


def scripts(text):
    out = set()
    for ch in text:
        if ch.isalpha():
            out.add(unicodedata.name(ch, "?").split(" ")[0])
    return out


with open(os.path.join(HERE, "sauna_glossary.csv"), newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    header = reader.fieldnames
    rows = list(reader)

if header != COLUMNS:
    err(f"columns are {header}, expected {COLUMNS}")
if len(rows) < 100:
    err(f"only {len(rows)} rows")

seen = set()
for i, r in enumerate(rows, start=2):
    tag = f"row {i} ({r.get('term')!r})"
    for c in COLUMNS:
        v = r[c]
        if v != v.strip() or "  " in v or "\n" in v or "\t" in v:
            err(f"{tag}: untidy whitespace in {c}")
        if v != unicodedata.normalize("NFC", v):
            err(f"{tag}: {c} is not NFC-normalized")
    for c in ("term", "language", "language_code", "meaning_en", "category", "tradition"):
        if not r[c]:
            err(f"{tag}: {c} is empty")
    key = (r["term"].casefold(), r["language"])
    if key in seen:
        err(f"{tag}: duplicate term for {r['language']}")
    seen.add(key)
    if r["language"] not in LANGUAGES:
        err(f"{tag}: unknown language {r['language']!r}")
    elif LANGUAGES[r["language"]] != r["language_code"]:
        err(f"{tag}: language_code {r['language_code']!r} does not match {r['language']}")
    if r["category"] not in CATEGORIES:
        err(f"{tag}: unknown category {r['category']!r}")

    term_scripts = scripts(r["term"])
    latin_only = term_scripts <= {"LATIN"}
    if latin_only and r["transliteration"]:
        err(f"{tag}: Latin-script term should not have a transliteration")
    if not latin_only:
        if not r["transliteration"]:
            err(f"{tag}: term in {sorted(term_scripts)} needs a transliteration")
        elif not scripts(r["transliteration"]) <= {"LATIN", "MODIFIER"}:
            err(f"{tag}: transliteration must be in Latin script")
    want = SCRIPT.get(r["language"], "LATIN")
    if want and want not in term_scripts and not (want == "LATIN" and latin_only):
        err(f"{tag}: expected {want} script for {r['language']}, found {sorted(term_scripts)}")
    if r["language"] == "Japanese" and not term_scripts & {"CJK", "HIRAGANA", "KATAKANA", "KATAKANA-HIRAGANA"}:
        err(f"{tag}: Japanese term is not in Japanese script")

    m = r["meaning_en"]
    if m and (not m[0].isupper() and not m[0] in "'\"" or m.endswith(".")):
        err(f"{tag}: meaning_en should start with a capital and have no final period")
    if len(m) > 140:
        err(f"{tag}: meaning_en is longer than 140 characters")
    if r["notes"] and not r["notes"].endswith((".", ")", "!")):
        err(f"{tag}: notes should end with a period")
    text = " ".join(r.values()).lower()
    for b in BANNED:
        if re.search(r"\b" + re.escape(b) + r"\b", text):
            err(f"{tag}: banned wording {b!r}")

# CSV and JSON carry the same data (empty string in CSV = null in JSON)
with open(os.path.join(HERE, "sauna_glossary.json"), encoding="utf-8") as f:
    data = json.load(f)
if len(data) != len(rows):
    err(f"JSON has {len(data)} records, CSV has {len(rows)}")
for r, j in zip(rows, data):
    if list(j) != COLUMNS:
        err(f"JSON keys differ for {r['term']!r}")
        break
    for c in COLUMNS:
        if (j[c] or "") != r[c]:
            err(f"CSV and JSON differ at {r['term']!r} / {c}")

# Traditions should match the Sauna Traditions of the World dataset where a copy is at hand.
known = None
for cand in (os.path.join(HERE, "sauna_traditions.csv"), os.path.join(HERE, "..", "..", "dataset", "sauna_traditions.csv")):
    if os.path.exists(cand):
        with open(cand, newline="", encoding="utf-8") as f:
            known = {row["name"] for row in csv.DictReader(f)}
        break
if known is not None:
    for r in rows:
        if r["tradition"] not in known and r["tradition"] not in EXTRA_TRADITIONS:
            err(f"tradition {r['tradition']!r} ({r['term']!r}) is not in the traditions dataset or EXTRA_TRADITIONS")

# README numbers
readme = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
langs = sorted({r["language"] for r in rows})
if f"{len(rows)} terms" not in readme:
    err(f"README.md does not say '{len(rows)} terms'")
if f"{len(langs)} languages" not in readme:
    err(f"README.md does not say '{len(langs)} languages'")

if errors:
    print(f"{len(errors)} problem(s):")
    for e in errors[:40]:
        print(" -", e)
    sys.exit(1)
by_lang = {}
for r in rows:
    by_lang[r["language"]] = by_lang.get(r["language"], 0) + 1
print(f"OK: {len(rows)} terms, {len(langs)} languages, {len({r['tradition'] for r in rows})} traditions"
      + ("" if known is not None else " (traditions dataset not found, cross-reference skipped)"))
print(", ".join(f"{k} {v}" for k, v in sorted(by_lang.items(), key=lambda kv: -kv[1])))
