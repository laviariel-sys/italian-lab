import flet as ft
from engine import ItalianEngine

engine = ItalianEngine(
    "assets/words_clean.json",
    "assets/sentences_clean.json"
)

word_index = 0
sentence_index = 0


def main(page: ft.Page):
    page.title = "ItalianLab"
    page.vertical_alignment = "center"

    output = ft.Text(size=30, text_align="center")

    def show_word(e):
        global word_index
        item = engine.get_word(word_index)

        if not item:
            output.value = "END"
        else:
            output.value = f"{item['en']}\n→ {item['it']}"
            word_index += 1

        page.update()

    def show_sentence(e):
        global sentence_index
        item = engine.get_sentence(sentence_index)

        if not item:
            output.value = "END"
        else:
            output.value = (
                f"{item['en']}\n\n"
                f"{item['masked']}\n\n"
                f"{item['full']}"
            )
            sentence_index += 1

        page.update()

    page.add(
        ft.Column([
            output,
            ft.Row([
                ft.ElevatedButton("WORDS", on_click=show_word),
                ft.ElevatedButton("SENTENCES", on_click=show_sentence),
            ], alignment="center")
        ])
    )


ft.app(target=main)