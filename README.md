# GhostVeil

Python tool for injecting secret message into custom image (more on [steganography](https://en.wikipedia.org/wiki/Steganography)).

<p align="center">
    <img src="./img/cover.png">
</p>

## Usage

Console:
```bash
python ghostveil.py "Memento mori" demo.png demo_output.png
```

More info:
```bash
python ghostveil.py -h
```

## Scripts

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

Run all scripts (lint check with fix & format & tests):
```bash
make all
```

## Dependencies

Please check [requirements.txt](./requirements.txt) for exact versions.
- [pillow](https://github.com/python-pillow/Pillow)
- [ruff](https://github.com/astral-sh/ruff)
- [codespell](https://github.com/codespell-project/codespell)
- [pytest](https://github.com/pytest-dev/pytest)