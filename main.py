import flet as ft
import asyncio
import random
import os
import re
import edge_tts
import pygame
from pypdf import PdfReader

# --- הגדרות נתיבים ---
# בשימוש בטלפון/Web, נחפש את התיקייה היחסית assets
ASSETS_DIR = "assets" 
TEMP_AUDIO = "temp_speech.mp3"

async def speak_text(text, lang="it"):
    """הקראה איכותית בקולות נשיים (AI) - אופטימיזציה למובייל"""
    try:
        # הגדרת קולות נשיים
        voice = "it-IT-ElsaNeural" if lang == "it" else "en-US-EmmaNeural"
        
        # מהירות: איטלקית איטית (-30%), אנגלית כמעט רגילה (-10%)
        rate = "-30%" if lang == "it" else "-10%"
        
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(TEMP_AUDIO)

        # אתחול נקי של הנגן
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        pygame.mixer.music.load(TEMP_AUDIO)
        pygame.mixer.music.play()
        
        # המתנה לסיום ההקראה
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)
        
        pygame.mixer.quit()
        
        # ניקוי קובץ זמני כדי לא להעמיס על זיכרון הטלפון
        if os.path.exists(TEMP_AUDIO):
            try: os.remove(TEMP_AUDIO)
            except: pass
            
    except Exception as e:
        print(f"Audio Error: {e}")

# --- פונקציות חילוץ נתונים (PDF) ---

def get_sentences_from_pdf(file_path):
    data = []
    if not os.path.exists(file_path): return data
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text = page.extract_text()
            if not text: continue
            clean_text = re.sub(r'\s+', ' ', text)
            items = re.split(r'(\d+)\s+', clean_text)
            for i in range(1, len(items), 2):
                line_content = items[i+1].strip()
                try:
                    split_en = line_content.split('.', 1)
                    if len(split_en) < 2: continue
                    en_text = split_en[0].strip() + "."
                    remainder = split_en[1].strip()
                    split_it = remainder.split('.', 1)
                    if len(split_it) < 2: continue
                    blanked_it = split_it[0].strip() + "."
                    after_it = split_it[1].strip()
                    
                    sol_match = re.search(r'([a-zA-ZàèéìòùÀÈÉÌÒÙ\s]*/[a-zA-ZàèéìòùÀÈÉÌÒÙ\s/]*)', after_it)
                    if not sol_match:
                        sol_match = re.search(r'([a-zA-ZàèéìòùÀÈÉÌÒÙ]+)', after_it)
                    
                    if sol_match:
                        raw_solution = sol_match.group(1).strip()
                        solutions = [s.strip() for s in raw_solution.split('/') if s.strip()]
                        full_it = blanked_it
                        for sol in solutions:
                            if "___" in full_it or "__" in full_it:
                                full_it = re.sub(r'_{2,}', sol, full_it, count=1)
                        full_it = re.sub(r'\s+', ' ', full_it.replace('_', '')).strip()
                        data.append({"en": en_text, "blanked": blanked_it, "full": full_it})
                except: continue
    except: pass
    return data

def get_words_from_pdf(file_path):
    words = []
    if not os.path.exists(file_path): return words
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text = page.extract_text()
            if not text: continue
            clean_text = re.sub(r'\s+', ' ', text)
            matches = re.finditer(r"([a-zA-ZàèéìòùÀÈÉÌÒÙ ']+?)\s*[\(\-\[ ]\s*([a-zA-Z\s\u0590-\u05fe/]+?)[\)\-\]]", clean_text)
            for match in matches:
                it_val = match.group(1).strip()
                en_val = match.group(2).strip()
                if len(it_val) > 1:
                    words.append({"it": it_val, "en": en_val})
    except: pass
    return words

def get_filtered_lists(mode="Words"):
    try:
        if not os.path.exists(ASSETS_DIR): return []
        all_files = [os.path.splitext(f)[0] for f in os.listdir(ASSETS_DIR) if f.endswith('.pdf')]
        word_pattern = re.compile(r"^[a-zA-Z]\d+$")
        if mode == "Words":
            return sorted([f for f in all_files if word_pattern.match(f)])
        else:
            return sorted([f for f in all_files if not word_pattern.match(f)])
    except: return []

# --- ממשק המשתמש (Main) ---

async def main(page: ft.Page):
    page.title = "Italian Lab AI"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    
    # התאמה למסכי טלפון
    page.padding = 20
    
    app_state = {"data": [], "running": False, "mode": "Words"}
    
    display_1 = ft.Text("Ready", size=24, weight="bold", text_align="center")
    display_2 = ft.Text("", size=28, weight="bold", color="blue-900", text_align="center")
    
    initial_options = get_filtered_lists("Words")
    list_dropdown = ft.Dropdown(
        label="Select List", 
        width=300,
        options=[ft.dropdown.Option(name) for name in initial_options],
        value=initial_options[0] if initial_options else None
    )

    async def change_mode(e):
        app_state["mode"] = e.control.data
        app_state["running"] = False
        words_btn.bgcolor = ft.Colors.BLUE_700 if app_state["mode"] == "Words" else ft.Colors.GREY_200
        words_btn.color = ft.Colors.WHITE if app_state["mode"] == "Words" else ft.Colors.BLACK
        sentences_btn.bgcolor = ft.Colors.BLUE_700 if app_state["mode"] == "Sentences" else ft.Colors.GREY_200
        sentences_btn.color = ft.Colors.WHITE if app_state["mode"] == "Sentences" else ft.Colors.BLACK
        
        available = get_filtered_lists(app_state["mode"])
        list_dropdown.options = [ft.dropdown.Option(name) for name in available]
        list_dropdown.value = available[0] if available else None
        page.update()

    async def start_session(e):
        if not list_dropdown.value: return
        
        path = os.path.join(ASSETS_DIR, f"{list_dropdown.value}.pdf")
        app_state["data"] = get_sentences_from_pdf(path) if app_state["mode"] == "Sentences" else get_words_from_pdf(path)
        
        if not app_state["data"]: 
            display_1.value = "No data found!"; page.update(); return

        app_state["running"] = True
        start_btn.visible = False; stop_btn.visible = True; page.update()

        while app_state["running"]:
            item = random.choice(app_state["data"])
            
            if app_state["mode"] == "Sentences":
                # 1. אנגלית + הקראה
                display_1.value = item["en"]; display_2.value = ""; page.update()
                await speak_text(item["en"], "en")
                await asyncio.sleep(3)
                if not app_state["running"]: break
                
                # 2. משפט חסר
                display_2.value = item["blanked"]; display_2.color = "orange-800"; page.update()
                await asyncio.sleep(4)
                if not app_state["running"]: break
                
                # 3. משפט מלא + הקראה כפולה
                display_2.value = item["full"]; display_2.color = "green-800"; page.update()
                await speak_text(item["full"], "it")
                await asyncio.sleep(1.0)
                await speak_text(item["full"], "it")
                
            else: # מצב Words
                display_1.value = item["en"]; display_2.value = ""; page.update()
                await speak_text(item["en"], "en")
                await asyncio.sleep(3)
                if not app_state["running"]: break
                
                display_2.value = item["it"]; display_2.color = "blue-900"; page.update()
                await speak_text(item["it"], "it")
                await asyncio.sleep(1.0)
                await speak_text(item["it"], "it")

            await asyncio.sleep(3)

    async def stop_session(e):
        app_state["running"] = False
        start_btn.visible = True; stop_btn.visible = False
        display_1.value = "Ready"; display_2.value = ""; page.update()

    # עיצוב כפתורים
    words_btn = ft.ElevatedButton("Words", data="Words", on_click=change_mode, bgcolor="blue700", color="white")
    sentences_btn = ft.ElevatedButton("Sentences", data="Sentences", on_click=change_mode, bgcolor="grey200", color="black")
    start_btn = ft.ElevatedButton("Start Session", on_click=start_session, icon=ft.Icons.PLAY_ARROW)
    stop_btn = ft.ElevatedButton("Stop", on_click=stop_session, visible=False, color="red", icon=ft.Icons.STOP)

    # בניית העמוד
    page.add(
        ft.Column([
            ft.Text("Italian Lab AI", size=32, weight="bold"),
            ft.Row([words_btn, sentences_btn], alignment="center"),
            list_dropdown,
            ft.Container(
                content=ft.Column([display_1, display_2], horizontal_alignment="center", spacing=20),
                padding=30, bgcolor="#f5f5f5", border_radius=15, width=350
            ),
            ft.Row([start_btn, stop_btn], alignment="center")
        ], horizontal_alignment="center", spacing=20)
    )

if __name__ == "__main__":
    # פקודה זו תומכת גם בהרצה מקומית וגם בפריסה ל-Web
    ft.app(target=main)