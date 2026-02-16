from unittest.mock import patch

from translator_pro.infra.online_translator import OnlineTranslator
from translator_pro.models.translation import TranslationResult


def test_online_translator_translate():
    """Test that OnlineTranslator calls deep_translator correctly."""
    with patch('translator_pro.infra.online_translator.GoogleTranslator') as mock_google:
        mock_instance = mock_google.return_value
        mock_instance.translate.return_value = "Hola"

        translator = OnlineTranslator()
        result = translator.translate("Hello", "en", "es")

        assert isinstance(result, TranslationResult)
        assert result.translated_text == "Hola"
        assert result.engine == "online"
        mock_google.assert_called_once_with(source="en", target="es")
