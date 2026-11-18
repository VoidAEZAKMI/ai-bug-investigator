.PHONY: install test lint format run

install:
	poetry install
test:
	poetry run pytest
lint:
	poetry run ruff check .
format:
	poetry run ruff format .

run:
	poetry run uvicorn ai_bug_investigator.api.main:app --reload --port 8000
	