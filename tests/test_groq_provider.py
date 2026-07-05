from providers.groq_provider import chat_with_groq
from unittest.mock import Mock, patch


def test_chat_with_groq_success():

    fake_response = Mock()

    fake_response.choices = [
        Mock(
            message=Mock(
                content="Hello!"
            )
        )
    ]

    fake_response.usage.prompt_tokens = 10
    fake_response.usage.completion_tokens = 5

    with patch(
        "providers.groq_provider.client.chat.completions.create",
        return_value=fake_response
    ):

        bot_reply, input_tokens, output_tokens = (
    chat_with_groq([], 0.7)
)

        assert bot_reply == "Hello!"
        assert input_tokens == 10
        assert output_tokens == 5


def test_chat_with_groq_exception():

    with patch(
        "providers.groq_provider.client.chat.completions.create",
        side_effect=Exception("API down")
    ):

        bot_reply, input_tokens, output_tokens = (
            chat_with_groq([], 0.7)
        )

        assert "Groq Error" in bot_reply
        assert input_tokens == 0
        assert output_tokens == 0