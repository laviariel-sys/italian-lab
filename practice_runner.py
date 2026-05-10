import json
import time
import asyncio
import edge_tts
import os
from pathlib import Path

BASE = Path(__file__).parent
DATA_FILE = BASE / "assets" / "words_clean.json"

VOICE_EN = "en-US-AriaNeural"
VOICE_IT = "it-IT-ElsaNeural"

TEMP_FILE = BASE / "temp.mp3"


# ================= LOAD DATA =================
with open(DATA_FILE, "r", encoding="utf-8") as f:
    words = json.load(f)

print("TOTAL WORDS:", len(words))


# ================= TTS =================
async def speak(text, voice, rate="+0%"):
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
    await communicate.save(str(TEMP_FILE))

    os.system(f'start "" "{TEMP_FILE}"')


# ================= MAIN LOOP =================
async def run():
    for w in words:
        en = w.get("en", "").strip()
        it = w.get("it", "").strip()

        if not en or not it:
            continue

        print("\n────────────")
        print(f"🇬🇧 {en}")

        await speak(en, VOICE_EN)
        await asyncio.sleep(3)

        print(f"🇮🇹 {it}")

        await speak(it, VOICE_IT, rate="-20%")
        await speak(it, VOICE_IT, rate="-20%")

        await asyncio.sleep(1)


# ================= START =================
asyncio.run(run())