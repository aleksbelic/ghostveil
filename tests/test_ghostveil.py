import pytest
from src.ghostveil import encode


def test_encode_raises_on_empty_message():
    with pytest.raises(ValueError, match="Please provide the message."):
        encode("", img_path="any.png", output_path="any.png")
