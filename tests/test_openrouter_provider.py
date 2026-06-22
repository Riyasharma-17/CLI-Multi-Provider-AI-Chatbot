from providers.openrouter_provider import chat_with_openrouter
from unittest.mock import Mock, patch


def test_chat_with_openrouter_success():

    fake_response = Mock()

    fake_response.choices = [
        Mock(
            message=Mock(
                content="Hello from OpenRouter!"
            )
        )
    ]

    fake_response.usage.prompt_tokens = 20
    fake_response.usage.completion_tokens = 8

    with patch(
        "providers.openrouter_provider.client.chat.completions.create",
        return_value=fake_response
    ):

        bot_reply, input_tokens, output_tokens = (
            chat_with_openrouter([])
        )

        assert bot_reply == "Hello from OpenRouter!"
        assert input_tokens == 20
        assert output_tokens == 8


def test_chat_with_openrouter_exception():

    with patch(
        "providers.openrouter_provider.client.chat.completions.create",
        side_effect=Exception("API down")
    ):

        bot_reply, input_tokens, output_tokens = (
            chat_with_openrouter([])
        )

        assert "OpenRouter Error" in bot_reply
        assert input_tokens == 0
        assert output_tokens == 0