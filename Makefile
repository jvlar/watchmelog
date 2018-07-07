default:
	@echo 'o/'

bootstrap:  ## Install required system packages for this project
	pip install --user -U poetry awscli pre-commit
	pre-commit install

install: ## Install project deps
	poetry install

format: ## Run Black formatter
	poetry run black .

lint: ## Check formatting with Black
	poetry run black --check .

test: ## Run unit tests
	poetry run pytest --cov watchmelog --junitxml test-results/junit/results.xml tests

run: ## Start app locally
	poetry run python watchmelog/app.py
