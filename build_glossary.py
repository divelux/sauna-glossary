#!/usr/bin/env python3
"""Source of truth for the Sauna Glossary. Writes sauna_glossary.csv and sauna_glossary.json.

Run:  python3 build_glossary.py

Each entry: term, language, language_code, transliteration, meaning_en, category, tradition, notes.
- term             the word as written in its own language and script
- language         English name of the language
- language_code    ISO 639-1 code (ISO 639-3 where there is no two-letter code)
- transliteration  Latin-script rendering for terms in other scripts; empty for Latin-script terms
- meaning_en       plain English meaning in a bathing context
- category         one of CATEGORIES
- tradition        the bathing tradition the term belongs to. Where possible this matches a
                   `name` in the Sauna Traditions of the World dataset
- notes            usage, variants, caveats

Only terms we could confirm are included. See README.md for how each was checked.
License: CC BY 4.0, DIVELUX, https://diveluxsaunahat.com
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
COLUMNS = ["term", "language", "language_code", "transliteration", "meaning_en", "category", "tradition", "notes"]
CATEGORIES = ["place", "room", "heat source", "steam", "tool", "practice", "person", "headwear", "cooling", "expression", "food and drink"]

FI, ET, SV, NO, DA, IS_ = ("Finnish", "fi"), ("Estonian", "et"), ("Swedish", "sv"), ("Norwegian", "no"), ("Danish", "da"), ("Icelandic", "is")
RU, UK, LV, LT = ("Russian", "ru"), ("Ukrainian", "uk"), ("Latvian", "lv"), ("Lithuanian", "lt")
DE, NL, FR, IT, ES = ("German", "de"), ("Dutch", "nl"), ("French", "fr"), ("Italian", "it"), ("Spanish", "es")
TR, AR, KA, LA, GA = ("Turkish", "tr"), ("Arabic", "ar"), ("Georgian", "ka"), ("Latin", "la"), ("Irish", "ga")
JA, KO, LKT, NAH, VRO = ("Japanese", "ja"), ("Korean", "ko"), ("Lakota", "lkt"), ("Nahuatl", "nah"), ("Võro", "vro")

FIN, EST, SWE, NOR = "Finnish sauna", "Estonian sauna", "Swedish bastu", "Norwegian badstue"
RUS, LIT, LAT, GER = "Russian banya", "Lithuanian pirtis", "Latvian pirts", "German Aufguss sauna"
TUR, MOR, GEO, ROM = "Turkish hammam", "Moroccan hammam", "Georgian sulfur bath", "Roman baths (historical)"
JPS, JPB, KOR = "Japanese sauna", "Japanese sento", "Korean jjimjilbang"

E = []  # entries


def add(term, lang, translit, meaning, category, tradition, notes=""):
    E.append({"term": term, "language": lang[0], "language_code": lang[1], "transliteration": translit,
              "meaning_en": meaning, "category": category, "tradition": tradition, "notes": notes})


# ---------------------------------------------------------------- Finnish
add("sauna", FI, "", "The heated room for sweat bathing, and the act of bathing in it", "place", FIN, "A Finnish word borrowed into many other languages.")
add("savusauna", FI, "", "Smoke sauna: heated by a stove with no chimney, the smoke is let out before bathing", "place", "Finnish smoke sauna", "")
add("kiuas", FI, "", "Sauna stove topped with stones", "heat source", FIN, "Wood-burning or electric.")
add("kiuaskivet", FI, "", "Sauna stones, the stones piled on the stove", "heat source", FIN, "Plural of kiuaskivi.")
add("löyly", FI, "", "The steam and wave of heat that rises when water is thrown on the hot stones", "steam", FIN, "Borrowed into other languages; Japanese ロウリュ comes from it.")
add("lauteet", FI, "", "The raised benches of a sauna", "room", FIN, "Plural; the higher the bench, the hotter the air.")
add("kiulu", FI, "", "Small wooden pail with one long stave as its handle, used for sauna water", "tool", FIN, "")
add("löylykauha", FI, "", "Ladle for throwing water on the stones", "tool", FIN, "Often just kauha, 'ladle'.")
add("vihta", FI, "", "Bundle of leafy birch twigs used to whisk the skin", "tool", FIN, "The word used in western Finland.")
add("vasta", FI, "", "Bundle of leafy birch twigs used to whisk the skin", "tool", FIN, "The word used in eastern Finland for the same thing as vihta.")
add("saunahattu", FI, "", "Sauna hat", "headwear", FIN, "Usually wool felt, worn dry. Used by some bathers, not all.")
add("pefletti", FI, "", "Small seat cover to sit on in the sauna", "tool", FIN, "Colloquial; the neutral word is laudeliina.")
add("avanto", FI, "", "Hole cut in the ice of a lake or the sea, for a cold dip", "cooling", FIN, "")
add("avantouinti", FI, "", "Ice swimming: swimming in a hole cut in the ice", "cooling", FIN, "A general word for winter swimming; often done between sauna rounds.")
add("saunoa", FI, "", "To take a sauna (verb)", "practice", FIN, "")
add("saunatonttu", FI, "", "The elf of Finnish folklore said to live in the sauna", "expression", FIN, "It is said to punish those who misbehave there.")

# ---------------------------------------------------------------- Estonian, Võro
add("saun", ET, "", "Sauna", "place", EST, "")
add("suitsusaun", ET, "", "Smoke sauna", "place", "Estonian smoke sauna (Võromaa)", "")
add("savvusann", VRO, "", "Smoke sauna", "place", "Estonian smoke sauna (Võromaa)", "The Võro-language name used in the UNESCO listing for Võromaa.")
add("keris", ET, "", "Sauna stove with stones", "heat source", EST, "")
add("leil", ET, "", "Steam from water thrown on the hot stones", "steam", EST, "Cognate of Finnish löyly.")
add("leiliruum", ET, "", "The hot room of a sauna", "room", EST, "Literally 'steam room'.")
add("saunalava", ET, "", "Raised platform in a sauna for taking the steam and whisking", "room", EST, "")
add("viht", ET, "", "Bundle of leafy twigs used to whisk the skin", "tool", EST, "")

# ---------------------------------------------------------------- Swedish, Norwegian, Danish, Icelandic
add("bastu", SV, "", "Sauna", "place", SWE, "Short for badstuga, 'bath cabin'.")
add("badstuga", SV, "", "Bath cabin; the older word that bastu comes from", "place", SWE, "")
add("bada bastu", SV, "", "To take a sauna", "practice", SWE, "Literally 'to bathe sauna'.")
add("bastuaggregat", SV, "", "Sauna heater", "heat source", SWE, "")
add("lave", SV, "", "Wooden bench in a sauna", "room", SWE, "Also bastulave, a form now used mostly in Finland-Swedish.")
add("kallbadhus", SV, "", "Open-air bathhouse built by or over the sea or a lake for cold-water bathing", "place", SWE, "Many have a sauna.")
add("badstue", NO, "", "Sauna", "place", NOR, "Also written badstu.")
add("saunagus", DA, "", "Session in which water with essential oils is poured on the stones and the hot air is fanned around", "practice", "Danish sauna", "The Danish counterpart of the German Aufguss.")
add("gusmester", DA, "", "The person who performs a saunagus, waving a towel or a fan", "person", "Danish sauna", "")
add("sundlaug", IS_, "", "Swimming pool; in Iceland an outdoor geothermal pool with hot tubs", "place", "Icelandic geothermal pool and hot tub", "")
add("heitur pottur", IS_, "", "Hot tub", "place", "Icelandic geothermal pool and hot tub", "Literally 'hot pot'.")
add("gufubað", IS_, "", "Steam bath", "place", "Icelandic geothermal pool and hot tub", "")

# ---------------------------------------------------------------- Russian, Ukrainian
add("баня", RU, "banya", "Russian steam bath", "place", RUS, "")
add("баня по-чёрному", RU, "banya po-chyornomu", "'Black' banya: smoke-heated, with no chimney", "place", "Russian black banya", "")
add("баня по-белому", RU, "banya po-belomu", "'White' banya: the stove has a chimney, so the room stays free of smoke", "place", RUS, "")
add("парилка", RU, "parilka", "The steam room of a banya", "room", RUS, "Also парная (parnaya).")
add("парная", RU, "parnaya", "The steam room of a banya", "room", RUS, "Also парилка (parilka).")
add("предбанник", RU, "predbannik", "The anteroom of a banya, for undressing, resting and tea", "room", RUS, "")
add("каменка", RU, "kamenka", "The banya stove with its stones", "heat source", RUS, "From камень, 'stone'.")
add("полок", RU, "polok", "The wide raised bench in the steam room, where bathers steam", "room", RUS, "")
add("пар", RU, "par", "Steam", "steam", RUS, "")
add("веник", RU, "venik", "Bundle of leafy twigs (birch, oak, eucalyptus) used to fan and whisk the skin", "tool", RUS, "")
add("парение", RU, "parenie", "Steaming and whisking with a venik", "practice", RUS, "")
add("парильщик", RU, "parilshchik", "The person who steams and whisks bathers", "person", RUS, "")
add("банщик", RU, "banshchik", "Bathhouse attendant", "person", RUS, "")
add("шайка", RU, "shaika", "Small wooden tub or tin basin with handles, for washing in a banya", "tool", RUS, "")
add("банная шапка", RU, "bannaya shapka", "Banya hat", "headwear", RUS, "Usually wool felt, worn dry. Also шапка для бани (shapka dlya bani).")
add("С лёгким паром!", RU, "S lyogkim parom!", "Friendly greeting to someone who has just come out of the banya", "expression", RUS, "Literally 'with light steam'. Also said after a bath or shower.")
add("лазня", UK, "laznia", "Bathhouse, steam bath", "place", RUS, "The Ukrainian word for the same kind of bath.")
add("віник", UK, "vinyk", "In a bathhouse, the bundle of leafy twigs used to whisk the skin", "tool", RUS, "The everyday meaning is 'broom'.")

# ---------------------------------------------------------------- Latvian, Lithuanian
add("pirts", LV, "", "Latvian sauna", "place", LAT, "")
add("melnā pirts", LV, "", "'Black' sauna: smoke-heated, with no chimney", "place", LAT, "Also dūmu pirts, 'smoke sauna'.")
add("pirtnieks", LV, "", "Bath master who leads the ritual", "person", LAT, "")
add("pirtsslota", LV, "", "Bath whisk, usually of birch twigs", "tool", LAT, "From slota, 'broom'.")
add("gars", LV, "", "Steam, usually the steam in a pirts", "steam", LAT, "A separate word spelled the same way means 'spirit'.")
add("lāva", LV, "", "Raised board platform in the pirts, usually stepped, for heating up and whisking", "room", LAT, "")
add("pirtis", LT, "", "Lithuanian sauna", "place", LIT, "")
add("dūminė pirtis", LT, "", "Smoke sauna: a pirtis with no chimney", "place", LIT, "")
add("pirtininkas", LT, "", "Bath master who leads the session", "person", LIT, "")
add("vanta", LT, "", "Bundle of leafy twigs used to whisk the skin", "tool", LIT, "")
add("vanojimas", LT, "", "Whisking with a vanta", "practice", LIT, "")
add("garas", LT, "", "Steam; in a pirtis, the steam from water poured on the hot stones", "steam", LIT, "")
add("plautai", LT, "", "The raised benches of a pirtis, for sitting, lying and whisking", "room", LIT, "Plural of plautas.")

# ---------------------------------------------------------------- German, Dutch
add("Aufguss", DE, "", "Session in which a sauna master pours water, often scented, on the stones and fans the hot air with a towel", "practice", GER, "Literally 'infusion' or 'pouring on'.")
add("Saunameister", DE, "", "Sauna master, the person who leads an Aufguss", "person", GER, "Also Aufgussmeister.")
add("Wedeln", DE, "", "Fanning the hot air toward the bathers with a towel during an Aufguss", "practice", GER, "An everyday verb meaning 'to wave'.")
add("Saunagang", DE, "", "One round in the sauna", "practice", GER, "")
add("Ruheraum", DE, "", "Rest room for lying down between rounds", "room", GER, "")
add("Tauchbecken", DE, "", "Cold plunge pool for cooling off after a sauna round", "cooling", GER, "")
add("Dampfbad", DE, "", "Steam bath", "place", "Steam room", "")
add("Biosauna", DE, "", "Soft sauna: lower temperature and higher humidity than a Finnish sauna", "place", "Bio sauna (soft sauna)", "Sanarium is a manufacturer's trade name for the same kind of room.")
add("Wenik", DE, "", "Bundle of birch twigs used to whisk the body, borrowed from Russian веник", "tool", GER, "")
add("Saunahut", DE, "", "Sauna hat", "headwear", GER, "Usually wool felt, worn dry. Also Saunamütze.")
add("opgieting", NL, "", "Pouring water on the sauna stove, and the session built around it", "practice", "Dutch sauna", "The Dutch word for Aufguss.")
add("saunameester", NL, "", "Sauna master: the staff member who looks after guests and performs the opgieting", "person", "Dutch sauna", "")
add("dompelbad", NL, "", "Cold plunge bath for cooling off after the sauna", "cooling", "Dutch sauna", "")

# ---------------------------------------------------------------- Turkish, Arabic, French, Georgian
add("hamam", TR, "", "Turkish bath", "place", TUR, "English usually writes hammam, after the Arabic.")
add("külhan", TR, "", "The furnace that heats the bath's floor, walls and water", "heat source", TUR, "")
add("göbektaşı", TR, "", "The heated marble platform in the middle of the hot room", "room", TUR, "Literally 'navel stone'. Also written göbek taşı.")
add("sıcaklık", TR, "", "The hot room of a hamam, where bathers wash", "room", TUR, "")
add("soğukluk", TR, "", "The cool room for resting", "room", TUR, "")
add("camekân", TR, "", "The glazed changing room of a hamam", "room", TUR, "In everyday Turkish the word now mostly means a shop window.")
add("kurna", TR, "", "Round marble or stone basin under the tap, where the water collects", "tool", TUR, "")
add("hamam tası", TR, "", "Shallow bowl for scooping water from the basin and pouring it over the body", "tool", TUR, "")
add("kese", TR, "", "Coarse mitt for scrubbing the skin", "tool", TUR, "")
add("peştemal", TR, "", "Flat-woven cotton wrap worn in the hamam", "tool", TUR, "")
add("nalın", TR, "", "Wooden clogs worn on the wet floor", "tool", TUR, "")
add("tellak", TR, "", "Male bath attendant who scrubs and washes bathers", "person", TUR, "")
add("natır", TR, "", "Female bath attendant", "person", TUR, "")
add("حمّام", AR, "ḥammām", "Bath, bathhouse", "place", MOR, "The word behind English hammam and Turkish hamam.")
add("صابون بلدي", AR, "ṣābūn baladī", "Soft black soap made from olive oil", "tool", MOR, "Known by its French-Moroccan name savon beldi.")
add("غاسول", AR, "ghāsūl", "Mineral clay used to wash the skin and hair", "tool", MOR, "Written rhassoul or ghassoul in English.")
add("savon noir", FR, "", "Soft soap made from vegetable oil and potash; in a hammam, the black olive soap used before the scrub", "tool", MOR, "Literally 'black soap'.")
add("gant de kessa", FR, "", "Rough Moroccan scrubbing glove used in hammams", "tool", MOR, "Kessa is the French spelling of the Arabic word for the glove.")
add("كيس", AR, "kīs", "Coarse cloth mitt used to rub off dead skin after the black soap", "tool", MOR, "Literally 'bag'. Written kessa in French and English.")
add("გოგირდის აბანო", KA, "gogirdis abano", "Sulfur bath", "place", GEO, "The domed bathhouses of Tbilisi's Abanotubani district.")
add("ქისა", KA, "kisa", "Fingerless mitt of coarse cloth for rubbing the body in the bath", "tool", GEO, "Variant: ქესა (kesa). The first meaning of the word is 'purse'.")
add("მექისე", KA, "mekise", "Bath attendant who gives the scrub with the kisa", "person", GEO, "")

# ---------------------------------------------------------------- Latin, Irish
add("thermae", LA, "", "Large public bath complex", "place", ROM, "")
add("balneae", LA, "", "Baths, usually smaller ones", "place", ROM, "")
add("apodyterium", LA, "", "Changing room", "room", ROM, "")
add("tepidarium", LA, "", "Warm room", "room", ROM, "")
add("caldarium", LA, "", "Hot room", "room", ROM, "")
add("frigidarium", LA, "", "Cold room with a cold plunge", "room", ROM, "")
add("laconicum", LA, "", "Dry sweating room", "room", ROM, "")
add("sudatorium", LA, "", "Vaulted sweating room", "room", ROM, "")
add("natatio", LA, "", "Swimming pool, the open-air pool of a bath complex", "place", ROM, "")
add("hypocaustum", LA, "", "Underfloor heating system", "heat source", ROM, "English: hypocaust.")
add("strigilis", LA, "", "Curved scraper for removing oil and sweat from the skin", "tool", ROM, "English: strigil.")
add("teach allais", GA, "", "Sweat house", "place", "Irish sweat house (historical)", "Literally 'house of sweat'.")

# ---------------------------------------------------------------- Japanese
add("サウナ", JA, "sauna", "Sauna", "place", JPS, "")
add("銭湯", JA, "sentō", "Neighborhood public bathhouse", "place", JPB, "")
add("温泉", JA, "onsen", "Hot spring, and the baths fed by one", "place", "Japanese onsen", "")
add("露天風呂", JA, "rotenburo", "Open-air bath", "place", "Japanese onsen", "")
add("岩盤浴", JA, "ganban'yoku", "Bedrock bathing: lying on stone slabs warmed to about 40 °C", "practice", JPS, "")
add("水風呂", JA, "mizuburo", "Cold-water bath taken after the sauna", "cooling", JPS, "")
add("外気浴", JA, "gaikiyoku", "Resting in the open air after the cold bath", "cooling", JPS, "")
add("ととのう", JA, "totonou", "The settled, relaxed state after repeating sauna, cold bath and rest", "expression", JPS, "A sauna slang use of a verb meaning 'to be put in order'.")
add("ロウリュ", JA, "rōryu", "Pouring water on the hot sauna stones for steam, or that steam", "steam", JPS, "From Finnish löyly. Also written ロウリュウ.")
add("アウフグース", JA, "aufugūsu", "Aufguss: staff fan the steam toward bathers with towels", "practice", JPS, "From German Aufguss.")
add("熱波師", JA, "neppashi", "'Heat-wave master': the person who fans hot air at the bathers", "person", JPS, "The Japanese name for an Aufguss performer.")
add("サウナー", JA, "saunā", "A sauna enthusiast", "person", JPS, "A Japanese-made English word, 'saunner'.")
add("サ飯", JA, "sameshi", "'Sauna meal': the food eaten after a sauna", "food and drink", JPS, "Short for サウナ飯.")
add("サウナハット", JA, "sauna hatto", "Sauna hat", "headwear", JPS, "Wool felt or cotton terry.")
add("手ぬぐい", JA, "tenugui", "Thin cotton hand towel", "tool", JPB, "Often folded on top of the head to keep it out of the bath water.")

# ---------------------------------------------------------------- Korean
add("찜질방", KO, "jjimjilbang", "Large bathhouse with heated rooms, baths and a shared lounge", "place", KOR, "")
add("한증막", KO, "hanjeungmak", "Traditional dome-shaped kiln sauna", "place", "Korean hanjeungmak", "")
add("불가마", KO, "bulgama", "'Fire kiln': a very hot kiln room in a jjimjilbang", "room", KOR, "")
add("목욕탕", KO, "mogyoktang", "Public bathhouse", "place", KOR, "")
add("냉탕", KO, "naengtang", "Cold pool", "cooling", KOR, "")
add("세신", KO, "sesin", "Full-body scrub given by an attendant", "practice", KOR, "Often romanized seshin.")
add("때밀이", KO, "ttaemiri", "Bathhouse worker who scrubs the dirt off bathers", "person", KOR, "Also called 세신사 (sesinsa).")
add("이태리타월", KO, "itaeri tawol", "'Italy towel': the coarse cloth used for scrubbing the skin", "tool", KOR, "The name comes from a brand. Also written 이태리 타올.")
add("양머리", KO, "yangmeori", "'Sheep head': a towel folded with a roll over each ear", "headwear", KOR, "A playful custom, not a heat hat.")
add("식혜", KO, "sikhye", "Sweet rice drink served cold", "food and drink", KOR, "")
add("맥반석 계란", KO, "maekbanseok gyeran", "Eggs baked on hot stones, a jjimjilbang snack", "food and drink", KOR, "")

# ---------------------------------------------------------------- Americas
add("inípi", LKT, "", "The Lakota purification ceremony held in a sweat lodge", "practice", "Native American sweat lodge", "Also iníkaǧapi. A sacred ceremony, not a recreational bath. Listed for reference only.")
add("temazcalli", NAH, "", "Sweat house, sweat bath", "place", "Temazcal", "From calli, 'house'; the first part is explained as 'to bathe' or as 'heat'. Spanish: temazcal.")
add("temazcal", ES, "", "Mesoamerican sweat house, and the ceremony held in it", "place", "Temazcal", "From Nahuatl temazcalli.")
add("temazcalero", ES, "", "The person who leads a temazcal", "person", "Temazcal", "Feminine: temazcalera.")

# ---------------------------------------------------------------- Italian
add("bagno turco", IT, "", "Turkish bath", "place", TUR, "Synonym: hammam.")


def main():
    rows = E
    with open(os.path.join(HERE, "sauna_glossary.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(HERE, "sauna_glossary.json"), "w", encoding="utf-8") as f:
        json.dump([{k: (r[k] if r[k] != "" else None) for k in COLUMNS} for r in rows], f, ensure_ascii=False, indent=2)
        f.write("\n")
    langs = sorted({r["language"] for r in rows})
    print(f"wrote {len(rows)} terms in {len(langs)} languages")


if __name__ == "__main__":
    main()
