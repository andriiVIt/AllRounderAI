import flet as ft
import requests


def main(page: ft.Page):
    # Page settings
    page.title = "AllRounderAI"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "auto"
    page.bgcolor = ft.Colors.SURFACE

    # Header text
    header = ft.Text(
        "AllRounderAI Chatbot",
        size=24,
        weight=ft.FontWeight.BOLD,
    )

    # Text field for conversation subject
    subject_field = ft.TextField(
        label="Subject",
        width=300,
        filled=True,
        border="underline",
        autofocus=True,
    )

    # Chat display area
    chat_view = ft.ListView(
        spacing=10,
        auto_scroll=True,
        expand=True
    )

    # Text field for user input
    user_input = ft.TextField(
        label="Your Message",
        expand=True,
        filled=True,
        border="underline",
        multiline=False,
        autofocus=False,
    )

    def add_message(role: str, text: str):
        if role == "user":
            bubble = ft.Container(
                bgcolor=ft.Colors.BLUE_50,
                border_radius=10,
                padding=10,
                content=ft.Text(text, color=ft.Colors.BLACK),
                alignment=ft.alignment.center_right,
            )
        else:
            bubble = ft.Container(
                bgcolor=ft.Colors.GREEN_50,
                border_radius=10,
                padding=10,
                content=ft.Text(text, color=ft.Colors.BLACK),
                alignment=ft.alignment.center_left,
            )
        chat_view.controls.append(bubble)
        page.update()

    def send_message(e):
        subj = subject_field.value.strip()
        msg = user_input.value.strip()

        if not subj or not msg:
            return

        add_message("user", msg)
        user_input.value = ""

        try:
            res = requests.post(
                "http://127.0.0.1:8000/chat",
                json={"subject": subj, "message": msg}
            )
            if res.ok:
                data = res.json()
                reply = data["reply"]
                add_message("assistant", reply)
            else:
                add_message("assistant", "⚠️ Error: Could not get response from server.")
        except Exception as ex:
            add_message("assistant", f"❌ Connection error: {ex}")

        page.update()

    def on_subject_change(e):
        chat_view.controls.clear()
        subj = subject_field.value

        if not subj:
            return

        try:
            res = requests.get(f"http://127.0.0.1:8000/history/{subj}")
            if res.ok:
                history = res.json()
                for msg in history:
                    add_message(msg["role"], msg["message"])
            else:
                add_message("assistant", "⚠️ Failed to load chat history.")
        except Exception as ex:
            add_message("assistant", f"❌ Error: {ex}")

        page.update()

    # Assign the event handler to subject field
    subject_field.on_change = on_subject_change

    send_btn = ft.ElevatedButton(
        text="Send",
        icon=ft.Icons.SEND,
        on_click=send_message,
        style=ft.ButtonStyle(
            color={"": ft.Colors.WHITE},
            bgcolor={"": ft.Colors.BLUE_400},
        ),
    )

    # Final page layout
    page.add(
        ft.Column(
            controls=[
                header,
                subject_field,
                chat_view,
                ft.Row([
                    user_input,
                    send_btn
                ], spacing=10),
            ],
            spacing=10,
            width=700,
            expand=True
        )
    )


ft.app(target=main)