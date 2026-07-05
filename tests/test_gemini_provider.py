from providers.gemini_provider import chat_with_gemini
from unittest.mock import Mock, patch


def test_chat_with_gemini_success():

    fake_response = Mock()

    fake_response.text = (
        "Hello from Gemini!"
    )

    with patch(
        "providers.gemini_provider.gemini_model.generate_content",
        return_value=fake_response
    ):

        bot_reply, input_tokens, output_tokens = (
            chat_with_gemini([], 0.7)
        )

        assert bot_reply == "Hello from Gemini!"
        assert input_tokens == 0
        assert output_tokens == 0


def test_chat_with_gemini_exception():

    with patch(
        "providers.gemini_provider.gemini_model.generate_content",
        side_effect=Exception("Quota exceeded")
    ):

        bot_reply, input_tokens, output_tokens = (
            chat_with_gemini([], 0.7)
        )

        assert "Gemini Error" in bot_reply
        assert input_tokens == 0
        assert output_tokens == 0