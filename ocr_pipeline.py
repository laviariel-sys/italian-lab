import re
import json
from pathlib import Path
from pdf2image import convert_from_path
import pytesseract

# =========================
# CONFIG
# =========================
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

POPPLER_PATH = r"C:\poppler\poppler-25.12.0\Library\bin"
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# =========================
# CLASSIFY FILES
# =========================
def classify_file(name: str):
    name = name.upper()

    if re.match(r"^[A-Z]\d+\.PDF$", name):
        return "WORDS"

    if name.startswith("ARE"):
        return "ARE"
    if name.startswith("ERE"):
        return "ERE"
    if name.startswith("IRE"):
        return "IRE"

    if name.startswith("PAST"):
        return "PAST"
    if name.startswith("FUTURE"):
        return "FUTURE"

    return "OTHER"


# =========================
# CLEAN OCR
# =========================
def clean_text(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^A-Za-zÀ-ž0-9àèéìòù\.\,\?\!\-\s]", "", text)
    return text.strip()


def extract_text(pdf_path: Path):
    print("OCR:", pdf_path.name)

    pages = convert_from_path(str(pdf_path), poppler_path=POPPLER_PATH)
    out = []

    for page in pages:
        txt = pytesseract.image_to_string(page, lang="ita+eng")
        txt = clean_text(txt)
        if txt:
            out.append(txt)

    return " ".join(out)


def parse_sentences(text: str):
    parts = re.split(r"(?<=[\.\!\?])\s+", text)
    return [p.strip() for p in parts if len(p.strip()) > 2]


# =========================
# MAIN PIPELINE
# =========================
def process():
    print("START ✔")

    output = {
        "ARE": [],
        "ERE": [],
        "IRE": [],
        "PAST": [],
        "FUTURE": [],
        "WORDS": [],
        "OTHER": []
    }

    pdfs = list(ASSETS_DIR.glob("*.pdf"))
    print("PDF COUNT:", len(pdfs))

    if not pdfs:
        print("NO FILES FOUND")
        return

    for file in pdfs:
        try:
            cat = classify_file(file.name)
            text = extract_text(file)

            output[cat].append({
                "file": file.name,
                "text": text,
                "sentences": parse_sentences(text)
            })

        except Exception as e:
            print("ERROR:", file.name, str(e))

    out_file = ASSETS_DIR / "sentences_clean.json"

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("DONE ✔")


if __name__ == "__main__":
    process()