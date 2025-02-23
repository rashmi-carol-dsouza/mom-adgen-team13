# Variables
POETRY := poetry

# Generic dynamic help
help:
	@echo "Choose a command:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


setup: ## Setup the project
	$(POETRY) shell
	$(POETRY) install

init-db: ## Initialize the database
	$(POETRY) run python scripts/init_db/init.py

.PHONY: help init-db
