import argparse
from PIL import Image
from pathlib import Path
from math import ceil
from typing import TypeAlias

Pixel: TypeAlias = tuple[int, int, int, int]


def encode(msg: str, img_path: str | Path, output_path: str | Path) -> None:
    if not msg:
        raise ValueError("Please provide the message.")

    img_path = Path(img_path)
    output_path = Path(output_path)

    msg_bit_string: str = "".join(format(ord(char), "08b") for char in msg)
    header_length_in_px: int = 4
    channel_count: int = 3

    max_msg_length_bit: int = 2 ** (header_length_in_px * channel_count) - 1
    max_msg_length: int = max_msg_length_bit // 8

    if len(msg_bit_string) > max_msg_length_bit:
        raise ValueError(
            f"Message too long ({len(msg_bit_string)}b). Max is {max_msg_length_bit}b ({max_msg_length} characters)."
        )

    header_bit_string: str = format(
        # set message length in header
        len(msg_bit_string),
        f"0{header_length_in_px * channel_count}b",
    )

    payload_bit_string: str = header_bit_string + msg_bit_string

    img: Image.Image = Image.open(img_path).convert(
        "RGBA"
    )  # ensure 4 channels (R, G, B, A)
    img_pixels: list[Pixel] = list(img.get_flattened_data())

    if header_length_in_px > len(img_pixels):
        raise ValueError(
            f"Provided image does NOT contain enough pixels ({len(img_pixels)}px) for header ({header_length_in_px}px).\nPlease provide bigger image or make message shorter."
        )

    if len(payload_bit_string) > len(img_pixels) * channel_count:
        raise ValueError(
            f"Provided image does NOT contain enough pixels ({len(img_pixels)}px) for your message ({len(msg_bit_string)}b).\nYour message needs at least {header_length_in_px + ceil(len(msg_bit_string) / channel_count)}px.\nPlease provide bigger image or make your message shorter."
        )

    output_pixels: list[Pixel] = []
    payload_bit_string_index: int = 0
    for i, img_pixel in enumerate(img_pixels):
        if payload_bit_string_index >= len(payload_bit_string):
            output_pixels.extend(img_pixels[i:])  # append remaining pixels unchanged
            break

        red, green, blue, alpha = img_pixel

        red = (red & 0b11111110) | int(payload_bit_string[payload_bit_string_index])
        payload_bit_string_index += 1

        if payload_bit_string_index < len(payload_bit_string):
            green = (green & 0b11111110) | int(
                payload_bit_string[payload_bit_string_index]
            )
            payload_bit_string_index += 1

        if payload_bit_string_index < len(payload_bit_string):
            blue = (blue & 0b11111110) | int(
                payload_bit_string[payload_bit_string_index]
            )
            payload_bit_string_index += 1

        output_pixels.append((red, green, blue, alpha))

    output: Image.Image = img.copy()
    output.putdata(output_pixels)
    output.save(output_path)

    print(f"Encoding complete! 👻\nOutput: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="GhostVeil - python steganography tool."
    )
    parser.add_argument("msg", help="Message to encode")
    parser.add_argument("img_path", help="Path to input image")
    parser.add_argument("output_path", help="Path to output image")
    args = parser.parse_args()

    encode(args.msg, args.img_path, args.output_path)
