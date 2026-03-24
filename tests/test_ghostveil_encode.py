import pytest
from pathlib import Path
from src.ghostveil import encode
import re

img_dir_path = Path(__file__).parent.parent / "img"


def test_encode_raises_on_empty_message():
    with pytest.raises(ValueError, match=re.escape("Please provide the message.")):
        encode("", img_path="test.png", output_path="test_output.png")


def test_encode_raises_on_empty_image_path():
    with pytest.raises(ValueError, match=re.escape("Please provide image path.")):
        encode("Hello, World!", img_path="", output_path="test_output.png")


def test_encode_raises_on_small_image():
    with pytest.raises(
        ValueError,
        match=re.escape(
            "Provided image does NOT contain enough pixels (1px) for header (4px).\nPlease provide bigger image or make message shorter."
        ),
    ):
        encode(
            "Hello, World!",
            img_path=img_dir_path / "1x1.png",
            output_path="test_output.png",
        )


def test_encode_raises_on_message_too_long():
    with pytest.raises(ValueError, match="Message too long"):
        encode(
            "X" * 10000,
            img_path=img_dir_path / "1x1.png",
            output_path="test_output.png",
        )
