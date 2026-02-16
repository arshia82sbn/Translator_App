from deep_translator import GoogleTranslator

from translator_pro.core.translator import TranslatorStrategy
from translator_pro.models.translation import TranslationResult


class OnlineTranslator(TranslatorStrategy):
    """Implementation of translation using Google Translate via deep-translator."""

    def translate(self, text: str, source_lang: str, target_lang: str) -> TranslationResult:
        """Translates text using Google Translate."""
        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        return TranslationResult(
            original_text=text,
            translated_text=translated,
            source_lang=source_lang,
            target_lang=target_lang,
            engine="online"
        )
