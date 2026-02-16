
import pyttsx3
import speech_recognition as sr


class SpeechService:
    """Service for speech recognition and text-to-speech."""

    def __init__(self) -> None:
        """Initializes the speech engines."""
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def listen(self, language_code: str, timeout: int = 5) -> str:
        """Listens for speech and converts it to text.

        Args:
            language_code: The language code to recognize.
            timeout: Maximum time to wait for speech.

        Returns:
            The recognized text.

        Raises:
            sr.UnknownValueError: If speech was not understood.
            sr.RequestError: If there was an error with the recognition service.
        """
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source, timeout=timeout)
            return str(self.recognizer.recognize_google(audio, language=language_code))

    def speak(self, text: str) -> None:
        """Converts text to speech.

        Args:
            text: The text to speak.
        """
        self.engine.say(text)
        self.engine.runAndWait()
