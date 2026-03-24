import argparse
from PIL import Image
from pathlib import Path
from math import ceil
from typing import TypeAlias

Pixel: TypeAlias = tuple[int, int, int, int]

HEADER_LENGTH_IN_PX: int = 4
CHANNEL_COUNT: int = 3


def get_output_path(img_path: Path) -> Path:
    return img_path.with_stem(img_path.stem + "_ghostveil")


def encode(
    msg: str, img_path: str | Path, output_path: str | Path | None = None
) -> None:
    if not msg:
        raise ValueError("Please provide the message.")

    if not img_path:
        raise ValueError("Please provide image path.")

    img_path = Path(img_path)

    if not img_path.exists():
        raise FileNotFoundError(f"Image not found: {img_path}")

    if output_path is None:
        output_path = get_output_path(img_path)
    else:
        output_path = Path(output_path)

    msg_bit_string: str = "".join(format(ord(char), "08b") for char in msg)

    max_msg_length_bit: int = 2 ** (HEADER_LENGTH_IN_PX * CHANNEL_COUNT) - 1
    max_msg_length: int = max_msg_length_bit // 8

    if len(msg_bit_string) > max_msg_length_bit:
        raise ValueError(
            f"Message too long ({len(msg_bit_string)}b). Max is {max_msg_length_bit}b ({max_msg_length} characters)."
        )

    header_bit_string: str = format(
        # set message length in header
        len(msg_bit_string),
        f"0{HEADER_LENGTH_IN_PX * CHANNEL_COUNT}b",
    )

    payload_bit_string: str = header_bit_string + msg_bit_string

    img: Image.Image = Image.open(img_path).convert(
        "RGBA"
    )  # ensure 4 channels (R, G, B, A)
    img_pixels: list[Pixel] = list(img.get_flattened_data())

    if HEADER_LENGTH_IN_PX > len(img_pixels):
        raise ValueError(
            f"Provided image does NOT contain enough pixels ({len(img_pixels)}px) for header ({HEADER_LENGTH_IN_PX}px).\nPlease provide bigger image or make message shorter."
        )

    if len(payload_bit_string) > len(img_pixels) * CHANNEL_COUNT:
        raise ValueError(
            f"Provided image does NOT contain enough pixels ({len(img_pixels)}px) for your message ({len(msg_bit_string)}b).\nYour message needs at least {HEADER_LENGTH_IN_PX + ceil(len(msg_bit_string) / CHANNEL_COUNT)}px.\nPlease provide bigger image or make your message shorter."
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


def decode(img_path: str | Path) -> str:
    if not img_path:
        raise ValueError("Please provide image path.")

    img_path = Path(img_path)

    if not img_path.exists():
        raise FileNotFoundError(f"Image not found: {img_path}")

    img: Image.Image = Image.open(img_path).convert("RGBA")
    img_pixels: list[Pixel] = list(img.get_flattened_data())

    if len(img_pixels) < HEADER_LENGTH_IN_PX:
        raise ValueError("Image is too small to contain a valid header.")

    # read header bits (first 4 px, RGB only)
    header_bits: str = ""
    for img_pixel in img_pixels[:HEADER_LENGTH_IN_PX]:
        red, green, blue, _ = img_pixel
        header_bits += str(red & 1)
        header_bits += str(green & 1)
        header_bits += str(blue & 1)

    msg_bit_length: int = int(header_bits, 2)

    msg_bits: str = ""
    bits_read: int = 0
    for img_pixel in img_pixels[HEADER_LENGTH_IN_PX:]:
        if bits_read >= msg_bit_length:
            break
        red, green, blue, _ = img_pixel
        for channel_value in (red, green, blue):
            if bits_read >= msg_bit_length:
                break
            msg_bits += str(channel_value & 1)
            bits_read += 1

    msg: str = "".join(
        chr(int(msg_bits[i : i + 8], 2)) for i in range(0, len(msg_bits), 8)
    )

    return msg


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="GhostVeil - Python steganography tool."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    encode_parser = subparsers.add_parser(
        "encode", help="Encode a message into an image"
    )
    encode_parser.add_argument("msg", help="Message to encode")
    encode_parser.add_argument("img_path", help="Path to input image")
    encode_parser.add_argument(
        "output_path", nargs="?", help="Path to output image (optional)"
    )

    decode_parser = subparsers.add_parser(
        "decode", help="Decode a message from an image"
    )
    decode_parser.add_argument("img_path", help="Path to encoded image")

    args = parser.parse_args()

    if args.command == "encode":
        img_path = Path(args.img_path)
        output_path = (
            Path(args.output_path) if args.output_path else get_output_path(img_path)
        )
        encode(args.msg, img_path, output_path)
        if args.verbose:
            print(f"Encoding complete! 👻\nOutput: {output_path}")
    elif args.command == "decode":
        msg = decode(args.img_path)
        if args.verbose:
            print(f"Decoding complete! 👻\nDecoded message: {msg}")
        else:
            print(msg)
