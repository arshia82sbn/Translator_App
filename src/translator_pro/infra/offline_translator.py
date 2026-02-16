from transformers import pipeline
from translator_pro.core.translator import TranslatorStrategy
from translator_pro.models.translation import TranslationResult
from typing import Any

class OfflineTranslator(TranslatorStrategy):
    """Implementation of translation using Hugging Face Transformers."""

    def __init__(self, model_name: str = "Helsinki-NLP/opus-mt-mul-en"):
        """Initializes the offline translator with a specific model.

        Args:
            model_name: The Hugging Face model ID.
        """
        # Note: pipeline loading can be slow and should be handled carefully in a real app
        self._pipeline = pipeline("translation", model=model_name)

    def translate(self, text: str, source_lang: str, target_lang: str) -> TranslationResult:
        """Translates text using the offline model."""
        # The Helsinki-NLP model usually expects specific format or handles it via kwargs
        # Original code used: self.offline_translator(text, src_lang=src_lang, tgt_lang=tgt_lang)
        result = self._pipeline(text, src_lang=source_lang, tgt_lang=target_lang)
        translated_text = str(result[0]['translation_text'])

        return TranslationResult(
            original_text=text,
            translated_text=translated_text,
            source_lang=source_lang,
            target_lang=target_lang,
            engine="offline"
        )
