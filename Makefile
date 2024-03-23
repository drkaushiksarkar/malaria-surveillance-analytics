.PHONY: install test lint report

install:
	pip install -e ".[dev,viz]"

test:
	pytest tests/ -v --cov=surveillance

lint:
	ruff check surveillance/ tests/

report:
	python -m surveillance.reports.generator --output reports/
