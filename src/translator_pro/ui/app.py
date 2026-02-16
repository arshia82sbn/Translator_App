import os
import threading
from typing import Any, List

import speech_recognition as sr
from CTkMessagebox import CTkMessagebox
from customtkinter import (
    CTk,
    CTkButton,
    CTkComboBox,
    CTkFrame,
    CTkImage,
    CTkLabel,
    CTkTextbox,
    set_appearance_mode,
    set_default_color_theme,
)
from PIL import Image

from translator_pro.api.facade import TranslatorFacade
from translator_pro.models.languages import LANGUAGES

# Initial settings
set_appearance_mode("dark")
set_default_color_theme("blue")


class TranslatorApp(CTk):  # type: ignore[misc]
    """Main GUI application for Translator Pro."""

    def __init__(self, **kw: Any) -> None:
        """Initializes the application and its UI components."""
        super().__init__(**kw)
        self.facade = TranslatorFacade()
        self.language_names: List[str] = [lang.capitalize() for lang in LANGUAGES.values()]

        self.title("Translator Pro")
        self.geometry("1080x550")

        self._setup_ui()
        self.label_change()

    def _setup_ui(self) -> None:
        """Sets up the UI elements."""
        assets_path = os.path.join(os.path.dirname(__file__), "assets")

        # Load images with safe handling
        def load_asset(name: str, size: tuple[int, int] = (50, 50)) -> CTkImage | None:
            path = os.path.join(assets_path, name)
            if os.path.exists(path):
                return CTkImage(Image.open(path), size=size)
            return None

        self.image_arrow = load_asset("arrow.png", size=(100, 100))
        self.mic_img = load_asset("micro.png")
        self.spk_img = load_asset("speaker 2.png")

        # Input language selection frame
        langentry_frame = CTkFrame(self, fg_color="#777777", corner_radius=20, width=450, height=100)
        langentry_frame.place(x=30, y=10)

        self.combo_entry = CTkComboBox(langentry_frame, values=self.language_names, font=("Roboto", 14))
        self.combo_entry.place(x=10, y=10)
        self.combo_entry.set("English")

        self.label_entry = CTkLabel(langentry_frame, text="ENGLISH", font=("Segoe UI", 30, "bold"), fg_color="blue")
        self.label_entry.place(x=10, y=50)

        # Output language selection frame
        langout_frame = CTkFrame(self, fg_color="#777777", corner_radius=20, width=450, height=100)
        langout_frame.place(x=600, y=10)

        self.combo_output = CTkComboBox(langout_frame, values=self.language_names, font=("Roboto", 14))
        self.combo_output.place(x=10, y=10)
        self.combo_output.set("Persian")

        self.label_output = CTkLabel(langout_frame, text="PERSIAN", font=("Segoe UI", 30, "bold"), fg_color="blue")
        self.label_output.place(x=10, y=50)

        # Arrow icon
        CTkLabel(self, image=self.image_arrow, text="").place(x=495, y=17)

        # Text frames
        noteentry_frame = CTkFrame(self, fg_color="#4964E0", corner_radius=20, width=450, height=350)
        noteentry_frame.place(x=30, y=130)

        noteout_frame = CTkFrame(self, fg_color="#4964E0", corner_radius=20, width=450, height=350)
        noteout_frame.place(x=600, y=130)

        # Input textbox
        self.text1 = CTkTextbox(noteentry_frame, font=("Roboto", 20), fg_color="white", text_color="black")
        self.text1.place(x=10, y=10, relwidth=0.95, relheight=0.9)

        # Output textbox
        self.text2 = CTkTextbox(noteout_frame, font=("Roboto", 20), fg_color="white", text_color="black")
        self.text2.place(x=10, y=10, relwidth=0.95, relheight=0.9)

        # Buttons
        CTkButton(self, text="Translate", font=("Arial", 20, "bold"), fg_color="#4964E0",
                  command=self._translate).place(x=500, y=500)

        CTkButton(langentry_frame, image=self.mic_img, text="",
                  command=self._start_listening, width=80).place(x=330, y=10)

        CTkButton(langout_frame, image=self.spk_img, text="",
                  command=self._speak, width=80).place(x=330, y=10)

        # Set a timer to auto-clear after 5 minutes
        self.after(300000, self.clear_textboxes_after_time)

        # Bind events
        self.text1.bind("<KeyRelease>", self.check_input_textbox)
        self.text1.bind("<FocusOut>", self.check_input_textbox)

    def clear_textboxes_after_time(self) -> None:
        """Display confirmation message and clear textboxes after 5 minutes."""
        response = CTkMessagebox(
            title="Confirmation",
            message="Do you want to clear the textboxes?",
            icon="question",
            option_1="Yes",
            option_2="No",
            title_color="#2645C4",
            button_color="#2645C4",
            button_hover_color="#1A349F"
        ).get()
        if response == "Yes":
            self.text1.delete("1.0", "end")
            self.text2.delete("1.0", "end")
        self.after(300000, self.clear_textboxes_after_time)

    def check_input_textbox(self, event: Any = None) -> None:
        """Clear output textbox if input textbox is empty."""
        if not self.text1.get("1.0", "end-1c").strip():
            self.text2.delete("1.0", "end")

    def label_change(self) -> None:
        """Update language labels based on selection."""
        self.label_entry.configure(text=self.combo_entry.get().upper())
        self.label_output.configure(text=self.combo_output.get().upper())
        self.after(1000, self.label_change)

    def _translate(self) -> None:
        """Trigger translation via the facade."""
        try:
            text = self.text1.get("1.0", "end-1c")
            if not text.strip():
                return

            result = self.facade.translate(
                text=text,
                source_lang_name=self.combo_entry.get(),
                target_lang_name=self.combo_output.get(),
                use_online=True
            )
            self.text2.delete("1.0", "end")
            self.text2.insert("1.0", result.translated_text)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Translation failed: {str(e)}", icon="cancel")

    def _start_listening(self) -> None:
        """Start the listening thread."""
        threading.Thread(target=self._listen_thread, daemon=True).start()

    def _listen_thread(self) -> None:
        """Thread for speech recognition and translation."""
        try:
            result = self.facade.listen_and_translate(
                source_lang_name=self.combo_entry.get(),
                target_lang_name=self.combo_output.get()
            )
            self.text1.delete("1.0", "end")
            self.text1.insert("1.0", result.original_text)
            self.text2.delete("1.0", "end")
            self.text2.insert("1.0", result.translated_text)
        except sr.UnknownValueError:
            self.after(0, lambda: CTkMessagebox(title="Error", message="No speech detected!", icon="warning"))
        except Exception as e:
            error_msg = str(e)
            self.after(0, lambda: CTkMessagebox(title="Error", message=f"Error: {error_msg}", icon="cancel"))

    def _speak(self) -> None:
        """Trigger TTS via the facade."""
        try:
            text = self.text2.get("1.0", "end-1c")
            if text.strip():
                self.facade.speak(text)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Speech synthesis failed: {str(e)}", icon="cancel")


def main() -> None:
    """Entry point for the application."""
    app = TranslatorApp()
    app.mainloop()

if __name__ == "__main__":
    main()
