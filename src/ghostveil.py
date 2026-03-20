from PIL import Image
from pathlib import Path
from math import ceil

src_dir_path = Path(__file__).parent
root_dir_path = src_dir_path.parent
img_dir_path = root_dir_path / "img"
img_path = img_dir_path / "test-original.png"
output_path = img_dir_path / "test-secret.png"

message = "2"
message_bit_string = ''.join(format(ord(char), '08b') for char in message)
message_bit_string_length = len(message_bit_string)

header_length_in_px = 4
channel_count = 3

header_bit_string = format(message_bit_string_length, f'0{header_length_in_px * channel_count}b') # set message length in header
header_bit_string_length = len(header_bit_string)

max_message_length_bit = 2 ** (header_length_in_px * channel_count) - 1 # don't count zero
max_message_length = max_message_length_bit // 8

payload = header_bit_string + message_bit_string

image = Image.open(img_path).convert('RGBA') # convert to PNG because it is lossless
pixels = list(image.get_flattened_data())

if message_bit_string_length > max_message_length_bit: 
    raise ValueError(f"Message too long ({message_bit_string_length}b). Max is {max_message_length_bit}b ({max_message_length} characters).")

if header_length_in_px > len(pixels):
    raise ValueError(f"Provided image does NOT contain enough pixels ({len(pixels)}px) for header ({header_length_in_px}px).\nPlease provide bigger image or make message shorter.")

if len(payload) > len(pixels) * 3: # R, G, B
    raise ValueError(f"\nProvided image does NOT contain enough pixels ({len(pixels)}px) for your message ({message_bit_string_length}b).\nYour message needs at least {header_length_in_px + ceil(message_bit_string_length / channel_count)}px.\nPlease provide bigger image or make your message shorter.")

new_pixels = []
message_bit_index = 0
for pixel_index, pixel in enumerate(pixels):
    r, g, b, a = pixel[0], pixel[1], pixel[2], pixel[3]
    if message_bit_index < message_bit_string_length:
        r = (r & 0b11111110) | int(message_bit_string[message_bit_index])
        message_bit_index += 1
    if message_bit_index < message_bit_string_length:
        g = (g & 0b11111110) | int(message_bit_string[message_bit_index])
        message_bit_index += 1
    if message_bit_index < message_bit_string_length:
        b = (b & 0b11111110) | int(message_bit_string[message_bit_index])
        message_bit_index += 1
    new_pixels.append((r, g, b, a))

new_image = image.copy()
new_image.putdata(new_pixels)
new_image.save(output_path)

print(f"Process complete!\nOutput: {output_path}")
