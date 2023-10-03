install:
	poetry install

dev:
	poetry run flask --app page_analyzer:app run

PORT ?= 5000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

lint:
	poetry run flake8 page_analyzer

build:
	poetry build

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=page_analyzer tests/ --cov-report xml

check: test lint

package-install:
	python3 -m pip install dist/*.whl

package-reinstall:
	python3 -m pip install dist/*.whl --force-reinstall

.PHONY: install dev start lint build test test-coverage check package-install package-reinstall