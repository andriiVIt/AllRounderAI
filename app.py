import flet as ft
import requests

def main(page: ft.Page):
    # Page settings
    page.title = "AllRounderAI"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "auto"
    page.bgcolor = ft.Colors.SURFACE  # Updated usage of Colors

    # We'll store messages in memory for now
    messages_list = []

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

    # A ListView to display chat messages with auto-scroll
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
        multiline=False,  # single-line input for the user message
        autofocus=False,
    )

    def add_message(role: str, text: str):
        """
        Adds a new message bubble to the chat view.

        role: 'user' or 'bot'
        text: the content of the message
        """
        if role == "user":
            # User messages: aligned right, for example
            bubble = ft.Container(
                bgcolor=ft.Colors.BLUE_50,
                border_radius=10,
                padding=10,
                content=ft.Text(text, color=ft.Colors.BLACK),
                alignment=ft.alignment.center_right,
            )
        else:
            # Bot or assistant messages: aligned left
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
        """
        Sends user input to the FastAPI endpoint
        and displays the bot response.
        """
        subj = subject_field.value.strip()
        msg = user_input.value.strip()

        if not subj or not msg:
            return

        # Add user's message bubble
        add_message("user", msg)
        user_input.value = ""

        try:
            # POST request to FastAPI
            res = requests.post(
                "http://127.0.0.1:8000/chat",
                json={"subject": subj, "message": msg}
            )
            if res.ok:
                data = res.json()
                reply = data["reply"]
                add_message("bot", reply)
            else:
                add_message("bot", "Error: Could not get response from server.")
        except Exception as ex:
            add_message("bot", f"Connection error: {ex}")

        page.update()

    send_btn = ft.ElevatedButton(
        text="Send",
        icon=ft.Icons.SEND,  # Updated usage of Icons
        on_click=send_message,
        style=ft.ButtonStyle(
            color={"": ft.Colors.WHITE},
            bgcolor={"": ft.Colors.BLUE_400},
        ),
    )

    # Page layout
    page.add(
        ft.Column(
            controls=[
                header,
                subject_field,
                chat_view,
                ft.Row(
                    controls=[user_input, send_btn],
                    spacing=10,
                )
            ],
            spacing=10,
            width=700,
            expand=True
        )
    )

ft.app(target=main)
