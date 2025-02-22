# Variables
POETRY := poetry
PRE_COMMIT := pre-commit
PYTHON := python3
DIR := bff_api

# Generic dynamic help
help:
	@echo "Choose a command:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

setup: ## Setup the project
	$(POETRY) shell
	pip install pre-commit
	poetry install
	@make pre-commit-install

install: ## Install dependencies
	$(POETRY) install

test: ## Run tests
	$(POETRY) run pytest

lint: ## Run linter
	$(POETRY) run pylint ${DIR}/ --rcfile=.pylintrc

start: ## Start the server
	$(POETRY) run python ${DIR}/main.py

init-db: ## Initialize the database
	$(POETRY) run python db/scripts/init_db/main.py

pre-commit-install: ## Install pre-commit hooks
	$(PRE_COMMIT) install

pre-commit-run: ## Run pre-commit hooks
	$(PRE_COMMIT) run --all-files

.PHONY: help install test lint start pre-commit-install pre-commit-run init-db
