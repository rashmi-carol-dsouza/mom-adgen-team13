# Variables
POETRY := poetry
PRE_COMMIT := pre-commit
PYTHON := python3
DIR := bff_api

setup:
	sam --version || exit 1
	$(POETRY) shell
	pip install pre-commit
	poetry install
	@make pre-commit-install

install:
	$(POETRY) install

test:
	$(POETRY) run pytest

lint:
	$(POETRY) run pylint ${DIR}/ --rcfile=.pylintrc

start:
	$(POETRY) run python ${DIR}/main.py

init-db:
	$(POETRY) run python db/scripts/init_db/main.py

pre-commit-install:
	$(PRE_COMMIT) install

pre-commit-run:
	$(PRE_COMMIT) run --all-files

.PHONY: install test lint start pre-commit-install pre-commit-run init-db
