import pdfplumber
import json
import os
import re

FILES = [f for f in os.listdir("assets") if f.endswith(".pdf")]

output = {
    "words": [],
    "sentences": [],
    "ARE": [],
    "ERE": [],
    "IRE": []
}

def clean(t):
    return re.sub(r"\s+", " ", t).strip()

def type_of(name):
    n = name.upper()
    if n.startswith("ARE"):
        return "ARE"
    if n.startswith("ERE"):
        return "ERE"
    if n.startswith("IRE"):
        return "IRE"
    if re.match(r"^[A-Z]\d", n):
        return "words"
    return "sentences"

for file in FILES:
    path = "assets/" + file
    kind = type_of(file)

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            for line in text.split("\n"):
                line = clean(line)
                if len(line) < 2:
                    continue

                parts = line.split(" ")
                if len(parts) < 2:
                    continue

                item = {"it": line, "en": ""}

                output[kind].append(item)

for k in output:
    with open(f"assets/{k}.json", "w", encoding="utf-8") as f:
        json.dump(output[k], f, ensure_ascii=False, indent=2)

print("DONE CLEAN PIPELINE")