from abc import ABC, abstractmethod

from translator_pro.models.translation import TranslationResult


class TranslatorStrategy(ABC):
    """Abstract base class for translation strategies."""

    @abstractmethod
    def translate(self, text: str, source_lang: str, target_lang: str) -> TranslationResult:
        """Translates text from source language to target language.

        Args:
            text: The text to translate.
            source_lang: The source language code.
            target_lang: The target language code.

        Returns:
            A TranslationResult object.
        """
        pass
