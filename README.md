# GhostVeil

Python [steganography](https://en.wikipedia.org/wiki/Steganography) tool for injecting a secret message into custom image.

<p align="center">
    <img src="./img/cover.png">
</p>

## Requirements

- Python 3.10+

## How it works

GhostVeil uses [LSB (Least Significant Bit)](https://en.wikipedia.org/wiki/Bit_numbering#Least_significant_bit) steganography to hide a message inside an image without any visible changes to the image.

### Encoding

Each pixel in a PNG image is made of 4 channels: **R**ed, **G**reen, **B**lue, and **A**lpha. Each channel is stored as a number from 0 to 255.

GhostVeil replaces the least significant bit of the R, G, and B channels of each pixel with a bit from the secret message. Changing only the last bit shifts the color value by at most 1, which is completely invisible to the human eye.

Before the message itself, GhostVeil writes a **header** into the first 4 pixels (12 bits) that stores the length of the message in bits. This allows the decoder to know exactly how many bits to read.
```
Pixel 1-4:   [ header  ] — stores message length (12 bits)
Pixel 5+:    [ message ] — stores message bits (3 bits per pixel)
```

### Decoding

GhostVeil reads the least significant bit of the R, G, and B channels of each pixel. It first reads the header from the first 4 pixels to determine the message length, then reads exactly that many bits from the remaining pixels and converts them back to text.

### Limits

- Maximum message length: **511 characters**
- Minimum image size: **5 pixels** (4 header + at least 1 message pixel)
- Only **lossless** image formats are supported (e.g. `PNG`)

## Install dependencies

Please check [requirements.txt](./requirements.txt) & [requirements-dev.txt](./requirements-dev.txt) for exact versions.

Runtime dependencies:
- [pillow](https://github.com/python-pillow/Pillow)

```bash
pip install -r requirements.txt
```

Dev tools:
- [ruff](https://github.com/astral-sh/ruff)
- [codespell](https://github.com/codespell-project/codespell)
- [pytest](https://github.com/pytest-dev/pytest)

```bash
pip install -r requirements-dev.txt
```

## Usage

⚠️ Only **lossless** image formats are supported (e.g. `PNG`). Lossy formats like `JPEG` will corrupt the hidden message.

### Usage in console

⚠️ `Encode` & `decode` functions are non-verbose by default to make piping possible.

Encode message into image:
```bash
python3 ghostveil.py encode "Memento mori" demo.png demo_output.png
```

ℹ️ Output image path is `optional` and by default will be generated in the same directory as input image with `_ghostveil` suffix:
```bash
python3 ghostveil.py encode "Memento mori" demo.png
# Output: demo_ghostveil.png
```

Decode message from image:
```bash
python3 ghostveil.py decode demo_output.png
```

Using in pipeline:
```bash
python3 ghostveil.py decode demo_output.png > secret_message.txt
```

To make process verbose, please use flag `-v` or `--verbose`.

Verbose encoding into message:
```bash
python3 ghostveil.py -v encode "Memento mori" demo.png demo_output.png
# Encoding complete! 👻
# Output: demo_output.png
```

Verbose decode message from image:
```bash
python3 ghostveil.py -v decode demo_output.png
# Decoding complete! 👻
# Decoded message: Memento mori
```

More info:
```bash
python3 ghostveil.py -h
python3 ghostveil.py encode -h
python3 ghostveil.py decode -h
```

### Usage in Python script

```python
from ghostveil import encode, decode

# Encode message into image
encode("Memento mori", img_path="demo.png", output_path="demo_output.png")

# Decode message from image
message = decode("demo_output.png")
print(message)  # Memento mori
```

ℹ️ Output image path is `optional` and by default will be generated in the same directory as input image with `_ghostveil` suffix:
```python
encode("Memento mori", img_path="demo.png")
message = decode("demo_ghostveil.png")
print(message)  # Memento mori
```

## DEV Scripts

Typo check:
```bash
codespell .
```

Lint check:
```bash
ruff check .
```

Lint check with fix:
```bash
ruff check . --fix
```

Format code:
```bash
ruff format .
```

Run unit tests:
```bash
pytest
```

Run all scripts (lint check with fix & format & tests - requires `make` installed on your system):
```bash
make all
```
