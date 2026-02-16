import googletrans
from typing import Dict

# Provide a clean interface to languages
LANGUAGES: Dict[str, str] = googletrans.LANGUAGES

def get_language_name(code: str) -> str:
    """Get the full name of a language from its code."""
    return LANGUAGES.get(code, code).capitalize()

def get_language_code(name: str) -> str:
    """Get the language code from its full name."""
    name_lower = name.lower()
    for code, lang_name in LANGUAGES.items():
        if lang_name == name_lower:
            return str(code)
    raise ValueError(f"Language '{name}' not found.")
