from utils.json_utils import display_response


def test_normal_response(capsys):

    display_response(
        "Hello World",
        json_mode=False
    )

    captured = capsys.readouterr()

    assert "Bot: Hello World" in captured.out


def test_valid_json(capsys):

    display_response(
        '{"topic":"Python","summary":"Language"}',
        json_mode=True
    )

    captured = capsys.readouterr()

    assert '"topic": "Python"' in captured.out


def test_invalid_json(capsys):

    display_response(
        '{"topic":"Python"',
        json_mode=True
    )

    captured = capsys.readouterr()

    assert "Invalid JSON received!" in captured.out