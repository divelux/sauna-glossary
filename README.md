---
license: cc-by-4.0
language:
- en
- fi
- et
- sv
- da
- is
- ru
- uk
- lv
- lt
- de
- nl
- fr
- it
- es
- tr
- ar
- ka
- la
- ga
- ja
- ko
- "no"
- vro
- lkt
- nah
multilinguality: multilingual
pretty_name: Sauna Glossary
size_categories:
- n<1K
task_categories:
- translation
tags:
- sauna
- banya
- hammam
- glossary
- terminology
- multilingual
- bathing-culture
- cultural-heritage
- reference-data
- tabular
configs:
- config_name: default
  data_files:
  - split: train
    path: sauna_glossary.csv
---

# Sauna Glossary

A multilingual glossary of sauna and bathhouse words: 145 terms in 25 languages, each with its meaning in plain English, a transliteration where the script is not Latin, and the bathing tradition it belongs to.

It covers the Finnish sauna (löyly, kiuas, vihta), the Russian banya (веник, парилка, предбанник), the Baltic pirts and pirtis, the German Aufguss, the Turkish and Moroccan hammam, Roman baths, the Japanese sauna and bathhouse (ととのう, 水風呂), the Korean jjimjilbang (찜질방) and more.

- **Version:** 1.0 (2026-11)
- **Publisher:** DIVELUX, makers of wool sauna hats (https://diveluxsaunahat.com)
- **License:** CC BY 4.0
- **Rows:** 145 terms, 25 languages, 8 columns

## What this dataset is, and is not

**It is a reference word list, compiled and checked by hand.** It is meant for writers, translators, app and website builders, and anyone who wants to know what the word on the sauna door means.

**It is not a dictionary and not complete.** Each language has only the bathing words we could confirm; many regional and dialect words are missing. Meanings are short glosses for a bathing context, not full definitions. Several words have everyday meanings as well (Ukrainian віник is also a broom; Latvian gars is also "spirit"), and the `notes` column says so where it matters.

We left out every term we could not confirm. A short list of what was left out, and why, is under "Known limitations".

Nothing here is medical advice.

## Files

| File | Description |
|---|---|
| `sauna_glossary.csv` | The glossary, one row per term (145 rows, 8 columns), UTF-8 |
| `sauna_glossary.json` | The same data as a JSON array; empty cells are `null` |
| `build_glossary.py` | Source of truth; regenerates the CSV and JSON files |
| `validate.py` | Checks columns, duplicates, vocabularies, scripts and transliterations, CSV/JSON agreement |
| `dataset-metadata.json` | Kaggle metadata |
| `CITATION.cff`, `LICENSE` | Citation file and CC BY 4.0 legal text |

## Data dictionary

| Column | Type | Description |
|---|---|---|
| `term` | string | The word as written in its own language and script. Unique together with `language`. |
| `language` | string | English name of the language. |
| `language_code` | string | ISO 639-1 code; ISO 639-3 where there is no two-letter code (`vro` Võro, `lkt` Lakota, `nah` Nahuatl). |
| `transliteration` | string | Latin-script rendering for terms in Cyrillic, Arabic, Georgian, Japanese or Korean script. Empty for Latin-script terms. |
| `meaning_en` | string | Short meaning in plain English, in a bathing context. |
| `category` | category | One of `place`, `room`, `heat source`, `steam`, `tool`, `practice`, `person`, `headwear`, `cooling`, `expression`, `food and drink`. |
| `tradition` | string | The bathing tradition the term belongs to. Where possible it matches `name` in the [Sauna Traditions of the World](https://huggingface.co/datasets/divelux/sauna-traditions-of-the-world) dataset, so the two can be joined. |
| `notes` | string | Usage, variants, literal meaning, caveats. May be empty. |

Transliteration follows common practice for each language: Revised Romanization for Korean, Hepburn for Japanese, a simple English-style romanization for Russian and Ukrainian, and a scholarly romanization with diacritics for Arabic.

## Terms per language

| Language | Code | Terms | Examples |
|---|---|---|---|
| Finnish | `fi` | 16 | sauna, savusauna, kiuas |
| Russian | `ru` | 16 | баня, баня по-чёрному, баня по-белому |
| Japanese | `ja` | 15 | サウナ, 銭湯, 温泉 |
| Turkish | `tr` | 13 | hamam, külhan, göbektaşı |
| Korean | `ko` | 11 | 찜질방, 한증막, 불가마 |
| Latin | `la` | 11 | thermae, balneae, apodyterium |
| German | `de` | 10 | Aufguss, Saunameister, Wedeln |
| Estonian | `et` | 7 | saun, suitsusaun, keris |
| Lithuanian | `lt` | 7 | pirtis, dūminė pirtis, pirtininkas |
| Latvian | `lv` | 6 | pirts, melnā pirts, pirtnieks |
| Swedish | `sv` | 6 | bastu, badstuga, bada bastu |
| Arabic | `ar` | 4 | حمّام, صابون بلدي, غاسول |
| Dutch | `nl` | 3 | opgieting, saunameester, dompelbad |
| Georgian | `ka` | 3 | გოგირდის აბანო, ქისა, მექისე |
| Icelandic | `is` | 3 | sundlaug, heitur pottur, gufubað |
| Danish | `da` | 2 | saunagus, gusmester |
| French | `fr` | 2 | savon noir, gant de kessa |
| Spanish | `es` | 2 | temazcal, temazcalero |
| Ukrainian | `uk` | 2 | лазня, віник |
| Irish | `ga` | 1 | teach allais |
| Italian | `it` | 1 | bagno turco |
| Lakota | `lkt` | 1 | inípi |
| Nahuatl | `nah` | 1 | temazcalli |
| Norwegian | `no` | 1 | badstue |
| Võro | `vro` | 1 | savvusann |

## Usage

pandas:

```python
import pandas as pd

g = pd.read_csv("sauna_glossary.csv")

# Every word for the leafy whisk
print(g[g["meaning_en"].str.contains("whisk", case=False)][["term", "language", "transliteration"]])

# What is on the sauna door in each language
print(g[(g["category"] == "place")][["language", "term", "transliteration", "meaning_en"]])
```

Hugging Face `datasets` (after the dataset is published; the repository id below is the intended one):

```python
from datasets import load_dataset

glossary = load_dataset("divelux/sauna-glossary", split="train")
print(glossary[0])
```

Join with the traditions table:

```python
import pandas as pd

g = pd.read_csv("sauna_glossary.csv")
t = pd.read_csv("sauna_traditions.csv")   # from Sauna Traditions of the World
print(g.merge(t, left_on="tradition", right_on="name", how="left")[
    ["term", "language", "tradition", "typical_air_temp_c_max"]
].head(10))
```

## How it was compiled

1. **Start from an existing table.** The first batch of terms comes from the local names, ritual and headwear columns of Sauna Traditions of the World, version 1.0.
2. **Add only what could be confirmed.** Every added term was looked up in November 2026 in at least one independent reference: a dictionary (Wiktionary, the Estonian EKSS, the Swedish SAOB, the Latvian Tezaurs, the Turkish Language Association's dictionary, the Standard Korean Language Dictionary, Kotobank), the Wikipedia article in the term's own language, an encyclopedia (the Lithuanian VLE) or a national tourism site.
3. **Drop the doubtful.** A term was dropped if the only support was shop listings or commercial blogs, or if dictionaries did not give the bathing sense. Three terms from the first batch were dropped this way too.
4. **Validate.** `validate.py` checks the structure: no duplicate terms per language, known categories and language codes, the expected script for each language, a transliteration for every term in a non-Latin script, and matching CSV and JSON.

## Known limitations

- **Coverage is uneven.** Finnish, Russian, Japanese, Turkish and Korean have the most entries; some languages have one or two.
- **Glosses, not definitions.** A few words name slightly different things from place to place, and several are everyday words with a bathing use (German Wedeln, Lithuanian garas, Turkish camekân).
- **Thinner support.** Danish *saunagus* and *gusmester* rest on the Danish Wikipedia article alone, Latvian *melnā pirts* on a tourism site and Wikipedia, and Georgian *მექისე* on Georgia's tourism site. They are in common use, but we could not reach a dictionary entry for them.
- **Variants.** Where two words name the same thing (Finnish vihta and vasta, Russian парилка and парная), both are listed and cross-referenced in `notes`.
- **Sacred practice.** Lakota *inipi* is a religious ceremony. It is listed for reference with deliberately limited detail.
- **Left out on purpose:** Estonian *saunamüts*, Latvian *pirts cepure* and Lithuanian *pirties kepurė* for a sauna hat (descriptive compounds we found only in shop listings, not in a dictionary); Russian *купель* as a plunge tub (dictionaries give only the baptismal font); Turkish *hararet* and *ılıklık* as room names (the Turkish Language Association's dictionary gives only their general senses); Japanese *サ活* and *サウナマット* (no dictionary or encyclopedia entry); and the spelling *kisi* for the Georgian scrubbing mitt (the dictionary form is ქისა, kisa).

Corrections are welcome. Please include a source.

## Citation

```bibtex
@misc{divelux_sauna_glossary_2026,
  author       = {{DIVELUX}},
  title        = {Sauna Glossary},
  year         = {2026},
  version      = {1.0},
  howpublished = {\url{https://diveluxsaunahat.com/pages/sauna-tools}},
  note         = {Multilingual reference glossary, CC BY 4.0}
}
```

Plain text: DIVELUX (2026). *Sauna Glossary* (Version 1.0) [Data set]. https://diveluxsaunahat.com/pages/sauna-tools

## License

[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). You may share and adapt the data for any purpose, including commercially, as long as you give credit to DIVELUX and link to https://diveluxsaunahat.com/pages/sauna-tools.

Made by DIVELUX, makers of wool sauna hats.
