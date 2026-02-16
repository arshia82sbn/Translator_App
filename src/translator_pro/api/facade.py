from typing import Optional

from translator_pro.core.speech import SpeechService
from translator_pro.core.translator import TranslatorStrategy
from translator_pro.infra.offline_translator import OfflineTranslator
from translator_pro.infra.online_translator import OnlineTranslator
from translator_pro.models.languages import get_language_code
from translator_pro.models.translation import TranslationResult


class TranslatorFacade:
    """Facade class providing a simple API for the Translator application."""

    def __init__(self) -> None:
        """Initializes the facade with default services."""
        self.online_translator = OnlineTranslator()
        # Initialize offline translator lazily to avoid slow startup
        self._offline_translator: Optional[OfflineTranslator] = None
        self.speech_service = SpeechService()

    @property
    def offline_translator(self) -> OfflineTranslator:
        """Lazily initializes and returns the offline translator."""
        if self._offline_translator is None:
            self._offline_translator = OfflineTranslator()
        return self._offline_translator

    def translate(
        self, text: str, source_lang_name: str, target_lang_name: str, use_online: bool = True
    ) -> TranslationResult:
        """Translates text between languages.

        Args:
            text: The text to translate.
            source_lang_name: The full name of the source language.
            target_lang_name: The full name of the target language.
            use_online: Whether to use the online engine.

        Returns:
            A TranslationResult object.
        """
        src_code = get_language_code(source_lang_name)
        tgt_code = get_language_code(target_lang_name)

        strategy: TranslatorStrategy = self.online_translator if use_online else self.offline_translator
        return strategy.translate(text, src_code, tgt_code)

    def listen_and_translate(self, source_lang_name: str, target_lang_name: str) -> TranslationResult:
        """Listens to speech and translates it using the offline engine.

        Args:
            source_lang_name: The name of the source language.
            target_lang_name: The name of the target language.

        Returns:
            The translation result.
        """
        src_code = get_language_code(source_lang_name)
        text = self.speech_service.listen(src_code)
        return self.translate(text, source_lang_name, target_lang_name, use_online=False)

    def speak(self, text: str) -> None:
        """Speaks the provided text.

        Args:
            text: The text to speak.
        """
        self.speech_service.speak(text)
