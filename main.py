import flet as ft

    def clear_screen():
        top_text.value = ""
        middle_text.value = ""
        bottom_text.value = ""
        page.update()

    def show_word():
        if not words:
            top_text.value = "No word files found"
            page.update()
            return

        item = random.choice(words)
        clear_screen()
        top_text.value = item["en"]
        page.update()

        def delayed_answer():
            time.sleep(3)
            bottom_text.value = item["it"]
            page.update()

        threading.Thread(target=delayed_answer, daemon=True).start()

    def show_sentence():
        if not sentences:
            top_text.value = "No sentence files found"
            page.update()
            return

        item = random.choice(sentences)
        clear_screen()
        top_text.value = item["en"]
        page.update()

        def delayed_sentence():
            time.sleep(4)
            middle_text.value = item["partial"]
            page.update()

            time.sleep(4)
            bottom_text.value = fill_blanks(item["partial"], item["solution"])
            page.update()

        threading.Thread(target=delayed_sentence, daemon=True).start()

    def next_item(e):
        if state["mode"] == "words":
            show_word()
        else:
            show_sentence()

    def set_words(e):
        state["mode"] = "words"
        show_word()

    def set_sentences(e):
        state["mode"] = "sentences"
        show_sentence()

    page.add(
        title,
        top_text,
        middle_text,
        bottom_text,
        ft.Row(
            [
                ft.ElevatedButton("WORDS", on_click=set_words),
                ft.ElevatedButton("SENTENCES", on_click=set_sentences),
                ft.ElevatedButton("NEXT", on_click=next_item),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    show_word()


ft.run(main)