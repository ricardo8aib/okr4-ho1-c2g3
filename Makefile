# A Self-Documenting Makefile: http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
SHELL = /bin/bash
OS = $(shell uname | tr A-Z a-z)
include extraction/.env
$(eval export $(shell sed -ne 's/ *#.*$$//; /./ s/=.*$$// p' extraction/.env))

.PHONY: format
format: ## Formats code
	poetry run black .
	poetry run isort .

.PHONY: create-infrastructure
create-infrastructure: ## Create infrastructure
	(cd infrastructure/; terraform init; terraform apply -auto-approve)

.PHONY: destroy-infrastructure
destroy-infrastructure: ## Destroy infrastructure
	(cd infrastructure/; terraform destroy -auto-approve)

.PHONY: extract-data
extract-data: ## Extract data
	poetry run python extraction/extraction.py