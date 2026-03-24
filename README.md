# GhostVeil

Python [steganography](https://en.wikipedia.org/wiki/Steganography) tool for injecting a secret message into custom image.

<p align="center">
    <img src="./img/demo.png">
</p>

## Requirements

- Python 3.10+

## Install dependencies

Please check [requirements.txt](./requirements.txt) & [requirements-dev.txt](./requirements-dev.txt) for exact versions.

- Runtime:
    - [pillow](https://github.com/python-pillow/Pillow)

- Dev:
    - [ruff](https://github.com/astral-sh/ruff)
    - [codespell](https://github.com/codespell-project/codespell)
    - [pytest](https://github.com/pytest-dev/pytest)

```bash
pip install -r requirements.txt       # runtime dependencies
pip install -r requirements-dev.txt   # dev tools
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
# Output: ./demo_ghostveil.png
```

Decode message from image:
```bash
python3 ghostveil.py decode demo_output.png
```

To make process verbose, please use flag `-v` or `--verbose`.

Verbose encoding into message:
```bash
python3 ghostveil.py -v encode "Memento mori" demo.png demo_output.png
# Encoding complete! 👻
# Output: ./img/demo_output.png
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
