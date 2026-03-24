import pytest
from pathlib import Path
from src.ghostveil import encode, decode
import re

img_dir_path = Path(__file__).parent.parent / "img"


def test_decode_raises_on_empty_image_path():
    with pytest.raises(ValueError, match=re.escape("Please provide image path.")):
        decode(img_path="")


def test_decode_raises_on_small_image():
    with pytest.raises(
        ValueError,
        match=re.escape("Image is too small to contain a valid header."),
    ):
        decode(
            img_path=img_dir_path / "1x1.png",
        )


def test_encode_decode_roundtrip(tmp_path):
    msg = "Memento mori"
    output_path = tmp_path / "test_output.png"
    encode(msg, img_path=img_dir_path / "demo.png", output_path=output_path)
    assert decode(output_path) == msg
