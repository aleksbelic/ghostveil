lint-fix:
	ruff check . --fix

format:
	ruff format .

test:
	pytest

all: lint-fix format test