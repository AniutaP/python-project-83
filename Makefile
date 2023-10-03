install:
	poetry install

dev:
	poetry run flask --app page_analyzer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

lint:
	poetry run flake8 page_analyzer

build:
	poetry build

package-install:
	poetry -m pip3 install --user dist/*.whl

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov

check: test lint

.PHONY: install dev start lint build package-install test test-coverage check