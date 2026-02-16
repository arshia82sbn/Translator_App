from unittest.mock import patch

from translator_pro.api.facade import TranslatorFacade
from translator_pro.models.translation import TranslationResult


@patch('translator_pro.api.facade.OnlineTranslator')
@patch('translator_pro.api.facade.SpeechService')
def test_facade_translate(mock_speech, mock_online):
    """Test that the facade correctly delegates translation calls."""
    mock_online_instance = mock_online.return_value
    mock_online_instance.translate.return_value = TranslationResult(
        original_text="Hello",
        translated_text="Bonjour",
        source_lang="en",
        target_lang="fr",
        engine="online"
    )

    facade = TranslatorFacade()
    result = facade.translate("Hello", "English", "French", use_online=True)

    assert result.translated_text == "Bonjour"
    mock_online_instance.translate.assert_called_once_with("Hello", "en", "fr")

@patch('translator_pro.api.facade.OfflineTranslator')
@patch('translator_pro.api.facade.SpeechService')
def test_facade_listen_and_translate(mock_speech, mock_offline):
    """Test the listen and translate flow in the facade."""
    mock_speech_instance = mock_speech.return_value
    mock_speech_instance.listen.return_value = "Hello"

    # Mocking the property access is a bit tricky, let's mock the whole class and then the attribute
    facade = TranslatorFacade()
    facade._offline_translator = mock_offline.return_value
    facade._offline_translator.translate.return_value = TranslationResult(
        original_text="Hello",
        translated_text="Bonjour",
        source_lang="en",
        target_lang="fr",
        engine="offline"
    )

    result = facade.listen_and_translate("English", "French")

    assert result.original_text == "Hello"
    assert result.translated_text == "Bonjour"
    mock_speech_instance.listen.assert_called_once_with("en")
