from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class TranslationResult:
    """Data class representing the result of a translation.

    Attributes:
        original_text: The source text.
        translated_text: The translated text.
        source_lang: The source language code.
        target_lang: The target language code.
        engine: The engine used for translation (online/offline).
    """
    original_text: str
    translated_text: str
    source_lang: str
    target_lang: str
    engine: str
