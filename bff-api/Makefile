# Variables
POETRY := poetry
PRE_COMMIT := pre-commit
PYTHON := python3
DIR := bff_api
TERRAFORM := terraform

# Generic dynamic help
help:
	@echo "Choose a command:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


setup: ## Setup the project
	sam --version || exit 1
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
	$(POETRY) run uvicorn bff_api.main:app --reload --port 5000

run: ## Run the server on production
	$(POETRY) run uvicorn bff_api.main:app --port 5000

init-db: ## Initialize the database
	$(POETRY) run python db/scripts/init_db/init.py

pre-commit-install: ## Install pre-commit hooks
	$(PRE_COMMIT) install

pre-commit-run: ## Run pre-commit hooks
	$(PRE_COMMIT) run --all-files

deploy-init: ## Initialize terraform
	cd ./deploy && $(TERRAFORM) init

deploy-plan: ## Plan terraform
	cd ./deploy && $(TERRAFORM) plan

deploy-apply: ## Apply terraform
	cd ./deploy && $(TERRAFORM) apply -auto-approve

deploy-destroy: ## Destory terraform infrastructure
	cd ./deploy && $(TERRAFORM) destroy -auto-approve

.PHONY: help deploy-init deploy-plan deploy-apply

.PHONY: help install test lint start pre-commit-install pre-commit-run init-db
