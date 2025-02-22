# Variables
TERRAFORM := terraform

# Generic dynamic help
help:
	@echo "Choose a command:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


deployer-iam-init: ## Initialize terraform
	cd ./deployer-iam && $(TERRAFORM) init

deployer-iam-plan: ## Plan terraform
	cd ./deployer-iam && $(TERRAFORM) plan

deployer-iam-apply: ## Apply terraform
	cd ./deployer-iam && $(TERRAFORM) apply

.PHONY: help tf-init tf-plan tf-apply
