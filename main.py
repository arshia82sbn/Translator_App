from customtkinter import *
from CTkMessagebox import CTkMessagebox
from deep_translator import GoogleTranslator
from transformers import pipeline
from PIL import Image
import speech_recognition as sr
import pyttsx3
import threading
import googletrans
import os

# Initial settings
set_appearance_mode("dark")
set_default_color_theme("blue")


class TranslatorApp(CTk):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.languages = googletrans.LANGUAGES
        self.languageV = list(self.languages.values())
        self.title("Translator Pro")
        self.geometry("1080x550")
        self._setup_ui()
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.offline_translator = pipeline("translation", model="Helsinki-NLP/opus-mt-mul-en")
        self.label_change()

    def _setup_ui(self):
        # Load images
        self.sp_image_for_button = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), "speaker.png")))
        self.google_button = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), "google.png")))
        self.image_arrow = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), "arrow.png")), size=(100, 100))
        self.mic_img = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), "micro.png")), size=(50, 50))
        self.spk_img = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), "speaker 2.png")), size=(50, 50))

        # Input language selection frame
        langentry_frame = CTkFrame(self, fg_color="#777777", corner_radius=20, width=450, height=100)
        langentry_frame.place(x=30, y=10)

        self.combo_entry = CTkComboBox(langentry_frame, values=self.languageV, font=("Roboto", 14))
        self.combo_entry.place(x=10, y=10)
        self.combo_entry.set("english")

        self.label_entry = CTkLabel(langentry_frame, text="ENGLISH", font=("Segoe UI", 30, "bold"), fg_color="blue")
        self.label_entry.place(x=10, y=50)

        # Output language selection frame
        langout_frame = CTkFrame(self, fg_color="#777777", corner_radius=20, width=450, height=100)
        langout_frame.place(x=600, y=10)

        self.combo_output = CTkComboBox(langout_frame, values=self.languageV, font=("Roboto", 14))
        self.combo_output.place(x=10, y=10)
        self.combo_output.set("persian")

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
        CTkButton(langentry_frame, image=self.mic_img, text="", command=self._start_listening,width=80).place(x=330, y=10)
        CTkButton(langout_frame, image=self.spk_img, text="", command=self._speak,width=80).place(x=330, y=10)

        # Set a timer to auto-clear after 5 minutes (300,000 milliseconds)
        self.after(300000, self.clear_textboxes_after_time)

        # Bind events to input textbox to check its content
        self.text1.bind("<KeyRelease>", self.check_input_textbox)
        self.text1.bind("<FocusOut>", self.check_input_textbox)

    def clear_textboxes_after_time(self):
        """Display confirmation message and clear textboxes after 5 minutes"""
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
        if response == "yes":
            self.text1.delete("1.0", "end")
            self.text2.delete("1.0", "end")
        # Reset the timer for another 5 minutes
        self.after(300000, self.clear_textboxes_after_time)

    def check_input_textbox(self, event=None):
        """Clear output textbox if input textbox is empty"""
        if not self.text1.get("1.0", "end-1c").strip():
            self.text2.delete("1.0", "end")

    def _start_listening(self):
        threading.Thread(target=self._listen_thread).start()

    # Method to update labels
    def label_change(self):
        c = self.combo_entry.get()
        c1 = self.combo_output.get()
        self.label_entry.configure(text=c.upper())
        self.label_output.configure(text=c1.upper())
        self.after(1000, self.label_change)

    def _get_lang_code(self, lang_name):
        return [k for k, v in self.languages.items() if v == lang_name][0]

    def _translate(self, use_online=True):
        try:
            text = self.text1.get("1.0", "end-1c")
            src_lang = self._get_lang_code(self.combo_entry.get())
            tgt_lang = self._get_lang_code(self.combo_output.get())

            if use_online:
                translated = GoogleTranslator(source=src_lang, target=tgt_lang).translate(text)
            else:
                translated = self.offline_translator(text, src_lang=src_lang, tgt_lang=tgt_lang)[0]['translation_text']

            self.text2.delete("1.0", "end")
            self.text2.insert("1.0", translated)

        except Exception as e:
            CTkMessagebox(title="Error", message=f"Translation failed: {str(e)}", icon="cancel")

    def _listen_thread(self):
        try:
            src_lang_code = self._get_lang_code(self.combo_entry.get())
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio, language=src_lang_code)
                self.text1.delete("1.0", "end")
                self.text1.insert("1.0", text)
                self._translate(use_online=False)  # Use offline model

        except sr.UnknownValueError:
            CTkMessagebox(title="Error", message="No speech detected!", icon="warning")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error: {str(e)}", icon="cancel")

    def _speak(self):
        try:
            text = self.text2.get("1.0", "end-1c")
            print(f"Text to speak: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Speech synthesis failed: {str(e)}", icon="cancel")


if __name__ == "__main__":
    app = TranslatorApp()
    app.mainloop()
