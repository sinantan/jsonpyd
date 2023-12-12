.PHONY: test format lint clean

test:
	poetry run pytest tests/test.py

format:
	poetry run black src/jsonpyd tests/

lint:
	poetry run flake8 src/jsonpyd tests/

clean:
	poetry run rm -rf dist/ build/ *.egg-info/
	poetry run find . -type f

bump:
	poetry version patch

build:
	poetry build

publish:
	poetry publish --build

