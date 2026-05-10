import json
from pathlib import Path

BASE = Path(__file__).parent
DATA = BASE / "assets" / "sentences.json"

with open(DATA, "r", encoding="utf-8") as f:
    data = json.load(f)

print("TOTAL ITEMS:", len(data))


print("\n--- RAW SAMPLE ---")
for i in range(10):
    item = data[i]
    print(item)


print("\n--- CLEAN CHECK ---")
valid = 0

for item in data:
    en = str(item.get("en", "")).strip()
    it = str(item.get("it", "")).strip()

    if en and it:
        valid += 1

print("VALID PAIRS:", valid)


print("\n--- LENGTH DEBUG ---")
for i in range(10):
    en = str(data[i].get("en", ""))
    print("TEXT:", en)
    print("SPLIT:", en.split())
    print("LEN:", len(en.split()))
    print("-----")