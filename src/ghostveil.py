from PIL import Image
from pathlib import Path
from math import ceil


def encode(msg: str, img_path: str | Path, output_path: str | Path):
    if not msg:
        raise ValueError("Please provide the message.")

    img_path = Path(img_path)
    output_path = Path(output_path)

    msg_bit_string = "".join(format(ord(char), "08b") for char in msg)
    header_length_in_px = 4
    channel_count = 3

    max_msg_length_bit = 2 ** (header_length_in_px * channel_count) - 1
    max_msg_length = max_msg_length_bit // 8

    if len(msg_bit_string) > max_msg_length_bit:
        raise ValueError(
            f"Message too long ({len(msg_bit_string)}b). Max is {max_msg_length_bit}b ({max_msg_length} characters)."
        )

    header_bit_string = format(
        # set message length in header
        len(msg_bit_string),
        f"0{header_length_in_px * channel_count}b",
    )

    payload_bit_string = header_bit_string + msg_bit_string
    payload_bit_string_length = len(payload_bit_string)

    img = Image.open(img_path).convert("RGBA")  # ensure 4 channels (R, G, B, A)
    img_pixels = list(img.get_flattened_data())

    if header_length_in_px > len(img_pixels):
        raise ValueError(
            f"Provided image does NOT contain enough pixels ({len(img_pixels)}px) for header ({header_length_in_px}px).\nPlease provide bigger image or make message shorter."
        )

    if len(payload_bit_string) > len(img_pixels) * channel_count:
        raise ValueError(
            f"Provided image does NOT contain enough pixels ({len(img_pixels)}px) for your message ({len(msg_bit_string)}b).\nYour message needs at least {header_length_in_px + ceil(len(msg_bit_string) / channel_count)}px.\nPlease provide bigger image or make your message shorter."
        )

    output_pixels = []
    payload_bit_string_index = 0
    for i, img_pixel in enumerate(img_pixels):
        if payload_bit_string_index >= payload_bit_string_length:
            output_pixels.extend(img_pixels[i:])  # append remaining pixels unchanged
            break

        red, green, blue, alpha = img_pixel

        red = (red & 0b11111110) | int(payload_bit_string[payload_bit_string_index])
        payload_bit_string_index += 1

        if payload_bit_string_index < payload_bit_string_length:
            green = (green & 0b11111110) | int(
                payload_bit_string[payload_bit_string_index]
            )
            payload_bit_string_index += 1

        if payload_bit_string_index < payload_bit_string_length:
            blue = (blue & 0b11111110) | int(
                payload_bit_string[payload_bit_string_index]
            )
            payload_bit_string_index += 1

        output_pixels.append((red, green, blue, alpha))

    output = img.copy()
    output.putdata(output_pixels)
    output.save(output_path)

    print(f"Encoding complete! 👻\nOutput: {output_path}")
