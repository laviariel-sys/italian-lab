import json

class ItalianEngine:
    def __init__(self, words_path, sentences_path):
        self.words = self._load(words_path)
        self.sentences = self._load(sentences_path)

    def _load(self, path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # תומך גם במבנה list וגם dict
        if isinstance(data, dict):
            if "WORDS" in data:
                return data["WORDS"]
            if "SENTENCES" in data:
                return data["SENTENCES"]

        return data

    # ---------------- WORD FLOW ----------------
    def get_word(self, index):
        if index >= len(self.words):
            return None

        item = self.words[index]

        return {
            "en": item.get("en", ""),
            "it": item.get("it", "")
        }

    # ---------------- SENTENCE FLOW ----------------
    def get_sentence(self, index):
        if index >= len(self.sentences):
            return None

        item = self.sentences[index]

        return {
            "en": item.get("en", ""),
            "masked": item.get("it_masked", ""),
            "full": item.get("it_full", ""),
            "solution": item.get("solution", "")
        }