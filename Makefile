.PHONY: install test run validate

install:
	pip install -e ".[dev]"

test:
	pytest

run:
	uvicorn ea_assistant.main:app --reload

validate:
	python scripts/validate_schemas.py
