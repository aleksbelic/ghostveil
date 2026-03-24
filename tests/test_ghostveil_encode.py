from PIL import Image
import pytest
from pathlib import Path
from src.ghostveil import encode, get_output_path
import re


def test_encode_raises_on_empty_message():
    with pytest.raises(ValueError, match=re.escape("Please provide the message.")):
        encode("", img_path="test.png", output_path="test_output.png")


def test_encode_raises_on_empty_image_path():
    with pytest.raises(ValueError, match=re.escape("Please provide image path.")):
        encode("Hello, World!", img_path="", output_path="test_output.png")


def test_encode_raises_on_small_image(tmp_path):
    small_img = Image.new("RGBA", (1, 1), (255, 255, 255, 255))  # 1x1 px
    small_img_path = tmp_path / "1x1.png"
    small_img.save(small_img_path)

    with pytest.raises(
        ValueError,
        match=re.escape(
            "Provided image does NOT contain enough pixels (1px) for header (4px).\nPlease provide bigger image or make message shorter."
        ),
    ):
        encode(
            "Hello, World!",
            img_path=small_img_path,
            output_path=tmp_path / "test_output.png",
        )


def test_encode_raises_on_message_too_long(tmp_path):
    img = Image.new("RGBA", (10, 10), (255, 255, 255, 255))  # 10x10 px
    img_path = tmp_path / "10x10.png"
    img.save(img_path)

    with pytest.raises(ValueError, match="Message too long"):
        encode(
            "X" * 10000,
            img_path=img_path,
            output_path="test_output.png",
        )


def test_get_output_path():
    img_path = Path("some/dir/demo.png")
    assert get_output_path(img_path) == Path("some/dir/demo_ghostveil.png")


def test_encode_raises_on_missing_image():
    with pytest.raises(
        FileNotFoundError, match=re.escape("Image not found: nonexistent.png")
    ):
        encode("Hello, World!", img_path="nonexistent.png")
