import json
import re
from pathlib import Path

BASE = Path(__file__).parent
INPUT = BASE / "assets" / "sentences.json"
OUTPUT = BASE / "assets" / "sentences_clean.json"


def extract_pairs(text):
    tokens = re.findall(r"[A-Za-zÀ-ÿ']+", text)

    pairs = []
    buffer = []

    for t in tokens:
        if len(t) < 3:
            continue

        buffer.append(t)

        # כל 2 מילים → זוג
        if len(buffer) == 2:
            it = buffer[0]
            en = buffer[1]

            pairs.append({
                "en": en,
                "it": it
            })

            buffer = []

    return pairs


with open(INPUT, "r", encoding="utf-8") as f:
    raw = json.load(f)


clean_words = []

for block in raw:
    text = block.get("text", "")
    clean_words.extend(extract_pairs(text))


# ניקוי כפילויות
seen = set()
final_words = []

for w in clean_words:
    key = (w["en"], w["it"])
    if key not in seen:
        seen.add(key)
        final_words.append(w)


final = {
    "WORDS": final_words,
    "SENTENCES": []
}

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(final, f, ensure_ascii=False, indent=2)

print("DONE ✔ WORDS:", len(final_words))