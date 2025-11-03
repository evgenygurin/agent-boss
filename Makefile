.PHONY: help install run test docker-up docker-down clean init

help: ## Show this help message
	@echo "Ultimate Boss Agent - Commands"
	@echo "=============================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt

init: ## Initialize boss knowledge base
	python init_boss_knowledge.py

run: ## Run the application locally
	python ultimate_boss_with_memory.py

test: ## Run tests
	python test_boss.py

docker-up: ## Start Docker containers
	docker-compose up -d

docker-down: ## Stop Docker containers
	docker-compose down

docker-logs: ## Show Docker logs
	docker-compose logs -f

docker-build: ## Build Docker images
	docker-compose build

clean: ## Clean generated files and caches
	rm -rf __pycache__
	rm -rf *.pyc
	rm -rf .pytest_cache
	rm -rf pagelogs/
	rm -rf boss_teachability_db/
	rm -rf boss_mem0_storage/
	rm -rf boss_chroma_db/
	rm -rf logs/

reset-memory: ## Reset all memory storage
	rm -rf boss_mem0_storage/
	rm -rf boss_chroma_db/
	rm -rf pagelogs/
	@echo "Memory reset complete. Run 'make init' to reinitialize."

dev: ## Run in development mode with auto-reload
	uvicorn ultimate_boss_with_memory:app --reload --host 0.0.0.0 --port 8000

check: ## Check code style
	@echo "Checking code style..."
	python -m pylint ultimate_boss_with_memory.py || true

format: ## Format code
	@echo "Formatting code..."
	python -m black ultimate_boss_with_memory.py init_boss_knowledge.py test_boss.py || true

.DEFAULT_GOAL := help
