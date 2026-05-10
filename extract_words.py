import json
import re
from pathlib import Path

BASE = Path(__file__).parent
INPUT = BASE / "assets" / "words.json"
OUTPUT = BASE / "assets" / "words_clean.json"

with open(INPUT, "r", encoding="utf-8") as f:
    data = json.load(f)

results = []

pattern = re.compile(r"([A-Za-zÀ-ÿ]+)\s*\(([^)]+)\)")

for item in data:
    text = item.get("it", "")

    matches = pattern.findall(text)

    for it_word, en_word in matches:
        results.append({
            "it": it_word.strip(),
            "en": en_word.strip()
        })

print("EXTRACTED:", len(results))

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("DONE ✔ words_clean.json created")