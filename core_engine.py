import json
import time
from pathlib import Path

BASE = Path(__file__).parent
DATA = BASE / "assets" / "sentences.json"

with open(DATA, "r", encoding="utf-8") as f:
    data = json.load(f)

print("TOTAL:", len(data))


def run_words():
    print("\n--- WORD MODE ---\n")

    count = 0

    for item in data:
        en = item.get("en", "").strip()
        it = item.get("it", "").strip()

        if not en or not it:
            continue

        # נחשב מילה גם אם זה 1–2 מילים (OCR לפעמים שובר)
        if len(en.split()) <= 2 and len(it.split()) <= 2:
            print(f"EN: {en}")
            time.sleep(1)

            print(f"IT: {it}")
            print("-----")
            time.sleep(1)

            count += 1
            if count == 20:
                break


def run_sentences():
    print("\n--- SENTENCE MODE ---\n")

    count = 0

    for item in data:
        en = item.get("en", "").strip()
        it = item.get("it", "").strip()

        if not en or not it:
            continue

        if len(en.split()) > 2:
            print(f"EN: {en}")
            time.sleep(2)

            print(f"IT: {it}")
            print("-----")
            time.sleep(2)

            count += 1
            if count == 10:
                break


if __name__ == "__main__":
    choice = input("\n1 = WORDS | 2 = SENTENCES\n>> ")

    if choice == "1":
        run_words()
    else:
        run_sentences()